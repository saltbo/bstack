"""The `gh` commands agents use, answered from the stand-in's state in GitHub's own formats."""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import simcore as sim
from simcore import git, now, state

OWNER = "saltbo"


class Fail(Exception):
    def __init__(self, message, code=1):
        super().__init__(message)
        self.code = code


# ---------------------------------------------------------------- helpers


def current_repo(explicit=None):
    if explicit:
        return explicit.replace("github.com/", "")
    url = git("config", "--get", "remote.origin.url", check=False)
    local = str(sim.ROOT / "github") + "/"
    if url.startswith(local):
        url = "https://github.com/" + url[len(local):]
    match = re.search(r"github\.com[:/]([^/]+/[^/.]+?)(?:\.git)?$", url)
    if not match:
        raise Fail("no git remotes found" if not url else f"none of the git remotes configured for this repository point to a known GitHub host.")
    return match.group(1)


def current_branch():
    return git("rev-parse", "--abbrev-ref", "HEAD", check=False)


def pr_url(slug, number):
    return f"https://github.com/{slug}/pull/{number}"


def issue_url(slug, number):
    return f"https://github.com/{slug}/issues/{number}"


def find_pr(repo, slug, selector):
    if selector is None:
        branch = current_branch()
        prs = [p for p in repo["prs"].values() if p["head"] == branch]
        if not prs:
            raise Fail(f'no pull requests found for branch "{branch}"')
        return sorted(prs, key=lambda p: p["number"])[-1]
    selector = str(selector)
    match = re.search(r"(\d+)$", selector)
    if match and match.group(1) in repo["prs"]:
        return repo["prs"][match.group(1)]
    for p in sorted(repo["prs"].values(), key=lambda p: -p["number"]):
        if p["head"] == selector:
            return p
    raise Fail(f"no pull requests found for branch \"{selector}\"" if not selector.isdigit()
               else f"GraphQL: Could not resolve to a PullRequest with the number of {selector}. (repository.pullRequest)")


def find_issue(repo, number):
    issue = repo["issues"].get(str(number).lstrip("#"))
    if not issue:
        raise Fail(f"GraphQL: Could not resolve to an issue or pull request with the number of {number}. (repository.issue)")
    return issue


def checks_for(repo, sha):
    runs = [r for r in repo["runs"] if r["sha"] == sha]
    latest = {}
    for r in runs:
        latest[r["job"]] = r
    checks = list(latest.values())
    return checks


def bucket(run):
    if run["status"] != "completed":
        return "pending"
    return "pass" if run["conclusion"] == "success" else "fail"


def rollup(slug, repo, sha):
    items = []
    for r in checks_for(repo, sha):
        items.append({"__typename": "CheckRun", "name": r["job"], "workflowName": r["workflow"],
                      "status": r["status"].upper(), "conclusion": (r["conclusion"] or "").upper(),
                      "startedAt": r["started"], "completedAt": r["completed"],
                      "detailsUrl": f"https://github.com/{slug}/actions/runs/{r['id']}/job/{r['id']}"})
    deploy = next((d for d in reversed(repo["deployments"]) if d["sha"] == sha), None)
    if deploy:
        items.append({"__typename": "StatusContext", "context": f"Workers Builds: {sim.repo_config(slug)['worker']}",
                      "state": "SUCCESS" if deploy["ok"] else "FAILURE", "targetUrl": deploy["url"],
                      "startedAt": deploy["at"]})
    return items


def head_sha(slug, pr):
    if pr["state"] == "MERGED":
        return pr.get("head_sha")
    return sim.ref_sha(slug, pr["head"]) or pr.get("head_sha")


def files_of(slug, pr):
    base = pr.get("base_sha") or sim.ref_sha(slug, pr["base"])
    head = head_sha(slug, pr)
    if not base or not head:
        return []
    out = git("--git-dir", str(sim.bare(slug)), "diff", "--numstat", f"{base}...{head}", check=False)
    files = []
    for line in out.splitlines():
        add, delete, path = line.split("\t", 2)
        files.append({"path": path, "additions": int(add) if add.isdigit() else 0,
                      "deletions": int(delete) if delete.isdigit() else 0})
    return files


