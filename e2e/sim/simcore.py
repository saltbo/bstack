"""A local stand-in for GitHub and Cloudflare that end-to-end sessions work against.

Everything lives under one root directory, `SIM_ROOT`:

- `github/<owner>/<repo>.git` are bare repositories. The session's git config
  rewrites `https://github.com/` to them, so a clone, a push, and `git remote -v`
  all look like GitHub.
- `state.json` holds pull requests, issues, comments, check runs, and deployments.
- A push runs the repository's workflow in a clean checkout, and for a Workers
  project it deploys the branch to a preview, or `main` to production, on the
  local workerd runtime. A proxy serves every deployment under `*.localhost`.
- `calls.log` records every `gh` and `wrangler` call, so a gap in the stand-in
  shows up as a call it did not understand.
"""

import contextlib
import fcntl
import json
import os
import re
import shutil
import signal
import socket
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(os.environ.get("SIM_ROOT", "/nonexistent"))
HERE = Path(__file__).resolve().parent


def real_wrangler(cwd):
    """The project's own wrangler, or the one installed for the machine."""
    for directory in [Path(cwd), *Path(cwd).parents]:
        script = directory / "node_modules/wrangler/bin/wrangler.js"
        if script.exists():
            return ["node", str(script)]
    return [os.environ.get("SIM_REAL_WRANGLER", "wrangler")]


def outside_env(extra=None):
    """The environment of a fresh terminal: nothing of the agent session that started the runner."""
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("CLAUDE", "T3CODE", "ANTHROPIC_", "MCP_", "OTEL_", "GIT_")) and k != "CLAUDECODE"}
    env.update(extra or {})
    return env


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------- state


@contextlib.contextmanager
def state(write=True):
    path = ROOT / "state.json"
    with open(ROOT / "state.lock", "a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        data = json.loads(path.read_text()) if path.exists() else {"repos": {}}
        yield data
        if write:
            tmp = path.with_suffix(".tmp")
            tmp.write_text(json.dumps(data, indent=1))
            tmp.replace(path)


def config():
    return json.loads((ROOT / "config.json").read_text())


def repo_config(slug):
    return config()["repos"][slug]


def log_call(tool, argv, code, note=""):
    with open(ROOT / "calls.log", "a") as f:
        f.write(json.dumps({"at": now(), "tool": tool, "argv": argv, "cwd": os.getcwd(),
                            "exit": code, "note": note}) + "\n")


def bare(slug):
    return ROOT / "github" / f"{slug}.git"


def git_env(env=None):
    """The environment for git, without the repository a calling git hook points at."""
    base = env if env is not None else os.environ
    return {k: v for k, v in base.items() if not k.startswith("GIT_") or k in ("GIT_CONFIG_GLOBAL", "GIT_EXEC_PATH")}


def git(*args, cwd=None, check=True, env=None):
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, env=git_env(env))
    if check and result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {result.stderr.strip()}")
    return result.stdout.strip()


def ref_sha(slug, ref):
    out = git("--git-dir", str(bare(slug)), "rev-parse", "--verify", "-q", f"refs/heads/{ref}", check=False)
    return out or None


def new_repo(data, slug):
    return data["repos"].setdefault(slug, {"next": 1, "prs": {}, "issues": {}, "runs": [],
                                           "deployments": [], "previews": {}, "production": None})


# ---------------------------------------------------------------- setup


