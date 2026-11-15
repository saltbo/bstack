# Hosts

Identify where you are running from the tools you actually have. Do not pass a field a tool's schema rejects, and do not claim a capability you do not have.

## Dispatch

Use the dispatch tool of the environment you are in, per the agents handbook. Check in this order.

1. **T3 Code**, when you have its `delegate_task` tool. Dispatch a worker or a verifier with `delegate_task`, using `isolation: "worktree"` so it has its own checkout and branch, with `role: "implementation"` for a builder and `role: "review"` for a verifier. The role only adds one line to the brief and labels the child thread, so the worker skill still carries the workflow. It appears as a child thread Saltbo can watch. Use `mode: "wait"` when your next step needs the result, and otherwise let its completion wake you. Pass a model in `target` only when he named one. `delegate_task` stays inside this thread's project, so for work in another repository start a thread in that repository's project with `t3_thread_launch`, opening its message with `/saltmode`, and follow it with `t3_thread_wait`.
2. **Herdr**, when `$HC_TERMINAL_ID` is set. Read `hc --skill` first. Work in another repository is an agent started there with `hc run --bg --name <name>`. A worker in this repository whose result comes back to you uses the harness's own subagents, as Herdr's manual says.
3. **Anywhere else**, the harness's own subagents, from the table below.

A worker starts with no context and does not load the worker skill by itself, whichever tool starts it. Give it a brief that stands alone and opens with the worker skill's path. If that path does not exist, look for `worker/SKILL.md` next to this skill's own directory. For a shell-spawned worker, name an output file and read the result from it.

## Harness tools

| Need | Claude Code | Codex | Pi |
| --- | --- | --- | --- |
| Subagent | `Agent` with `subagent_type: "general-purpose"` and `run_in_background: false` when you need its result to continue | The spawn tool, else `codex exec` through the shell | `subagent({ agent: "delegate", task })` from pi-subagents |
| Read-only explorer | `Agent` with `subagent_type: "Explore"` | `codex exec --sandbox read-only` | `subagent({ agent: "reviewer", task })` |
| Isolated checkout | `isolation: "worktree"` on the `Agent` call | `git worktree add` at the base revision | `worktree: true` |
| Cheaper worker | The `model` and `effort` fields of `Agent` | Not available; use the session model | `model`, when `subagent({ action: "models" })` lists it |
| Ask him a question | `AskUserQuestion` | One concise question in the reply | `ask_user_question`, else plain text |
| Recurring check | `/loop` or the scheduling tool | A bounded polling loop | `bg_run` with a completion predicate |
| Worker skill to name in every brief | `~/.claude/skills/worker/SKILL.md` | `~/.agents/skills/worker/SKILL.md` | `~/.agents/skills/worker/SKILL.md` |
| Handbook, for the paths you give a worker | `~/.claude/skills/handbook/` | `~/.agents/skills/handbook/` | `~/.agents/skills/handbook/` |
| Project instructions | `CLAUDE.md` | `AGENTS.md` | `AGENTS.md` |

## Limits

Every agent on these hosts shares one machine and one usage quota. A fan-out that would be cheap on separate cloud machines can exhaust the quota here and stop the whole run for hours. These limits follow from that.

- Keep at most three workers in flight. A fourth is fine when it is a read-only explorer. Start the next one as each finishes.
- Use one verifier per change, not a panel. Several reviewers on the same model mostly repeat each other.
- A worker that only runs commands and reports the output, such as a gate run or a CI watch, can run at lower effort or on the host's mid-tier model when the host lets you choose. Builders and verifiers stay on the session model. A worker on a weaker model reports evidence, and you decide what blocks.
- Use the agent types in the table. A user-defined agent type brings its own model and prompt, so use one only when he names it.
- A read-only brief is not a permission boundary. Check `git status` after a read-only agent returns.
- When the host offers one model family, an independent verifier is still the same model with a fresh context. Say so when you report its verdict.
