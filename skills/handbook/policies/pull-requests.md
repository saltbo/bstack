---
id: pull-requests
version: 2
audience: leader, worker
applies: all
---

# Pull requests

## Decisions

### Commits

- A direct change, as [verification](../lifecycle/verification.md) defines it, is committed on trunk with no PR.
- Each PR has its own branch from trunk, which is `main`. Do not add unrelated changes to an existing PR. Use Conventional Commits, `type(scope): subject`, with no trailing period.
- Before you commit, read your own diff once and remove what a careful engineer would not have written, such as dead code, guards for states that cannot occur, and comments that restate the code. Keep a comment only for a reason the code cannot show.
- Use `git push --force-with-lease` on your own branch. Do not force-push a branch someone else pushes to.

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
- After a merge, delete the branch and its worktree, locally and on the remote, and put any follow-up on a new branch.
- Squash-merge. Then read the PR back with `gh pr view <n> --json state,mergedAt`, because a merge queue can accept the command without merging.
- After a rebase, earlier proof still stands when `git patch-id` of the change is unchanged.

### CI and review bots

- Read the failing log before you retry. A failure in code the diff never touched usually means a stale base, so check that before you call it a flake. A real flake gets one rerun, and you report that it flaked.
- Check each comment from a review bot against the code. Fix the real ones and dismiss the rest with a one-line reason. A bot comment blocks the merge only when it meets the blocking rule in [verification](../lifecycle/verification.md).
