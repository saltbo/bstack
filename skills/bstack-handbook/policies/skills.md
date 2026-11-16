---
id: skills
version: 4
audience: leader, worker
applies: all
---

# Skill index

Specialist skills are not loaded into the session. They live in a store that the `skills` command reads. When a task needs one, find it with `skills list --search <keywords>` and load it with `skills show <name>`, which prints its instructions and its base directory.

## Decisions

- **Skills are stored by source and loaded on demand.** The agent's own skill directories hold only the `skill-finder` router and the few pinned skills. Everything else, saltmode and the three skills it uses included, is read with `skills show`. (2026-11-15)
- **A tool that prints its own guide is read from the tool**, not from a skill. `ego-browser skill` and `hc --skill` are the two so far. Read the guide before the first use in a session. (2026-11-15)

## Index

The store is searchable, so this table lists only what a search by topic might miss.

| When the task involves | Read |
| --- | --- |
| Agent identity, authenticated `git`, `gh`, `wrangler` | `realmroot`, pinned |
| Dotfiles and global agent instructions | `manage-dotfiles`, native |
| Creating a git worktree by hand | `manage-worktrees`, native |
| Cloudflare Workers, D1, deploy commands | `skills show` on `cloudflare`, `wrangler`, `workers-best-practices` |
| shadcn/ui components | `skills show shadcn` |
| App Store Connect: builds, TestFlight, submission, metadata | `skills list --search asc` |
| Flutter and Dart: layout, routing, tests, localization | `skills list --search flutter` |
| Driving a browser, per [verification](../lifecycle/verification.md) | `ego-browser skill` |
| Running agents under Herdr | `hc --skill` |
