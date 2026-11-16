---
id: pull-requests
version: 3
audience: leader, worker
applies: all
---

# Pull requests

## Decisions

### Commits

- A direct change, as [verification](../lifecycle/verification.md) defines it, is committed on trunk with no PR.
- Each PR has its own branch from trunk, which is `main`. Do not add unrelated changes to an existing PR. Use Conventional Commits, `type(scope): subject`, with no trailing period.
- A commit holds nothing a careful engineer would not have written, such as dead code, guards for states that cannot occur, and comments that restate the code. A comment stays only for a reason the code cannot show.
- A force-push is for your own branch only, and never overwrites someone else's commits.

### The PR

- Use `gh` unless the project uses another forge. Open the PR as a draft. Mark it ready only when CI is green and every acceptance criterion has been checked on the preview, per [verification](../lifecycle/verification.md). Ready is the handoff to the leader.
- Prefer several narrow PRs to one large PR. Link the PR to its issue and close the issue on merge.
- Keep the body under about 40 lines, because it becomes the squash commit body. Use these headings and drop one that has nothing to say.
  - `## Why` gives the problem and the approach in one to three sentences.
  - `## What changed` has one to three bullets.
  - `## Scope` says what the PR covers and what it leaves out on purpose.
  - `## Verification` lists each acceptance criterion with the preview evidence that showed it, as a screenshot or a command and its output.
  - `## Handbook` lists the handbooks the work followed, as `id@version`.

### Merge

The leader merges, or a worker whose brief says to.

- Merge when the PR passes [verification](../lifecycle/verification.md).
- Squash-merge. The PR counts as merged when the forge says it is, because a merge queue can accept the command without merging.
- After a merge, nothing of the PR is left behind. Its branch and its worktree are gone, locally and on the remote. A follow-up goes on a new branch.
- After a rebase, earlier proof still stands when the change itself is unchanged.

### CI and review bots

- Read the failing log before you retry. A failure in code the diff never touched usually means a stale base, so check that before you call it a flake. A real flake gets one rerun, and you report that it flaked.
- Check each comment from a review bot against the code. Fix the real ones and dismiss the rest with a one-line reason. A bot comment blocks the merge only when it meets the blocking rule in [verification](../lifecycle/verification.md).
