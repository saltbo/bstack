---
name: xplan
description: Plans the work agreed in the conversation as docket tasks, has the
  user approve them on a review card, dispatches each to a worker, then runs the
  rest under autopilot, accepting and merging every PR. Explicit entry only.
disable-model-invocation: true
---

# Xplan

The user has talked the work through with you and wants it planned and built. You plan it in docket, the user approves the plan on a review card, workers build the tasks, and you accept and merge each PR. Workers follow the [worker](../bstack-worker/SKILL.md) skill. What the user has already decided is in the [handbook](../bstack-handbook/SKILL.md).

## Plan

The plan is the project's draft tasks in docket, posted as one review card, per [hosts](references/hosts.md). The card is the one place the user is asked anything, and a question that belongs to a task goes on that task. A returned task is revised into the next card, until every task is approved or dropped.

Each task is one PR and holds everything its worker needs. That is the job, the goal and why, the acceptance criteria as a closed list of scenarios in `spec/`, the handbooks that apply by path, the paths it may change, and the tasks it depends on. A worker's job ends at its PR passing, with every criterion proved, per the worker skill.

- The first task is an end-to-end slice on the real surface. A foundation grows inside the slices that use it.
- Tasks are cut by feature or module.
- After the first task, at least two can proceed in parallel.

## Run under autopilot

From the approval on, the work runs under [autopilot](../autopilot/SKILL.md), and nothing more is asked.

- Each approved task goes to a worker once the tasks it depends on are done, per hosts. The brief opens with `skills show bstack-worker`, then `docket task <project> <id>`.
- Stay in the session while a worker's result is owed, because a host that cannot wake you ends the session there.
- When a worker hands in its PR, make the leader's acceptance from [verification](../bstack-handbook/lifecycle/verification.md) against the task's criteria. A PR that passes is merged under autopilot, and its task accepted. One that fails has its task rejected with what must change, and the same brief runs the fix round.
- The work is done, and reported, as autopilot says, against the plan's goal. The order of the run and its state are in [run](references/run.md).