def setup(root, cfg):
    """Create the bare repositories from fixture directories and write the git config."""
    root.mkdir(parents=True, exist_ok=True)
    (root / "config.json").write_text(json.dumps(cfg, indent=1))
    hook = root / "hooks/post-receive"
    hook.parent.mkdir(parents=True, exist_ok=True)
    hook.write_text(f'#!/bin/sh\nexec "{sys.executable}" "{HERE / "sim.py"}" hook "$@"\n')
    hook.chmod(0o755)
    for slug, repo in cfg["repos"].items():
        path = root / "github" / f"{slug}.git"
        git("init", "-q", "--bare", "-b", "main", str(path))
        git("--git-dir", str(path), "config", "core.hooksPath", str(hook.parent))
        git("--git-dir", str(path), "config", "sim.slug", slug)
        seed = Path(repo["fixture"])
        work = root / "seed" / slug
        shutil.copytree(seed, work, symlinks=True, ignore=shutil.ignore_patterns("node_modules", "__pycache__"))
        env = dict(os.environ, SIM_ROOT=str(root), SIM_SEED="1")
        git("init", "-q", "-b", "main", cwd=work)
        git("add", "-A", cwd=work)
        git("-c", "user.name=Saltbo", "-c", "user.email=saltbo@example.com", "-c", "core.hooksPath=/dev/null",
            "commit", "-qm", "Initial commit", cwd=work)
        git("push", "-q", str(path), "main", cwd=work, env=env)
        shutil.rmtree(work)
    global ROOT
    ROOT = root
    with state() as data:
        for slug, repo in cfg["repos"].items():
            entry = new_repo(data, slug)
            for issue in repo.get("issues", []):
                number = entry["next"]
                entry["next"] += 1
                entry["issues"][str(number)] = {"number": number, "title": issue["title"], "body": issue.get("body", ""),
                                                "state": "OPEN", "author": "saltbo", "created": now(), "updated": now(),
                                                "comments": [], "labels": issue.get("labels", [])}
    for slug, repo in cfg["repos"].items():
        if repo.get("production"):
            deploy(slug, "main", ref_sha(slug, "main"), production=True)


def gitconfig(root, name, email):
    """GitHub over SSH is rewritten to https, which the stand-in's transport serves."""
    return (f"[user]\n\tname = {name}\n\temail = {email}\n"
            f"[url \"https://github.com/\"]\n\tinsteadOf = git@github.com:\n\tinsteadOf = ssh://git@github.com/\n"
            f"[init]\n\tdefaultBranch = main\n[push]\n\tautoSetupRemote = true\n")


def exec_path(root):
    """git's own helpers, with the https transport replaced by the stand-in's."""
    env = {k: v for k, v in os.environ.items() if k != "GIT_EXEC_PATH"}
    real = Path(subprocess.run(["git", "--exec-path"], capture_output=True, text=True, env=env).stdout.strip())
    target = root / "git-core"
    target.mkdir(parents=True, exist_ok=True)
    for item in real.iterdir():
        if item.name not in ("git-remote-https", "git-remote-http"):
            (target / item.name).symlink_to(item)
    for name in ("git-remote-https", "git-remote-http"):
        (target / name).symlink_to(HERE / "git-remote-https")
    return target


# ---------------------------------------------------------------- push hook


def hook(lines):
    slug = git("config", "sim.slug")
    if os.environ.get("SIM_SEED"):
        return
    for line in lines:
        old, new, ref = line.split()
        if not ref.startswith("refs/heads/"):
            continue
        branch = ref[len("refs/heads/"):]
        if set(new) == {"0"}:
            stop_preview(slug, branch)
            continue
        spawn("pushed", slug, branch, new)


def spawn(*args):
    logs = ROOT / "logs"
    logs.mkdir(exist_ok=True)
    out = open(logs / f"{args[0]}-{args[2].replace('/', '_')}-{args[3][:7]}.log", "a")
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_") or k in ("GIT_CONFIG_GLOBAL", "GIT_EXEC_PATH")}
    subprocess.Popen([sys.executable, str(HERE / "sim.py"), *args], stdout=out, stderr=out,
                     stdin=subprocess.DEVNULL, start_new_session=True, env=dict(env, SIM_ROOT=str(ROOT)))


def pushed(slug, branch, sha):
    """What GitHub Actions and Workers Builds do after a push."""
    cfg = repo_config(slug)
    jobs = workflows(slug, sha)
    with state() as data:
        repo = data["repos"][slug]
        run_id = 9000 + len(repo["runs"]) + 1
        runs = [{"id": run_id + i, "workflow": job[0], "job": job[1], "sha": sha, "branch": branch,
                 "status": "queued", "conclusion": None, "started": None, "completed": None,
                 "log": None} for i, job in enumerate(jobs)]
        repo["runs"].extend(runs)
    try:
        if cfg.get("preview") if branch != "main" else cfg.get("production"):
            deploy(slug, branch, sha, production=branch == "main")
        for run in runs:
            run_job(slug, run["id"])
    except Exception as exc:  # a gap in the stand-in must not leave checks pending forever
        log_call("platform", ["pushed", slug, branch, sha], 1, f"stand-in error: {exc!r}")
        with state() as data:
            for run in data["repos"][slug]["runs"]:
                if run["sha"] == sha and run["status"] != "completed":
                    run.update(status="completed", conclusion="failure", completed=now())
        raise


