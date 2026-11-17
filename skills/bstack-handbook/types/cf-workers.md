---
id: cf-workers
version: 4
audience: leader, worker
applies: projects that declare this type
---

# Cloudflare Workers app

Typical stack: Hono on Workers, D1, a React SPA. A project of this type follows [deploy](../lifecycle/deploy.md). This file holds what is specific to the type.

## Decisions

- **Tests run on GitHub Actions. Deploys run on Cloudflare Workers Builds.** GitHub Actions runs the project's gate on every push. Workers Builds, connected to the repository, deploys the production branch and creates a preview for every other branch. Where [verification](../lifecycle/verification.md) says CI is green, both have passed on the commit.
- **Every project of this type has a preview for each PR.** Workers Builds produces it with its preview command, `npx wrangler preview`, and reports the address on the PR. Preview proof and the leader's sample run there.
- **Preview code is per branch. Preview data is shared.** A project with a database has one preview D1 database, separate from production, that every branch's preview uses. It works as the pre-release database. A project without a database needs nothing more than the per-branch preview.
- **A push to the production branch deploys.** Agents push and re-check, and do not run a manual deploy. A D1 migration needed by a release is applied as part of it. (repeated, 2026-06-26, 2026-06-02)
- **No always-on staging Worker and no per-PR databases created by hand.** Previews of the one Worker share the pre-release database. (2026-09-22, 2026-11-13)
- **Local development runs on the Workers runtime**, not Node. (2026-09-22)
- **Naming.** A D1 database has the same name as its Worker, and Workers carry the product prefix. (2026-08-12)
- **Static assets never pass through the Worker.** Only explicitly listed paths are routed to code. Do not add a Worker or a route when a path on the existing one will do. (2026-07-20, 2026-08-15)
- **Use the platform's own observability and rate limiting.** (2026-08-14)
- **Config.** Non-sensitive values live in the wrangler config and only real secrets are secrets. The frontend gets its config from one backend endpoint, not from build-time variables. (2026-06-28, 2026-07-31)
- **Large uploads and downloads are streamed**, never buffered in Worker memory. (2026-05-13)
- **A response that carries an ETag sends `Cache-Control: no-transform`.** Cloudflare's compression otherwise turns a strong ETag into a weak one, and the `If-Match` a client sends back no longer matches. (2026-11-15)

## Open

- A preview needs sign-in, and the identity provider matches callback addresses exactly, so a preview's address is not registered. Until decided, the worker adds that preview's callback and origin to the project's application in the identity provider when the preview is created, and removes them after the PR merges. This is part of the task and needs no approval. (Seen on bstack-playground issue 3.)
- Two PRs change the schema of the shared pre-release database at the same time. Until decided: an additive migration is applied to the shared database, since other previews ignore what they do not use. A PR that needs a destructive migration gets its own temporary copy, created and removed by the pipeline and never by hand, and the shared database changes only when that PR merges. The pre-release database holds nothing of value, so it is rebuilt from trunk's migrations whenever it has drifted. In a development project, skip the copy and rebuild instead. The automatic copy has not been tried.
- How is a local build exposed for an external callback? Until decided, a cloudflared tunnel at `<project>-saltbo.tftt.cc`.
