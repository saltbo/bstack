---
id: testing
version: 1
audience: worker
applies: all
---

# Testing

What tests a project has and how they are written. Who checks what, and when, is in [verification](verification.md).

## Decisions

- **Each behavior is tested once, at the cheapest layer that can prove all of it.** The full set of cases lives at the layer that owns the rule. Higher layers prove the wiring and one representative outcome. (2026-08-08)
- **Unit tests go through a module's public contract**, with in-memory fakes that ship with the interface they stand in for. (2026-08-02)
- **An integration test names one real boundary** and runs the production schema, codec, and middleware for it. Repository tests run on the production database engine with the real migrations. (2026-09)
- **End-to-end tests enter through the product's real entry point and mock nothing inside the project.** Only dependencies outside the project may be faked. Each run has its own database, config, and ports, starts clean, and never shares state with the development environment. It uses a seeded test account. (2026-05-20, 2026-08-02)
- **No retries, quarantine, fixed sleeps, or skips in required tests.** Fix the race or wait on observable state. Clocks, random values, and identifiers are injected. (2026-09)
- **A scenario states behavior in product language**, with no tables, HTTP paths, selectors, or mocks. It is proved by ordinary tests that carry its id, and no separate BDD runner is required. A refactor leaves scenarios unchanged. (2026-07-06, 2026-09)
- **While iterating, run only the tests for what changed**, frontend and backend separately. The full suite runs in CI, which finishes in about three minutes with independent parts in parallel. (2026-08-05, 2026-08-30)
- **No coverage target unless the project declares one.** Business logic is not reclassified or left to higher layers to get around one. (2026-09)
- **The gate runs the same commands locally and in CI.** It fails on a focused, skipped, or retried required test and on a missing report, and it checks that every scenario has a test. A custom lint rule has a fixture that passes and one that tries to get around it. (2026-09)
- **Script names.** `test` runs unit tests and `test:e2e` runs end-to-end tests. No other test entry points. (2026-05-25)
- **A failed end-to-end run keeps its evidence**, such as the trace, screenshots, and boundary logs, before cleanup. PR screenshots are not stored in the repository. (2026-07-05, 2026-09)
- **One end-to-end suite serves every environment.** The target and identity are injected. The subset that may run against production is picked by an explicit tag and never resets, seeds, or changes business data. (2026-06-07, 2026-09-03)
