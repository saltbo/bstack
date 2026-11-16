---
id: operate
version: 1
audience: leader
applies: all
---

# Operate

## Decisions

- **A failed deploy is repaired without asking**, by the rule for the project's stage below, and reported.
- **In a live project, roll back first, and keep the evidence.** Before rolling back, save whatever the investigation needs and a rollback would destroy, such as logs or a snapshot of the affected data. If it will still be there afterwards, roll back at once. Then find the root cause. (2026-11-15)
- **In a development project, there is no need to roll back first.** Go straight to the root cause. (2026-11-15)
- **Find the cause, not a way around it.** Rolling back a suspect dependency upgrade to test it is fine. Rewriting around the problem is not. (2026-06-02)
- **Live data is migrated, not accommodated.** No compatibility or mapping logic in code. A one-off data fix is a throwaway script run against the database, kept out of the product code. (repeated, 2026-08-21, 2026-09-03)
- **Migrations stay simple and run directly**, without downtime windows. Migrations that never shipped are squashed into one. A project not yet launched needs none. (2026-08-06, 2026-06-07)
- **A backfill is resumable and idempotent.** (2026-09)
- **Stop redeploying when the same failure comes back with no new evidence.** (2026-09)
- **A data fix covers every tenant**, not only his account, and new records are fixed and verified before existing ones. (2026-09-03, 2026-09-05)
- **Dependency upgrades merge when the gate is green.** A new major is adopted fully, without keeping the old one. A gap upstream is handled by checking the latest release, then a patch, then a fork with a PR upstream. (2026-06-06, 2026-08-02)
- **Clean up.** Merged branches and their worktrees, local and remote, obsolete environments, and anything a test created on a live system. (repeated, 2026-09-22, 2026-11-10)
- **Long-running services run from trunk**, not from a worktree. (2026-11-12)

## Open

- Before a migration or any change to real data, where does the backup go? Until decided, the provider's own snapshot or export, taken and verified before the change.
