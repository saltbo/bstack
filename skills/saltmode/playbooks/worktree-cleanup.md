### Worktree and simulator cleanup

1. Snapshot and audit. Record `df -h /`, then list worktrees with `git worktree list --porcelain` (never hand-typed paths). For each, record branch, merge state against the PR base (`git branch --merged origin/<base>` or the forge's PR state), tracked uncommitted edits (`wip:N`), untracked files (`scratch:N`), and last commit time. Bucket each as `safe` (merged, clean), `verify-recent` (touched recently), or `hold` (wip or unmerged).
2. The bucket is advice, not permission. Worktrees the user says are in use are the real artifact (principle-prove-it-works). Get that set from the user and cross-check every candidate; the in-use set wins over the bucket.
3. Verify usage before deleting. For every `verify-recent` row, or anything you doubt, check for running processes in the path (`lsof +D <path>`), an active agent session using it, and recent edits. Arena and repro trees spawned by an ongoing task are in use even when merged-looking.
4. Pause on irreversible loss. `wip:N` is N tracked uncommitted edits. Show the diff and get a decision first, since removing a clean worktree is recoverable from its branch but uncommitted work is gone. `scratch:N` is untracked throwaway, safe to drop, but name the files. Per Autonomy, clean and merged and not-in-use proceeds. `wip` and in-use pause.
5. Prune the confirmed set. Per path, `git worktree remove --force <path>`. If the dir survives on ignored build artifacts, `rm -rf` it, then `git worktree prune`. Branch refs survive, so no commits are lost. Confirm with `df -h /` and re-list.
6. Simulators and other reclaimers. Simulators are usually the next-biggest win. `xcrun simctl --set testing delete all` (XCTestDevices clones), `xcrun simctl delete unavailable`, and `xcrun simctl runtime list` then `runtime delete <id>` for old runtimes. More when needed: Xcode `DerivedData` and `iOS DeviceSupport`.

This is the one playbook that deletes user state with no code review to catch a slip, so the gates above are the review.

**Reply:** `df -h /` before and after with space reclaimed, the worktrees pruned, and a one-line reason for each held back (in-use by which chat, or uncommitted work).
