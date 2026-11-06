# Verification Governance

Establish what the task is governing: coverage thresholds, BDD traceability,
production inventories, execution integrity, or CI enforcement. Reading this
module does not adopt every mechanism or expand a local change to the whole repo.

For a new governance setup, use BEP preferences in the relevant references.
For an existing project, inspect its configured policy and supported runners;
preserve them unless the requested work includes a policy transition. A new
project's test pyramid does not require a bespoke proof adapter before it can
have useful tests. Introduce machinery only for the formal guarantees in scope.

- [Coverage measurement](coverage-policy.md): independent denominators and
  behavioral coverage; thresholds come from the user or project, not BEP defaults.
- [Identities](identities.md): stable mappings and adopted BDD tracing.
- [Inventories](inventories.md): authoritative production discovery and
  applicability. Runtime details are in the backend/frontend verification profiles
  in the bundled [backend](../backend/verification.md) and
  [frontend](../frontend/verification.md) profiles when that governance is in scope.
- [Execution](execution.md): framework adapters and native-report integrity.
- [CI](ci.md): enforcing the selected required gates.

A test proves one behavior at its cheapest complete layer. A native passing
report proves execution; source discovery proves expectation, never execution.
Preserve failed, skipped, and retry evidence rather than turning it into a pass.

Validate the implemented collector, adapter, or rule locally with meaningful
positive and bypass-oriented negative cases. Reconcile the declared scope with
actual execution. Report missing evidence as a limitation of that guarantee;
do not block unrelated work or invent coverage estimates. Never weaken an
adopted gate just to finish the task.
