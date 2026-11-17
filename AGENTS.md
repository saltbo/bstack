# bstack

Saltbo's working system for coding agents. It is a handbook of his standing decisions and the skills that run under it. [README](README.md) describes it for a reader. This file is for an agent that changes it.

## What this repository is for

It solves one problem. An agent that is unsure what it should do looks here and finds what it should do. How to do it is left to the agent, which already knows.

## How the text is written

Everything under `skills/` and `.agents/skills/` gives information and goals.

- Information is what an agent cannot work out by itself. That is what Saltbo has decided and why, facts about his environment, who holds which role, and the process the work moves through, meaning who hands what to whom and when something counts as done. A process is information, and it stays.
- A goal is the result that has to hold, such as "nothing of the PR is left behind after a merge".
- Execution is left to the agent. That is which command to run, with which flags, in which order. A tool is named when the choice of tool is itself a decision, or a fact the agent could not guess, and how to call it is left to the agent.
- A rule carries its reason where the reason is not obvious, so an agent can judge a case the rule did not foresee.
- When an agent got something wrong, ask first whether the text caused it. If the goal was already stated, the text is not at fault and gets no new line.
- Write plain sentences, without emphasis in capitals. The line budgets in `tests/test_bundle.py` keep every file small. Raise one only with a reason.

## What is where

| Path | Holds |
| --- | --- |
| `skills/bstack-handbook/` | The handbook. Installed on his machines |
| `skills/autopilot/` | Takes work already under way in a session to merged and proved. Installed |
| `skills/bugfix/` | Fixes one bug, then finishes under autopilot. Installed |
| `skills/xplan/` | The coordinator skill. It breaks work into tasks, delegates them to workers, and merges under autopilot. Installed |
| `skills/bstack-worker/` | The worker skill. Installed |
| [.agents/skills/keeper/](.agents/skills/keeper/SKILL.md) | The keeper skill. It serves this repository only and is installed nowhere else |
| [docs/evaluation.md](docs/evaluation.md) | How the skills behaved in real sessions |
| `tests/` | Checks of structure, links, budgets, and versions. They do not prove behavior |

## How it is maintained

- Handbooks and skills are changed here, after the work, by the keeper, from evidence of what the text made an agent do.
- A handbook entry is a Decision, a Default, or an Open question. Nothing becomes a Decision until Saltbo has confirmed it as a standing one. A handbook marked `owner-only` is changed only by him.
- Every change to a handbook raises its version through `skills/bstack-handbook/scripts/handbook.py`, which also keeps the index, the lock, and the changelog. The skills carry no version, and the commit records a change to one.
- The issue tracker takes only problems with the text of a handbook or a skill. A defect in a product or a tool is filed with that product.
- A change is done when the repository tests and the handbook check pass, it is merged to `main`, and the installed copy on his machine matches `main`. The pre-commit hook runs both checks.

## Handbook

Types: none. This is a repository of text and matches no type handbook
Stage: live
Facts: installed on Saltbo's machine from this checkout by the `skills` command of bbox. autopilot, bugfix, and xplan are pinned, and the pins point at this working tree, so the branch checked out here is the leader that runs
Preview: none. Nothing is deployed
Exceptions: none
