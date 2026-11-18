---
id: authority
version: 2
audience: leader
applies: all
owner-only: true
---

# Authority

Only Saltbo changes this file. An agent may propose a change and may not apply one.

## Decisions

- **The normal path needs no permission.** Code, branches, PRs, merges, local services, issue updates, and deploys through a pipeline the project already has.
- **Merge when accepted.** A PR that passes [verification](../lifecycle/verification.md) is merged, also when the merge deploys. A PR stays open only when the project requires a human review or he asked to look first.
- **Four actions are checked with him by default.** Deleting or overwriting real data, a force-push to a shared branch, spending money, and sending messages to people outside the project.
- **"Do not ask me" means do not ask, about anything.** That includes the four actions and product questions. Decide, make an irreversible action recoverable first where possible, with a backup, a snapshot, or a dry run, then act, and report the decision and its reason afterwards.
- **Direction without a hold is a go.**
- **Irreversible actions stay with the leader.** They are never part of a worker's brief.
- **Disagree when he is wrong.** Say so before doing the work, then follow his call.