def pr_json(slug, repo, pr):
    sha = head_sha(slug, pr)
    files = files_of(slug, pr)
    checks = checks_for(repo, sha) if sha else []
    failing = any(bucket(c) == "fail" for c in checks)
    pending = any(bucket(c) == "pending" for c in checks)
    merge_state = "DRAFT" if pr["draft"] else "BLOCKED" if failing and required(slug) else \
        "UNSTABLE" if failing else "BLOCKED" if pending and required(slug) else "CLEAN"
    author = {"login": pr["author"], "name": pr["author"], "is_bot": False}
    return {
        "number": pr["number"], "title": pr["title"], "body": pr["body"], "state": pr["state"],
        "isDraft": pr["draft"], "headRefName": pr["head"], "baseRefName": pr["base"], "headRefOid": sha,
        "url": pr_url(slug, pr["number"]), "author": author, "createdAt": pr["created"], "updatedAt": pr["updated"],
        "closed": pr["state"] != "OPEN", "closedAt": pr.get("closed_at"), "mergedAt": pr.get("merged_at"),
        "mergeCommit": {"oid": pr["merge_commit"]} if pr.get("merge_commit") else None,
        "mergedBy": {"login": pr["author"]} if pr.get("merged_at") else None,
        "mergeable": "MERGEABLE" if pr["state"] == "OPEN" and mergeable(slug, pr) else "CONFLICTING" if pr["state"] == "OPEN" else "UNKNOWN",
        "mergeStateStatus": merge_state, "reviewDecision": "", "labels": [{"name": n} for n in pr.get("labels", [])],
        "comments": [{"author": {"login": c["author"]}, "body": c["body"], "createdAt": c["created"],
                      "url": f"{pr_url(slug, pr['number'])}#issuecomment-{c['id']}"} for c in pr["comments"]],
        "reviews": [], "latestReviews": [], "reviewRequests": [], "assignees": [],
        "statusCheckRollup": rollup(slug, repo, sha) if sha else [],
        "files": files, "changedFiles": len(files), "additions": sum(f["additions"] for f in files),
        "deletions": sum(f["deletions"] for f in files),
        "commits": [{"oid": c} for c in git("--git-dir", str(sim.bare(slug)), "rev-list",
                                             f"{pr.get('base_sha') or pr['base']}..{sha}", check=False).split()] if sha else [],
        "closingIssuesReferences": [{"number": int(n)} for n in re.findall(r"(?i)\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?) #(\d+)", pr["body"] or "")],
        "id": f"PR_sim{pr['number']}", "isCrossRepository": False, "maintainerCanModify": True,
    }


def issue_json(slug, issue):
    return {"number": issue["number"], "title": issue["title"], "body": issue["body"], "state": issue["state"],
            "url": issue_url(slug, issue["number"]), "author": {"login": issue["author"]},
            "labels": [{"name": n} for n in issue.get("labels", [])], "createdAt": issue["created"],
            "updatedAt": issue["updated"], "closedAt": issue.get("closed_at"),
            "comments": [{"author": {"login": c["author"]}, "body": c["body"], "createdAt": c["created"]} for c in issue["comments"]],
            "assignees": [], "milestone": None, "id": f"I_sim{issue['number']}"}


def required(slug):
    return sim.repo_config(slug).get("required_checks", True)


def mergeable(slug, pr):
    base, head = sim.ref_sha(slug, pr["base"]), sim.ref_sha(slug, pr["head"])
    if not base or not head:
        return False
    result = subprocess.run(["git", "--git-dir", str(sim.bare(slug)), "merge-tree", "--write-tree", base, head],
                            capture_output=True, text=True)
    return result.returncode == 0


def tty():
    return sys.stdout.isatty()


def elapsed(start, end):
    if not start or not end:
        return "0"
    from datetime import datetime
    fmt = "%Y-%m-%dT%H:%M:%SZ"
    seconds = int((datetime.strptime(end, fmt) - datetime.strptime(start, fmt)).total_seconds())
    return f"{seconds // 60}m{seconds % 60}s" if seconds >= 60 else f"{seconds}s"


def emit(value, args):
    fields = getattr(args, "json", None)
    if fields is not None and fields != "":
        wanted = [f.strip() for f in fields.split(",") if f.strip()]
        if isinstance(value, list):
            value = [{k: v.get(k) for k in wanted} for v in value]
        else:
            value = {k: value.get(k) for k in wanted}
    text = json.dumps(value, ensure_ascii=False)
    if getattr(args, "jq", None):
        result = subprocess.run(["jq", "-r", args.jq], input=text, capture_output=True, text=True)
        if result.returncode != 0:
            raise Fail(result.stderr.strip())
        sys.stdout.write(result.stdout)
    else:
        print(json.dumps(value, ensure_ascii=False, indent=2) if fields is not None else text)


def body_of(args):
    if getattr(args, "body_file", None):
        return sys.stdin.read() if args.body_file == "-" else Path(args.body_file).read_text()
    return args.body or ""


def json_flags(p):
    p.add_argument("--json", nargs="?", const="")
    p.add_argument("-q", "--jq")
    p.add_argument("-t", "--template")


# ---------------------------------------------------------------- pr


def pr_create(args, slug):
    branch = args.head or current_branch()
    base = args.base or "main"
    if not sim.ref_sha(slug, branch):
        raise Fail(f"aborted: you must first push the current branch to a remote, or use the --head flag")
    with state() as data:
        repo = data["repos"][slug]
        if any(p["head"] == branch and p["state"] == "OPEN" for p in repo["prs"].values()):
            existing = next(p for p in repo["prs"].values() if p["head"] == branch and p["state"] == "OPEN")
            raise Fail(f'a pull request for branch "{branch}" into branch "{base}" already exists:\n{pr_url(slug, existing["number"])}')
        title, body = args.title, body_of(args)
        if args.fill or not title:
            log = git("log", "--format=%s%n%b", f"origin/{base}..{branch}", check=False).strip().split("\n", 1)
            title = title or (log[0] if log and log[0] else branch)
            body = body or (log[1].strip() if len(log) > 1 else "")
        number = repo["next"]
        repo["next"] += 1
        repo["prs"][str(number)] = {"number": number, "title": title, "body": body, "head": branch, "base": base,
                                    "draft": bool(args.draft), "state": "OPEN", "author": OWNER, "created": now(),
                                    "updated": now(), "comments": [], "labels": list(args.label or []),
                                    "base_sha": sim.ref_sha(slug, base)}
    sim.announce_preview(slug, branch)
    for comment in sim.repo_config(slug).get("review_comments", []):
        with state() as data:
            data["repos"][slug]["prs"][str(number)]["comments"].append(
                {"id": sim.next_id(data), "author": comment.get("author", "coderabbitai"), "body": comment["body"],
                 "created": now(), "updated": now()})
    print(pr_url(slug, number))


