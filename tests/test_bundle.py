"""Verify the role skills and the handbook are self-contained, explicit-only, versioned, and lean."""

from pathlib import Path
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / "skills"
SKILLS = ["autopilot", "bugfix", "xplan", "bstack-worker", "bstack-handbook"]
# bugfix and xplan end under autopilot, so each links to it.
ENTRIES = ["bugfix", "xplan"]
# The keeper serves this repository only, so it lives outside the installed suite.
KEEPER = ROOT / ".agents/skills/keeper"
KEEPER_LINE_BUDGET = 50
HANDBOOK = SUITE / "bstack-handbook"
LINK = re.compile(r"\[[^\]\n]+\]\(([^\s)]+)\)")
# Budgets keep the role skills and each handbook small. Raise one only with a reason.
LINE_BUDGETS = {
    "autopilot/SKILL.md": 45,
    "bugfix/SKILL.md": 35,
    "xplan/SKILL.md": 40,
    "bstack-worker/SKILL.md": 70,
    "bstack-handbook/SKILL.md": 90,
}
HANDBOOK_LINE_BUDGET = 65
SHOUTING = re.compile(r"\b(MUST|NEVER|ALWAYS|CRITICAL|IMPORTANT|MANDATORY)\b")
REMOVED = re.compile(
    r"playbooks/|host-adapter|poteto|pstack|principle-|\b(swarm|arena|interrogate|architect|unslop)\b skill"
)


def local_targets(source):
    text = re.sub(r"```.*?```", "", source.read_text(), flags=re.S)
    for target in LINK.findall(text):
        url = urlsplit(target)
        if not url.scheme and not url.netloc and url.path:
            yield (source.parent / unquote(url.path)).resolve()


def handbook_files():
    files = []
    for group in ("lifecycle", "types", "policies"):
        files += sorted((HANDBOOK / group).glob("*.md"))
    return files


