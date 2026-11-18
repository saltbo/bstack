"""The stand-in for GitHub, without an agent: a branch goes from push to a merged PR as gh reports it."""

from pathlib import Path
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "e2e/sim"))
import simcore  # noqa: E402

WORKFLOW = """name: CI
on: [push, pull_request]
jobs:
  test:
    name: test
    steps:
      - uses: actions/checkout@v4
      - run: python3 -m unittest -q
      - run: |
          echo one
          echo two
"""


class WorkflowTests(unittest.TestCase):
    def test_jobs_and_shell_steps_are_read(self):
        name, jobs = simcore.parse_workflow(WORKFLOW)
        self.assertEqual("CI", name)
        self.assertEqual([{"name": "test", "steps": ["python3 -m unittest -q", "echo one\necho two"]}], jobs)


class GitHubFlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp()).resolve()
        sim = cls.tmp / "sim"
        fixture = ROOT / "e2e/fixtures/orderdesk"
        clean = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        cls.env = dict(clean, SIM_ROOT=str(sim), GIT_EXEC_PATH=str(simcore.exec_path(cls.tmp)),
                       GIT_CONFIG_GLOBAL=str(cls.tmp / "gitconfig"),
                       PATH=os.pathsep.join([str(ROOT / "e2e/sim/bin"), os.environ["PATH"]]))
        (cls.tmp / "gitconfig").write_text(simcore.gitconfig(sim, "Tester", "t@example.com"))
        cls.saved = dict(os.environ)
        os.environ.clear()
        os.environ.update(cls.env)
        simcore.setup(sim, {"proxy_port": 1, "repos": {"saltbo/orderdesk": {"fixture": str(fixture), "worker": None}}})
        cls.work = cls.tmp / "orderdesk"
        cls.sh(["git", "clone", "-q", "https://github.com/saltbo/orderdesk.git", str(cls.work)], cwd=cls.tmp)

    @classmethod
    def tearDownClass(cls):
        os.environ.clear()
        os.environ.update(cls.saved)
        shutil.rmtree(cls.tmp, ignore_errors=True)

    @classmethod
    def sh(cls, args, cwd=None, check=True):
        result = subprocess.run(args, cwd=cwd or cls.work, env=cls.env, capture_output=True, text=True)
        if check and result.returncode != 0:
            raise AssertionError(f"{args}: {result.stdout}{result.stderr}")
        return result

    def test_a_branch_goes_from_push_to_merged(self):
        self.assertIn("https://github.com/saltbo/orderdesk.git", self.sh(["git", "remote", "-v"]).stdout)
        self.sh(["git", "checkout", "-q", "-b", "fix/readme"])
        (self.work / "NOTE.md").write_text("note\n")
        self.sh(["git", "add", "NOTE.md"])
        self.sh(["git", "-c", "user.name=T", "-c", "user.email=t@e", "commit", "-qm", "docs: add a note"])
        self.sh(["git", "push", "-q", "-u", "origin", "fix/readme"])
        url = self.sh(["gh", "pr", "create", "--draft", "--title", "docs: add a note", "--body", "x"]).stdout.strip()
        self.assertEqual("https://github.com/saltbo/orderdesk/pull/1", url)
        checks = self.sh(["gh", "pr", "checks", "--watch", "--json", "name,bucket"]).stdout
        self.assertEqual([{"name": "test", "bucket": "pass"}], json.loads(checks))
        # Outside a terminal gh prints only tab-separated rows, which scripts wait on.
        self.assertEqual(["test", "pass"], self.sh(["gh", "pr", "checks"]).stdout.split("\t")[:2])
        refused = self.sh(["gh", "pr", "merge", "--squash"], check=False)
        self.assertNotEqual(0, refused.returncode)
        self.assertIn("still a draft", refused.stderr)
        self.sh(["gh", "pr", "ready"])
        merged = self.sh(["gh", "pr", "merge", "--squash", "--delete-branch"]).stdout
        self.assertIn("Squashed and merged pull request saltbo/orderdesk#1", merged)
        self.assertEqual("main", self.sh(["git", "branch", "--show-current"]).stdout.strip())
        state = json.loads(self.sh(["gh", "pr", "view", "1", "--json", "state,mergeCommit"]).stdout)
        self.assertEqual("MERGED", state["state"])
        heads = self.sh(["git", "ls-remote", "--heads", "origin"]).stdout
        self.assertNotIn("fix/readme", heads)
        deadline = time.time() + 30
        while time.time() < deadline:
            runs = json.loads(self.sh(["gh", "run", "list", "--json", "headBranch,conclusion"]).stdout)
            if any(r["headBranch"] == "main" and r["conclusion"] for r in runs):
                break
            time.sleep(0.5)
        self.assertIn({"headBranch": "main", "conclusion": "success"}, runs)


if __name__ == "__main__":
    unittest.main()
