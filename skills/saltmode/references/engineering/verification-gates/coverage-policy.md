# Coverage Measurement

BEP sets no default coverage thresholds. Ordinary changes follow
[tdd](../../../../tdd/SKILL.md): prove the change, without unrelated coverage
expansion. Use this reference only when the user asks to build or audit coverage
governance; the thresholds are the ones the user or the project declares.

## Measure Independent Coverage Denominators

Keep each governed gate's denominator independent: Unit production code, BDD
scenario traceability, Integration boundaries, frontend behavior inventory, and
Critical E2E journeys. A required suite with skipped tests is not passing.

Measure Unit production code with statement coverage, or the ecosystem's
closest production-code equivalent, per production package or module and for
changed code. Exclude generated code and generated mocks. Do not reclassify
business logic as an Adapter or execute it only through Integration or E2E to
evade the Unit denominator.

Do not represent Integration, BDD, frontend behavior, or E2E confidence with
line coverage. Compute them from passing required inventory pairs:

```text
behavioral coverage = passing required (item, profile) pairs
                      / all required (item, profile) pairs
```

A skipped test, wrong-layer mapping, missing profile, stale identity, or mapping
without an executable passing native-report item is uncovered.
