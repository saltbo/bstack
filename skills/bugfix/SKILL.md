---
name: bugfix
description: Fixes one bug. The agent reproduces it, fixes its cause, then
  finishes under autopilot. Explicit entry only.
disable-model-invocation: true
---

# Bugfix

The user handed you a bug. Fix it yourself, starting at once, because a confirmed bug needs no go-ahead, per [planning](../bstack-handbook/lifecycle/planning.md). What the user has already decided is in the [handbook](../bstack-handbook/SKILL.md).

## Done

- The bug is reproduced first, by a test or a command that fails on trunk. When it cannot be reproduced, the report says what was tried and the work stops there.
- The acceptance criteria start with the scenario the bug broke, added to `spec/` when none covers it, followed by the nearby behavior the fix could break.
- The cause is fixed, and the report names it.
- The report carries the test's failing output before the fix and its passing output after.
- The change holds this one bug. Other bugs found on the way are follow-ups.

A request for behavior nothing promised is a feature, and goes to [xplan](../xplan/SKILL.md).

## Then

Once the fix runs locally, load [autopilot](../autopilot/SKILL.md) and carry the fix through it.
