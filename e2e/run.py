#!/usr/bin/env python3
"""Run end-to-end cases: one real Claude Code session per case, on a local stand-in for GitHub and Cloudflare.

A case is a directory holding `case.json`, `request.md`, the user's request, and
`check.sh`, which judges the outcome against the stand-in's state afterwards.
`case.json` names the repositories on the stand-in, each from a fixture under
`e2e/fixtures/`, and the one the session starts in.

The session starts in a clone of that repository, with dependencies installed,
and works as it would on Saltbo's machine. `git` and `gh` reach the stand-in's
GitHub, a push runs the repository's workflow and, for a Workers project,
deploys a preview or production on the local Workers runtime. It sees only this
checkout's skills and the user-level instructions in `sim/user-agents.md`, and
none of the user's own skills, settings, MCP servers, or credentials. Browser checks run in ego-browser task spaces of their own, which
are closed afterwards. Nothing else it does leaves the scratch directory, which
is removed afterwards. One run at a time holds the machine, because sessions
choose local ports for their own dev servers. The transcript, the stand-in's state and call log, and the reports
go to `e2e/results/<time>/<case>/`.

  e2e/run.py [case ...] [--model M] [--timeout SECONDS] [--keep]
"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from datetime import datetime
from pathlib import Path

E2E = Path(__file__).resolve().parent
ROOT = E2E.parent
SIM = E2E / "sim"
SESSION = ROOT / ".agents/skills/revise-from-evidence/scripts/session.py"
CACHE = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "bstack-e2e"
INSTALLED = ["autopilot", "bstack-handbook", "bstack-worker", "bstack-writing", "bugfix", "xplan"]
PINNED = ["autopilot", "bugfix", "xplan", "bstack-writing"]
# Tools on the machine that would reach real services, or carry the user's own setup.
HIDDEN_TOOLS = ["realmroot", "gh", "wrangler", "hc", "agent-browser"]
DOCKET = Path(os.environ.get("BSTACK_E2E_DOCKET", Path.home() / "Develop/bogit/docket"))
# The user-level instructions of the stand-in's machine, maintained here for it.
USER_INSTRUCTIONS = SIM / "user-agents.md"
# What a session must never change on the user's machine. A change is reported as a leak.
GUARDED = [Path.home() / p for p in (".claude/skills", ".agents/skills", ".agents/.skill-lock.json", ".gitconfig",
                                     ".config/gh", ".local/share/bbox/skills", ".local/share/docket/tasks.db")]

sys.path.insert(0, str(SIM))
import simcore  # noqa: E402
import user as sim_user  # noqa: E402

ORIGINAL_ENV = dict(os.environ)


def sh(args, cwd, env=None, check=True, **kw):
    result = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True, **kw)
    if check and result.returncode != 0:
        sys.exit(f"{' '.join(map(str, args))} failed:\n{result.stdout}{result.stderr}")
    return result


def clean_path(root):
    """The user's PATH, with the tools that would reach real services left out.

    A directory that holds one of them is replaced by a directory of links to everything else in it."""
    entries = []
    for i, entry in enumerate(os.environ["PATH"].split(os.pathsep)):
        directory = Path(entry)
        if not entry or not directory.is_dir():
            continue
        if not any((directory / tool).exists() for tool in HIDDEN_TOOLS):
            entries.append(entry)
            continue
        farm = root / "path" / str(i)
        farm.mkdir(parents=True)
        for item in directory.iterdir():
            if item.name not in HIDDEN_TOOLS:
                (farm / item.name).symlink_to(item)
        entries.append(str(farm))
    return os.pathsep.join(entries)


def dependencies(fixture):
    """node_modules for a fixture with a lockfile, built once and cloned into every checkout."""
    lock = fixture / "pnpm-lock.yaml"
    if not lock.exists():
        return None
    key = hashlib.sha256(lock.read_bytes() + (fixture / "package.json").read_bytes() + str(SIM).encode()).hexdigest()[:16]
    target = CACHE / "deps" / key / "node_modules"
    if target.exists():
        return target
    build = Path(tempfile.mkdtemp(prefix="deps-", dir=CACHE))
    shutil.copy(lock, build)
    shutil.copy(fixture / "package.json", build)
    sh(["pnpm", "install", "--frozen-lockfile"], build)
    shim = build / "node_modules/.bin/wrangler"
    if shim.exists():
        shim.unlink()
        shim.write_text('#!/bin/sh\nif [ -n "$SIM_ROOT" ]; then exec "${SIM_PYTHON:-python3}" "$SIM_HOME/sim.py" wrangler "$@"; fi\n'
                        'exec node "$(dirname "$0")/../wrangler/bin/wrangler.js" "$@"\n')
        shim.chmod(0o755)
    target.parent.mkdir(parents=True, exist_ok=True)
    (build / "node_modules").rename(target)
    shutil.rmtree(build)
    return target


def platform(case, root):
    """Bring up the stand-in: its repositories, the proxy for deployments, and the session's environment."""
    spec = json.loads((case / "case.json").read_text())
    sim_root = root / "sim"
    proxy_port = simcore.free_port()
    repos = {}
    for slug, repo in spec["repos"].items():
        fixture = (case / repo["fixture"]).resolve()
        seed = root / "fixtures" / slug
        shutil.copytree(fixture, seed, ignore=shutil.ignore_patterns("node_modules", "__pycache__"))
        for path in seed.rglob("*.md"):
            path.write_text(path.read_text().replace("{{PROXY_PORT}}", str(proxy_port)))
        deps = dependencies(fixture)
        repos[slug] = {**repo, "fixture": str(seed), "deps": str(deps) if deps else None}
    cfg = {"proxy_port": proxy_port, "repos": repos}

    path = os.pathsep.join([str(SIM / "bin"), clean_path(root)])
    env = {k: v for k, v in simcore.outside_env().items()
           if not k.startswith(("GH_", "GITHUB_", "CLOUDFLARE_", "CF_", "REALMROOT"))}
    gh_config = root / "gh"
    gh_config.mkdir()
    gitconfig = root / "gitconfig"
    gitconfig.write_text(simcore.gitconfig(sim_root, "Saltbo", "saltbo@example.com"))
    env.update(PATH=path, SIM_ROOT=str(sim_root), GIT_EXEC_PATH=str(simcore.exec_path(root)), SIM_HOME=str(SIM), SIM_PYTHON=sys.executable,
               SIM_CI_PATH=path, GIT_CONFIG_GLOBAL=str(gitconfig), GH_CONFIG_DIR=str(gh_config),
               CLOUDFLARE_API_TOKEN="sim-no-real-cloudflare", CLOUDFLARE_ACCOUNT_ID="0123456789abcdef0123456789abcdef",
               BBOX_SKILLS_HOME=str(root / "store"), BBOX_SKILLS_LOCK=str(root / "skill-lock.json"),
               WRANGLER_SEND_METRICS="false")
    os.environ.update({k: env[k] for k in ("SIM_ROOT", "SIM_HOME", "SIM_PYTHON", "SIM_CI_PATH", "GIT_CONFIG_GLOBAL", "GIT_EXEC_PATH")})
    os.environ["PATH"] = path
    simcore.ROOT = sim_root
    sim_root.mkdir()
    proxy = subprocess.Popen([sys.executable, str(SIM / "sim.py"), "proxy", str(proxy_port)], env=env,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    simcore.setup(sim_root, cfg)
    with simcore.state() as data:
        data["proxy_pid"] = proxy.pid

    start = spec["start"]
    work = root / "Develop" / start.split("/")[1]
    sh(["git", "clone", "-q", f"https://github.com/{start}.git", str(work)], root, env)
    if repos[start].get("deps"):
        sh(["cp", "-cR", repos[start]["deps"], str(work / "node_modules")], root)
    (work / ".git/info/exclude").write_text(".claude/\n")
    (work / ".claude/skills").mkdir(parents=True)
    # User-level settings stay out, so these reach the session as the project's local instructions.
    shutil.copy(USER_INSTRUCTIONS, work / ".claude/CLAUDE.md")
    # The session's own `skills` calls refresh the router skill, so they must see the same directories.
    env["BBOX_SKILLS_AGENT_DIRS"] = str(work / ".claude/skills")
    sh(["skills", "install", *[a for n in INSTALLED for a in ("-s", n)], str(ROOT)], root, env)
    for name in PINNED:
        sh(["skills", "pin", name], root, env)
    return spec, work, env, proxy_port


def fingerprint():
    """Names, sizes, and modification times under the guarded paths, without following links.

    `~/.claude/skills/synced` is left out: every Claude Code process refreshes it from claude.ai by itself."""
    seen = {}
    for base in GUARDED:
        paths = [base] if not base.is_dir() or base.is_symlink() else [base, *base.rglob("*")]
        for path in paths:
            if "/.claude/skills/synced" in str(path):
                continue
            try:
                st = path.lstat()
            except FileNotFoundError:
                continue
            seen[str(path)] = (st.st_size, int(st.st_mtime))
    return seen


def browser_spaces():
    """The ids of the ego-browser task spaces that exist now. Each run works in spaces of its own."""
    script = "console.log(JSON.stringify((await listTaskSpaces()).map((s) => s.id)))"
    result = subprocess.run(["ego-browser", "nodejs", "-e", script], capture_output=True, text=True, timeout=60,
                            env=simcore.outside_env(), stdin=subprocess.DEVNULL)
    try:
        # The embedded runtime writes console output to stderr.
        return set(json.loads((result.stdout + result.stderr).strip().splitlines()[-1]))
    except (ValueError, IndexError):
        return set()


def close_spaces(ids):
    """Close the task spaces a run left open, as `finish()` would have."""
    for space in ids:
        script = f"const task = await taskSpace({int(space)}); await task.finish({{ keep: [] }});"
        subprocess.run(["ego-browser", "nodejs", "-e", script], capture_output=True, text=True, timeout=60,
                       env=simcore.outside_env(), stdin=subprocess.DEVNULL)


def start_docket(root, env):
    """A docket server of the session's own, so its cards and tasks never reach the user's board."""
    port, token = simcore.free_port(), uuid.uuid4().hex
    data = root / "docket"
    log = open(root / "docket.log", "w")
    proc = subprocess.Popen(["node", str(DOCKET / "server.mjs")], cwd=DOCKET, stdout=log, stderr=log,
                            env=dict(env, DOCKET_PORT=str(port), DOCKET_DATA=str(data), DOCKET_TOKEN=token),
                            start_new_session=True)
    if not simcore.wait_port(port, 30):
        sys.exit(f"docket did not start: {(root / 'docket.log').read_text()}")
    config = {"mcpServers": {"docket": {"type": "http", "url": f"http://127.0.0.1:{port}/mcp",
                                        "headers": {"Authorization": f"Bearer {token}"}}}}
    return proc, sim_user.Docket(f"http://127.0.0.1:{port}/mcp", token, data / "tasks.db"), config


def wait_quiet(seconds=120):
    """Let builds and deployments started by the session's last push finish before judging."""
    deadline = time.time() + seconds
    while time.time() < deadline:
        with simcore.state(write=False) as data:
            busy = any(r["status"] != "completed" for repo in data["repos"].values() for r in repo["runs"])
        if not busy:
            return
        time.sleep(1)


def transcript_dir(work):
    return Path.home() / ".claude/projects" / str(work.resolve()).replace("/", "-").replace(".", "-").replace("_", "-")


def run_case(case, out, args):
    os.environ.clear()
    os.environ.update(ORIGINAL_ENV)
    root = Path(tempfile.mkdtemp(prefix=f"bstack-e2e-{case.name}-")).resolve()
    out.mkdir(parents=True, exist_ok=True)
    work = None
    try:
        before = fingerprint()
        spaces_before = browser_spaces()
        spec, work, env, proxy_port = platform(case, root)
        mcp = {"mcpServers": {}}
        docket = stop = None
        persona = (case / "user.md").read_text() if (case / "user.md").exists() else ""
        person = sim_user.User(persona, out / "user.log")
        if spec.get("docket"):
            docket_proc, docket, mcp = start_docket(root, env)
            stop = sim_user.threading.Event()
            watcher = sim_user.threading.Thread(target=sim_user.watch_cards, args=(docket, person, stop), daemon=True)
            watcher.start()
        (root / "mcp.json").write_text(json.dumps(mcp))
        session = str(uuid.uuid4())
        base = ["--setting-sources", "project,local", "--permission-mode", "bypassPermissions",
                "--output-format", "json", "--mcp-config", str(root / "mcp.json"), "--strict-mcp-config"]
        if args.model:
            base += ["--model", args.model]
        started = time.time()
        budget = spec.get("timeout", args.timeout)
        prompt, first, final, turns, cost, replies = (case / "request.md").read_text(), True, {}, 0, 0.0, 0
        while True:
            command = ["claude", "-p", prompt, *(["--session-id", session] if first else ["--resume", session]), *base]
            remaining = budget - (time.time() - started)
            try:
                run = subprocess.run(command, cwd=work, env=env, capture_output=True, text=True, timeout=max(remaining, 30),
                                     stdin=subprocess.DEVNULL)
                final = json.loads(run.stdout) if run.stdout.strip().startswith("{") else {"result": run.stdout + run.stderr}
            except subprocess.TimeoutExpired:
                final = {"result": f"timed out after {budget} s"}
                break
            turns += final.get("num_turns") or 0
            cost += final.get("total_cost_usd") or 0
            first = False
            text = str(final.get("result", ""))
            if replies >= spec.get("max_replies", 3) or not sim_user.asks_user(text):
                break
            prompt, replies = person.reply(text), replies + 1
        if stop:
            stop.set()
        seconds = round(time.time() - started)
        wait_quiet()

        (out / "final.txt").write_text(str(final.get("result", "")))
        check_env = dict(env, STATE=str(root / "sim/state.json"), WORK=str(work), PROXY_PORT=str(proxy_port),
                         DOCKET_DB=str(root / "docket/tasks.db"), FINAL=str(out / "final.txt"),
                         E2E_LIB=str(E2E / "lib.sh"))
        check = sh(["bash", str(case / "check.sh")], work, check_env, check=False)

        saved = transcript_dir(work)
        if saved.exists():
            shutil.copytree(saved, out / "transcript", dirs_exist_ok=True)
        report = sh([sys.executable, str(SESSION), "report", str(out / "transcript" / f"{session}.jsonl"), "--json"],
                    ROOT, check=False)
        signals = json.loads(report.stdout) if report.returncode == 0 else {"error": report.stderr}
        (out / "report.md").write_text(sh([sys.executable, str(SESSION), "report",
                                           str(out / "transcript" / f"{session}.jsonl")], ROOT, check=False).stdout)
        for name in ("state.json", "calls.log"):
            if (root / "sim" / name).exists():
                shutil.copy(root / "sim" / name, out / name)
        (out / "check.txt").write_text(check.stdout + check.stderr)
        calls = [json.loads(l) for l in (out / "calls.log").read_text().splitlines()] if (out / "calls.log").exists() else []
        summary = {
            "case": case.name, "session": session, "outcome": "pass" if check.returncode == 0 else "fail",
            "seconds": seconds, "turns": turns, "cost_usd": round(cost, 2), "user_replies": replies,
            "cards_answered": sum(1 for l in (out / "user.log").read_text().splitlines() if '"card:' in l) if (out / "user.log").exists() else 0,
            "skills": sorted({s["name"] for s in signals.get("skills", [])}),
            "failed_calls": len(signals.get("failed_calls", [])),
            "repeated_errors": len(signals.get("repeated_failures", [])),
            "questions_to_user": len(signals.get("questions_to_user", [])),
            "subagents": signals.get("subagents", []),
            "platform_calls": len(calls),
            "platform_gaps": [c["argv"] for c in calls if c.get("note")],
        }
        if spec.get("docket"):
            docket_proc.terminate()
            shutil.copytree(root / "docket", out / "docket", dirs_exist_ok=True)
        simcore.shutdown()
        if transcript_dir(work).exists():
            shutil.rmtree(transcript_dir(work))
        left = sorted(browser_spaces() - spaces_before)
        close_spaces(left)
        summary["browser_spaces_left_open"] = left
        after = fingerprint()
        summary["leaks"] = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
        (out / "result.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
        return summary
    finally:
        if simcore.ROOT.exists():
            simcore.shutdown()
        if work is not None and transcript_dir(work).exists():
            shutil.rmtree(transcript_dir(work))
        if args.keep:
            print(f"kept {root}", file=sys.stderr)
        else:
            shutil.rmtree(root, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("cases", nargs="*", help="case names; all when omitted")
    parser.add_argument("--model")
    parser.add_argument("--timeout", type=int, default=1800)
    parser.add_argument("--keep", action="store_true", help="keep the scratch directory")
    parser.add_argument("-j", "--jobs", type=int, default=1,
                        help="cases to run at once; give it only to cases whose sessions start no dev server")
    parser.add_argument("--results", help=argparse.SUPPRESS)
    parser.add_argument("--no-lock", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    # Sessions pick local ports for their own dev servers, so two runs at once can reach each other's.
    if not args.no_lock:
        CACHE.mkdir(parents=True, exist_ok=True)
        lock = open(CACHE / "run.lock", "w")
        try:
            import fcntl
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print("another e2e run is in progress; waiting for it", file=sys.stderr)
            fcntl.flock(lock, fcntl.LOCK_EX)
    names = args.cases or sorted(p.name for p in E2E.iterdir() if (p / "case.json").exists())
    results = Path(args.results) if args.results else E2E / "results" / datetime.now().strftime("%Y%m%d-%H%M%S")
    failed = False
    if args.jobs > 1:
        # Each case in a process of its own, because a case sets the process environment for its session.
        from concurrent.futures import ThreadPoolExecutor
        base = [sys.executable, str(Path(__file__).resolve()), "--no-lock", "--results", str(results),
                "--timeout", str(args.timeout), *(["--model", args.model] if args.model else []),
                *(["--keep"] if args.keep else [])]
        def one(name):
            return subprocess.run(base + [name], capture_output=True, text=True, stdin=subprocess.DEVNULL)
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            for name, done in zip(names, pool.map(one, names)):
                lines = [l for l in done.stdout.splitlines() if l.startswith("{")]
                print(lines[-1] if lines else json.dumps({"case": name, "outcome": "error", "stderr": done.stderr[-500:]}))
                failed |= done.returncode != 0
    else:
        for name in names:
            summary = run_case(E2E / name, results / name, args)
            failed |= summary["outcome"] != "pass"
            print(json.dumps(summary, ensure_ascii=False))
    print(f"results in {results}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