# ---------------------------------------------------------------- CI


def parse_workflow(text):
    """The name of a workflow file, and its jobs with their shell steps. Supports the subset fixtures use."""
    name, jobs, job, section = "CI", [], None, None
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        indent = len(line) - len(line.lstrip())
        i += 1
        if not stripped or stripped.startswith("#"):
            continue
        if indent == 0:
            section = stripped.rstrip(":")
            if stripped.startswith("name:"):
                name = stripped[5:].strip().strip("'\"")
            continue
        if section != "jobs":
            continue
        if indent == 2 and stripped.endswith(":"):
            job = {"name": stripped[:-1], "steps": []}
            jobs.append(job)
        elif job and indent == 4 and stripped.startswith("name:"):
            job["name"] = stripped[5:].strip().strip("'\"")
        elif job and stripped.lstrip("- ").startswith("run:"):
            body = stripped.lstrip("- ")[4:].strip()
            if body not in ("|", ">", "|-", ">-"):
                job["steps"].append(body)
                continue
            block, base = [], None
            while i < len(lines) and (not lines[i].strip() or len(lines[i]) - len(lines[i].lstrip()) > indent):
                if lines[i].strip():
                    base = base if base is not None else len(lines[i]) - len(lines[i].lstrip())
                    block.append(lines[i][base:])
                i += 1
            job["steps"].append("\n".join(block))
    return name, jobs


def workflows(slug, sha):
    """Every job that a push runs, as (workflow name, job name, steps)."""
    listing = git("--git-dir", str(bare(slug)), "ls-tree", "--name-only", sha, ".github/workflows/", check=False)
    jobs = []
    for path in listing.splitlines():
        if not path.endswith((".yml", ".yaml")):
            continue
        text = git("--git-dir", str(bare(slug)), "show", f"{sha}:{path}")
        if not re.search(r"\b(push|pull_request)\b", text.split("jobs:")[0]):
            continue
        name, parsed = parse_workflow(text)
        jobs += [(name, job["name"], job["steps"]) for job in parsed]
    return jobs


def checkout(slug, sha, dest):
    if dest.exists():
        shutil.rmtree(dest)
    git("clone", "-q", str(bare(slug)), str(dest))
    git("checkout", "-q", sha, cwd=dest)
    deps = repo_config(slug).get("deps")
    if deps and Path(deps).exists():
        subprocess.run(["cp", "-cR", deps, str(dest / "node_modules")], check=True)


def run_job(slug, run_id):
    with state() as data:
        run = next(r for r in data["repos"][slug]["runs"] if r["id"] == run_id)
        run["status"], run["started"] = "in_progress", now()
        sha, job_name = run["sha"], run["job"]
    steps = next((j[2] for j in workflows(slug, sha) if j[1] == job_name), [])
    work = ROOT / "ci" / f"{run_id}"
    checkout(slug, sha, work)
    log, ok = [], True
    env = ci_env()
    for step in steps:
        log.append(f"##[group]Run {step.splitlines()[0]}")
        result = subprocess.run(["bash", "-eo", "pipefail", "-c", step], cwd=work, capture_output=True, text=True, env=env)
        log.append(result.stdout + result.stderr)
        log.append("##[endgroup]")
        if result.returncode != 0:
            log.append(f"##[error]Process completed with exit code {result.returncode}.")
            ok = False
            break
    log_path = ROOT / "logs" / f"run-{run_id}.log"
    log_path.parent.mkdir(exist_ok=True)
    log_path.write_text("\n".join(log))
    with state() as data:
        run = next(r for r in data["repos"][slug]["runs"] if r["id"] == run_id)
        run.update(status="completed", conclusion="success" if ok else "failure", completed=now(), log=str(log_path))
    shutil.rmtree(work, ignore_errors=True)


def ci_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith(("SIM_", "GIT_")) or k == "GIT_EXEC_PATH"}
    env.update(CI="true", GITHUB_ACTIONS="true", PATH=os.environ.get("SIM_CI_PATH", os.environ["PATH"]))
    return env


# ---------------------------------------------------------------- Cloudflare


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def host_for(slug, branch, production):
    name = repo_config(slug)["worker"]
    label = re.sub(r"[^a-z0-9-]", "-", branch.lower())[:40].strip("-")
    return f"{name}.localhost" if production else f"{label}-{name}.localhost"


def public_url(host):
    return f"http://{host}:{config()['proxy_port']}"


