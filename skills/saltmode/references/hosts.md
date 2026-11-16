# Hosts

Identify where you are running from the tools you actually have, and call them as their own schemas describe. Do not claim a capability you do not have.

## Dispatch

Use the dispatch tool of the environment you are in, per the agents handbook. Check in this order.

1. **T3 Code**, when you have its `delegate_task` tool. Dispatch a worker or a verifier with `delegate_task`, using `isolation: "worktree"` so it has its own checkout and branch, with `role: "implementation"` for a builder and `role: "review"` for a verifier. The role only adds one line to the brief and labels the child thread, so the worker skill still carries the workflow. It appears as a child thread Saltbo can watch. Use `mode: "wait"` when your next step needs the result, and otherwise let its completion wake you. Pass a model in `target` only when he named one. `delegate_task` stays inside this thread's project, so for work in another repository start a thread in that repository's project with `t3_thread_launch`, opening its message by telling it to run `skills show saltmode` and work under it, and follow it with `t3_thread_wait`.
2. **Herdr**, when `$HC_TERMINAL_ID` is set. Read `hc --skill` first. Work in another repository is an agent started there with `hc run --bg --name <name>`. A worker in this repository whose result comes back to you uses the harness's own subagents, as Herdr's manual says.
3. **Anywhere else**, the harness's own subagent tool, with an isolated checkout for each worker. On Pi that tool comes from pi-subagents. On Codex without a spawn tool, use `codex exec` through the shell.

A worker starts with no context and does not load the worker skill by itself, whichever tool starts it. Give it a brief that stands alone and opens with `skills show bstack-worker`. That prints the skill and its base directory, and the handbook is `bstack-handbook/` beside it, which is where the handbook paths in your brief point. For a shell-spawned worker, name an output file and read the result from it.

## Limits

Every agent on these hosts shares one machine and one usage quota. A fan-out that would be cheap on separate cloud machines can exhaust the quota here and stop the whole run for hours. Size what you start to that. These are the usual limits.

- About three workers in flight, with the next one started as each finishes.
- One verifier per change, not a panel. Several reviewers on the same model mostly repeat each other.
- A worker that only runs commands and reports the output, such as a gate run or a CI watch, can run at lower effort or on a cheaper model when the host lets you choose. Builders and verifiers stay on the session model.
- A user-defined agent type brings its own model and prompt, so use one only when he names it.
- A read-only brief is not a permission boundary. Check `git status` after a read-only agent returns.
- When the host offers one model family, an independent verifier is still the same model with a fresh context. Say so when you report its verdict.
