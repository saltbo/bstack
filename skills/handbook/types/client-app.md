---
id: client-app
version: 1
audience: leader, worker
applies: projects that declare this type
---

# Client app

Typical stack: Flutter or native iOS, shipped through a store. A project of this type follows [release](../lifecycle/release.md) and [versioning](../lifecycle/versioning.md). This file holds what is specific to the type.

## Decisions

- **Anything likely to change is server-side config**, such as pricing, quotas, and fallback addresses, so a change needs no new release. (2026-09-17)
- **Build numbers rise automatically on every build**, and a release build comes from a version tag. Encryption use is declared in `Info.plist`. (2025-11-19, 2025-12-14)
- **During interactive UI tuning, show every change live** with hot reload and leave tests for afterwards. When he approves, write the behavior into the spec and add the tests. A UI preview may mock data only. (2026-09-06, 2026-09-07)
- **One implementation, at most two layouts**, desktop and mobile. (2026-07-16)
- **Agents never operate his own physical phone.** (2026-09-24)
- **Every finished task's build goes to TestFlight automatically.** Submitting to store review is his decision for now. (2026-11-15)

## Open

- How do build and version numbers advance? Until decided, per [versioning](../lifecycle/versioning.md), with the build number from CI.
- Who owns screenshots and store metadata? Until decided, the agent prepares them and the PR shows them.
