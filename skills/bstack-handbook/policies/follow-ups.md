---
id: follow-ups
version: 3
audience: leader, worker
applies: all
---

# Follow-ups

## Decisions

- **A problem outside the task goes to the project's issue tracker.** One issue per problem, with the command or observation that shows it. It does not go into the current PR.
- **The tracker of `saltbo/bstack` takes only problems with the text of a handbook or a skill.** That is a text that led an agent to the wrong action, or was silent where the agent had to decide. The issue names the handbook id and version and the session or PR where it showed. A defect or a missing feature in a product or a tool goes to that product, also when a handbook entry mentions the subject. (2026-11-15)
- **A worker lists follow-ups in its report.** The leader files them.
- **A gap in another project or upstream is filed there**, with a tracking issue in the project that depends on it. (2026-08-29)
- **An issue is written from the user's view.** The title and body describe the symptom. A comment gives the cause, the workaround, and the one upstream issue to track. (2026-05-05)
- **Something uncertain is an issue, not a task.** Proposals are issues as well, not memory notes. (2026-06-27)
- **An agent's own mistake becomes an issue against the skill or handbook**, not a promise to do better. (2026-05-05)

## Open

- When are a worker's follow-ups filed? Until decided, the leader files them as issues before it merges the PR, so they survive if its session ends after the merge. (saltbo/bstack issue 7.)
