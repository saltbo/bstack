---
name: autopilot
description: The hand-over for work already under way in a session. From here
  the agent takes the change to merged and proved on its own, which means
  finishing it, committing, opening the PR, proving it, accepting it against the
  handbook, merging, and reporting. Sent mid-conversation, and the last step of
  bugfix and xplan. Explicit entry only.
disable-model-invocation: true
---

# Autopilot

The user has been working with you in this session and now hands the rest over. Without this skill you would stop once the work runs locally and wait. With it you carry the change to merged and proved without another turn from the user, who reads the result later. What has already been decided is in the [handbook](../bstack-handbook/SKILL.md).

You build and you judge your own work. You do not dispatch workers. Splitting work across agents belongs to [xplan](../xplan/SKILL.md).

## What it covers

The change this conversation agreed on, or the one [bugfix](../bugfix/SKILL.md) or xplan handed you. Nothing is added to it. Something you notice outside it is a follow-up, per [follow-ups](../bstack-handbook/policies/follow-ups.md). When a question that [planning](../bstack-handbook/lifecycle/planning.md) reserves for the user is still open, ask it once with your recommended default, and finish everything that does not depend on the answer.

The failure this skill exists to prevent is process outgrowing the work. When a step of your own method, or a handbook Default, would cost more than the risk it removes, skip it and say so in one line. That freedom does not reach the handbook's Decisions, which are followed as written.

## Start

1. Read the handbook index, [authority](../bstack-handbook/policies/authority.md), [verification](../bstack-handbook/lifecycle/verification.md), and [pull requests](../bstack-handbook/policies/pull-requests.md), and the project's `Handbook` block. For a change in behavior, also the handbooks for the project's types and for the stage the work is in.
2. Pick the change's path from the verification handbook. Everything after this is sized to that path.
3. Fix the bar. If the conversation did not leave a closed list of acceptance criteria, write it now from what was agreed, as scenarios in `spec/` for a change in behavior. The bar is written before the checks, and every check uses it and nothing else.

## What has to hold before it counts as done

- The project's gate passes without being loosened. A bug fix shows red, then green.
- A direct change is on trunk, with CI and the deploy watched and the result looked at once. Any other change is on its own branch and PR, per the pull requests handbook, opened as a draft and marked ready only when CI is green and every criterion is proved.
- Every criterion has been seen working locally and on the preview, as a user would see it, with the evidence in the PR. Because you built the change, this walk stands in for the leader's sample, and you also make the leader's acceptance checks from the verification handbook.
- A high-risk change has had its second check, from one verifier with a fresh context, started with the environment's own tool per the [hosts](../xplan/references/hosts.md) reference.
- The PR is merged, per authority, and the forge says so. Nothing of it is left behind. Where the merge deploys, the changed behavior has been checked live once.
- An architecture decision the work settled, or a project fact later work needs, is recorded after the merge as a direct change, per the [project](../bstack-handbook/lifecycle/project.md) handbook. What did not block is filed as a follow-up.

A blocker is investigated and fixed, not worked around. After two real attempts at the same obstacle, stop and report it with what you tried.

## Before you ask

Look the question up in the handbook, in the order its index gives. Follow a decision that answers it. Use the interim default of an open entry. Decide a reversible question that nothing covers. Ask the user only what planning and authority reserve for the user, all at once, while the rest of the work keeps moving. Keep a list of the questions you answered yourself. They go in your report as pending decisions.

## Report

Follow [reporting](../bstack-handbook/policies/reporting.md). Write in the language the user used. Lead with what now works and the PR, then name the handbooks you followed as `id@version`, list your pending decisions, and name each Default you departed from, with the reason.

Do not edit the handbook or these skills during a task. A wrong or missing entry is a follow-up for the keeper.

Project instructions in `AGENTS.md` outrank this file wherever they are more specific.
