---
id: project
version: 1
audience: leader
applies: all
---

# Starting a project

## Decisions

- **A project declares its type and its facts, not its rules.** Its `AGENTS.md` carries the block described in the [index](../SKILL.md). Rules live in this handbook.
- **A new product gets its own repository.** A separate client app gets its own repository too. (2026-10-02, 2026-07-09)
- **A full-stack web project starts from `saas-web-starter`**, with frontend and backend in one repository, on the Workers runtime, with pnpm and the latest toolchain. (2026-10-15)
- **Sign-in is Realmroot over OIDC.** The app checks tokens and permissions in API middleware and builds no login or session layer of its own. (2026-05-26, 2026-11-15)
- **Every repository has a `spec/` folder of `.feature` files** as the source of truth for product behavior, and its gate checks that each scenario is covered by a test, per [testing](testing.md). Markdown does not hold product behavior or API descriptions. (2026-06-27, 2026-09-03, 2026-11-15)
- **Every repository has a `docs/adr/` folder of architecture decision records.** An ADR keeps a project decision that later engineering work needs to know, with its reason. Judge by lasting architectural relevance. Being reversible does not rule a decision out, and incidental implementation detail does not belong. A missing folder is a gap to close, like a missing `spec/`. (2026-09-02, 2026-11-15)
- **Each record has its place.** `spec/` says what the product does. `docs/adr/` says why the project is built the way it is. This handbook holds what applies across projects. A choice that would hold for his other projects too is reported for the handbook, not written as an ADR. (2026-11-15)
- **The leader writes the ADR.** When a task settles such a decision, including one a worker reports under its decisions, the leader records it in the same PR. Before reopening a technical choice, read the ADRs. A decision that replaces an earlier one says so and marks the old record superseded. (2026-11-15)
- **The feedback loop is set up, not described.** Hooks, CI checks, and test commands exist and run. (2026-07-06)
- **Nothing personal goes in the repository**, such as a local development domain. (2026-07-30)
- **The agent creates the repository.** A product repository goes under the product's organization, and anything else under his own account. (2026-08-14, 2026-11-15)