def deploy(slug, branch, sha, production, source=None):
    """Workers Builds: build the commit and run it on workerd, then record the deployment."""
    cfg = repo_config(slug)
    target = "production" if production else "preview"
    where = ROOT / "cf" / slug / (target if production else f"preview-{branch.replace('/', '_')}")
    where.mkdir(parents=True, exist_ok=True)
    persist = ROOT / "cf" / slug / f"{target}-state"
    code = where / "code"
    host = host_for(slug, branch, production)
    stop_deployment(slug, branch, production)
    if source:
        if code.exists():
            shutil.rmtree(code)
        shutil.copytree(source, code, symlinks=True, ignore=shutil.ignore_patterns("node_modules", ".git", ".wrangler"))
        deps = repo_config(slug).get("deps")
        if deps:
            subprocess.run(["cp", "-cR", deps, str(code / "node_modules")], check=True)
    else:
        checkout(slug, sha, code)
    env = ci_env()
    ok, log = True, []
    for step in cfg.get("build", []) + [m.replace("{persist}", str(persist)) for m in cfg.get("migrate", [])]:
        result = subprocess.run(["bash", "-eo", "pipefail", "-c", step], cwd=code, capture_output=True, text=True, env=env)
        log.append(f"$ {step}\n{result.stdout}{result.stderr}")
        if result.returncode != 0:
            ok = False
            break
    port, pid = None, None
    if ok:
        port = free_port()
        out = open(where / "workerd.log", "a")
        proc = subprocess.Popen(real_wrangler(code) + ["dev", "--port", str(port), "--ip", "127.0.0.1",
                                 "--persist-to", str(persist), "--show-interactive-dev-session=false"],
                                cwd=code, stdout=out, stderr=out, stdin=subprocess.DEVNULL,
                                start_new_session=True, env=env)
        pid = proc.pid
        ok = wait_port(port, 60)
        if not ok:
            log.append((where / "workerd.log").read_text()[-2000:])
    record = {"id": f"{sha[:8]}-{target}", "branch": branch, "sha": sha, "target": target, "host": host,
              "url": public_url(host), "port": port, "pid": pid, "ok": ok, "at": now(), "log": "\n".join(log)[-4000:]}
    with state() as data:
        repo = data["repos"][slug]
        repo["deployments"].append({k: v for k, v in record.items() if k != "log"})
        if production:
            repo["production"] = record
        else:
            repo["previews"][branch] = record
        routes = data.setdefault("routes", {})
        if ok:
            routes[host] = port
    if not production:
        announce_preview(slug, branch)
    return record


def wait_port(port, seconds):
    deadline = time.time() + seconds
    while time.time() < deadline:
        with socket.socket() as s:
            if s.connect_ex(("127.0.0.1", port)) == 0:
                return True
        time.sleep(0.3)
    return False


def stop_deployment(slug, branch, production):
    with state() as data:
        repo = data["repos"].get(slug) or {}
        old = repo.get("production") if production else repo.get("previews", {}).get(branch)
    if old and old.get("pid"):
        with contextlib.suppress(ProcessLookupError, PermissionError):
            os.killpg(old["pid"], signal.SIGTERM)


def stop_preview(slug, branch):
    stop_deployment(slug, branch, False)
    with state() as data:
        old = data["repos"][slug]["previews"].pop(branch, None)
        if old:
            data.get("routes", {}).pop(old["host"], None)


def announce_preview(slug, branch):
    """Workers Builds comments on the pull request of the branch with the preview's state and URL."""
    with state() as data:
        repo = data["repos"][slug]
        preview = repo["previews"].get(branch)
        pr = next((p for p in repo["prs"].values() if p["head"] == branch and p["state"] == "OPEN"), None)
        if not preview or not pr:
            return
        status = "✅ Deployment successful!" if preview["ok"] else "❌ Deployment failed"
        url = preview["url"] if preview["ok"] else "-"
        body = ("## Deploying with &nbsp;<a href=\"https://workers.dev\"><img alt=\"Cloudflare Workers\" "
                "src=\"https://workers.cloudflare.com/logo.svg\" width=\"16\"></a> &nbsp;Cloudflare Workers\n\n"
                "The latest updates on your project. Learn more about [integrating Git with Workers]"
                "(https://developers.cloudflare.com/workers/ci-cd/builds/git-integration/).\n\n"
                "| Status | Name | Latest Commit | Preview URL | Updated (UTC) |\n| - | - | - | - | - |\n"
                f"| {status} | {repo_config(slug)['worker']} | {preview['sha'][:7]} | {url} | {preview['at']} |")
        bot = "cloudflare-workers-and-pages"
        mine = [c for c in pr["comments"] if c["author"] == bot]
        if mine:
            mine[0].update(body=body, updated=now())
        else:
            pr["comments"].append({"id": next_id(data), "author": bot, "body": body, "created": now(), "updated": now()})


