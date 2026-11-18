"""`wrangler` as the agent sees it: remote commands act on the stand-in's Cloudflare, local ones run the real wrangler."""

import os
import subprocess
import sys
from pathlib import Path

import simcore as sim
from simcore import git, state


def slug_here():
    url = git("config", "--get", "remote.origin.url", check=False)
    for slug in sim.config()["repos"]:
        if url.rstrip("/").removesuffix(".git").endswith(slug):
            return slug
    return None


def persist_for(slug, argv):
    target = "preview" if "--preview" in argv else "production"
    return sim.ROOT / "cf" / slug / f"{target}-state"


def main(argv):
    code, note = 0, ""
    slug = slug_here()
    verb = argv[0] if argv else ""
    try:
        if verb == "whoami":
            print(" ⛅️ wrangler\n───────────────────\nGetting User settings...\n"
                  "👋 You are logged in with an OAuth Token, associated with the email saltbo@example.com.\n"
                  "┌──────────────┬──────────────────────────────────┐\n│ Account Name │ Account ID                       │\n"
                  "├──────────────┼──────────────────────────────────┤\n│ Saltbo       │ 0123456789abcdef0123456789abcdef │\n"
                  "└──────────────┴──────────────────────────────────┘")
        elif verb == "login":
            print("Successfully logged in.")
        elif verb == "deploy" and slug:
            sha = git("rev-parse", "HEAD")
            record = sim.deploy(slug, git("rev-parse", "--abbrev-ref", "HEAD"), sha, production=True, source=Path.cwd())
            if not record["ok"]:
                print(record["log"], file=sys.stderr)
                code = 1
            else:
                print(f"Uploaded {sim.repo_config(slug)['worker']}\nDeployed {sim.repo_config(slug)['worker']} triggers\n  {record['url']}\n"
                      f"Current Version ID: {record['id']}")
        elif verb in ("versions", "deployments") and argv[1:2] == ["list"] and slug:
            with state(write=False) as data:
                for d in data["repos"][slug]["deployments"][-10:]:
                    print(f"Created:     {d['at']}\nVersion(s):  (100%) {d['id']}\nTarget:      {d['target']}\nURL:         {d['url']}\n")
        elif verb == "tail" and slug:
            log = sim.ROOT / "cf" / slug / "production" / "workerd.log"
            print("Successfully created tail, expires at (in 6 hours)\nConnected to the production worker, waiting for logs...")
            if log.exists():
                print("\n".join(log.read_text().splitlines()[-40:]))
        elif verb == "d1" and "--remote" in argv and slug:
            persist = persist_for(slug, argv)
            rest = [a for a in argv if a not in ("--remote", "--preview")] + ["--local", "--persist-to", str(persist)]
            code = subprocess.run(real(Path.cwd()) + rest).returncode
        else:
            code = subprocess.run(real(Path.cwd()) + argv).returncode
    except Exception as exc:  # a gap in the stand-in
        print(f"✘ [ERROR] {exc}", file=sys.stderr)
        code, note = 1, f"stand-in error: {exc!r}"
    sim.log_call("wrangler", argv, code, note)
    return code


def real(cwd):
    return sim.real_wrangler(cwd)
