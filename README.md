# bstack

Saltbo's working system for coding agents. It has a handbook of his standing
decisions and three explicit skills, one per role. It runs on Claude Code, Codex,
and Pi.

| Part | Role |
| --- | --- |
| `bstack-handbook` | Versioned decisions by lifecycle stage and project type, plus an index of specialist skills. Agents look here before asking him |
| `saltmode` | Leader. Saltbo invokes it. It talks to him, dispatches workers, accepts their work, and merges |
| `bstack-worker` | Worker. The leader names it in every brief. It fixes how one change is built or verified and how it is reported |
| `bstack-keeper` | Keeper. After the work, it traces wrong behavior to the text that caused it, revises that text, and raises its version |

## Design

Current models plan, decompose, and verify well without being told how. So this
system does not teach method. It records what an agent cannot work out by itself,
which is what Saltbo has already decided, and it keeps that record versioned so a
behavior can be traced to the text that produced it. Each handbook is one flat
file of dated decisions.

- A handbook entry is a decision with its reason, a default an agent may depart
  from with a stated reason, or an open question with the default to use until
  he answers.
- Every PR and every worker report names the handbooks it followed as `id@version`.
- A leader or worker never edits a handbook during a task. The keeper revises it
  afterwards, and each revision records what was seen and what should change.
- A project declares its type and its facts. The rules stay here.

## Install

```bash
skills install saltbo/bstack
```

`skills` is the store command from [bbox](https://github.com/saltbo/bbox). It keeps
the four skills under `~/.local/share/bbox/skills/` and out of the directories an
agent scans, so nothing is loaded until it is asked for. Pi needs
`pi install npm:pi-subagents` for subagents.

## Use

All four are explicit-only. Tell the agent to load the leader for work and the
keeper for a review of how the work went.

```
Run `skills show saltmode` and work under it. Fix this regression.
Run `skills show bstack-keeper` and work under it. Review yesterday's session.
```

## Layout

| Path | Holds |
| --- | --- |
| [bstack-handbook/SKILL.md](skills/bstack-handbook/SKILL.md) | The lookup order, the index with versions, and the project declaration format |
| [bstack-handbook/lifecycle/](skills/bstack-handbook/lifecycle) | One file per stage: project, planning, design, api, backend, frontend, build, testing, verification, versioning, deploy, release, operate |
| [bstack-handbook/types/](skills/bstack-handbook/types) | One file per kind of project: Cloudflare Workers app, client app, Go tool, self-hosted service |
| [bstack-handbook/policies/](skills/bstack-handbook/policies) | Policies that apply to every task: authority, identity, resources, pull requests, follow-ups, reporting, agents, and the index of specialist skills |
| [bstack-handbook/CHANGELOG.md](skills/bstack-handbook/CHANGELOG.md) | Every revision, with what was seen and what it should change |
| [saltmode/](skills/saltmode/SKILL.md) | Leader skill, with [program](skills/saltmode/references/program.md) and [hosts](skills/saltmode/references/hosts.md) |
| [bstack-worker/](skills/bstack-worker/SKILL.md) | Worker skill |
| [bstack-keeper/](skills/bstack-keeper/SKILL.md) | Keeper skill |

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
