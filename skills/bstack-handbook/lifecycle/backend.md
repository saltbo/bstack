---
id: backend
version: 2
audience: worker
applies: projects with a backend
---

# Backend

## Decisions

- **Organize by business capability.** Domain code imports no web framework, database, queue, vendor SDK, or runtime config. Only the composition root knows the concrete adapters. (2026-09)
- **A use case exists only when it owns something**, such as a rule, a state change, a transaction, or orchestration across dependencies. Otherwise the transport validates, calls the port, and maps the result. Delete any layer that only forwards its arguments. (2026-09)
- **An interface is a port only at a real system boundary**, such as a database, a queue, external HTTP, the clock, or id generation. The module that uses a port owns it, with its types and its fake. Internals with one implementation have no interface. (2026-08-02, 2026-09)
- **Dependencies are passed explicitly and wired by hand in the composition root.** No service locator and no app-wide dependency bag. A dependency-injection framework is used only where the ecosystem has a mature one, so not in TypeScript. (2026-08-02)
- **Database rows, SDK objects, and wire types stay inside their adapter or transport.** (2026-09)
- **Layer boundaries are enforced by an import lint that fails CI**, not by a directory diagram. (2026-09)
- **The use case owns the transaction.** No transaction opens in a handler, and no network call happens inside one. Prefer one conditional write or a database constraint over read-then-write. (2026-09)
- **Repositories are shaped around domain resources, not tables.** Use the ORM's own API, not hand-built SQL. The schema itself follows [database](database.md). (2025-10-10, 2026-06-06)
- **A cache keeps the port's behavior unchanged.** It does not serve stale data silently or fail open. Fix the design first, and add a cache only if it is still slow. (2026-07-26, 2026-09)
- **Config is parsed once at startup, and a bad config stops startup.** (2026-09)
- **Background work is idempotent**, since delivery is at least once. A message carries its own id, a trace id, and an idempotency key. Long-running work keeps its state in storage, not in memory. (2026-09)
- **Each port has a small fixed set of error categories.** The adapter maps provider errors into them and keeps the cause. Expected failures are returned, and unexpected ones are thrown with their context, never disguised as an unknown error. (2026-08-02)
- **Log at the boundary only.** Each request, job, and scheduled entry emits one structured completion event, with credentials and bodies redacted. A request and the jobs it starts share a trace id. (2026-08-02)
- **A lower layer never knows its consumers.** A problem is fixed in the project that owns it, not worked around downstream. (2026-09-02)
