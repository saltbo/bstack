---
id: skills
version: 7
audience: leader, worker
applies: all
---

# Skill index

Specialist skills are not loaded into the session. They live in a store that the `skills` command reads. When a task needs one, search the store and load the skill from it. Loading prints the skill's instructions and its base directory.

## Decisions

- **Skills are stored by source and loaded on demand.** The agent's own skill directories hold only the `skill-finder` router and the few pinned skills. Everything else, the leader skills and the handbook and worker they use included, is loaded from the store. (2026-11-15)
- **A tool that prints its own guide is read from the tool**, not from a skill. `ego-browser skill` and `hc --skill` are the two so far. Read the guide before the first use in a session. (2026-11-15)

## Index

The store is searchable, so this table lists only what a search by topic might miss.

| When the task involves | Read |
| --- | --- |
| Writing or revising Markdown: `AGENTS.md`, `README.md`, a skill, a prompt | [bstack-writing](../../bstack-writing/SKILL.md), pinned |
| Agent identity, authenticated `git`, `gh`, `wrangler` | `realmroot`, pinned |
| Dotfiles and global agent instructions | `manage-dotfiles`, native |
| Creating a git worktree by hand | `manage-worktrees`, native |
| Cloudflare Workers, D1, deploy commands | `cloudflare`, `wrangler`, `workers-best-practices` |
| shadcn/ui components | `shadcn` |
| App Store Connect: builds, TestFlight, submission, metadata | the `asc-*` family |
| Flutter and Dart: layout, routing, tests, localization | the `flutter-*` and `dart-*` families |
| Driving a browser, per [verification](../lifecycle/verification.md) | `ego-browser skill` |
| Running agents under Herdr | `hc --skill` |
