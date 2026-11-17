# Running a program

Use this when the work needs several PRs or the user will be away while it runs. The aim is a steady sequence of merged PRs, each proved, with the first one merged early. The plan the run follows is the one in the project's `docs/plans/`, and each merge goes through [autopilot](../../autopilot/SKILL.md).

## Run

You coordinate. Each PR has one worker, dispatched per the Workers section of [xplan](../SKILL.md) and working in its own worktree, so your context stays small. The worker builds, proves the change locally and on the preview, and marks its PR ready. Then you apply the verification handbook to its report and merge.

- Take the first PR all the way to merged before you dispatch others. It tests the plan, your brief, and the project's gates at the cost of one PR.
- Run independent PRs in parallel, within the host's limits. A dependent PR waits for its parent to merge and then branches from trunk. Avoid stacks. When one is unavoidable, keep it two PRs deep.
- A fix round goes to whichever worker is cheaper, the same one or a new one.
- Rebase only when trunk conflicts with the PR or changed something the PR depends on.
- When one PR is stuck, set it aside, note why, and take the next one that does not depend on it.

Stop and rethink the plan when the first PR has not merged after its fix round and re-check, or when you have spent more effort verifying than building. Either the PR is too big, or the bar is wrong, or the approach is. Say what you changed.

## State on disk

Keep a trail file next to the plan, outside your context. Add one line per decision or event, with the time, what happened, why, and a pointer to the evidence such as a commit, a PR, a file, or a log. Record each worker you dispatch and what it owns. A restart, a compaction, or a replacement agent has to be able to resume from the trail, the PRs, and git, without the conversation.

## Unattended runs

- Workers wake you when they finish, so you rarely need a timer. Set a recurring check only for work that cannot notify you, such as a separate thread or CI on a host without events. Run it no more often than every thirty minutes and cancel it when the program ends.
- A check judges progress by side effects, such as pushes, PR state, and trail lines, not by what an agent says about itself. Replace an agent that has produced nothing since the last check and is not waiting on you.
- Message the user only when something changed worth knowing, such as a merge, a decision made on the user's behalf, a blocker, or a change of plan. Otherwise stay quiet.
- A usage-limit error is not a failure of the work. Do not replace the agents it stopped. Note in the trail where each stood, and resume from their side effects after the limit resets.

## Finish

Report against the goal. Say what merged and how each PR was proved, with links. List the decisions you made on the user's behalf and why, what you set aside, and anything that only the user can do.
