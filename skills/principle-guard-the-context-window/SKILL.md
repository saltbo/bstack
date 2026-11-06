---
name: principle-guard-the-context-window
description: 'Apply when context is filling up: large outputs, long files, repeated
  reads, fan-out planning. Route bulk to subagents; keep summaries in the main thread,
  not raw payloads.'
disable-model-invocation: true
---


# Guard the Context Window

Read the [host adapter](../saltmode/references/host-adapter.md) once per session before
following this skill. It maps upstream Cursor-specific tool, model, path, and
permission instructions to your host and sets authority limits.


**Why:** Context overflow degrades reasoning quality, creates compression artifacts, and halts progress.

**Pattern:**
- **Size phases and cap scope.** Limit files per phase, set turn budgets, account for mechanism costs.