class BundleTests(unittest.TestCase):
    def test_suite_is_the_role_skills_and_the_handbook(self):
        self.assertEqual({SUITE / n / "SKILL.md" for n in SKILLS}, set(SUITE.rglob("SKILL.md")))
        for name in SKILLS:
            metadata = (SUITE / name / "SKILL.md").read_text().split("---", 2)[1]
            self.assertRegex(metadata, rf"(?m)^name: {name}$")
            self.assertRegex(metadata, r"(?m)^description: \S")

    def test_every_skill_is_explicit_only_on_every_host(self):
        for name in SKILLS:
            with self.subTest(skill=name):
                metadata = (SUITE / name / "SKILL.md").read_text().split("---", 2)[1]
                self.assertRegex(metadata, r"(?m)^disable-model-invocation: true$")
                codex = (SUITE / name / "agents/openai.yaml").read_text()
                self.assertRegex(codex, r"(?m)^policy:\n  allow_implicit_invocation: false$")
                self.assertIn("$" + name, codex)

    def test_leader_brief_names_the_worker_skill_criteria_and_handbooks(self):
        leader = (SUITE / "xplan/SKILL.md").read_text()
        for phrase in ("The brief opens with `skills show bstack-worker`", "acceptance criteria as a closed list", "the handbooks that apply"):
            self.assertIn(phrase, leader)

    def test_bugfix_and_xplan_finish_under_autopilot(self):
        autopilot = (SUITE / "autopilot/SKILL.md").resolve()
        for name in ENTRIES:
            with self.subTest(entry=name):
                self.assertIn(autopilot, set(local_targets(SUITE / name / "SKILL.md")))

    def test_worker_report_format_is_fixed(self):
        worker = (SUITE / "bstack-worker/SKILL.md").read_text()
        for field in ("STATE:", "CRITERIA:", "GATE / CI:", "HANDBOOKS:", "DECISIONS:", "FINDINGS:", "FOLLOW-UPS:", "NOT DONE:"):
            self.assertIn(field, worker)

    def test_handbook_versions_lock_and_index_are_consistent(self):
        result = subprocess.run([sys.executable, str(HANDBOOK / "scripts/handbook.py"), "check"],
                                capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_a_changed_handbook_fails_the_check_until_it_is_bumped(self):
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / "handbook"
            shutil.copytree(HANDBOOK, copy)
            tool = [sys.executable, str(copy / "scripts/handbook.py")]
            target = copy / "lifecycle/build.md"
            target.write_text(target.read_text() + "\n- Another open question?\n")
            changed = subprocess.run(tool + ["check"], capture_output=True, text=True)
            self.assertEqual(1, changed.returncode)
            self.assertIn("run handbook.py bump build", changed.stderr)
            before = int(re.search(r"(?m)^version: (\d+)$", (HANDBOOK / "lifecycle/build.md").read_text()).group(1))
            bumped = subprocess.run(tool + ["bump", "build", "--source", "t", "--saw", "x", "--expect", "y"],
                                    capture_output=True, text=True)
            self.assertIn(f"build@{before} -> build@{before + 1}", bumped.stdout)
            self.assertEqual(0, subprocess.run(tool + ["check"], capture_output=True).returncode)
            self.assertIn(f"## build@{before + 1}", (copy / "CHANGELOG.md").read_text())
            owner = copy / "policies/authority.md"
            owner.write_text(owner.read_text() + "\n- Loosened.\n")
            refused = subprocess.run(tool + ["bump", "authority", "--source", "t", "--saw", "x", "--expect", "y"],
                                     capture_output=True, text=True)
            self.assertNotEqual(0, refused.returncode)
            self.assertIn("owner-only", refused.stderr)

    def test_handbook_is_flat(self):
        for group in ("lifecycle", "types", "policies"):
            with self.subTest(group=group):
                self.assertFalse([p for p in (HANDBOOK / group).iterdir() if p.is_dir()])
        loose = sorted(p.name for p in HANDBOOK.glob("*.md"))
        self.assertEqual(["CHANGELOG.md", "SKILL.md"], loose)

    def test_every_handbook_has_decisions_or_open_entries_and_fits_its_budget(self):
        for path in handbook_files():
            with self.subTest(handbook=path.relative_to(HANDBOOK).as_posix()):
                text = path.read_text()
                self.assertTrue("## Decisions" in text or "## Open" in text)
                self.assertLessEqual(text.count("\n"), HANDBOOK_LINE_BUDGET)

    def test_role_text_stays_within_its_line_budget(self):
        for name, budget in LINE_BUDGETS.items():
            with self.subTest(file=name):
                self.assertLessEqual((SUITE / name).read_text().count("\n"), budget)

    def test_role_and_handbook_text_does_not_shout(self):
        for path in [SUITE / n for n in LINE_BUDGETS] + handbook_files():
            with self.subTest(file=path.relative_to(SUITE).as_posix()):
                self.assertIsNone(SHOUTING.search(path.read_text()))

    def test_no_reference_to_removed_machinery(self):
        for source in SUITE.rglob("*.md"):
            with self.subTest(path=source.relative_to(SUITE)):
                self.assertIsNone(REMOVED.search(source.read_text()))

    def test_script_launchers_are_executable(self):
        for path in SUITE.rglob("*"):
            if path.is_file() and path.read_bytes().startswith(b"#!"):
                with self.subTest(path=path.relative_to(SUITE)):
                    self.assertTrue(os.access(path, os.X_OK))

    def test_installed_suite_is_self_contained_and_every_file_is_reachable(self):
        with tempfile.TemporaryDirectory() as directory:
            installed = Path(directory).resolve() / "skills"
            shutil.copytree(SUITE, installed)
            visited = set()
            pending = [installed / n / "SKILL.md" for n in SKILLS]
            while pending:
                source = pending.pop().resolve()
                if source in visited:
                    continue
                visited.add(source)
                if source.suffix != ".md":
                    continue
                for target in local_targets(source):
                    self.assertTrue(target.is_relative_to(installed), f"link leaves the suite: {source}: {target}")
                    self.assertTrue(target.exists(), f"missing file: {source}: {target}")
                    pending.append(target)
            unreachable = set(installed.rglob("*.md")) - visited
            self.assertFalse(unreachable, f"markdown no link reaches: {sorted(unreachable)}")
            result = subprocess.run(
                [sys.executable, str(installed / "bstack-handbook/scripts/check_resource_paths.py"),
                 "--profile", "existing", "/v1/orders/{orderId}"],
                cwd=directory, capture_output=True, text=True,
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_keeper_is_local_explicit_only_and_lean(self):
        text = (KEEPER / "SKILL.md").read_text()
        metadata = text.split("---", 2)[1]
        self.assertRegex(metadata, r"(?m)^name: keeper$")
        self.assertRegex(metadata, r"(?m)^disable-model-invocation: true$")
        self.assertRegex((KEEPER / "agents/openai.yaml").read_text(), r"(?m)^policy:\n  allow_implicit_invocation: false$")
        self.assertLessEqual(text.count("\n"), KEEPER_LINE_BUDGET)
        self.assertIsNone(SHOUTING.search(text))
        self.assertFalse((SUITE / "bstack-keeper").exists())

    def test_repository_docs_have_resolvable_local_links(self):
        for source in [ROOT / "README.md", ROOT / "AGENTS.md", KEEPER / "SKILL.md", *sorted((ROOT / "docs").glob("*.md"))]:
            for target in local_targets(source):
                self.assertTrue(target.exists(), f"missing documentation target: {source}: {target}")


if __name__ == "__main__":
    unittest.main()
