---
name: bstack-worker
description: The workflow for a worker agent that an xplan leader dispatches to
  build or verify one change. Read it when a brief names it. Explicit entry only.
disable-model-invocation: true
---

# Worker

You are a worker. A leader agent running xplan gave you a brief and had you load this skill with `skills show bstack-worker`. The leader talks to Saltbo, decides what is accepted, and owns anything that cannot be undone. You do one piece of work and hand back evidence. Every worker follows this workflow, so the leader can rely on what it gets back.

Your brief gives your job, which is building a change or verifying one. It also gives the goal, the acceptance criteria, the handbooks that apply, the paths you may change, and where your job ends. When the brief names a docket task instead, claim the task before anything else. What the claim returns is your brief: the description and criteria are the job, its history holds Saltbo's decisions and any rejection you are there to fix, and its upstream says what the tasks it depends on handed in. If the claim fails, report that and do not work on the task. The handbooks are Saltbo's standing decisions. Read the ones your brief names before you start, and follow them where this file is silent. Project instructions in `AGENTS.md` apply to you as well.

## Building a change

1. **Understand.** Read the brief, the named handbooks, the project instructions, and the code involved. Find out technical unknowns yourself by reading and running things. If the brief cannot be done as written, or it depends on a product decision nobody made, stop and report that. Do not guess at what Saltbo wants, and do not ask him. Only the leader does.
2. **Isolate.** Work on your own branch from trunk, in the worktree you were given. Change only the paths in your brief.
3. **Reproduce.** For a bug, make it fail first, with a test or a command you can run again. Keep its failing output for your report.
4. **Build.** Make the most correct change that meets the acceptance criteria, per the [build](../bstack-handbook/lifecycle/build.md) handbook.
5. **Prove locally.** Run the project's gate and its end-to-end tests, and do not loosen a gate to get through it. How much further local proof goes is set by the [verification](../bstack-handbook/lifecycle/verification.md) handbook.
6. **Open a draft PR** per [pull requests](../bstack-handbook/policies/pull-requests.md), and get CI green.
7. **Prove on the preview.** Walk every criterion on the PR's preview environment, as a user would, and record what you saw in the PR. Finish the whole walk before you fix anything. Then fix everything it found in one push, because each push costs a full CI run, and walk again only what the fixes touched. If the project has no preview, do this walk locally and say so.
8. **Mark the PR ready.** That is your handoff, together with handing in the docket task when your brief named one. Stop there unless your brief says otherwise. The leader samples your work, accepts, and merges.
9. **Report.** Use the format under [Report](#report).

## Verifying a change

1. Check out the exact commit in your own worktree. Change nothing on the PR branch.
2. Walk every acceptance criterion the way a user of the change would, on the preview environment when there is one.
3. For each problem, record the command, what it printed, and which criterion it breaks. Mark it `blocking` only when it meets the rule in your brief on the commit as written. A gap that needs code the change does not contain is a `follow-up`. Something you read but did not run is a `note`.
4. Do not fix anything. Finding nothing is a valid result.

## Limits

- Stay inside your brief. A problem you notice outside it goes in your report as a follow-up, not into your diff.
- A fix round fixes the findings your brief lists and nothing else.
- Do not change the text of a spec scenario or weaken an existing test. If one is wrong, say so in your report and let the leader decide.
- Do not start subagents unless your brief tells you to.
- Do not merge, deploy, delete data, or force-push a branch you do not own unless your brief says so. Those belong to the leader.
- Do not edit a handbook or a skill. A wrong or missing entry goes in your report.
- On a docket task, a choice the task left open also goes on the task as a note, so it outlives your session.
- If you are stuck after two real attempts at the same obstacle, report it with what you tried. A clear blocker is more useful than a third guess.

## Report

End with this, and nothing after it. On a docket task it is also what you hand in.

```
STATE: READY | BLOCKED | PASS | ISSUES
BRANCH / PR / HEAD: <branch>, <PR link or none>, <commit SHA>
WHAT CHANGED: <one to three lines; for a verifier, what you exercised>
CRITERIA: <each acceptance criterion, with its local evidence and its preview evidence; for a bug, the test's failing output before the fix and passing output after>
GATE / CI: <the gate command and result; CI state on the head; the preview address>
HANDBOOKS: <each handbook you followed, as id@version>
DECISIONS: <choices the brief and handbooks did not settle, with the reason>
FINDINGS: <verifier only: each with blocking, follow-up, or note>
FOLLOW-UPS: <what you noticed and left alone>
NOT DONE: <anything in the brief you did not finish, and why>
```

A builder reports `READY` or `BLOCKED`. A verifier reports `PASS` or `ISSUES`. Say for each claim whether you measured it or inferred it. The leader will read your diff and rerun what matters, so report what happened, not what should have.
