---
name: autopilot
description: Hands the rest of the session's work to the agent. It carries the
  agreed change to merged and proved without stopping, then reports. Explicit
  entry only.
disable-model-invocation: true
---

# Autopilot

The user has handed you the rest of this work. Carry the agreed change to merged and proved, then report. The user reads the result later, with no turns in between.

The change is the one agreed in this conversation, with the scope that was agreed. What the user has already decided is in the [handbook](../bstack-handbook/SKILL.md).

## Done

The work is done when all of these hold.

- Its acceptance criteria are a closed list, written before any check runs. For a change in behavior they are scenarios in `spec/`.
- It took the path that [verification](../bstack-handbook/lifecycle/verification.md) gives it, and every check of that path passed on the commit that merged.
- It is merged per [pull requests](../bstack-handbook/policies/pull-requests.md) and [authority](../bstack-handbook/policies/authority.md), and where the merge deploys, the changed behavior works live.
- What it settled for later work is recorded per [project](../bstack-handbook/lifecycle/project.md), and what it found outside its scope is filed per [follow-ups](../bstack-handbook/policies/follow-ups.md).

## On the way

A question goes to the handbook first, in the order its index gives. The user is asked only what [planning](../bstack-handbook/lifecycle/planning.md) and authority reserve, once and all together, each with a recommended default, while everything that does not depend on the answer moves on. Every other question is yours to decide, and goes in the report as pending.

Process stays smaller than the work. A step of your own method, or a handbook Default, that costs more than the risk it removes is skipped, with one line saying so. The handbook's Decisions are followed as written.

A blocker gets two real attempts at its cause. After that, the report carries it, with what was tried.

## Report

Follow [reporting](../bstack-handbook/policies/reporting.md), in the language the user used. It leads with what now works and the PR, then the handbooks followed as `id@version`, the pending decisions, and each Default departed from, with the reason.

The handbook and these skills stay as they are during the work. A wrong or missing entry is a follow-up for the keeper. Project instructions in `AGENTS.md` outrank this file wherever they are more specific.
