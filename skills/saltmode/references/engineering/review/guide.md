# Engineering Review

Review findings follow [interrogate](../../../../interrogate/SKILL.md): report
only what you ran, never fix during review, and leave style, naming, and
structure out. Fixes run in the playbook that follows, across every instance of
the pattern per [fix root causes](../../../../principle-fix-root-causes/SKILL.md).
This guide adds risk-based depth and severity.

Classify each non-mechanical change before choosing review depth:

- **High risk:** public or cross-service contracts; authentication,
  authorization, security, or privacy; money, billing, credit, or quota;
  persisted data or migration; concurrency, transactions, distributed work;
  production delivery or another hard-to-reverse decision.
- **Low risk:** localized, reversible, internal, and none of the high-risk
  conditions.
- **Medium risk:** every other non-mechanical change.

Turn the classification into inspection depth:

- Low risk: run the local behavior, affected callers, and focused acceptance.
- Medium risk: trace the changed boundary end to end, exercise failure behavior,
  and verify the relevant integration or interaction seam.
- High risk: explicitly exercise the affected authorization, money, persistence,
  compatibility, concurrency, or recovery invariants with negative and
  adversarial cases. Do not make unrelated high-risk domains part of the review
  just to complete a checklist.

Neither model agreement nor an author's success report substitutes for a run.
Classify severity: `blocking` means the requested outcome is wrong or incomplete,
a supported contract breaks, security or data integrity is at risk, or an
applicable configured gate fails; otherwise it is `non-blocking`.

Lead with findings ordered by severity and include precise file and line
locations. Then state assumptions, unanswered questions, verification evidence,
and a concise change summary. If there are no findings, say so and identify any
remaining test or review limitation.
