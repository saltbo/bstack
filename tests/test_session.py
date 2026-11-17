"""Check the keeper's session script on a small synthetic transcript, and the shape of the behavior cases."""

from pathlib import Path
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".agents/skills/keeper/scripts/session.py"
SESSION = "00000000-0000-4000-8000-000000000001"


def at(second):
    return f"2026-11-17T10:00:{second:02d}.000Z"


def assistant(second, *blocks):
    return {"type": "assistant", "timestamp": at(second), "message": {"content": list(blocks)}}


def user(second, content, meta=False):
    return {"type": "user", "timestamp": at(second), "isMeta": meta, "message": {"content": content}}


def call(id_, name, args):
    return {"type": "tool_use", "id": id_, "name": name, "input": args}


def result(id_, text, error=False):
    return {"type": "tool_result", "tool_use_id": id_, "content": text, "is_error": error}


TRANSCRIPT = [
    user(0, "Fix the paging bug."),
    assistant(1, call("a", "Bash", {"command": "skills show bugfix; cat x/bstack-handbook/lifecycle/testing.md"})),
    user(2, [result("a", "Skill: bugfix ...")]),
    assistant(3, call("b", "Skill", {"skill": "bstack-writing"})),
    user(4, [result("b", "Launching skill")]),
    user(4, [{"type": "text", "text": "Base directory for this skill: /s/bstack-writing\n\n# Writing"}], meta=True),
    assistant(5, call("c", "Bash", {"command": "sed -i '' 's/a/b/' one.md; echo done"})),
    user(6, [result("c", "gsed: can't read s/a/b/: No such file or directory\ndone")]),
    assistant(7, call("d", "Bash", {"command": "sed -i '' 's/c/d/' two.md"})),
    user(8, [result("d", "gsed: can't read s/c/d/: No such file or directory")]),
    assistant(9, call("e", "Bash", {"command": "false"})),
    user(10, [result("e", "Exit code 1", error=True)]),
    assistant(11, {"type": "text", "text": "Done, cited verification@6.\n\nShall I also push it?"}),
    user(30, "Yes."),
]


class SessionScriptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home = tempfile.TemporaryDirectory()
        project = Path(cls.home.name) / "projects/-work"
        project.mkdir(parents=True)
        (project / f"{SESSION}.jsonl").write_text("\n".join(json.dumps(r) for r in TRANSCRIPT) + "\n")
        subagents = project / SESSION / "subagents"
        subagents.mkdir(parents=True)
        (subagents / "agent-abcdef0123.jsonl").write_text(json.dumps(user(12, "Review the diff.")) + "\n")
        (subagents / "agent-abcdef0123.meta.json").write_text(json.dumps({"agentType": "reviewer"}))
        env = dict(os.environ, CLAUDE_CONFIG_DIR=cls.home.name)
        out = subprocess.run([sys.executable, str(SCRIPT), "report", SESSION, "--json"],
                             capture_output=True, text=True, env=env)
        assert out.returncode == 0, out.stderr
        cls.report = json.loads(out.stdout)

    @classmethod
    def tearDownClass(cls):
        cls.home.cleanup()

    def test_skills_are_found_however_they_were_loaded(self):
        self.assertEqual({("bugfix", "skills show"), ("bstack-writing", "Skill tool")},
                         {(s["name"], s["via"]) for s in self.report["skills"]})

    def test_handbook_text_read_through_the_shell_is_listed(self):
        self.assertIn("bstack-handbook/lifecycle/testing.md", [t["path"] for t in self.report["texts_read"]])

    def test_a_failure_hidden_in_a_compound_command_counts(self):
        self.assertEqual(["error in output", "error in output", "failed"],
                         [f["how"] for f in self.report["failed_calls"]])

    def test_the_same_error_with_different_arguments_is_grouped(self):
        self.assertEqual(1, len(self.report["repeated_failures"]))
        self.assertEqual(2, len(self.report["repeated_failures"][0]["events"]))

    def test_questions_and_citations_and_briefs(self):
        self.assertEqual(1, len(self.report["questions_to_user"]))
        self.assertEqual({"verification@6": 1}, self.report["handbooks_cited"])
        self.assertEqual(["reviewer:abcdef01"], self.report["subagents"])
        self.assertEqual(["Fix the paging bug.", "Yes."], [m["text"] for m in self.report["user_messages"]])


class CaseLayoutTests(unittest.TestCase):
    def test_every_end_to_end_case_has_a_request_a_fixture_and_a_check(self):
        cases = [p for p in (ROOT / "e2e").iterdir() if p.is_dir() and p.name[0] not in "._" and p.name != "results"]
        self.assertTrue(cases)
        for case in cases:
            with self.subTest(case=case.name):
                for part in ("request.md", "fixture", "check.sh"):
                    self.assertTrue((case / part).exists(), part)

    def test_every_eval_case_has_a_prompt_and_graders(self):
        cases = [p for p in (ROOT / "evals").iterdir() if p.is_dir() and p.name[0] not in "._" and p.name != "results"]
        self.assertTrue(cases)
        for case in cases:
            with self.subTest(case=case.name):
                self.assertTrue((case / "prompt.md").exists())
                self.assertTrue(list((case / "graders").glob("*.md")))

    def test_the_scripts_are_executable(self):
        for path in (SCRIPT, ROOT / "e2e/run.py"):
            self.assertTrue(os.access(path, os.X_OK), path)


if __name__ == "__main__":
    unittest.main()