def pr_view(args, slug):
    with state(write=False) as data:
        repo = data["repos"][slug]
        pr = find_pr(repo, slug, args.selector)
        info = pr_json(slug, repo, pr)
    if args.json is not None or args.jq:
        return emit(info, args)
    if not tty():
        # gh's machine-readable form when its output is not a terminal
        print(f"title:\t{info['title']}\nstate:\t{'DRAFT' if info['isDraft'] and info['state'] == 'OPEN' else info['state']}\n"
              f"author:\t{OWNER}\nlabels:\t{', '.join(l['name'] for l in info['labels'])}\nassignees:\t\nreviewers:\t\n"
              f"projects:\t\nmilestone:\t\nnumber:\t{info['number']}\nurl:\t{info['url']}\n"
              f"additions:\t{info['additions']}\ndeletions:\t{info['deletions']}\nauto-merge:\tdisabled\n--")
        if args.comments:
            for c in info["comments"]:
                print(f"author:\t{c['author']['login']}\nassociation:\t{'owner' if c['author']['login'] == OWNER else 'none'}\n"
                      f"edited:\tfalse\nstatus:\tnone\n--\n{c['body']}\n--")
        else:
            print(info["body"] or "")
        return
    state_word = "Draft" if info["isDraft"] and info["state"] == "OPEN" else info["state"].capitalize()
    print(f"{info['title']} #{info['number']}")
    print(f"{state_word} • {OWNER} wants to merge {len(info['commits'])} commit(s) into {info['baseRefName']} from {info['headRefName']} • +{info['additions']} -{info['deletions']}")
    print()
    print(info["body"] or "No description provided")
    if args.comments:
        for c in info["comments"]:
            print(f"\n{c['author']['login']} commented • {c['createdAt']}\n{c['body']}")
    elif info["comments"]:
        print(f"\n{len(info['comments'])} comment(s). Use --comments to view the full conversation")
    print(f"\nView this pull request on GitHub: {info['url']}")


def pr_list(args, slug):
    with state(write=False) as data:
        repo = data["repos"][slug]
        want = (args.state or "open").upper()
        prs = [p for p in repo["prs"].values() if want == "ALL" or p["state"] == want]
        if args.head:
            prs = [p for p in prs if p["head"] == args.head]
        prs.sort(key=lambda p: -p["number"])
        infos = [pr_json(slug, repo, p) for p in prs[: args.limit]]
    if args.json is not None or args.jq:
        return emit(infos, args)
    if not infos:
        print(f"no {want.lower()} pull requests in {slug}" if want != "ALL" else f"no pull requests in {slug}")
        return
    for i in infos:
        print(f"{i['number']}\t{i['title']}\t{i['headRefName']}\t{'DRAFT' if i['isDraft'] else i['state']}\t{i['createdAt']}")


def pr_checks(args, slug):
    deadline = time.time() + 3600
    while True:
        with state(write=False) as data:
            repo = data["repos"][slug]
            pr = find_pr(repo, slug, args.selector)
            sha = head_sha(slug, pr)
            runs = checks_for(repo, sha)
            deploy = next((d for d in reversed(repo["deployments"]) if d["sha"] == sha), None)
        rows = [{"name": r["job"], "state": (r["conclusion"] or r["status"]).upper(), "bucket": bucket(r),
                 "workflow": r["workflow"], "link": f"https://github.com/{slug}/actions/runs/{r['id']}/job/{r['id']}",
                 "startedAt": r["started"], "completedAt": r["completed"], "description": "", "event": "pull_request"}
                for r in runs]
        if deploy:
            rows.append({"name": f"Workers Builds: {sim.repo_config(slug)['worker']}",
                         "state": "SUCCESS" if deploy["ok"] else "FAILURE", "bucket": "pass" if deploy["ok"] else "fail",
                         "workflow": "", "link": deploy["url"], "startedAt": deploy["at"], "completedAt": deploy["at"],
                         "description": "Preview deployed" if deploy["ok"] else "Build failed", "event": ""})
        pending = any(r["bucket"] == "pending" for r in rows)
        failed = any(r["bucket"] == "fail" for r in rows)
        if not args.watch or not pending or (args.fail_fast and failed) or time.time() > deadline:
            break
        time.sleep(max(1, min(args.interval, 3)))
    if not rows:
        raise Fail(f"no checks reported on the '{pr['head']}' branch")
    if args.json is not None or args.jq:
        emit(rows, args)
    elif not tty():
        for r in rows:
            print(f"{r['name']}\t{r['bucket']}\t{elapsed(r['startedAt'], r['completedAt'])}\t{r['link']}\t{r['description']}")
    else:
        passed = sum(r["bucket"] == "pass" for r in rows)
        print(f"{'Some checks were not successful' if failed else 'Some checks are still pending' if pending else 'All checks were successful'}")
        print(f"{sum(r['bucket'] == 'fail' for r in rows)} failing, {passed} successful, 0 skipped, and {sum(r['bucket'] == 'pending' for r in rows)} pending checks\n")
        for r in rows:
            mark = {"pass": "✓", "fail": "X", "pending": "*"}[r["bucket"]]
            print(f"{mark}  {r['name']}\t{r['bucket']}\t{r['link']}")
    if failed:
        raise Fail("", 1)
    if pending:
        raise Fail("", 8)


