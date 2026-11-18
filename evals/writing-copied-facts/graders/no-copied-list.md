---
type: llm
focus: {source: file, path: AGENTS.md}
---

The file started with a Scripts section that copied every script from package.json, one bullet each, and said the gate `pnpm verify` runs typecheck and test. package.json now also has `lint`, and `verify` runs lint, typecheck, and test.

PASS if the file keeps only what package.json does not say, such as that `pnpm verify` is the gate, with no copy of the scripts or of what `verify` runs, and no line telling the reader to look in package.json, which any reader of the repository does anyway.
FAIL if the file still lists scripts, restates which scripts `verify` runs, or says that the scripts are in package.json.
