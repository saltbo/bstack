---
id: design
version: 2
audience: worker
applies: all
---

# Design

Principles that hold for any design. The conventions for each area are in [openapi](openapi.md), [backend](backend.md), and [frontend](frontend.md).

## Decisions

- **Design for the end state.** Do not justify a design with "for now", and do not ship a cut-down "V1". (2026-08-28)
- **Keep it simple.** Fewer tables, fields, options, and abstractions. Do not add complexity for rare cases or for needs nobody has stated. Leave a manual exit for the rare case. (repeated)
- **Standards over custom.** Integrate through standard protocols such as OIDC and OAuth exactly as specified. API rules rest on RFCs, not habit. (2026-08-02)
- **Get the data model right first.** A flawed base makes everything built on it need rework. (2026-10-19)
