# Programs

Use this when the work needs several PRs or he will be away while it runs. The aim is a steady sequence of merged PRs, each proved, with the first one merged early.

## Plan

Write a short plan, one screen if you can, in the project's `docs/plans/`. It holds three things.

- The goal, and what he will be able to do at the end.
- The PRs in order. Each gets its acceptance criteria, as scenarios in `spec/`, meaning what a user can see or do after it merges and how that will be shown.
- Which PRs depend on which.

Shape the plan as follows. Each point is here because the opposite has stalled a real program.

- The first PR is the end-to-end slice that [planning](../../bstack-handbook/lifecycle/planning.md) asks for, on the real surface. It is not the platform or the foundation. A foundation built before anything uses it grows without limit, and everything else queues behind it.
- A requirement that cuts across the product, such as an auth model or a compliance checklist, enters each PR as that PR first needs it. Decide the target design up front and build it incrementally.
- After the first PR merges, at least two PRs can proceed independently. If the graph is a single chain, look for a cut.
- Work that only he can do, such as approving a registration in his own account, sits at the end and off the path of everything else.

Post the plan together with any question only he can answer, then begin. He can redirect while you work. Wait for a go only when he asked for a plan and nothing else.

## Run

You coordinate. Each PR has one worker, dispatched per the Workers section of the skill and working in its own worktree, so your context stays small. The worker builds, proves the change locally and on the preview, and marks its PR ready. Then you apply the verification handbook to its report and merge.

- Take the first PR all the way to merged before you dispatch others. It tests the plan, your brief, and the project's gates at the cost of one PR.
- Run independent PRs in parallel, within the host's limits. A dependent PR waits for its parent to merge and then branches from trunk. Avoid stacks. When one is unavoidable, keep it two PRs deep.
- A fix round goes to whichever worker is cheaper, the same one or a new one.
- Rebase only when trunk conflicts with the PR or changed something the PR depends on.
- When one PR is stuck, set it aside, note why, and take the next one that does not depend on it.

Stop and rethink the plan when the first PR has not merged after its fix round and re-check, or when you have spent more effort verifying than building. Either the PR is too big, or the bar is wrong, or the approach is. Tell him what you changed.

## State on disk

Keep a trail file next to the plan, outside your context. Add one line per decision or event, with the time, what happened, why, and a pointer to the evidence such as a commit, a PR, a file, or a log. Record each worker you dispatch and what it owns. A restart, a compaction, or a replacement agent has to be able to resume from the trail, the PRs, and git, without the conversation.

## Unattended runs

- Workers wake you when they finish, so you rarely need a timer. Set a recurring check only for work that cannot notify you, such as a separate thread or CI on a host without events. Run it no more often than every thirty minutes and cancel it when the program ends.
- A check judges progress by side effects, such as pushes, PR state, and trail lines, not by what an agent says about itself. Replace an agent that has produced nothing since the last check and is not waiting on you.
- Message him only when something changed that he would want to know, such as a merge, a decision made on his behalf, a blocker, or a change of plan. Otherwise stay quiet.
- A usage-limit error is not a failure of the work. Do not replace the agents it stopped. Note in the trail where each stood, and resume from their side effects after the limit resets.

## Finish

Report against the goal. Say what merged and how each PR was proved, with links. List the decisions you made for him and why, what you set aside, and anything that only he can do.
