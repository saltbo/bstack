---
id: skills
version: 1
audience: leader, worker
applies: all
---

# Skill index

Specialist skills are not loaded into the session. When a task needs one, find it here and read its `SKILL.md` from the path given.

## Decisions

- **Only saltmode and the three skills it uses load by default.** Everything else is found through this index.

## Index

| When the task involves | Skill | Where |
| --- | --- | --- |
| Agent identity, authenticated `git`, `gh`, `wrangler` | `realmroot` | still installed globally |
| Dotfiles and global agent instructions | `manage-dotfiles` | still installed globally |
| Creating a git worktree by hand | `manage-worktrees` | still installed globally |
| Cloudflare Workers, D1, deploy commands | `cloudflare`, `wrangler`, `workers-best-practices` | still installed globally |
| shadcn/ui components | `shadcn` | still installed globally |
| App Store Connect: builds, TestFlight, submission, metadata | the `asc-*` family | still installed globally |
| Flutter: layout, routing, tests, localization | the `flutter-*` family | still installed globally |
| Browser automation and UI checks | `playwright-cli` | still installed globally |

## Open

- Where does the library of unloaded skills live, and how is it updated? Until decided, the skills stay installed globally and this index is advisory.
