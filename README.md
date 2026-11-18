# bstack

Saltbo's working system for coding agents. It has a handbook of his standing
decisions, skills that carry work from a request to merged, and a skill for
writing the Markdown that agents and people read. It runs on Claude Code,
Codex, and Pi.

| Part | Role |
| --- | --- |
| `bstack-handbook` | Versioned decisions by lifecycle stage and project type, plus an index of specialist skills. Agents look here before asking him |
| `autopilot` | Hand-over. Sent in the middle of a session, it carries the agreed change to merged and proved, then reports |
| `bugfix` | One or more bugs, such as a list of issues. The agent reproduces each, fixes its cause in a PR of its own, then finishes each under autopilot |
| `xplan` | Coordinator. It settles the requirement, breaks it into docket tasks, has them approved on a review card, delegates each to a worker, then accepts and merges every PR under autopilot |
| `bstack-worker` | Worker. The xplan leader names it in every brief. It fixes how one change is built or verified and how it is reported |
| `bstack-writing` | Writing. How AGENTS.md, README.md, skills, and other Markdown are written, and how they are revised by rewriting the sentence at fault rather than adding one |

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
- A handbook is revised after the work that showed the problem, and each
  revision records what was seen and what should change. A task runs on one
  version throughout.
- A project declares its type and its facts. The rules stay here.

## Install

```bash
skills install saltbo/bstack
```

`skills` is the store command from [bbox](https://github.com/saltbo/bbox). It keeps
the skills under `~/.local/share/bbox/skills/` and out of the directories an
agent scans, so a skill is loaded only once it is asked for or pinned. Pi needs
`pi install npm:pi-subagents` for subagents.

```bash
for name in autopilot bugfix xplan bstack-writing; do skills pin "$name"; done
```

Pinning exposes a skill natively. autopilot, bugfix, and xplan can then be entered as
`/autopilot` in Claude Code and Pi, or `$autopilot` in Codex. `bstack-writing`
is the one skill an agent loads without being asked, because it is needed
whenever Markdown is written, and nobody remembers to ask for it then.

## Use

Every skill except `bstack-writing` is explicit-only. Tell the agent to load the entry that fits the work.

```
Run `skills show bugfix` and work under it. Fix this regression.
Run `skills show xplan` and work under it. Add export to CSV.
Run `skills show autopilot` and finish this.
```

Any agent working in this repository maintains it. [AGENTS.md](AGENTS.md) says
what the repository is for and how its text is written and changed, and the
project skill `revise-from-evidence` says how a wrong behavior is traced to its
text, revised, and proved.

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
| [bstack-writing/](skills/bstack-writing/SKILL.md) | Writing skill, with a page each for AGENTS.md, README.md, and skills |
| [.agents/skills/revise-from-evidence/](.agents/skills/revise-from-evidence/SKILL.md) | Project skill for tracing a behavior to its text, revising it, and proving it |
| [AGENTS.md](AGENTS.md) | What the repository is for, how its text is written, and how it is maintained |
| `evals/`, `e2e/` | Behavior cases for one skill and for the whole system |

## Checks

A pre-commit hook runs both checks below before every commit. Enable it once per clone with `pre-commit install`.

```bash
python3 -B -m unittest discover -s tests -v
python3 skills/bstack-handbook/scripts/handbook.py check
python3 skills/bstack-handbook/scripts/check_resource_paths.py --profile bep '/orders/{orderId}'
```

The tests cover structure, links, invocation metadata, line budgets, and the
rule that a changed handbook must have its version raised. They
do not prove agent behavior. Two kinds of run do, and they cost real sessions.

```bash
claude plugin eval . --scaffold --trust-plugin --allow-tools Edit Write
python3 e2e/run.py
```

The first scores each skill with and without bstack. The second runs whole
sessions on a local stand-in for GitHub and Cloudflare, from the request to a
merged PR running in production, and reports on their transcripts.
[Evaluation](docs/evaluation.md) describes both and records the last runs.
