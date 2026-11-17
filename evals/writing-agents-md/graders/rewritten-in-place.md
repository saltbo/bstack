---
type: llm
focus: {source: file, path: AGENTS.md}
---

The file started with the convention "Use the logging module for output." under Conventions, and 18 lines in all.

PASS if that line is gone and, in its place, the Conventions list states in one item where a CLI command's results go (stdout) and where diagnostics go (logging), and the file is at most 19 lines.
FAIL if the old line is kept, or the correction is added as a separate rule, note, or section, or the file grew by more than one line.
