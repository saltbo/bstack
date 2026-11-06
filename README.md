# bstack

Saltbo's engineering skill suite with one entry, `saltmode`. An adaptation of [pstack](https://github.com/cursor/plugins/tree/fd268b808c786469e6dd8c8d9db864d0de4d669e/pstack)
for Claude Code, Codex, and Pi, merged with this repository's BEP engineering
preferences. The coordinating entry `poteto-mode` becomes `saltmode`; the other
skills keep their upstream names.

## Install

The suite is plain [Agent Skills](https://agentskills.io). Install every skill
together so the entry can read its dependencies:

```bash
npx skills add saltbo/bstack --skill '*' --agent claude-code --global --yes
npx skills add saltbo/bstack --skill '*' --agent codex --global --yes
npx skills add saltbo/bstack --skill '*' --agent pi --global --yes
```

Claude Code installs to `~/.claude/skills/`; Codex and Pi share `~/.agents/skills/`.

Pi has no built-in subagents. Install the extensions the adapter maps to:

```bash
pi install npm:pi-subagents                       # required: subagent fan-out and review
pi install npm:@juicesharp/rpiv-ask-user-question # recommended: structured questions
pi install npm:pi-background-tasks                # recommended: background waits
```

## Use

`saltmode` is the single entry. Every skill is explicit-only, so nothing loads
from prompt matching; the entry picks a playbook and reads the other skills it needs.

| Host | Invoke |
| --- | --- |
| Claude Code | `/saltmode Fix this regression and verify it.` |
| Codex | `$saltmode Fix this regression and verify it.` |
| Pi | `/skill:saltmode Fix this regression and verify it.` |

## Responsibilities

| Skill | Responsibility |
| --- | --- |
| `saltmode` | Task routing, playbooks, coordination, completion, BEP engineering references |
| `how` / `why` | Current behavior and architecture / historical rationale |
| `architect` | Caller usage, types, interfaces, module shape, design alternatives |
| `arena` | Competing candidates, comparison, selection, synthesis |
| `swarm` | Partitioned parallel work and consolidated coverage |
| `interrogate` | Independent adversarial review and verified findings |
| `tdd` | Failing regression first, then causal implementation |
| `benchmark-checklist` | Validate performance measurements before using them |
| `show-me-your-work` | Reviewable decision and evidence trail |
| `create-verification-skill` / `maintain-verification-skill` | Generate and maintain project-specific app-driving proof |
| `figure-it-out` | Construct a rigorous workflow when no narrow playbook fits |

The [catalog](skills/saltmode/references/skills.md) lists all 56 skills,
including the principle skills. [upstream.json](upstream.json) pins the source
revision and records every rename, removal, and adaptation.

## Host Adaptation

Workflow text keeps pstack's tool names and model slugs. The
[host adapter](skills/saltmode/references/host-adapter.md) maps them to each
host: subagents (`Agent` in Claude Code, the spawn tool or `codex exec` in Codex,
`subagent` from pi-subagents in Pi), read-only modes, model overrides, skill and transcript paths, and
unavailable features. Models inherit the session by default.
`setup-pstack` writes a per-role model rule only when asked.

Explicit-only invocation is set by `disable-model-invocation: true` in each
`SKILL.md` (Claude Code, Pi) and `allow_implicit_invocation: false` in each
`agents/openai.yaml` (Codex).

## BEP Engineering References

BEP preferences live in `skills/saltmode/references/engineering/`, indexed from
[saltmode](skills/saltmode/SKILL.md):
backend, frontend/UI, HTTP, OpenAPI, testing, review and audit, debugging,
delivery, production verification, and verification gates. The skills that use
them link there. Where BEP and pstack said the same thing, the pstack skill is
canonical and BEP keeps only its additional detail. Where they disagreed, the
chosen side is recorded in the text.

## Checks

```bash
python3 -B -m unittest discover -s tests -v
python3 skills/saltmode/scripts/check_resource_paths.py --profile bep '/orders/{orderId}'
```

Checks enforce the skill inventory, explicit-only metadata on every host, the
host adapter link, portable cross-skill links, the absence of Cursor- and
Grok-specific dependencies, and path-helper behavior. They do not prove workflow
behavior. [Host validation](docs/host-validation.md) records the per-host load
and routing check; [behavior evaluation](docs/skill-behavior-evaluation.md) lists
the playbook cases.

## Attribution

The pstack code and skill content are MIT licensed, copyright 2026 Lauren Tan.
See [its retained license](licenses/pstack-MIT.txt). Source is pinned to
`fd268b808c786469e6dd8c8d9db864d0de4d669e`. This repository retains its own
[license](LICENSE) and the existing attribution in adapted BEP references.
