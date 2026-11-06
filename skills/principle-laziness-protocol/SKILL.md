---
name: principle-laziness-protocol
description: Apply when refactoring, evaluating diff size, or tempted to add abstractions,
  layers, or signal threading. Bias toward deletion and the smallest change that solves
  the problem.
disable-model-invocation: true
---


# Laziness Protocol

Read the [host adapter](../saltmode/references/host-adapter.md) once per session before
following this skill. It maps upstream Cursor-specific tool, model, path, and
permission instructions to your host and sets authority limits.


- **Consolidate decisions.** Do not repeat the same choice in several places. Put it behind one source of truth and pass the result as a simple flag.
- **Minimize the diff.** Make the smallest change that solves the problem. Fewer lines beat "elegant" boilerplate.