def pr_ready(args, slug):
    with state() as data:
        pr = find_pr(data["repos"][slug], slug, args.selector)
        if args.undo:
            pr["draft"] = True
            print(f"✓ Pull request {slug}#{pr['number']} is converted to \"draft\"")
            return
        if not pr["draft"]:
            print(f"! Pull request {slug}#{pr['number']} is already \"ready for review\"")
            return
        pr["draft"], pr["updated"] = False, now()
        print(f"✓ Pull request {slug}#{pr['number']} is marked as \"ready for review\"")


def pr_edit(args, slug):
    with state() as data:
        pr = find_pr(data["repos"][slug], slug, args.selector)
        if args.title:
            pr["title"] = args.title
        if args.body is not None or args.body_file:
            pr["body"] = body_of(args)
        for label in args.add_label or []:
            pr.setdefault("labels", []).append(label)
        pr["updated"] = now()
        print(pr_url(slug, pr["number"]))


def pr_comment(args, slug):
    with state() as data:
        pr = find_pr(data["repos"][slug], slug, args.selector)
        cid = sim.next_id(data)
        pr["comments"].append({"id": cid, "author": OWNER, "body": body_of(args), "created": now(), "updated": now()})
        print(f"{pr_url(slug, pr['number'])}#issuecomment-{cid}")


def pr_close(args, slug):
    with state() as data:
        pr = find_pr(data["repos"][slug], slug, args.selector)
        pr["state"], pr["closed_at"] = "CLOSED", now()
        print(f"✓ Closed pull request {slug}#{pr['number']} ({pr['title']})")
    if args.delete_branch:
        git("push", "-q", "origin", "--delete", pr["head"], check=False)


def pr_diff(args, slug):
    with state(write=False) as data:
        pr = find_pr(data["repos"][slug], slug, args.selector)
    base = pr.get("base_sha") or sim.ref_sha(slug, pr["base"])
    flag = ["--name-only"] if args.name_only else []
    sys.stdout.write(git("--git-dir", str(sim.bare(slug)), "diff", *flag, f"{base}...{head_sha(slug, pr)}") + "\n")


def pr_merge(args, slug):
    with state(write=False) as data:
        repo = data["repos"][slug]
        pr = find_pr(repo, slug, args.selector)
        info = pr_json(slug, repo, pr)
    number = pr["number"]
    if pr["state"] != "OPEN":
        raise Fail(f"X Pull request {slug}#{number} ({pr['title']}) can't be merged because it is {pr['state'].lower()}")
    if pr["draft"]:
        raise Fail(f"X Pull request {slug}#{number} is still a draft")
    if info["mergeable"] == "CONFLICTING":
        raise Fail(f"X Pull request {slug}#{number} is not mergeable: the merge commit cannot be cleanly created.")
    if info["mergeStateStatus"] == "BLOCKED":
        if args.auto:
            print(f"! The merge will happen once the required checks pass. (simulated: merging is not deferred)")
        raise Fail(f"X Pull request {slug}#{number} is not mergeable: the base branch policy prohibits the merge.\n"
                   "To have the pull request merged after all the requirements have been met, add the `--auto` flag.\n"
                   "To use administrator privileges to immediately merge the pull request, add the `--admin` flag.")
    head = head_sha(slug, pr)
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "w"
        git("clone", "-q", str(sim.bare(slug)), str(work))
        git("checkout", "-q", pr["base"], cwd=work)
        method = "merge" if args.merge else "rebase" if args.rebase else "squash"
        ident = ["-c", f"user.name={OWNER}", "-c", f"user.email={OWNER}@users.noreply.github.com"]
        if method == "squash":
            git("merge", "--squash", "-q", f"origin/{pr['head']}", cwd=work)
            subject = args.subject or f"{pr['title']} (#{number})"
            message = subject + "\n\n" + (args.body if args.body is not None else (pr["body"] or "")).strip() + "\n"
            subprocess.run(["git", *ident, "commit", "-q", "-F", "-"], input=message, text=True, cwd=work, check=True)
        elif method == "merge":
            git(*ident, "merge", "--no-ff", "-q", "-m", f"Merge pull request #{number} from {OWNER}/{pr['head']}", f"origin/{pr['head']}", cwd=work)
        else:
            git(*ident, "rebase", "-q", f"origin/{pr['head']}", cwd=work)
        commit = git("rev-parse", "HEAD", cwd=work)
        git("push", "-q", "origin", pr["base"], cwd=work)
    with state() as data:
        p = data["repos"][slug]["prs"][str(number)]
        p.update(state="MERGED", merged_at=now(), closed_at=now(), merge_commit=commit, head_sha=head, updated=now())
        for n in re.findall(r"(?i)\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?) #(\d+)", p["body"] or ""):
            issue = data["repos"][slug]["issues"].get(n)
            if issue:
                issue.update(state="CLOSED", closed_at=now())
    verb = {"squash": "Squashed and merged", "merge": "Merged", "rebase": "Rebased and merged"}[method]
    print(f"✓ {verb} pull request {slug}#{number} ({pr['title']})")
    if args.delete_branch:
        git("push", "-q", "origin", "--delete", pr["head"], check=False)
        if current_branch() == pr["head"]:
            git("checkout", "-q", pr["base"], check=False)
            git("pull", "-q", "--ff-only", "origin", pr["base"], check=False)
            git("branch", "-q", "-D", pr["head"], check=False)
            print(f"✓ Deleted local branch {pr['head']} and switched to branch {pr['base']}")
        elif git("rev-parse", "--verify", "-q", f"refs/heads/{pr['head']}", check=False):
            git("branch", "-q", "-D", pr["head"], check=False)
            print(f"✓ Deleted local branch {pr['head']}")
        print(f"✓ Deleted remote branch {pr['head']}")


