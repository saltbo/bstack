# Backend Engineering

Apply BEP dependency and ownership preferences to the code you touch. When a
requirement reshapes a boundary, redesign it per [redesign from first principles](../../../../principle-redesign-from-first-principles/SKILL.md)
instead of bolting onto the old shape. Published contracts follow [compatibility](../delivery/compatibility.md).

Read only what the decision needs:

- [Ownership](ownership.md): module boundaries, dependency injection,
  use cases, ports, models, and stable errors.
- [Persistence](persistence.md): transactions, repositories, and caches.
- [Messaging](messaging.md): queues, durable jobs, and events.
- [Lifecycle](lifecycle.md): startup, readiness, and shutdown.
- [Verification](verification.md): only when designing or auditing
  formal backend proof inventories and architecture enforcement.

Use [http guidance](../http/guide.md) only for an HTTP semantic change and
[openapi guidance](../openapi/guide.md) only for REST resource or representation design.
Read those internal modules only for the affected protocol or resource decision.

For implementation, complete local acceptance: run the smallest meaningful
checks and exercise the changed behavior, fix failures caused by the change,
and report evidence. For test design use [testing guidance](../testing/guide.md); merely running
existing tests does not require loading it. Review-only requests remain read-only.
