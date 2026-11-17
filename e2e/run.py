#!/usr/bin/env python3
"""Run end-to-end cases: one real Claude Code session per case on bstack as it is in this checkout.

Each case is a directory holding `request.md`, the user's request; `fixture/`, the
repository the session starts in; and `check.sh`, which runs in that repository
afterwards and exits non-zero when the outcome is wrong. A case with a `remote`
file gets a local bare repository as `origin`.

The session sees only this checkout's skills, installed and pinned the way the
`skills` command installs them on Saltbo's machine, and none of the user's own
skills or instructions. After the run, the keeper's session script reports on
the transcript, and the results go to `e2e/results/<time>/<case>/`.

  e2e/run.py [case ...] [--model M] [--timeout SECONDS] [--keep]
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import uuid
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = Path(__file__).resolve().parent
SESSION = ROOT / ".agents/skills/keeper/scripts/session.py"
INSTALLED = ["autopilot", "bstack-handbook", "bstack-worker", "bstack-writing", "bugfix", "xplan"]
PINNED = ["autopilot", "bugfix", "xplan", "bstack-writing"]
GIT = ["git", "-c", "user.name=fixture", "-c", "user.email=fixture@example.com"]


def sh(args, cwd, env=None, check=True):
    result = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True)
    if check and result.returncode != 0:
        sys.exit(f"{' '.join(map(str, args))} failed:\n{result.stdout}{result.stderr}")
    return result


def prepare(case, scratch):
    work = scratch / "work"
    shutil.copytree(case / "fixture", work)
    sh(["git", "init", "-q", "-b", "main"], work)
    (work / ".git/info/exclude").write_text(".claude/\n")
    sh(GIT + ["add", "-A"], work)
    sh(GIT + ["commit", "-qm", "Initial commit"], work)
    if (case / "remote").exists():
        sh(["git", "init", "-q", "--bare", "-b", "main", str(scratch / "origin.git")], scratch)
        sh(["git", "remote", "add", "origin", str(scratch / "origin.git")], work)
        sh(["git", "push", "-q", "-u", "origin", "main"], work)

    env = dict(os.environ,
               BBOX_SKILLS_HOME=str(scratch / "store"),
               BBOX_SKILLS_AGENT_DIRS=str(work / ".claude/skills"),
               BBOX_SKILLS_LOCK=str(scratch / "skill-lock.json"))
    (work / ".claude/skills").mkdir(parents=True)
    selection = [arg for name in INSTALLED for arg in ("-s", name)]
    sh(["skills", "install", *selection, str(ROOT)], scratch, env)
    for name in PINNED:
        sh(["skills", "pin", name], scratch, env)
    return work, env


def run_case(case, out, args):
    scratch = Path(tempfile.mkdtemp(prefix=f"bstack-e2e-{case.name}-"))
    try:
        work, env = prepare(case, scratch)
        session = str(uuid.uuid4())
        command = ["claude", "-p", (case / "request.md").read_text(), "--session-id", session,
                   "--setting-sources", "project,local", "--permission-mode", "bypassPermissions",
                   "--output-format", "json"]
        if args.model:
            command += ["--model", args.model]
        started = datetime.now()
        try:
            run = subprocess.run(command, cwd=work, env=env, capture_output=True, text=True, timeout=args.timeout)
            final = json.loads(run.stdout) if run.stdout.strip().startswith("{") else {"result": run.stdout + run.stderr}
        except subprocess.TimeoutExpired:
            final = {"result": f"timed out after {args.timeout} s"}
        seconds = round((datetime.now() - started).total_seconds())

        check = sh(["bash", str(case / "check.sh")], work, dict(env, ORIGIN=str(scratch / "origin.git")), check=False)
        report = sh([sys.executable, str(SESSION), "report", session, "--json"], ROOT, check=False)
        signals = json.loads(report.stdout) if report.returncode == 0 else {"error": report.stderr}

        out.mkdir(parents=True, exist_ok=True)
        (out / "final.txt").write_text(str(final.get("result", "")))
        (out / "check.txt").write_text(check.stdout + check.stderr)
        (out / "report.md").write_text(sh([sys.executable, str(SESSION), "report", session], ROOT, check=False).stdout)
        summary = {
            "case": case.name,
            "session": session,
            "outcome": "pass" if check.returncode == 0 else "fail",
            "seconds": seconds,
            "turns": final.get("num_turns"),
            "cost_usd": final.get("total_cost_usd"),
            "skills": sorted({s["name"] for s in signals.get("skills", [])}),
            "failed_calls": len(signals.get("failed_calls", [])),
            "repeated_errors": len(signals.get("repeated_failures", [])),
            "questions_to_user": len(signals.get("questions_to_user", [])),
            "subagents": len(signals.get("subagents", [])),
        }
        (out / "result.json").write_text(json.dumps(summary, indent=2))
        return summary
    finally:
        if args.keep:
            print(f"kept {scratch}", file=sys.stderr)
        else:
            shutil.rmtree(scratch, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("cases", nargs="*", help="case names; all when omitted")
    parser.add_argument("--model")
    parser.add_argument("--timeout", type=int, default=1800)
    parser.add_argument("--keep", action="store_true", help="keep the scratch repository")
    args = parser.parse_args()

    names = args.cases or sorted(p.name for p in CASES.iterdir() if (p / "request.md").exists())
    results = CASES / "results" / datetime.now().strftime("%Y%m%d-%H%M%S")
    failed = False
    for name in names:
        summary = run_case(CASES / name, results / name, args)
        failed |= summary["outcome"] != "pass"
        print(json.dumps(summary))
    print(f"results in {results}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
