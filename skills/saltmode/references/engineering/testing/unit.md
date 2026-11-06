# Unit Testing

## Write Behavioral Unit Tests

Test a public module through its public contract. For a substitutable capability,
use in-memory Fakes and simple Stubs supplied with the Port or contract. Test
pure functions, immutable values, and UI components directly.

Choose assertions per
[test behavior, not implementation](../../../../principle-test-behavior-not-implementation/SKILL.md).

Inject time, random values, identifiers, and nondeterministic boundaries. Cover
normal behavior, meaningful error handling, and critical invariants.

Apply mutation testing periodically to critical pure business modules such as
money calculations, authorization rules, and state machines, or when those
modules change materially. Track mutation score separately from statement
coverage. Mutation testing is not a universal per-PR gate.
