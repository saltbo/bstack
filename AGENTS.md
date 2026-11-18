# bstack

Saltbo's working system for coding agents. It is a handbook of his standing decisions and the skills that run under it. [README](README.md) describes it for a reader. This file is for an agent that changes it.

## What this repository is for

It solves one problem. An agent that is unsure what it should do looks here and finds what it should do. How to do it is left to the agent, which already knows.

## How the text is written

Every document here is written and revised per [bstack-writing](skills/bstack-writing/SKILL.md), and everything under `skills/` and `.agents/skills/` also per its page on [skills](skills/bstack-writing/references/skills.md). The line budgets in `tests/test_bundle.py` keep every file small. Raise one only with a reason.

## What is where

| Path | Holds |
| --- | --- |
| `skills/bstack-handbook/` | The handbook. Installed on his machines |
| `skills/autopilot/` | Takes work already under way in a session to merged and proved. Installed |
| `skills/bugfix/` | Fixes one bug, then finishes under autopilot. Installed |
| `skills/xplan/` | The coordinator skill. It breaks work into tasks, delegates them to workers, and merges under autopilot. Installed |
| `skills/bstack-worker/` | The worker skill. Installed |
| `skills/bstack-writing/` | How Markdown is written and revised, skills included. Installed, pinned, and loaded without being asked for |
| [.agents/skills/revise-from-evidence/](.agents/skills/revise-from-evidence/SKILL.md) | How to trace a wrong behavior to the text that caused it, revise it, and prove the revision, with `scripts/session.py`. A skill of this repository only, linked into `.claude/skills/` because Claude Code reads skills only from there |
| `evals/` | Cases for one skill, run by `claude plugin eval`, which loads `skills/` through `.claude-plugin/plugin.json` |
| `e2e/` | Cases for the whole system, each one real session on the local stand-in for GitHub and Cloudflare in `e2e/sim/`, run by `e2e/run.py` |
| [docs/evaluation.md](docs/evaluation.md) | How to run both, and how the skills behaved in recorded runs |
| `tests/` | Checks of structure, links, budgets, and versions. They do not prove behavior |

## How it is maintained

- Any agent working in this repository maintains it. A handbook or a skill changes here from evidence of what its text made an agent do, as [revise-from-evidence](.agents/skills/revise-from-evidence/SKILL.md) describes, and never in the middle of a task that runs on it, because a task runs on one version from start to finish.
- A handbook entry is a Decision, a Default, or an Open question. Nothing becomes a Decision until Saltbo has confirmed it as a standing one. A handbook marked `owner-only` is changed only by him.
- Every change to a handbook raises its version through `skills/bstack-handbook/scripts/handbook.py`, which also keeps the index, the lock, and the changelog. The skills carry no version, and the commit records a change to one.
- The issue tracker takes only problems with the text of a handbook or a skill. A defect in a product or a tool is filed with that product.
- A change is done when the repository tests and the handbook check pass, it is merged to `main`, and the installed copy on his machine matches `main`. The pre-commit hook runs both checks. A change to how agents behave also carries the eval and end-to-end runs that exercise it.

## Handbook

Types: none. This is a repository of text and matches no type handbook
Stage: live
Facts: installed on Saltbo's machine from this checkout by the `skills` command of bbox, whose `skills list` shows which skills are pinned. Pins point at this working tree, so the branch checked out here is the one that runs
Preview: none. Nothing is deployed
Exceptions: none