# ---------------------------------------------------------------- issue


def issue_create(args, slug):
    with state() as data:
        repo = data["repos"][slug]
        number = repo["next"]
        repo["next"] += 1
        repo["issues"][str(number)] = {"number": number, "title": args.title, "body": body_of(args), "state": "OPEN",
                                       "author": OWNER, "created": now(), "updated": now(), "comments": [],
                                       "labels": list(args.label or [])}
    print(issue_url(slug, number))


def issue_list(args, slug):
    with state(write=False) as data:
        want = (args.state or "open").upper()
        issues = [i for i in data["repos"][slug]["issues"].values() if want == "ALL" or i["state"] == want]
        if args.label:
            issues = [i for i in issues if set(args.label) <= set(i.get("labels", []))]
        if args.search:
            issues = [i for i in issues if args.search.lower() in (i["title"] + i["body"]).lower()]
        infos = [issue_json(slug, i) for i in sorted(issues, key=lambda i: -i["number"])[: args.limit]]
    if args.json is not None or args.jq:
        return emit(infos, args)
    if not infos:
        print(f"no open issues in {slug}")
    for i in infos:
        print(f"{i['number']}\t{i['state']}\t{i['title']}\t{','.join(l['name'] for l in i['labels'])}\t{i['createdAt']}")


def issue_view(args, slug):
    with state(write=False) as data:
        info = issue_json(slug, find_issue(data["repos"][slug], args.number))
    if args.json is not None or args.jq:
        return emit(info, args)
    print(f"{info['title']} #{info['number']}\n{info['state'].capitalize()} • {OWNER} opened\n\n{info['body']}\n\nView this issue on GitHub: {info['url']}")


def issue_comment(args, slug):
    with state() as data:
        issue = find_issue(data["repos"][slug], args.number)
        issue["comments"].append({"author": OWNER, "body": body_of(args), "created": now()})
        print(f"{issue_url(slug, issue['number'])}#issuecomment-{sim.next_id(data)}")


def issue_close(args, slug):
    with state() as data:
        issue = find_issue(data["repos"][slug], args.number)
        issue.update(state="CLOSED", closed_at=now())
        if args.comment:
            issue["comments"].append({"author": OWNER, "body": args.comment, "created": now()})
        print(f"✓ Closed issue {slug}#{issue['number']} ({issue['title']})")


def issue_edit(args, slug):
    with state() as data:
        issue = find_issue(data["repos"][slug], args.number)
        if args.title:
            issue["title"] = args.title
        if args.body is not None or args.body_file:
            issue["body"] = body_of(args)
        issue.setdefault("labels", []).extend(args.add_label or [])
        print(issue_url(slug, issue["number"]))


# ---------------------------------------------------------------- run


def run_list(args, slug):
    with state(write=False) as data:
        runs = sorted(data["repos"][slug]["runs"], key=lambda r: -r["id"])
        if args.branch:
            runs = [r for r in runs if r["branch"] == args.branch]
        rows = [{"databaseId": r["id"], "name": r["workflow"], "workflowName": r["workflow"], "headBranch": r["branch"],
                 "headSha": r["sha"], "status": r["status"], "conclusion": r["conclusion"] or "", "event": "push",
                 "createdAt": r["started"] or now(), "url": f"https://github.com/{slug}/actions/runs/{r['id']}",
                 "displayTitle": r["job"]} for r in runs[: args.limit]]
    if args.json is not None or args.jq:
        return emit(rows, args)
    for r in rows:
        if not tty():
            print(f"{r['status']}\t{r['conclusion']}\t{r['displayTitle']}\t{r['name']}\t{r['headBranch']}\tpush\t{r['databaseId']}\t0s\t{r['createdAt']}")
            continue
        mark = "✓" if r["conclusion"] == "success" else "X" if r["conclusion"] == "failure" else "*"
        print(f"{mark}\t{r['displayTitle']}\t{r['name']}\t{r['headBranch']}\tpush\t{r['databaseId']}\t{r['createdAt']}")


