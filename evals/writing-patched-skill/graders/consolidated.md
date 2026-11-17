---
type: llm
focus: {source: file, path: skills/changelog/SKILL.md}
---

The file started at 21 lines, with a Notes section of four patches that narrowed the steps above it.

PASS if the rule for which PRs get an entry is stated once, where the steps decide it, with its reason (the changelog is for users of the release), covering README-only PRs, CI and tests, dependency bumps, and the security exception, and the file is no longer than 21 lines.
FAIL if the README case is added as one more exclusion beside the old patches, or a Notes or exceptions section remains, or the file grew.
