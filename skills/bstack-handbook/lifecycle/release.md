---
id: release
version: 1
audience: leader
applies: artifacts others install
---

# Release

Releasing means handing an artifact to someone else, such as an app to a store, an image to a registry, or a binary to a package manager.

## Decisions

- **Artifacts go to their official channel, under the product's organization.** SDKs to npm or PyPI, binaries as prebuilt downloads, not source builds and not release attachments. (2026-08-14, 2026-09-03)
- **An agent may cut a tag when the work needs a release.** After tagging, check that the published artifact installs and runs. (2026-07-20, 2026-09-03)
- **A fix needed in a dependency is made there, tagged, and then picked up**, not patched locally in the consumer. (2026-07-01)
- **Public legal pages ship final, not as drafts.** (2026-09-08)
- **A store submission waits for him.** Builds reach TestFlight automatically, and he decides when one is submitted for review. (2026-11-15)

## Open

- Does a public image or package push wait for Saltbo? Until decided, no when the project's pipeline does it on a tag, and yes for a first-ever publication.
