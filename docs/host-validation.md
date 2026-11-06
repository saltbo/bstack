# Host Validation · 2026-11-05

Checks that the suite loads and routes correctly on each supported host. This is
not a behavior evaluation of the playbooks; see
[behavior evaluation](skill-behavior-evaluation.md) for those cases.

## Setup

- Hosts: Claude Code 2.1.319, Codex CLI 0.166.0, Pi 1.4.0.
- Installed with `npx skills add <repo> --skill '*' --agent <host> --copy`, into a
  disposable git project and globally. Installed trees matched the source byte for
  byte, executable bits included.
- A global copy shadows a project copy on Codex and Pi (both read
  `~/.agents/skills/`). Replace an older global install before testing a new one.

## Task

One read-only prompt per host through the explicit entry (`/saltmode`,
`$saltmode`, `/skill:saltmode`): report the entry path followed, the host the
adapter identifies and its read-only subagent mapping, the first heading of the
sibling `how` skill read by relative path, and whether any other suite skill was
loaded automatically.

## Results

| Host | Entry read | Host identified | Read-only subagent | Sibling read | Other skills auto-loaded |
| --- | --- | --- | --- | --- | --- |
| Claude Code | Installed copy | Claude Code | `Agent` with `Explore` | `# How` | None |
| Codex | Installed copy | Codex | Native spawn tool; fallback `codex exec --sandbox read-only` | `# How` | None |
| Pi | Installed copy | Pi | `pi -p --no-session --tools read,grep,find,ls` | `# How` | None; Pi excludes `disable-model-invocation` skills from its prompt (`core/skills.js`) |

## Limits

No full playbook run, real deploy, or cross-model review was exercised on any
host. The repository unit tests cover structure, links, and metadata only.
