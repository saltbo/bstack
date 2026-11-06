# Frontend Remote Data

Apply these preferences to the code you touch. Formal project-wide CI governance is a separate task.

## Put Remote Access At A Feature Boundary

Derive the typed client, wire types, and runtime schemas from one authoritative
protocol source per
[type-system discipline](../../../../principle-type-system-discipline/SKILL.md).
Keep generated files isolated and never edit them.

Keep a small environment-specific transport boundary in `shared/api` or its
repository equivalent. It owns base URL, correlation, credentials, decoding,
and protocol-level error normalization. A feature owns its query and mutation
definitions, cache keys, freshness policy, invalidation, stable error mapping,
and user-visible reconciliation. A route or page composes those definitions.
Presentational components receive data and emit semantic events; they do not
call `fetch`, an RPC client, or a query cache directly.

Do not mechanically reproduce backend Repository, Use Case, Port, and Adapter
layers for ordinary frontend CRUD. Introduce a dependency-free client domain or
application module only for substantial browser-owned behavior such as an
editor, local workflow, offline engine, or complex deterministic state machine.

Every query declares its freshness and invalidation semantics. Every mutation
declares duplicate-submission, conflict, cancellation, and uncertain-result
behavior. Default to server-confirmed updates. Use optimistic updates only for
low-risk reversible operations with explicit rollback and authoritative
resynchronization. Never display an uncertain write as confirmed success.

## Validate Every Runtime Boundary

TypeScript proves compile-time relationships, not runtime data. Decode and
validate untrusted values before they enter a feature:

- API and streaming responses;
- URL path, query, fragment, and navigation state;
- local storage, session storage, IndexedDB, cache, and imported files;
- `postMessage`, BroadcastChannel, Service Worker, extension, and third-party
  script events;
- public runtime configuration and server-rendered bootstrap data.

Prefer a schema derived from the protocol's authoritative contract. Treat the
decoded value as a new trusted value; do not spread `unknown` data into a typed
object. Reject `as`, non-null assertions, silent defaults, or fallback parsing
used only to bypass a failed boundary check. A schema mismatch is an explicit
contract failure and enters the unexpected-failure observability path.

For presentation of loading, errors, and uncertain outcomes, read the
[UI/UX feedback guidance](ui-ux.md#model-rendering-and-failure-deliberately)
when that interaction is being designed or changed.