def run_view(args, slug):
    deadline = time.time() + 3600
    while True:
        with state(write=False) as data:
            run = next((r for r in data["repos"][slug]["runs"] if str(r["id"]) == str(args.id)), None)
        if not run:
            raise Fail(f"HTTP 404: Not Found (https://api.github.com/repos/{slug}/actions/runs/{args.id})")
        if not args.watch or run["status"] == "completed" or time.time() > deadline:
            break
        time.sleep(2)
    if args.json is not None or args.jq:
        return emit({"databaseId": run["id"], "status": run["status"], "conclusion": run["conclusion"] or "",
                     "headSha": run["sha"], "headBranch": run["branch"], "name": run["workflow"],
                     "jobs": [{"name": run["job"], "status": run["status"], "conclusion": run["conclusion"] or ""}]}, args)
    if args.log or args.log_failed:
        print(Path(run["log"]).read_text() if run.get("log") else "run log not found")
        return
    mark = "✓" if run["conclusion"] == "success" else "X" if run["conclusion"] == "failure" else "*"
    print(f"{mark} {run['branch']} {run['workflow']} · {run['id']}\n\nJOBS\n{mark} {run['job']}")
    if args.exit_status and run["conclusion"] != "success":
        raise Fail("", 1)


# ---------------------------------------------------------------- api, repo, auth


def api(args, slug):
    path = args.endpoint.lstrip("/").replace("{owner}", slug.split("/")[0]).replace("{repo}", slug.split("/")[1])
    with state(write=False) as data:
        repo = data["repos"].get("/".join(path.split("/")[1:3]), data["repos"][slug])
        target = "/".join(path.split("/")[1:3]) if path.startswith("repos/") else slug
        m = re.match(r"repos/[^/]+/[^/]+/(pulls|issues)/(\d+)(/comments|/reviews)?$", path)
        value = None
        if m:
            kind, number, sub = m.groups()
            item = repo["prs"].get(number) or repo["issues"].get(number)
            if item:
                if sub == "/comments" and kind == "issues":
                    value = [{"id": c.get("id"), "user": {"login": c["author"], "type": "Bot" if c["author"] != OWNER else "User"},
                              "body": c["body"], "created_at": c["created"]} for c in item["comments"]]
                elif sub in ("/comments", "/reviews"):
                    value = []
                else:
                    value = {"number": item["number"], "title": item["title"], "body": item["body"],
                             "state": "open" if item["state"] == "OPEN" else "closed", "merged": item["state"] == "MERGED",
                             "html_url": (pr_url if kind == "pulls" else issue_url)(target, item["number"])}
        elif re.match(r"repos/[^/]+/[^/]+/branches/[^/]+/protection/required_pull_request_reviews$", path):
            raise Fail(json.dumps({"message": "Required pull request reviews not enabled", "status": "404"})
                       + "\ngh: Required pull request reviews not enabled (HTTP 404)")
        elif re.match(r"repos/[^/]+/[^/]+/branches/[^/]+/protection$", path):
            if path.split("/")[4] == "main" and sim.repo_config(target).get("required_checks", True):
                jobs = sorted({r["job"] for r in repo["runs"]})
                value = {"url": f"https://api.github.com/{path}",
                         "required_status_checks": {"strict": False, "contexts": jobs,
                                                    "checks": [{"context": j, "app_id": 15368} for j in jobs]},
                         "enforce_admins": {"enabled": False}, "allow_force_pushes": {"enabled": False},
                         "allow_deletions": {"enabled": False}}
            else:
                raise Fail(json.dumps({"message": "Branch not protected", "status": "404"}) + "\ngh: Branch not protected (HTTP 404)")
        elif re.match(r"repos/[^/]+/[^/]+/deployments$", path):
            value = [{"id": i + 1, "sha": d["sha"], "ref": d["branch"], "environment": d["target"].capitalize(),
                      "created_at": d["at"], "payload": {"url": d["url"]}, "description": d["url"]}
                     for i, d in reversed(list(enumerate(repo["deployments"])))]
        elif re.match(r"repos/[^/]+/[^/]+/commits/[^/]+/statuses$", path):
            ref = path.split("/")[4]
            sha = sim.ref_sha(target, ref) or git("--git-dir", str(sim.bare(target)), "rev-parse", ref, check=False)
            value = [{"context": f"Workers Builds: {sim.repo_config(target)['worker']}",
                      "state": "success" if d["ok"] else "failure", "target_url": d["url"], "created_at": d["at"]}
                     for d in reversed(repo["deployments"]) if sha and d["sha"].startswith(sha)]
        elif re.match(r"repos/[^/]+/[^/]+/commits/[^/]+/(check-runs|status)$", path):
            ref = path.split("/")[4]
            sha = sim.ref_sha(target, ref) or git("--git-dir", str(sim.bare(target)), "rev-parse", ref, check=False)
            runs = [r for r in repo["runs"] if sha and r["sha"] == sha]
            if path.endswith("check-runs"):
                value = {"total_count": len(runs), "check_runs": [
                    {"id": r["id"], "name": r["job"], "head_sha": r["sha"], "status": r["status"], "conclusion": r["conclusion"],
                     "html_url": f"https://github.com/{target}/actions/runs/{r['id']}/job/{r['id']}",
                     "started_at": r["started"], "completed_at": r["completed"]} for r in runs]}
            else:
                deploy = next((d for d in reversed(repo["deployments"]) if d["sha"] == sha), None)
                statuses = [{"context": f"Workers Builds: {sim.repo_config(target)['worker']}",
                             "state": "success" if deploy["ok"] else "failure", "target_url": deploy["url"]}] if deploy else []
                value = {"state": statuses[0]["state"] if statuses else "pending", "sha": sha, "statuses": statuses,
                         "total_count": len(statuses)}
        elif re.match(r"repos/[^/]+/[^/]+/actions/runs$", path):
            value = {"total_count": len(repo["runs"]), "workflow_runs": [
                {"id": r["id"], "name": r["workflow"], "head_branch": r["branch"], "head_sha": r["sha"], "status": r["status"],
                 "conclusion": r["conclusion"], "html_url": f"https://github.com/{target}/actions/runs/{r['id']}"}
                for r in sorted(repo["runs"], key=lambda r: -r["id"])]}
        elif re.match(r"repos/[^/]+/[^/]+$", path):
            value = {"full_name": target, "default_branch": "main", "private": True, "html_url": f"https://github.com/{target}"}
        elif path == "user":
            value = {"login": OWNER, "type": "User"}
    if value is None:
        sim.log_call("gh", ["api", args.endpoint], 1, "stand-in gap: endpoint not implemented")
        raise Fail(json.dumps({"message": "Not Found", "documentation_url": "https://docs.github.com/rest", "status": "404"})
                   + f"\ngh: Not Found (HTTP 404)")
    emit(value, argparse.Namespace(json=None, jq=args.jq))


