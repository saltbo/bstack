---
id: docker-service
version: 1
audience: leader, worker
applies: projects that declare this type
---

# Self-hosted service

Typical stack: A container image others or we run. A project of this type follows [release](../lifecycle/release.md) for the image, and [deploy](../lifecycle/deploy.md) when we run it ourselves. This file holds what is specific to the type.

## Decisions

- **Images are built in CI, never on the server.** The server only pulls. (2026-08-26)
- **One image repository**, with variants told apart by tag. (2026-06-06)
- **The image runs complete on start.** Runtime dependencies and data files are baked in, and database migrations run at startup. Paths inside the container match local paths. (2026-06-01, 2026-06-06)
- **The compose file in the repository is the deployment example.** It is not repeated in the README. (2026-06-06)

## Open

- Which registry and which tags (`latest`, version, commit)? Until decided, the project's existing registry with a version tag and a commit tag.
- How is an upgrade rolled back? Until decided, by redeploying the previous version tag.
