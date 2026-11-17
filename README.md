# bstack

Saltbo's working system for coding agents. It has a handbook of his standing
decisions and explicit skills for three roles. The leader and worker skills are installed, and the keeper stays in this repository. It runs on Claude Code, Codex,
and Pi.

| Part | Role |
| --- | --- |
| `bstack-handbook` | Versioned decisions by lifecycle stage and project type, plus an index of specialist skills. Agents look here before asking him |
| `autopilot` | Hand-over. Sent in the middle of a session, it carries the agreed change to merged and proved, then reports |
| `bugfix` | One bug. The agent reproduces it, fixes its cause, then finishes under autopilot |
| `xplan` | Coordinator. It breaks the agreed work into docket tasks, has them approved on a review card, delegates each to a worker, then accepts and merges every PR under autopilot |
| `bstack-worker` | Worker. The xplan leader names it in every brief. It fixes how one change is built or verified and how it is reported |
| `keeper` | Keeper, for this repository only. After the work, it traces wrong behavior to the text that caused it, revises that text, and raises its version |

## Design

Current models plan, decompose, and verify well without being told how. So this
system records only what an agent cannot work out by itself, which is what
Saltbo has already decided, and it keeps that record versioned so a
behavior can be traced to the text that produced it. Each handbook is one flat
file of dated decisions.

- A handbook entry is a decision with its reason, a default an agent may depart
  from with a stated reason, or an open question with the default to use until
  he answers.
- Every PR and every worker report names the handbooks it followed as `id@version`.
- The keeper revises a handbook after the work, and each revision records what
  was seen and what should change. A task runs on one version throughout.
- A project declares its type and its facts. The rules stay here.

## Install

```bash
skills install saltbo/bstack
```

`skills` is the store command from [bbox](https://github.com/saltbo/bbox). It keeps
the handbook, the leader, and the worker under `~/.local/share/bbox/skills/` and out of the directories an
agent scans, so nothing is loaded until it is asked for. Pi needs
`pi install npm:pi-subagents` for subagents.

## Use

Every skill is explicit-only. Tell the agent to load the entry that fits the work.

```
Run `skills show bugfix` and work under it. Fix this regression.
Run `skills show xplan` and work under it. Add export to CSV.
Run `skills show autopilot` and finish this.
```

The keeper reviews how the work went and revises the text. It is a project skill
of this repository, in `.agents/skills/keeper`, so it is entered from a session
here. [AGENTS.md](AGENTS.md) says what the repository is for and how its text is
written.

`skills pin autopilot bugfix xplan` exposes them natively, so they can also be entered as
`/autopilot` in Claude Code and Pi, or `$autopilot` in Codex.

## Layout

| Path | Holds |
| --- | --- |
| [bstack-handbook/SKILL.md](skills/bstack-handbook/SKILL.md) | The lookup order, the index with versions, and the project declaration format |
| [bstack-handbook/lifecycle/](skills/bstack-handbook/lifecycle) | One file per stage: project, planning, design, openapi, backend, frontend, build, testing, verification, versioning, deploy, release, operate |
| [bstack-handbook/types/](skills/bstack-handbook/types) | One file per kind of project: Cloudflare Workers app, client app, Go tool, self-hosted service |
| [bstack-handbook/policies/](skills/bstack-handbook/policies) | Policies that apply to every task: authority, identity, resources, pull requests, follow-ups, reporting, agents, and the index of specialist skills |
| [bstack-handbook/CHANGELOG.md](skills/bstack-handbook/CHANGELOG.md) | Every revision, with what was seen and what it should change |
| [autopilot/](skills/autopilot/SKILL.md) | Hand-over skill, from built to merged |
| [bugfix/](skills/bugfix/SKILL.md) | Bug skill |
| [xplan/](skills/xplan/SKILL.md) | Leader skill |
| [bstack-worker/](skills/bstack-worker/SKILL.md) | Worker skill |
| [.agents/skills/keeper/](.agents/skills/keeper/SKILL.md) | Keeper skill, for this repository only |
| [AGENTS.md](AGENTS.md) | What the repository is for, how its text is written, and how it is maintained |

## Checks

A pre-commit hook runs both checks below before every commit. Enable it once per clone with `pre-commit install`.

```bash
python3 -B -m unittest discover -s tests -v
python3 skills/bstack-handbook/scripts/handbook.py check
python3 skills/bstack-handbook/scripts/check_resource_paths.py --profile bep '/orders/{orderId}'
```

The tests cover structure, links, explicit-only metadata, line budgets, and the
rule that a changed handbook must have its version raised. They
do not prove agent behavior. [Evaluation](docs/evaluation.md) records the
behavior cases and the last run.

## History

Until November 2026 this repository was a 56-skill port of
[pstack](https://github.com/cursor/plugins/tree/fd268b808c786469e6dd8c8d9db864d0de4d669e/pstack).
Its first real program spent five hours on four review rounds for one PR and
merged nothing. The port was then replaced by this system. [upstream.json](upstream.json)
records what was removed. The performance checklist in the handbook's `lifecycle/build.md` and parts of the
engineering references derive from MIT-licensed work, credited in
[the skill license](skills/bstack-handbook/LICENSE.txt) and [licenses](licenses/pstack-MIT.txt).
