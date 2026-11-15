# Hosts

The skill runs on Claude Code, Codex, and Pi. Identify the host from the tools you actually have. Do not pass a field the tool schema rejects, and do not claim a capability the host does not expose.

| Need | Claude Code | Codex | Pi |
| --- | --- | --- | --- |
| Dispatch a worker | `Agent` with `subagent_type: "general-purpose"` and `run_in_background: false` when you need its result to continue | The spawn tool, else `codex exec` through the shell | `subagent({ agent: "delegate", task })` from pi-subagents |
| Read-only explorer | `Agent` with `subagent_type: "Explore"` | `codex exec --sandbox read-only` | `subagent({ agent: "reviewer", task })` |
| Isolated checkout | `isolation: "worktree"` on the `Agent` call | `git worktree add` at the base revision | `worktree: true` |
| Worker model, per the agents handbook | `model: "opus"` on the `Agent` call | Not available; use the session model | `model`, when `subagent({ action: "models" })` lists it |
| Ask him a question | `AskUserQuestion` | One concise question in the reply | `ask_user_question`, else plain text |
| Recurring check | `/loop` or the scheduling tool | A bounded polling loop | `bg_run` with a completion predicate |
| Worker skill to name in every brief | `~/.claude/skills/worker/SKILL.md` | `~/.agents/skills/worker/SKILL.md` | `~/.agents/skills/worker/SKILL.md` |
| Independent session for another repository | A T3 Code thread when running in T3 Code, `hc` when running in Herdr | The same | The same |
| Handbook, for the paths you give a worker | `~/.claude/skills/handbook/` | `~/.agents/skills/handbook/` | `~/.agents/skills/handbook/` |
| Project instructions | `CLAUDE.md` | `AGENTS.md` | `AGENTS.md` |

A worker starts with no context and does not load the worker skill by itself. Give it a brief that stands alone and opens with that path. If the path does not exist, look for `worker/SKILL.md` next to this skill's own directory. For a shell-spawned worker, name an output file and read the result from it.

## Limits

Every agent on these hosts shares one machine and one usage quota. A fan-out that would be cheap on separate cloud machines can exhaust the quota here and stop the whole run for hours. These limits follow from that.

- Keep at most three workers in flight. A fourth is fine when it is a read-only explorer. Start the next one as each finishes.
- Use one verifier per change, not a panel. Several reviewers on the same model mostly repeat each other.
- Workers run on the model the agents handbook names, not on the session's. A worker that only runs commands and reports the output, such as a CI watch, can run on the host's mid-tier model. Whatever its model, a worker reports evidence, and you decide what blocks.
- Use the agent types in the table. A user-defined agent type brings its own model and prompt, so use one only when he names it.
- A read-only brief is not a permission boundary. Check `git status` after a read-only agent returns.
- When the host offers one model family, an independent verifier is still the same model with a fresh context. Say so when you report its verdict.
