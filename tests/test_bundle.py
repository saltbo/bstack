"""Verify independent skills and the portable coordinating suite."""

from pathlib import Path
import re
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / "skills"
BUNDLE = SUITE / "saltmode"
LINK = re.compile(r"\[[^\]\n]+\]\(([^\s)]+)\)")


def local_targets(source):
    text = re.sub(r"```.*?```", "", source.read_text(), flags=re.S)
    for target in LINK.findall(text):
        url = urlsplit(target)
        if not url.scheme and not url.netloc:
            yield (source.parent / unquote(url.path)).resolve() if url.path else source


class BundleTests(unittest.TestCase):
    def test_script_launchers_are_executable(self):
        for path in SUITE.rglob("*"):
            if path.is_file() and path.read_bytes().startswith(b"#!"):
                with self.subTest(path=path.relative_to(SUITE)):
                    self.assertTrue(os.access(path, os.X_OK))

    def test_specialists_are_independently_registered(self):
        entries = sorted(SUITE.rglob("SKILL.md"))
        self.assertEqual(sorted(SUITE.glob("*/SKILL.md")), entries)
        self.assertIn(BUNDLE / "SKILL.md", entries)
        expected = set(json.loads((ROOT / "upstream.json").read_text())["skills"])
        self.assertEqual(expected, {p.parent.name for p in entries})
        self.assertNotIn("poteto-mode", expected)
        self.assertFalse(list(SUITE.glob("bep-*")))
        for entry in entries:
            metadata = entry.read_text().split("---", 2)[1]
            self.assertRegex(metadata, rf"(?m)^name: {re.escape(entry.parent.name)}$")

    def test_every_skill_routes_through_the_host_adapter(self):
        adapter = BUNDLE / "references/host-adapter.md"
        self.assertTrue(adapter.is_file())
        self.assertFalse((BUNDLE / "references/codex.md").exists())
        for entry in SUITE.glob("*/SKILL.md"):
            with self.subTest(skill=entry.parent.name):
                self.assertIn(adapter.resolve(), set(local_targets(entry)))

    def test_every_skill_is_explicit_only(self):
        for entry in SUITE.glob("*/SKILL.md"):
            metadata = entry.read_text().split("---", 2)[1]
            with self.subTest(skill=entry.parent.name):
                self.assertRegex(metadata, r"(?m)^disable-model-invocation: true$")

    def test_no_cursor_or_grok_specific_dependencies(self):
        banned = re.compile(r"\.cursor/|cursor-team-kit|grok-|pstack-models\.mdc|Cursor's built-in")
        for source in SUITE.rglob("*.md"):
            with self.subTest(path=source.relative_to(SUITE)):
                self.assertIsNone(banned.search(source.read_text()))

    def test_codex_requires_explicit_invocation_for_every_skill(self):
        for entry in SUITE.glob("*/SKILL.md"):
            metadata = (entry.parent / "agents/openai.yaml").read_text()
            with self.subTest(skill=entry.parent.name):
                self.assertRegex(metadata, r"(?m)^policy:\n  allow_implicit_invocation: false$")
                self.assertIn("$" + entry.parent.name, metadata)

    def test_installed_copy_is_self_contained_and_every_reference_is_reachable(self):
        with tempfile.TemporaryDirectory() as directory:
            installed = Path(directory).resolve() / "installed/skills"
            shutil.copytree(SUITE, installed)
            visited = set()
            pending = [installed / "saltmode/SKILL.md"]
            while pending:
                source = pending.pop().resolve()
                if source in visited:
                    continue
                visited.add(source)
                for target in local_targets(source):
                    self.assertTrue(target.is_relative_to(installed), f"external local dependency: {source}: {target}")
                    self.assertTrue(target.exists(), f"missing bundled file: {source}: {target}")
                    if target.is_dir():
                        for name in ("SKILL.md", "README.md"):
                            if (target / name).is_file():
                                pending.append(target / name)
                    elif target.suffix == ".md":
                        pending.append(target)
            self.assertTrue(set(installed.glob("*/SKILL.md")).issubset(visited))
            for source in installed.rglob("*.md"):
                for target in local_targets(source):
                    self.assertTrue(target.is_relative_to(installed), f"external local dependency: {source}: {target}")
                    self.assertTrue(target.exists(), f"missing bundled file: {source}: {target}")
            result = subprocess.run(
                [sys.executable, str(installed / "saltmode/scripts/check_resource_paths.py"),
                 "--profile", "existing", "/v1/orders/{orderId}"],
                cwd=directory, capture_output=True, text=True,
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_active_repository_docs_have_resolvable_local_links(self):
        for source in [ROOT / "README.md", *sorted((ROOT / "docs").glob("*.md"))]:
            for target in local_targets(source):
                self.assertTrue(target.is_file(), f"missing documentation target: {source}: {target}")


if __name__ == "__main__":
    unittest.main()
