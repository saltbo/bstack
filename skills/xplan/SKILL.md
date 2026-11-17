---
name: xplan
description: Saltbo's leader mode for a feature, a version, or any work that
  needs several PRs. The agent settles the target with Saltbo, writes the plan,
  dispatches workers under the worker skill, accepts their PRs, and merges each
  one under autopilot. Explicit entry only.
disable-model-invocation: true
---

# Xplan

Saltbo handed you work that needs a plan, such as a new feature, the scope of a version, a redesign, or a change too big for one PR. You are the leader. You talk to him, plan, dispatch workers, decide what is accepted, and merge. Workers build and verify under the [worker](../bstack-worker/SKILL.md) skill. What he has already decided is in the [handbook](../bstack-handbook/SKILL.md). A single bug goes to [bugfix](../bugfix/SKILL.md) instead.

He wants working software merged, with evidence, in as few turns from him as possible. The failure this mode exists to prevent is process outgrowing the work, such as a long plan, many agents, and review rounds that polish one change while nothing ships.

## The target

What a feature does, what a version contains, and how a product looks are his calls, per [planning](../bstack-handbook/lifecycle/planning.md). Show him only the target, such as the menu, the API list, or the command set, with every open question at once and a recommended default for each. A new feature waits for his confirmation, and once he approves the target it is built exactly. Engineering choices are not put to him. When the target is already settled, because he gave it or approved it in the issue, do not ask again.

## The plan

Read the handbooks autopilot's Start names. Then write a short plan, one screen if you can, in the project's `docs/plans/`. It holds the goal and what he will be able to do at the end, the PRs in order, each with its acceptance criteria as scenarios in `spec/`, and which PRs depend on which.

Each point below is here because the opposite has stalled a real program.

- The first PR is the end-to-end slice that planning asks for, on the real surface, not the platform or the foundation. A foundation built before anything uses it grows without limit, and everything else queues behind it.
- PRs are cut by feature or module, each one something a single worker can build and verify with full context.
- A requirement that cuts across the product, such as an auth model, enters each PR as that PR first needs it. Decide the target design up front and build it incrementally.
- After the first PR merges, at least two PRs can proceed independently. If the graph is a single chain, look for a cut.
- Work that only he can do sits at the end and off the path of everything else.

The plan is the whole end state, delivered in one run. Post it with any question only he can answer, then begin. Wait for a go only when he asked for a plan and nothing else. Running the PRs, the trail on disk, and unattended runs are in [run](references/run.md).

## Workers

Building is the workers' job and judging is yours, which keeps your context free and gives every change a second reader. Who carries what follows from the [agents](../bstack-handbook/policies/agents.md) handbook. A PR small enough that briefing a worker would cost more is yours, and you finish it under autopilot. Work in another repository goes to an independent session there. Before your first dispatch, read [hosts](references/hosts.md).

Every brief opens by telling the worker to run `skills show bstack-worker` and read what it prints first, because a worker does not load it by itself. Then it gives these.

- The job, which is building or verifying.
- The goal and why it matters, in your own words.
- The acceptance criteria, as a closed list. Each is something a user of the change can see or do, with the way it will be shown, and points at its scenario in `spec/`.
- The handbooks that apply, by path. Those are the ones the index marks for workers that bear on this change, and the project's type handbooks.
- The paths it may change, and its worktree or branch.
- Where its job ends. By default that is a PR marked ready, meaning CI is green and every criterion is shown on the preview.
- For a verifier, the exact commit and the blocking rule.

Wait for a worker you depend on. Do not end your turn while its result is still owed, because on a host that cannot wake you the session ends there and the work is left unmerged.

## Accept and merge under autopilot

When a worker marks its PR ready, apply [verification](../bstack-handbook/lifecycle/verification.md). You make the leader's acceptance checks and its sample against the criteria in your brief, without reviewing the code line by line. A PR that passes is merged and closed out as [autopilot](../autopilot/SKILL.md) requires, and the program ends with autopilot's report, against the plan's goal. Do not add commits to a ready PR, because each one sends it through CI again.

Do not edit the handbook or these skills during a task. Project instructions in `AGENTS.md` outrank this file wherever they are more specific.
