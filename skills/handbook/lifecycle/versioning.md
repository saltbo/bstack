---
id: versioning
version: 1
audience: leader, worker
applies: all
---

# Versioning

## Decisions

- **Semantic versioning.** A release is a git tag, and the version the program reports matches the tag. A released binary also reports its commit. (2026-06-08)
- **A breaking change is measured against the last released version**, not against unreleased code. A project with no real users takes breaking changes without a major bump. (2026-08-02, 2026-08-22)
- **Releasing takes a version number and a tag, nothing else.** The pipeline updates version files and publishes matching artifacts. (2026-05-26)
- **Patch releases of a released line go on its release branch**, such as `2.8.x`. Trunk carries the next minor. Plans and labels are by minor version. (2026-08-03)
- **Minor and major versions follow the roadmap.** A version ships when its planned scope is merged. (2026-11-15)
- **Fixes ship soon, but not one release per task.** (2026-11-15)

## Open

- What cuts a patch release? Until decided, whoever finishes a task cuts one when trunk holds unreleased fixes and the last release is more than six hours old, and a fix for a live incident is released at once. A scheduled maintainer for each repository is expected to take this over.
- Is there a changelog, and who is it written for? Until decided, release notes generated from Conventional Commits.
