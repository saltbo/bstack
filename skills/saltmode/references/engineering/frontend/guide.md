# Frontend Engineering

Apply BEP preferences to the code you touch. When a requirement reshapes a
boundary, redesign it per [redesign from first principles](../../../../principle-redesign-from-first-principles/SKILL.md)
instead of bolting onto the old shape.
UI/UX design and frontend implementation share this module, with separate
references. Keep server policy authoritative and each state/effect with one owner.

Read only the relevant reference:

- [Ownership and state](ownership.md): features, dependencies, state,
  and effect lifecycles.
- [Remote data](remote-data.md): transport, decoding, and reconciliation.
- [UI/UX](ui-ux.md): page composition, navigation, forms, feedback,
  responsive interaction, components, and accessibility. Read for designing or
  changing these interactions; a layout task does not need the architecture refs.
- [Security and storage](security-storage.md): identity, scripts,
  durable browser data, and offline behavior.
- [Performance](performance.md): rendering, telemetry, and compatibility.
- [Verification](verification.md): only for formal frontend inventories,
  architecture enforcement, or browser-quality governance.

For implementation, local acceptance is required: use focused checks and inspect
affected interaction and responsive behavior in a local browser when applicable.
Fix change-caused failures and report what was exercised. Choose test layers with
[testing guidance](../testing/guide.md) when designing tests; do not load it just to run them.
Read [HTTP guidance](../http/guide.md) only when HTTP semantics change.
Review-only requests remain read-only; an explicit request to fix findings
includes in-scope correction and local acceptance.
