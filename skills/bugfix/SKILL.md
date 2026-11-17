---
name: bugfix
description: The entry for fixing a bug. The agent confirms and reproduces
  the bug, writes the bar for its fix, fixes the cause itself, and then takes the
  fix to merged and proved under autopilot. Explicit entry only.
disable-model-invocation: true
---

# Bugfix

The user handed you a bug. A confirmed bug goes straight to work, per [planning](../bstack-handbook/lifecycle/planning.md), so the fix starts at once. You fix it yourself. What has already been decided is in the [handbook](../bstack-handbook/SKILL.md), and [verification](../bstack-handbook/lifecycle/verification.md) sets the path the fix takes.

## What has to hold

- **It is a bug.** Something that once worked, or that a spec scenario, a document, or the product plainly promises, does not work. A request for behavior nothing promised is a feature, and goes to [xplan](../xplan/SKILL.md) instead. Say so in one line and switch.
- **It is reproduced before it is fixed.** A test or a command shows it failing on trunk. If real attempts still leave it unreproduced, report what you tried and what would reproduce it, and stop there.
- **The cause is fixed.** The report names the cause. A retry, a wider timeout, or a caught error is the fix only when the cause lies outside the project, and then the report says where it lies.
- **The bar is written first.** The scenario the bug broke is the first criterion. When no scenario covers it, add one to `spec/` in product language. The rest of the bar is the nearby behavior the fix could break, kept short.
- **It shows red, then green**, per verification. The report carries the new test's failing output before the fix and its passing output after.
- **One bug, one change.** Its path is picked from the verification handbook like any other change. Other bugs found on the way are follow-ups, or a separate change when they block this one.

## Then finish under autopilot

Once the fix runs locally, load [autopilot](../autopilot/SKILL.md) and carry the fix to merged and proved under it, without stopping to wait. Its report also carries the cause and the red and green output.
