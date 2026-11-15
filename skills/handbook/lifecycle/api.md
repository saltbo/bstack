---
id: api
version: 2
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
- **Status codes.** `400` for malformed syntax, `422` for valid syntax that breaks a domain rule, `404` for a resource that is absent or deliberately hidden, `409` for a conflict with current state, `428` when a required `If-Match` is missing, `412` when it is stale, `401` with `WWW-Authenticate` for missing credentials, `403` for missing authority, `415` for an unsupported content type. (2026-09)
- **Every error is RFC 9457 `application/problem+json`.** Its `type` is a stable URI of the form `https://<api host>/problems/<kebab-case-name>` and is the only machine identity. There is no `code` field, at the top level or per field. `title` is the same for every occurrence of a type. `detail` describes this occurrence for a person. `status` repeats the HTTP status. `instance` is `urn:request:{requestId}`. A value a client must act on is a typed extension field, never something to parse out of prose. Nothing internal is exposed, such as a stack trace or an internal identifier. (2026-08-08, 2026-09, 2026-11-15)
- **A validation problem lists every failure at once** in an `errors` array of `{pointer, detail}`. `pointer` is a JSON Pointer into the logical request, whose top level is `body`, `query`, `path`, and `headers`, such as `#/body/tags/3` or `#/headers/If-Match`. (2026-08-08, 2026-09)

  ```json
  {
    "type": "https://api.example.com/problems/validation-error",
    "title": "Request validation failed",
    "status": 422,
    "detail": "One or more request values are invalid.",
    "instance": "urn:request:01JZ8Y6M8W7Q",
    "errors": [{ "pointer": "#/body/displayName", "detail": "must not be empty" }]
  }
  ```
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
