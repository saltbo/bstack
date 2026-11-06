---
name: setup-pstack
description: Configure which models pstack uses per role and at what reasoning budget.
  Detects your available models and writes a model rule that overrides the
  skill defaults. Use for /setup-pstack, "configure pstack models", "pstack budget",
  or changing pstack's model choices.
disable-model-invocation: true
---


# Setup pstack

Read the [host adapter](../saltmode/references/host-adapter.md) once per session before
following this skill. It maps upstream Cursor-specific tool, model, path, and
permission instructions to your host and sets authority limits.


Write the model rule, which sets pstack's model per role, at the host's path from the [host adapter](../saltmode/references/host-adapter.md): `~/.claude/rules/pstack-models.md` on Claude Code, `~/.agents/pstack-models.md` on Codex and Pi. Run only when the user asks; ordinary saltmode use never requires it.

## Steps

### 1. Detect available models

- Claude Code: the `model` values the `Agent` tool schema lists, each with an effort from its `effort` values. Write a real model as `<model> <effort>`, such as `opus xhigh`.
- Codex: the models the host lists for subagents or `codex exec -m`. If none are listed, every role is `inherit-parent`.
- Pi: `subagent({ action: "models" })`. Write a real model as `<provider>/<id>`.

Never write a model you have not confirmed is available. `inherit-parent` and `auto` are always valid.

### 2. Load current state

The default role-to-model mapping is the rule shape in step 5, with each `claude-opus-5-5-xhigh` mapped to the host's equivalent per the adapter, or `inherit-parent` when the host has none. If the rule file already exists, read it and treat its `# budget` line and role values as the current choices. Drop a line whose role is not in step 5.

### 3. Budget, map, and confirm

**(a) Ask for a budget.** Ask one question. Offer these four options with these exact labels, and name the current budget when the rule records one. With no rule, say that `large` matches the skill defaults.

- `unlimited — max reasoning`
- `large — xhigh reasoning`
- `medium — high reasoning`
- `small — medium reasoning`

**(b) Apply it.** Build the working table from the skill defaults, and on a re-run keep any role you changed by family, list, or alias (`inherit-parent`, `auto`). `unlimited`, `large`, `medium`, and `small` set the effort token of every real slug, panel entries included, to `max`, `xhigh`, `high`, or `medium`. The effort token is the last token, or the one before a trailing `fast`, on the ladder `max` > `xhigh` > `high` > `medium` > `low`. If the result is not a detected slug, use the same family's detected slug with the highest effort at or below the target, else mark the role as needing a choice. `inherit-parent` and `auto` do not change. So `unlimited` turns `claude-opus-5-5-xhigh` into `claude-opus-5-5-max`, `large` keeps the defaults, and `small` turns it into `claude-opus-5-5-medium`.

**(c) Show the roles and confirm.** Show every role with its model, marking any real slug not in the detected set as needing a choice. Also list each line step 2 dropped. Ask whether to accept as-is or change specific roles, offering the detected models plus `inherit-parent` and `auto` (both mean: this role runs on the parent chat model, which is how Auto users stay on Auto) as the options. Ask one question. For panel roles (arena runners, architect runners, interrogate reviewers) the value is a list, and one subagent runs per entry, alias entries included, so the list length sets the count. `arena cross-judge pool` is also a list, but Arena runs one judge. It tries only values from a family other than the parent's, in list order, so order it by preference. An `inherit-parent` or `auto` value never judges. `swarm workers` is the default model for every worker unless a race or comparison assigns another model per arm.

### 4. Validate

Every real model written must be in the detected set. `inherit-parent` and `auto` always pass. If a chosen model is not available, stop and ask again.

### 5. Write the rule

Write the rule file with no frontmatter: the comment lines, a `# budget` line with the chosen label and its target effort, and one line per role, using the labels saltmode uses. Overwrite the whole file so re-runs stay idempotent. Never put role lines in `CLAUDE.md` or `AGENTS.md`. Shape:

```
# pstack model configuration. One line per role. Delete a line to fall back to the skill default.
# `inherit-parent` or `auto` as a value: the role runs on the session model. Alias entries in a panel list still count toward its fan-out.
# budget: large (xhigh)
feature, refactoring: inherit-parent
bug-fix: inherit-parent
perf-issue: inherit-parent
hillclimb: inherit-parent
judgment and prose: claude-opus-5-5-xhigh
hardest tasks: claude-opus-5-5-xhigh
how explorer: inherit-parent
how explainer: claude-opus-5-5-xhigh
why investigators: inherit-parent
why synthesizer: claude-opus-5-5-xhigh
reflect tooling: inherit-parent
reflect judgment, divergent, synthesizer: claude-opus-5-5-xhigh
arena runners: claude-opus-5-5-xhigh, inherit-parent
arena cross-judge pool: claude-opus-5-5-xhigh, inherit-parent
swarm workers: inherit-parent
architect runners: claude-opus-5-5-xhigh, inherit-parent
interrogate reviewers: claude-opus-5-5-xhigh, inherit-parent
```

On Codex and Pi the rule is not auto-loaded: saltmode reads it at the start of a run when it exists.

### 6. Confirm

Tell the user where the rule was written and that it applies to new runs. Re-running this skill updates it.

### 7. Offer a verification skill (optional)

Check whether the project has a way to drive the real app for proof (a `verify-*` skill, or an existing harness). If not, offer once: "want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with /create-verification-skill." On yes, invoke `/create-verification-skill` (read `../create-verification-skill/SKILL.md`). On no, move on without pushing.

### 8. Offer a formal verification skill (optional)

Check whether the project already has a formal verification skill (a project skill that runs a model checker, a proof, or another verifier against the code). If not, offer once: "want a formal verification skill, so agents can prove a key property of your code holds in every case in scope, not only the cases tests reach? I can generate one with /create-formal-verification-skill." On yes, invoke `/create-formal-verification-skill` (read `../create-formal-verification-skill/SKILL.md`). On no, move on without pushing.
