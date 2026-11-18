---
name: revise-from-evidence
description: Traces what an agent did wrong under bstack to the handbook or skill
  text that caused it, revises that text, and proves the revision by rerunning
  the behavior. Use it when working on an issue in saltbo/bstack, analysing a
  session or an end-to-end run, acting on a correction Saltbo gave about how a
  run went, or checking whether an earlier revision held.
---

# Revising from evidence

Saltbo wants agents to stop asking what he already answered and to stop repeating a mistake once it has been seen. A revision of the handbook or a skill is a claim that the next run will behave differently, so it starts from evidence of what the text made an agent do, and it ends with a run that shows the change. [AGENTS.md](../../../AGENTS.md) says how this repository is maintained, and [bstack-writing](../../../skills/bstack-writing/SKILL.md) how its text is revised.

## Evidence

- An issue in `saltbo/bstack` names the host and the session it came from. A report's pending decisions and follow-ups, and what Saltbo said in a session, are evidence too.
- A PR's `Handbook` section and a report's `HANDBOOKS` line say which versions the work ran on.
- An end-to-end run in `e2e/results/` holds the transcript, the stand-in's state and call log, and the case's check. [Evaluation](../../../docs/evaluation.md) says how to run the cases.

[scripts/session.py](scripts/session.py) turns a Claude Code session into numbered evidence. `report <session or .jsonl>` lists the skills it loaded, the skill and handbook files it read, the handbooks it cited, its failed calls and the errors it hit more than once, its questions to Saltbo, its long waits, and its totals. `events <session> --from N --to M` prints a stretch of the timeline in full. It judges nothing: read the events behind a signal to see what the agent decided and which sentence it followed. Measure before you judge, such as how long a PR sat between built and merged, how many fix rounds it took, and how often Saltbo was asked.

## What the evidence decides

- A behavior the text caused gets that text rewritten. A behavior the text already ruled out, or one a harness, tool, or model limit caused, gets no new line here. A defect in a tool is filed with that tool. A fact about Saltbo's machine that broke a usual command, such as `sed` being GNU sed, goes in his user-level instructions, `~/.agents/AGENTS.md`, which chezmoi manages.
- A wrong behavior seen in an end-to-end run counts only when the stand-in behaved like the real service. A call the stand-in got wrong is fixed in `e2e/sim/` first, and the run repeated.
- Something Saltbo said that should hold from now on, across projects, becomes a Decision only after he confirms it as one. Until then it is an Open entry with its interim default. A project fact goes in that project's `Handbook` block.

## Proof

A revision is proved by behavior. Rerun the evals and end-to-end cases that exercise the changed text, and the case that showed the problem when there is one, and compare them with the last recorded run. The PR carries those results.

For each changelog entry whose outcome is `pending`, find later work that ran on that version or a later one. Set the outcome to `held` when the behavior in `Saw` did not come back, and to `recurred` when it did, then revise again from why the last change did not work.

## Report

Say what changed and why, as `id@old` to `id@new` with the evidence and the runs that prove it, which earlier revisions held or recurred, and what waits for Saltbo: changes to owner-only handbooks and Open entries ready to become Decisions.
