---
id: planning
version: 4
audience: leader
applies: all
---

# Planning features and versions

Saltbo takes part here only where the product's direction changes. Inside its direction, features are planned and built like any other work.

## Decisions

- **A change of direction waits for him.** That is a change to the product's positioning or to a global rule in its `UX.md` or `DESIGN.md` (see [project](project.md)), something the positioning rules out, removing or reshaping a core capability, pricing and licensing, and what goes into a version. Ask all open questions at once, each with a recommended default.
- **A confirmed bug, and a feature inside the positioning, go straight to work.** The agent judges it against the positioning, builds it to `UX.md` and `DESIGN.md`, merges it, and reports what it built and why. Most such features are what a mature product of its kind is expected to have, such as i18n, search, sort, and paging, and he does not want to review them one by one. A request the positioning does not settle goes to him with the agent's assessment and a recommendation. A project with no positioning yet gets one drafted for his confirmation before its first feature. (2026-09-13, 2026-11-26)
- **Everything after the plan runs on its own.** Once the scope is agreed, the work runs to merged without another turn from him.
- **First PR.** A plan's first PR is a slice that works end to end, so the pipeline is proved early. The design it builds toward is the full end state.
- **Every PR in a plan carries its acceptance criteria**, per [verification](verification.md).
- **He approves the target, then it is built exactly.** For a change of direction, show him only the target version, such as the menu, the API list, or the command set. After he approves, implement that without improvising and without switching proposals. (repeated, 2026-08-04)
- **Engineering choices are the agent's.** Pick the most standard best-practice option. (2026-08-02)
- **A plan is the whole end state, delivered in one run.** PRs are an order of delivery, and the run continues through all of them. (2026-08-11, 2026-11-12)
- **Tasks are cut by feature or module**, each one something a single agent can build and verify with full context, never by job role and never as a step list. (2026-05-04, 2026-06-01)
- **Large changes are planned as tasks in docket**, where he reviews them on a card and each task keeps its own history. (2026-08-29, 2026-11-16)