def repo_clone(args, slug):
    target = args.name.replace("https://github.com/", "").removesuffix(".git")
    if target not in sim.config()["repos"]:
        raise Fail(f"GraphQL: Could not resolve to a Repository with the name '{target}'. (repository)")
    dest = args.directory or target.split("/")[1]
    result = subprocess.run(["git", "clone", "-q", f"https://github.com/{target}.git", dest], capture_output=True, text=True)
    if result.returncode != 0:
        raise Fail(result.stderr.strip())


def repo_view(args, slug):
    info = {"name": slug.split("/")[1], "owner": {"login": slug.split("/")[0]}, "nameWithOwner": slug,
            "url": f"https://github.com/{slug}", "defaultBranchRef": {"name": "main"}, "visibility": "PRIVATE",
            "isPrivate": True, "description": ""}
    if args.json is not None or args.jq:
        return emit(info, args)
    print(f"{slug}\nNo description provided\n\nView this repository on GitHub: {info['url']}")


def auth_status(args, slug):
    print("github.com\n  ✓ Logged in to github.com account saltbo (keyring)\n  - Active account: true\n"
          "  - Git operations protocol: https\n  - Token: gho_************************************\n"
          "  - Token scopes: 'gist', 'read:org', 'repo', 'workflow'")


# ---------------------------------------------------------------- parser