def next_id(data):
    data["ids"] = data.get("ids", 3000000000) + 1
    return data["ids"]


# ---------------------------------------------------------------- proxy


def serve_proxy(port):
    """Route `<name>.localhost` to the workerd process of that deployment."""
    import http.client
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    class Proxy(BaseHTTPRequestHandler):
        def handle_any(self):
            host = (self.headers.get("Host") or "").split(":")[0]
            with state(write=False) as data:
                target = data.get("routes", {}).get(host)
            if not target:
                self.send_response(404)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(b"There is nothing here yet.\n")
                return
            length = int(self.headers.get("Content-Length") or 0)
            body = self.rfile.read(length) if length else None
            conn = http.client.HTTPConnection("127.0.0.1", target, timeout=60)
            # The Worker sees the address the client used, as it would behind Cloudflare.
            headers = dict(self.headers.items())
            conn.request(self.command, self.path, body=body, headers=headers)
            resp = conn.getresponse()
            data = resp.read()
            self.send_response(resp.status)
            for k, v in resp.getheaders():
                if k.lower() not in ("transfer-encoding", "connection", "content-length"):
                    self.send_header(k, v)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        do_GET = do_POST = do_PUT = do_PATCH = do_DELETE = do_HEAD = do_OPTIONS = handle_any

        def log_message(self, *args):
            pass

    ThreadingHTTPServer(("127.0.0.1", port), Proxy).serve_forever()


def shutdown():
    """Stop every process the stand-in started."""
    with state(write=False) as data:
        pids = [d.get("pid") for repo in data["repos"].values() for d in repo["deployments"]]
        pids.append(data.get("proxy_pid"))
    groups = [pid for pid in filter(None, pids) if signal_group(pid, signal.SIGTERM)]
    deadline = time.time() + 10
    while groups and time.time() < deadline:
        time.sleep(0.2)
        groups = [pid for pid in groups if signal_group(pid, 0)]


def signal_group(pid, sig):
    """Send `sig` to a process group, and say whether the group still exists."""
    try:
        os.killpg(pid, sig)
        return True
    except (ProcessLookupError, PermissionError):
        return False


def processes_under(root):
    """The processes, other than this one, whose command line or working directory lies under `root`.

    A session starts servers of its own, such as `pnpm dev`, in a session of their own, so they
    outlive it unless something stops them."""
    forms = {str(root)} | ({str(root).removeprefix("/private")} if str(root).startswith("/private/") else set())
    def under(text):
        return any(text == f or f + "/" in text or text.endswith(" " + f) for f in forms)
    found = {}
    ps = subprocess.run(["ps", "-axo", "pid=,command="], capture_output=True, text=True).stdout
    for line in ps.splitlines():
        pid, _, command = line.strip().partition(" ")
        if pid.isdigit() and under(command):
            found[int(pid)] = command
    lsof = subprocess.run(["lsof", "-a", "-d", "cwd", "-Fpn"], capture_output=True, text=True).stdout
    pid = None
    for line in lsof.splitlines():
        if line.startswith("p"):
            pid = int(line[1:])
        elif line.startswith("n") and pid and pid not in found and under(line[1:]):
            found[pid] = subprocess.run(["ps", "-o", "command=", "-p", str(pid)], capture_output=True, text=True).stdout.strip()
    found.pop(os.getpid(), None)
    return {pid: command for pid, command in found.items() if command}


def stop_processes_under(root, grace=5):
    """Stop every process under `root`, TERM first and KILL after `grace` seconds. Returns what was running."""
    running = processes_under(root)
    left = running
    for sig in (signal.SIGTERM, signal.SIGKILL):
        for pid in left:
            with contextlib.suppress(ProcessLookupError, PermissionError):
                os.kill(pid, sig)
        deadline = time.time() + grace
        while left and time.time() < deadline:
            time.sleep(0.2)
            left = processes_under(root)
        if not left:
            break
    return running
