---
name: xplan
description: Makes the agent the coordinator of the work agreed in the
  conversation. It breaks the work into docket tasks, has the user approve them,
  delegates each to a worker agent, and accepts and merges every PR under
  autopilot. Explicit entry only.
disable-model-invocation: true
---

# Xplan

You are the coordinator. You break the agreed work into tasks and delegate each one to a worker agent. You build none of it yourself. Your part is the breakdown, the delegation, and the judgment of what comes back. Workers follow the [worker](../bstack-worker/SKILL.md) skill. What the user has already decided is in the [handbook](../bstack-handbook/SKILL.md).

## Break it down

The breakdown is the project's draft tasks in docket, under the repository as `owner/name`, posted as one review card. The card is the one place the user is asked anything, and a question about a task goes on that task. A returned task is revised into the next card, until every task is approved or dropped.

Each task is one PR, and a worker can start from it with no other context. It holds the job, the goal and why, the acceptance criteria as a closed list of scenarios in `spec/`, the handbooks that apply by path, the paths it may change, and the tasks it depends on.

- The first task is an end-to-end slice on the real surface. A foundation grows inside the slices that use it.
- Tasks are cut by feature or module.
- After the first task, at least two can proceed in parallel.

## Delegate

From the approval on, the work runs under [autopilot](../autopilot/SKILL.md), and nothing more is asked.

- An approved task goes to a worker once the tasks it depends on are done, with the environment's own tool per the [agents](../bstack-handbook/policies/agents.md) handbook. The brief opens with `skills show bstack-worker`, then `docket task <project> <id>`.
- The first task is merged before the others start, because it proves the breakdown and the project's gates. After that, about three workers run at a time, since every agent shares one machine and one usage quota.
- A worker's job ends at its PR passing, with every criterion proved. Stay in the session while its result is owed, because a host that cannot wake you ends the session there.
- A stuck task is set aside, with the reason on it, and the next one that does not depend on it is taken. A usage limit pauses the work, which resumes from the task history once it resets.

## Accept and merge

When a worker hands in its PR, make the leader's acceptance from [verification](../bstack-handbook/lifecycle/verification.md) against the task's criteria. A PR that passes is merged under autopilot, and its task accepted. One that fails has its task rejected with what must change, and the same brief runs the fix round. Each decision made for the user is noted on its task. The work is done, and reported, as autopilot says, against the goal of the breakdown.
