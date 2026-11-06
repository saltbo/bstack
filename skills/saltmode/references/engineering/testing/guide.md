# Software Testing

## Build A Proportionate Test Pyramid

Use many fast Unit tests for rules and state transitions, focused Integration
tests for real boundaries, and a small set of critical E2E journeys. This is a
responsibility model, not a fixed numerical ratio or a demand for every layer
when the system has no corresponding boundary.

Assign each behavior to the cheapest layer that can prove it completely:

- Unit: domain decisions, deterministic transformations, orchestration behind
  fake external ports, and browserless component interaction.
- Integration: real datastore, router/middleware, codec, queue, or browser semantics.
- Contract: independently deployed consumers and providers agreeing on a wire contract.
- E2E: a critical user journey through the real application stack.

Cover the full decision matrix once at its owning layer. Higher layers prove
wiring and representative outcomes, not the same matrix again. Browser-only
semantics need real-browser proof; do not add a duplicate simulated Unit matrix.
Assertion design follows
[test behavior, not implementation](../../../../principle-test-behavior-not-implementation/SKILL.md).

When the project has a verification skill, its `features/` map is the maintained
verification source per
[create-verification-skill](../../../../create-verification-skill/SKILL.md). Keep
it current with the E2E suite and link each critical journey to the map entry it
proves.

## Fit The Project And Change

For a new project, establish a lightweight pyramid using the stack's native
runner, isolated fixtures, and clear local commands. For an existing project,
reuse its runners and conventions; add missing proof at the affected boundary.
Do not impose a suite rewrite, new BDD framework, or coverage governance for an
ordinary test change. Keep complete critical behavior coverage and fast feedback
as the goals, rather than raw test counts or duplicated line coverage.

- [Unit](unit.md): behavioral assertions and test doubles.
- [Integration and contracts](integration.md): real boundary semantics.
- [E2E](e2e.md): critical journeys, isolation, and failure evidence.
- [Specifications](specifications.md): creating product specifications
  or working in a project that already uses BDD.
- [Live E2E](live-e2e.md): creating or changing E2E runner/fixtures,
  or preparing a deployable regression subset.

Use [verification gates guidance](../verification-gates/guide.md) only when building or auditing formal coverage or
CI governance. Its metadata and thresholds are not prerequisites to testing.

## Close The Local Feedback Loop

Regression proof follows [tdd](../../../../tdd/SKILL.md); proof on the real artifact and
reporting a blocked check follow
[prove it works](../../../../principle-prove-it-works/SKILL.md). In addition, run
the necessary type/build/contract checks, and broaden checks only when changed
boundaries or unresolved failures justify the extra cost.

Keep fast feedback available separately from the critical E2E suite. Improve
isolation, reuse safe setup, and parallelize independent tests. Do not hide
failures using retries or skips. Local acceptance does not authorize deployment.
