# Audit Scope And BEP Preferences

Compare requested outcomes and supported behavior first. Apply BEP ownership,
contract, testing, and delivery preferences. Do not require new BDD tooling or a
new coverage protocol merely because this audit is comprehensive.

Inspect the relevant boundaries for concrete risks: ownership and dependencies;
error propagation; concurrency and state; authentication and authorization;
supported contracts and data migrations; test-layer sufficiency; local acceptance;
and, only for a deployment task, live regression and recovery.

Keep general coding guidance out of a second mandatory handbook. Specialist
references own detailed rules. Formal thresholds and proof inventories apply only
to adopted governance or the policy work requested in this audit.

For new products, BEP favors lightweight domain behavior specifications, a test
pyramid, and clear local acceptance commands. Existing products keep their native
specification/test conventions unless the task includes changing them. Pure
libraries do not need product BDD merely to fit this preference.

Scale review depth to concrete risk. Independent review gates named by the
playbooks are mandatory; when the independent reviewer cannot run, report the gate
as unmet.

For each finding, record evidence and severity. Interrogate reports and does not
fix. The playbook that follows fixes the pattern, not just the instance, per
[fix root causes](../../../../principle-fix-root-causes/SKILL.md). Completion means
the requested outcome and applicable acceptance are satisfied.

The feedback-loop, vertical-slice, deep-module, seam, behavior-testing, diagnosis,
and two-axis review ideas were adapted from Matt Pocock's MIT-licensed
[skills](https://github.com/mattpocock/skills) repository, copyright 2026 Matt Pocock.
The BEP choices reflect this repository owner's preferences.
