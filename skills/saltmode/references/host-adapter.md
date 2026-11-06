# Host Adapter

The suite preserves pstack's skill names and responsibilities, but upstream
wording uses Cursor tool names and model slugs. This adapter maps them to the
supported hosts: Claude Code, Codex, and Pi. User and host instructions take
precedence, followed by this adapter, then the workflow text. Read it once per
session; do not reload it for every leaf skill.

Identify the host from the tools you actually have. Never pass a field or value
the tool schema rejects, and never claim a capability the host does not expose.

## Entry And Skill Invocation

Every suite skill is explicit-only. The user starts work with the single entry:
`/saltmode` in Claude Code, `$saltmode` in Codex, `/skill:saltmode` in Pi.
`/name` in workflow text means that host's mention of skill `name`, not a shell
command.

To run another suite skill, read `../<name>/SKILL.md` relative to saltmode,
follow it, then return to the current playbook. Do not wait for the host to
auto-load it, and do not ask the user to invoke it. A named principle means the
corresponding `principle-*` skill. The [catalog](skills.md) links every skill; do
not load every body. Preserve the goal and selected workflow across follow-ups
within the active task.

## Tools And Subagents

| Workflow text | Claude Code | Codex | Pi |
| --- | --- | --- | --- |
| `Task` spawn | `Agent` tool | The agent-spawn tool; else `codex exec` via shell | `pi -p --no-session "<brief>"` via bash |
| `generalPurpose` | `subagent_type: "general-purpose"` | Default role | Default `pi -p` |
| `poteto-agent`, `comment-sicko` | `general-purpose` given the [delegate brief](agents/poteto-agent.md) or [comment reviewer brief](agents/comment-sicko.md) | Same briefs | Same briefs, passed in the prompt |
| `readonly: true` | `subagent_type: "Explore"` plus a no-edits brief | A no-edits brief; `codex exec --sandbox read-only` | `--tools read,grep,find,ls` plus a no-edits brief |
| `environment: "cloud"`, `cloud_base_branch` | `isolation: "worktree"`; name the base revision | A `git worktree` at the base revision | A `git worktree` at the base revision; run `pi -p` there |
| `run_in_background` | Omit; subagents notify on completion | The tool's async mode, or a background shell job | A background bash job writing to a named output file |
| `resume` | Spawn fresh and paste the earlier result | Resume only if the schema supports it | `pi -p --session <id>` |
| `AskQuestion` | `AskUserQuestion`; plain text in `-p` mode | One concise question | One concise question |
| Todo list | `TodoWrite` | The plan tool | A compact checklist in the reply |
| `Grep`, `Glob`, `Read`, `Bash` | Native tools | Shell with scoped `rg` | `read`, `bash`, scoped `rg` |
| `create-skill` | `skill-creator` if installed | `skill-creator` | `skill-creator` if installed, else the Agent Skills spec |
| `/loop`, wake on event | Background command that notifies on exit, or `/loop` | Bounded polling loop with a completion predicate | Bounded polling loop with a completion predicate |

A shell-spawned subagent (`codex exec`, `pi -p`) has a fresh context: give it a
standalone brief with the mode path, goal, playbook step, scope, and output file,
and read its result from that file. A `readonly` flag or brief is not a
permission boundary: inspect `git status` and artifacts afterward. Follow the
host's concurrency limit and give each writer isolated output. Independent
review gates stay mandatory: when a gate's independent agent cannot run, report
the gate as unmet, never as passed.

## Models And Role Configuration

Model slugs in workflow text are upstream defaults. `inherit-parent` and `auto`
mean the session model. Use a model override only when the host lists it; never
probe guessed slugs.

| Workflow text | Claude Code | Codex | Pi |
| --- | --- | --- | --- |
| `claude-<family>-<version>-<effort>` | `model: "<family>"`, `effort: "<effort>"` | Session model | `--model anthropic/<id>:<effort>` if `pi --list-models` shows it |
| `inherit-parent`, `auto` | Omit `model` | Omit the override | Omit `--model` |
| The model rule | `~/.claude/rules/pstack-models.md` | `~/.agents/pstack-models.md` | `~/.agents/pstack-models.md` |

A cross-family panel needs models from different families. When the host offers
only one family, use independently scoped same-model reviewers and state the
diversity limitation. [setup-pstack](../../setup-pstack/SKILL.md) writes the model
rule only when the user asks.

## Paths And Transcripts

| Workflow text | Claude Code | Codex | Pi |
| --- | --- | --- | --- |
| Project skills `.agents/skills/` | `.claude/skills/` | `.agents/skills/` | `.agents/skills/` or `.pi/skills/` |
| User skills `~/.agents/skills/` | `~/.claude/skills/` | `~/.agents/skills/` | `~/.agents/skills/` or `~/.pi/agent/skills/` |
| Always-applied project rules | `CLAUDE.md` | `AGENTS.md` | `AGENTS.md` |
| This workspace's transcripts | `~/.claude/projects/<path with / and . as ->/*.jsonl` | `~/.codex/sessions/YYYY/MM/DD/*.jsonl` whose session metadata `cwd` is this workspace | `~/.pi/agent/sessions/--<path with / as ->--/*.jsonl` |

Read only this workspace's transcripts for this task; never sweep other
workspaces or another product's storage. Without a transcript, use a clearly
labeled session digest. User-specified destinations take precedence. Generated
project instructions belong to the project's actual instruction mechanism.

## Unavailable Features

When a step needs a service the host does not provide, use an equivalent the
host actually has; a forge command such as `gh pr create` is an equivalent, not a
skip. Otherwise write one line, `Skipped on <host>: <step>. <reason>.`, and
continue independent work. A later step that needs the skipped output gets a
named placeholder. A required missing check remains unverified, never reported as
passed.

## Evidence

Use the actual product surface for proof. Unit tests, screenshots, model
agreement, build success, simulated deployments, and real-provider regression are
distinct evidence. Report uncertainty and coverage gaps explicitly. When a
workflow asks for a decision trail, log observable actions, choices, and evidence
pointers, not hidden reasoning. Never paste secrets or credentials into evidence.
