---
id: go-cli
version: 1
audience: leader, worker
applies: projects that declare this type
---

# Go command line tool or service

Typical stack: Go, goreleaser, Homebrew tap. A project of this type follows [release](../lifecycle/release.md) and [versioning](../lifecycle/versioning.md). This file holds what is specific to the type.

## Decisions

- **Released with GoReleaser**, as prebuilt binaries, with a Docker image and a Homebrew tap under the product's organization. Never `go install`. (2026-06-08, 2026-09-03)
- **A CLI's default profile is production.** Other environments are named profiles. (2026-07-30)
- **Code layout.** Shared infrastructure sits under `pkg/`, one type per file, and OS-specific detail is hidden in a low-level package. (2026-06-28, 2026-06-29)
