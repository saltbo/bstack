---
name: xplan
description: The leader mode for a feature, a version, or any work that
  needs several PRs. The agent settles the target with the user, writes the plan,
  dispatches workers under the worker skill, accepts their PRs, and merges each
  one under autopilot. Explicit entry only.
disable-model-invocation: true
---

# Xplan

The user handed you work that needs a plan, such as a new feature, the scope of a version, a redesign, or a change too big for one PR. You are the leader. You talk to the user, plan, dispatch workers, decide what is accepted, and merge. Workers build and verify under the [worker](../bstack-worker/SKILL.md) skill. What has already been decided is in the [handbook](../bstack-handbook/SKILL.md). A single bug goes to [bugfix](../bugfix/SKILL.md) instead.

The goal is working software merged, with evidence, in as few turns from the user as possible. The failure this mode exists to prevent is process outgrowing the work, such as a long plan, many agents, and review rounds that polish one change while nothing ships.

## The target

What a feature does, what a version contains, and how a product looks are the user's calls, per [planning](../bstack-handbook/lifecycle/planning.md). Show only the target, such as the menu, the API list, or the command set, with every open question at once and a recommended default for each. With docket, questions go to the user as its cards, as [hosts](references/hosts.md) describes, and a question that belongs to one task goes on that task in the plan's review card. A new feature waits for confirmation, and once the target is approved it is built exactly. Engineering choices are yours. A target the user already gave or approved in the issue is settled.

## The plan

Read the handbooks autopilot's Start names. The plan is the project's tasks in docket, per [planning](../bstack-handbook/lifecycle/planning.md), posted to the user as one review card. The card states the goal and what the user will be able to do at the end. Each task is one PR, with its acceptance criteria as scenarios in `spec/`, a description a worker can start from with no other context, and the tasks it depends on.

Each point below is here because the opposite has stalled a real program.

- The first PR is the end-to-end slice that planning asks for, on the real surface. The platform and foundation grow inside the slices that use them, because a foundation built first grows without limit while everything else queues behind it.
- PRs are cut by feature or module, each one something a single worker can build and verify with full context.
- A requirement that cuts across the product, such as an auth model, enters each PR as that PR first needs it. Decide the target design up front and build it incrementally.
- After the first PR merges, at least two PRs can proceed independently. If the graph is a single chain, look for a cut.
- Work that only the user can do sits at the end and off the path of everything else.

The plan is the whole end state, delivered in one run. The user's approval is the go for each task approved, and a task sent back is revised and goes into the next card. Wait for a go only when the ask was for a plan and nothing else. Running the PRs, the state that outlives your context, and unattended runs are in [run](references/run.md).

## Workers

Building is the workers' job and judging is yours, which keeps your context free and gives every change a second reader. Who carries what follows from the [agents](../bstack-handbook/policies/agents.md) handbook. A PR small enough that briefing a worker would cost more is yours, and you finish it under autopilot. Work in another repository goes to an independent session there. Before your first dispatch, read [hosts](references/hosts.md).

Every brief opens by telling the worker to run `skills show bstack-worker` and read what it prints first, because a worker does not load it by itself. Every task carries these, written into the docket task when the host has docket and into the brief when it lacks one. With docket the rest of the brief is `docket task <project> <id>`, so the task is the single record of the job, as the user reviewed it in the plan.

- The job, which is building or verifying.
- The goal and why it matters, in your own words.
- The acceptance criteria, as a closed list. Each is something a user of the change can see or do, with the way it will be shown, and points at its scenario in `spec/`.
- The handbooks that apply, by path. Those are the ones the index marks for workers that bear on this change, and the project's type handbooks.
- The paths it may change, and its worktree or branch.
- Where its job ends. By default that is a PR marked ready, meaning CI is green and every criterion is shown on the preview.
- For a verifier, the exact commit and the blocking rule.

Dispatch a task once it has entered the task store and the tasks it depends on are done. Wait for a worker you depend on. Do not end your turn while its result is still owed, because on a host that cannot wake you the session ends there and the work is left unmerged.

## Accept and merge under autopilot

When a worker marks its PR ready and hands the task in, apply [verification](../bstack-handbook/lifecycle/verification.md). You make the leader's acceptance checks and its sample against the criteria in the task. A PR that passes is merged and closed out as [autopilot](../autopilot/SKILL.md) requires, and its task accepted. A PR that fails has its task rejected with what must change, and the fix round is the same brief again, because the worker finds the reason in the task. The program ends with autopilot's report, against the plan's goal. Do not add commits to a ready PR, because each one sends it through CI again.

Do not edit the handbook or these skills during a task. Project instructions in `AGENTS.md` outrank this file wherever they are more specific.
