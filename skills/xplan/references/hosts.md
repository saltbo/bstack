# Hosts

Identify where you are running from the tools you actually have, and call them as their own schemas describe. Do not claim a capability you do not have.

## Dispatch

Use the dispatch tool of the environment you are in, per the agents handbook. Check in this order.

1. **T3 Code**, when you have its `delegate_task` tool. A worker or a verifier is a delegated task in its own worktree, with the implementation role for a builder and the review role for a verifier. The role only labels the child thread and adds one line to the brief, so the worker skill still carries the workflow. The user can watch the child thread. Name a model only when the user named one. `delegate_task` stays inside this thread's project, so work in another repository is a new thread in that repository's project, started with `t3_thread_launch` and told to run autopilot.
2. **Herdr**, when `$HC_TERMINAL_ID` is set. Its guide is `hc --skill`. Work in another repository is an agent started there with `hc run`. A worker in this repository whose result comes back to you uses the harness's own subagents, as Herdr's guide says.
3. **Anywhere else**, the harness's own subagent tool, with an isolated checkout for each worker. On Pi that tool comes from pi-subagents. On Codex without a spawn tool it is `codex exec`.

A worker starts with no context and does not load the worker skill by itself, whichever tool starts it. Its brief opens with `skills show bstack-worker`. That prints the skill and its base directory, and the handbook is `bstack-handbook/` beside it, which is where the handbook paths in a task point. With docket, the rest of the brief is only `docket task <project> <id>`, because the task carries everything else. Without it, the brief stands alone and carries the task itself.

## Task store

When you have the docket tools, docket holds the plan's tasks and their history, and it is how you ask the user things. The user answers its cards on any device, a phone included, and a card spares them reading a wall of text. Without docket, ask in text, and each brief carries its task.

- A choice between options is a choice card, with your recommended option marked.
- A plan is a review card with the project as its commit target. What the user approves enters the task store and can be claimed, what the user marks to change stays in planning with the reason, and what the user drops is cancelled. The answer to a question on a task stays on that task, where its worker reads it.
- Planning is outside the dependency graph. A task enters only after the tasks it depends on have entered, and one approved while a dependency is still being changed enters by itself when that dependency does.
- The project key is the repository as `owner/name`, the same for you and every worker.

## Limits

Every agent on these hosts shares one machine and one usage quota. A fan-out that would be cheap on separate cloud machines can exhaust the quota here and stop the whole run for hours. Size what you start to that. These are the usual limits.

- About three workers in flight, with the next one started as each finishes.
- One verifier per change, not a panel. Several reviewers on the same model mostly repeat each other.
- A worker that only runs commands and reports the output, such as a gate run or a CI watch, can run at lower effort or on a cheaper model when the host lets you choose. Builders and verifiers stay on the session model.
- A user-defined agent type brings its own model and prompt, so use one only when the user names it.
- A read-only brief is not a permission boundary. Confirm that such an agent changed nothing.
- When the host offers one model family, an independent verifier is still the same model with a fresh context. Say so when you report its verdict.
