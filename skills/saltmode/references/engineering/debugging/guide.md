# Software Debugging

The method lives in pstack: the [Bug fix](../../../playbooks/bug-fix.md) and
[Perf issue](../../../playbooks/perf-issue.md) playbooks,
[fix root causes](../../../../principle-fix-root-causes/SKILL.md), and
[attack the premise](../../../../principle-attack-the-premise/SKILL.md). Vet any
measured difference with [benchmark-checklist](../../../../benchmark-checklist/SKILL.md).
Authority for fix and diagnosis-only requests is in the
[host adapter](../../host-adapter.md). These BEP refinements add to them:

- Reduce the symptom to the smallest deterministic reproduction or controlled
  probe, and trace the real public seam and affected dependency boundary.
- Remove temporary instrumentation before finishing.
- For performance regressions, compare a baseline and look first at queries,
  fan-out, concurrency, memory, and dependency calls before micro-optimizing.
