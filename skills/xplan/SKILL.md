---
name: xplan
description: Leads work that needs several PRs, such as a feature or a version.
  The agent settles the target with the user, plans it as tasks, dispatches
  workers, accepts their PRs, and merges each under autopilot. Explicit entry only.
disable-model-invocation: true
---

# Xplan

The user handed you work that needs several PRs, such as a feature, a version, or a redesign. You plan it, hand the PRs to workers, accept them, and merge. Workers follow the [worker](../bstack-worker/SKILL.md) skill. What the user has already decided is in the [handbook](../bstack-handbook/SKILL.md).

## Target

What a feature does, what a version holds, and how a product looks are the user's calls, per [planning](../bstack-handbook/lifecycle/planning.md). Show only the target, with every open question at once and a recommended default for each, as docket cards when the host has docket, per [hosts](references/hosts.md). A target the user already gave or approved is settled. The approved target is built exactly.

## Plan

The plan is the project's tasks in docket, posted as one review card that states the goal. Each task is one PR, with its acceptance criteria as scenarios in `spec/`, a description a worker can start from cold, and the tasks it depends on. An approved task can start, and a returned one is revised into the next card.

- The first PR is an end-to-end slice on the real surface. A foundation grows inside the slices that use it.
- PRs are cut by feature or module, one worker each.
- After the first PR, at least two PRs can proceed in parallel.
- Work only the user can do sits last, off the path of the rest.

## Workers

A task goes to a worker, per the [agents](../bstack-handbook/policies/agents.md) handbook. One smaller than its brief is yours, finished under [autopilot](../autopilot/SKILL.md). Dispatch per hosts, once the task is in the store and the tasks it depends on are done. The brief opens with `skills show bstack-worker`, then `docket task <project> <id>`, or the task itself when there is no docket.

A task holds the job, which is building or verifying, the goal and why, the acceptance criteria as a closed list, the handbooks that apply by path, the paths and branch it may change, and where its job ends, by default a PR marked ready. A verifier's task also holds the commit and the blocking rule.

Stay in the session while a worker's result is owed, because a host that cannot wake you ends the session there. The order of the run, the state it keeps, and unattended runs are in [run](references/run.md).

## Accept

When a worker hands in a ready PR, make the leader's acceptance from [verification](../bstack-handbook/lifecycle/verification.md) against the task's criteria. A PR that passes is merged and closed out under autopilot, and its task accepted. One that fails has its task rejected with what must change, and the same brief runs the fix round. The program ends with autopilot's report, against the plan's goal.