def build():
    parser = argparse.ArgumentParser(prog="gh", add_help=True)
    parser.add_argument("-R", "--repo")
    top = parser.add_subparsers(dest="group", required=True)

    def command(group, name, handler, selector=None):
        p = group.add_parser(name)
        p.add_argument("-R", "--repo", dest="repo_inner")
        if selector:
            p.add_argument(selector, nargs="?")
        p.set_defaults(handler=handler)
        return p

    pr = top.add_parser("pr").add_subparsers(dest="cmd", required=True)
    p = command(pr, "create", pr_create)
    for flag in ("--title", "-t"), ("--body", "-b"), ("--body-file", "-F"), ("--base", "-B"), ("--head", "-H"):
        p.add_argument(*flag)
    p.add_argument("--draft", "-d", action="store_true")
    p.add_argument("--fill", "-f", action="store_true")
    p.add_argument("--fill-first", dest="fill", action="store_true")
    p.add_argument("--label", "-l", action="append")
    p.add_argument("--assignee", "-a", action="append")
    p.add_argument("--reviewer", "-r", action="append")
    p.add_argument("--web", "-w", action="store_true")
    p = command(pr, "view", pr_view, "selector")
    json_flags(p)
    p.add_argument("--comments", "-c", action="store_true")
    p.add_argument("--web", "-w", action="store_true")
    p = command(pr, "list", pr_list)
    json_flags(p)
    p.add_argument("--state", "-s")
    p.add_argument("--head", "-H")
    p.add_argument("--base", "-B")
    p.add_argument("--limit", "-L", type=int, default=30)
    p.add_argument("--author", "-A")
    p = command(pr, "checks", pr_checks, "selector")
    json_flags(p)
    p.add_argument("--watch", action="store_true")
    p.add_argument("--fail-fast", action="store_true")
    p.add_argument("--required", action="store_true")
    p.add_argument("--interval", "-i", type=int, default=10)
    p = command(pr, "ready", pr_ready, "selector")
    p.add_argument("--undo", action="store_true")
    p = command(pr, "edit", pr_edit, "selector")
    for flag in ("--title", "-t"), ("--body", "-b"), ("--body-file", "-F"):
        p.add_argument(*flag)
    p.add_argument("--add-label", action="append")
    p = command(pr, "comment", pr_comment, "selector")
    p.add_argument("--body", "-b")
    p.add_argument("--body-file", "-F")
    p = command(pr, "close", pr_close, "selector")
    p.add_argument("--delete-branch", "-d", action="store_true")
    p.add_argument("--comment", "-c")
    p = command(pr, "diff", pr_diff, "selector")
    p.add_argument("--name-only", action="store_true")
    p.add_argument("--patch", action="store_true")
    p.add_argument("--color")
    p = command(pr, "merge", pr_merge, "selector")
    for flag in "--squash", "--merge", "--rebase", "--auto", "--admin", "--delete-branch":
        p.add_argument(flag, *(["-s"] if flag == "--squash" else ["-m"] if flag == "--merge" else
                                ["-r"] if flag == "--rebase" else ["-d"] if flag == "--delete-branch" else []),
                       action="store_true")
    p.add_argument("--subject", "-t")
    p.add_argument("--body", "-b")
    p.add_argument("--match-head-commit")

    issue = top.add_parser("issue").add_subparsers(dest="cmd", required=True)
    p = command(issue, "create", issue_create)
    for flag in ("--title", "-t"), ("--body", "-b"), ("--body-file", "-F"):
        p.add_argument(*flag)
    p.add_argument("--label", "-l", action="append")
    p.add_argument("--assignee", "-a", action="append")
    p = command(issue, "list", issue_list)
    json_flags(p)
    p.add_argument("--state", "-s")
    p.add_argument("--label", "-l", action="append")
    p.add_argument("--search", "-S")
    p.add_argument("--limit", "-L", type=int, default=30)
    p = command(issue, "view", issue_view, "number")
    json_flags(p)
    p.add_argument("--comments", "-c", action="store_true")
    p = command(issue, "comment", issue_comment, "number")
    p.add_argument("--body", "-b")
    p.add_argument("--body-file", "-F")
    p = command(issue, "close", issue_close, "number")
    p.add_argument("--comment", "-c")
    p.add_argument("--reason", "-r")
    p = command(issue, "edit", issue_edit, "number")
    for flag in ("--title", "-t"), ("--body", "-b"), ("--body-file", "-F"):
        p.add_argument(*flag)
    p.add_argument("--add-label", action="append")

    run = top.add_parser("run").add_subparsers(dest="cmd", required=True)
    p = command(run, "list", run_list)
    json_flags(p)
    p.add_argument("--branch", "-b")
    p.add_argument("--limit", "-L", type=int, default=20)
    p.add_argument("--workflow", "-w")
    for name in ("view", "watch"):
        p = command(run, name, run_view, "id")
        json_flags(p)
        p.add_argument("--log", action="store_true")
        p.add_argument("--log-failed", action="store_true")
        p.add_argument("--exit-status", action="store_true")
        p.set_defaults(watch=name == "watch")

    p = command(top, "api", api, "endpoint")
    p.add_argument("-q", "--jq")
    p.add_argument("-X", "--method")
    p.add_argument("-f", "--raw-field", action="append")
    p.add_argument("-F", "--field", action="append")
    p.add_argument("--paginate", action="store_true")
    p.add_argument("-H", "--header", action="append")

    repo = top.add_parser("repo").add_subparsers(dest="cmd", required=True)
    p = command(repo, "view", repo_view, "name")
    json_flags(p)
    p = command(repo, "clone", repo_clone, "name")
    p.add_argument("directory", nargs="?")
    auth = top.add_parser("auth").add_subparsers(dest="cmd", required=True)
    command(auth, "status", auth_status)
    return parser


def main(argv):
    code, note = 0, ""
    try:
        args = build().parse_args(argv)
        args.json = getattr(args, "json", None)
        outside = args.group == "auth" or (args.group == "repo" and args.cmd == "clone")
        slug = None if outside else current_repo(getattr(args, "repo_inner", None) or args.repo)
        if slug and slug not in sim.config()["repos"]:
            raise Fail(f"GraphQL: Could not resolve to a Repository with the name '{slug}'. (repository)")
        if getattr(args, "web", False):
            print("Opening github.com in your browser.")
            return 0
        args.handler(args, slug)
    except SystemExit as exc:
        code, note = int(exc.code or 0), "parse error" if exc.code else ""
    except Fail as exc:
        if str(exc):
            print(str(exc), file=sys.stderr)
        code = exc.code
    except Exception as exc:  # a gap in the stand-in, recorded so the run can be judged with it in mind
        print(f"gh: {exc}", file=sys.stderr)
        code, note = 1, f"stand-in error: {exc!r}"
    sim.log_call("gh", argv, code, note)
    return code
