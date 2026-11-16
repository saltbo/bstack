---
id: agents
version: 5
audience: leader
applies: all
---

# Agents and sessions

## Decisions

- **One session per git repository.** Work in another repository goes to an independent session, which runs saltmode as the leader of that repository. The first leader gives it the goal and the acceptance criteria and follows it by its PRs and its report. (2026-11-15)
- **The rule of two subagents and five review rounds is retired.** Acceptance has one fix round. (2026-11-15)
- **Guidance for agents lives in skills and this handbook**, written as rules that trust the model, not as step-by-step procedure, and without project implementation detail. (2026-06-27, 2026-09-13)
- **Dispatch uses the tool of the environment the leader runs in.** In T3 Code that is T3's own delegation, in Herdr it is `hc`, and elsewhere it is the harness's own subagents. This holds for workers, verifiers, and sessions in other repositories. (2026-11-15)
- **A worker has no helper subagents.** It writes its own tests, and the leader is the second reader. (2026-11-15)

## Defaults

- **Work in the leader's own repository goes to workers.** The leader builds a change itself when it is small and the leader already holds the context it needs, because briefing a worker from nothing would cost more than the change. It dispatches when the work would crowd its own context, has parts that can run in parallel, or deserves a second reader. (2026-11-15)

## Open

- A scheduled maintainer for each repository, which would cut releases and do upkeep, is planned and not designed.
