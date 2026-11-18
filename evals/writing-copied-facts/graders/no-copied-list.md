---
type: llm
focus: {source: file, path: AGENTS.md}
---

The file started with a Scripts section that copied every script from package.json, one bullet each, and said the gate `pnpm verify` runs typecheck and test. package.json now also has `lint`, and `verify` runs lint, typecheck, and test.

PASS if the file no longer copies the list of scripts and instead points to package.json for them, keeping at most what package.json does not say, such as that `pnpm verify` is the gate. Saying what the gate consists of is fine only if it matches package.json.
FAIL if the file still lists the scripts one by one, with `lint` added to the list, or states a gate that does not match package.json.
