---
name: bugfix
description: Fixes the bugs the user hands over, one or several, such as a list
  of issues. The agent reproduces each, fixes its cause, and finishes each fix
  under autopilot. Explicit entry only.
disable-model-invocation: true
---

# Bugfix

The user handed you one or more bugs, described in the conversation or as issues. Fix them yourself, starting at once, because a confirmed bug needs no go-ahead, per [planning](../bstack-handbook/lifecycle/planning.md). What the user has already decided is in the [handbook](../bstack-handbook/SKILL.md).

Each bug is its own fix, with its own reproduction and its own PR, linked to its issue when it has one. Two bugs with one cause are one fix, and its PR closes both issues. Whether you build a fix or a worker does is set by [agents](../bstack-handbook/policies/agents.md). A worker's brief opens with `skills show bstack-worker` and carries the bug, its issue, and its acceptance criteria. A bug in another repository goes to a session there.

## Done

- Each bug is reproduced first, by a test or a command that fails on trunk. When one cannot be reproduced, the report says what was tried, and the work on that bug stops there while the others go on.
- The acceptance criteria of a fix start with the scenario the bug broke, added to `spec/` when none covers it, followed by the nearby behavior the fix could break.
- Each cause is fixed, and the report names it.
- The report carries each test's failing output before its fix and its passing output after.
- Each change holds its own bug. Other bugs found on the way are follow-ups.

## Then

Once a fix runs locally, load [autopilot](../autopilot/SKILL.md) and carry the fix through it. The work is done when every bug is merged or reported as not reproduced, and one report covers them all.
