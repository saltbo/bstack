---
id: planning
version: 1
audience: leader
applies: all
---

# Planning features and versions

This is the stage Saltbo takes part in. A new feature, the scope of a version, and a product design are his calls.

## Decisions

- **These wait for him.** What a new feature does, what goes into a version, and how a product looks and behaves. Ask all open questions at once, each with a recommended default.
- **Everything after the plan does not wait.** Once the scope is agreed, the work runs to merged without another turn from him.
- **First PR.** A plan's first PR is a slice that works end to end, so the pipeline is proved early. The design it builds toward is the full end state.
- **Every PR in a plan carries its acceptance criteria**, per [verification](verification.md).
- **He approves the target, then it is built exactly.** For a feature or a redesign, show him only the target version, such as the menu, the API list, or the command set. After he approves, implement that without improvising and without switching proposals. (repeated, 2026-08-04)
- **Engineering choices are not brought to him as a menu.** Pick the most standard best-practice option. (2026-08-02)
- **A plan is the whole end state, delivered in one run.** PRs are an order of delivery, not a way to stop and check in. (2026-08-11, 2026-11-12)
- **Tasks are cut by feature or module**, each one something a single agent can build and verify with full context, never by job role and never as a step list. (2026-05-04, 2026-06-01)
- **A confirmed bug goes straight to work. A new feature or requirement waits for his confirmation in the issue.** (2026-09-13)
- **Large changes are planned in a document in the repository**, not only in chat. (2026-08-29)
