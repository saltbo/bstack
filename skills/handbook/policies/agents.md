---
id: agents
version: 1
audience: leader
applies: all
---

# Agents and sessions

## Decisions

- **One session per git repository.** Work in the leader's own repository goes to workers. Work in another repository goes to an independent session, which runs saltmode as the leader of that repository. The first leader gives it the goal and the acceptance criteria and follows it by its PRs and its report. (2026-11-15)
- **The rule of two subagents and five review rounds is retired.** Acceptance has one fix round. (2026-11-15)
- **Guidance for agents lives in skills and this handbook**, written as rules that trust the model, not as step-by-step procedure, and without project implementation detail. (2026-06-27, 2026-09-13)
- **An independent session uses the mechanism of the place the leader runs in**, a T3 Code thread inside T3 Code and `hc` inside Herdr. (2026-11-15)
- **A worker has no helper subagents.** It writes its own tests, and the leader is the second reader. (2026-11-15)

## Open

- A scheduled maintainer for each repository, which would cut releases and do upkeep, is planned and not designed.
