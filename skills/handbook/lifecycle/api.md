---
id: api
version: 1
audience: worker
applies: projects with an HTTP API
---

# API design

Saltbo's conventions for an HTTP API. They choose between legitimate alternatives, so follow them even where another style would also be sound. `scripts/check_resource_paths.py --profile bep '<path>'` checks path names.

## Decisions

- **Paths.** Literal segments are plural lowercase kebab-case nouns. Path parameters, query parameters, and JSON properties are lowerCamelCase. Identifiers are opaque and stable. (2026-09)
- **One canonical URI per resource**, shared by every caller. No role, client type, service, or team in a path. Access is decided by permissions. The current user is `/account`. (2026-08-05, 2026-08-10)
- **No verbs and no action routes.** An action becomes creating, replacing, or deleting a noun resource. Cancel is `PUT .../cancellation`, a retry is a new job that names its source, approve is an approval resource. (2026-09)
- **Nest only what cannot exist outside its parent.** Anything with its own lifecycle gets a top-level URI. Grouping is shown by one OpenAPI tag per operation, not by a URI prefix. (2026-09)
- **Create with `PUT` when the client controls the identifier, with `POST` on the collection when the server assigns it.** A create returns `201` with `Location`. A delete returns `204` and is a soft delete by default. (2026-09, 2026-09-03)
- **`PATCH` is `application/merge-patch+json`.** Create, replace, and update return the full resource, and honor `Prefer: return=minimal`. (2026-09)
- **Status codes.** `400` for malformed syntax, `422` for valid syntax that breaks a domain rule, `428` when a required `If-Match` is missing, `412` when it is stale, `401` with `WWW-Authenticate` for missing credentials, `403` for missing authority. (2026-09)
- **Every error is RFC 9457 `application/problem+json`** with a stable `type` URI. Validation problems carry an `errors` array of `{pointer, detail}`. There is no `code` field. `instance` is `urn:request:{requestId}`. All problems are reported in one response, not one at a time. (2026-08-08, 2026-09)
- **One pagination profile per project**, page or cursor, on every collection that can grow. A collection returns `{ "items": [...], "pagination": {...} }` and a single resource is returned bare. Navigation links go in the `Link` header. (2026-09)
- **Sorting is `orderBy=createdAt desc,id asc`** with a unique tie-breaker. Filters are separately declared typed parameters. Related resources are embedded only through listed `include` values. (2026-09)
- **A missing property is omitted.** `null` is used only when null means something in the domain. (2026-09)
- **Concurrency uses `ETag` and `If-Match`** on every mutable resource, with no separate version field. (2026-09, 2026-09-05)
- **`Idempotency-Key` only where a client must retry an unknown outcome** or a duplicate is costly. A replay returns the original response, and reuse with different content returns `422`. (2026-09)
- **Long-running work is a job resource named for its domain**, such as `/datasets/{datasetId}/export-jobs`, never a generic `/operations`. Creating it returns `201`. (2026-09)
- **No version in the URI.** A project that needs versioning uses one `API-Version: YYYY-MM-DD` header. A project that does not need it has none. (2026-09, confirmed 2026-11-15)
- **Every operation declares its security scheme and scopes in the contract.** Authentication produces one normalized principal, a separate component authorizes, and handlers never read tokens or branch on roles. Every endpoint is in the contract, and scopes decide who may call it. (2026-08-02, 2026-09-04)
- **`operationId` is `list`, `get`, `create`, `replace`, `update`, or `delete` plus the resource**, unique and stable. (2026-08-04)
- **The server generates `Request-Id` for every request** and returns it on every response. A caller's own id goes in `Client-Request-Id`. (2026-09)
- **The contract is defined once, in code**, and the OpenAPI document and every SDK are generated from it. The project's own frontend may call over RPC, and outside clients use OpenAPI. (2026-06-05, 2026-11-15)
- **Errors, pagination, sorting, preconditions, idempotency, correlation, and authorization are each built once at the framework boundary.** Handlers take validated input and return a domain result. (2026-08-02)
