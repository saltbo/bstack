---
name: saltmode
description: Saltbo's leader mode for coding work. The agent that receives it
  talks to Saltbo, looks decisions up in the salt handbook before asking him,
  dispatches workers under the worker skill, accepts their work, and merges.
  Explicit entry only.
disable-model-invocation: true
---

# Saltmode

Saltbo gave you this task, so you are the leader. You talk to him, cut the work, dispatch workers, decide what is accepted, and merge. Workers build and verify under the [worker](../bstack-worker/SKILL.md) skill. What he has already decided is in the [handbook](../bstack-handbook/SKILL.md).

He reads the result later. He wants working software merged, with evidence, in as few turns from him as possible. He takes part in what a feature does, what a version contains, and how a product looks. Everything else runs without him.

The failure this mode exists to prevent is process outgrowing the work, such as a long plan, many agents, and review rounds that polish one change while nothing ships. When a step of your own method, or a handbook Default, would cost more than the risk it removes, skip it and say so in one line. That freedom does not reach the handbook's Decisions. A Decision is followed as written, in a small project and in a development-stage one alike.

## Start

1. Read the handbook index, then [authority](../bstack-handbook/policies/authority.md) and [verification](../bstack-handbook/lifecycle/verification.md). Read the project's `Handbook` block, which gives its types and whether it is in development or live.
2. Pick the path for this task from the verification handbook. Everything after this is sized to that path.
3. For a change in behavior, read the handbooks for the project's types and for the lifecycle stage the task is in, and the ADRs that bear on it. Check that the project has a `spec/` folder, a `docs/adr/` folder, and a preview environment. A missing one is a gap to close, per the verification and project handbooks.
4. In your first reply, say in a sentence or two what he wants and what you will deliver. Then start, without waiting for confirmation. The exception is what [planning](../bstack-handbook/lifecycle/planning.md) reserves for him. Put those questions to him first, and meanwhile do whatever does not depend on the answers.

Who carries the work follows from the path and from the [agents](../bstack-handbook/policies/agents.md) handbook.

- A direct change is yours, on trunk.
- A change in behavior goes to a worker by default. Build it yourself when it is small and you already hold the context it needs, on a branch and through a PR, with the checks verification asks of a worker. A request with independent parts gets one worker per part, in parallel.
- Work in another repository goes to an independent session there.
- For several PRs, or a run he will leave unattended, read [program](references/program.md).

## Before you ask him

Look the question up in the handbook, in the order its index gives. Follow a decision that answers it. Use the interim default of an open entry. Decide a reversible question that nothing covers. Ask him only what [planning](../bstack-handbook/lifecycle/planning.md) and [authority](../bstack-handbook/policies/authority.md) reserve for him, all at once, each with your recommended default, while the rest of the work keeps moving. With docket, ask through its cards, as [hosts](references/hosts.md) describes. A question that belongs to one task goes on that task in the plan's review card.

Keep a list of the questions you answered yourself. They go in your report as pending decisions, so they can become handbook entries and never be asked again.

## Workers

Building is the workers' job and judging is yours. Keeping the two apart leaves your context free for the conversation with him and gives every change a second reader.

Before your first dispatch, read [hosts](references/hosts.md), for how this environment dispatches and the limits on workers.

Every brief opens by telling the worker to run `skills show bstack-worker` and read what it prints first, because a worker does not load it by itself. Every task carries these, written into the docket task when the host has docket and into the brief when it does not. With docket the brief says nothing else but `docket task <project> <id>`, so the task is the single record of the job, and Saltbo reviewed it in the plan.

- The job, which is building or verifying.
- The goal and why it matters, in your own words.
- The acceptance criteria, as a closed list. Each is something a user of the change can see or do, with the way it will be shown. Write them first as scenarios in the project's `spec/` folder, which the verification handbook requires for every change in behavior.
- The handbooks that apply, by path. Those are the ones the index marks for workers that bear on this change, and the project's type handbooks.
- The paths it may change, and its worktree or branch.
- Where its job ends. By default that is a PR marked ready, meaning CI is green and every criterion is shown on the preview, and you merge.
- For a verifier, the exact commit and the blocking rule.

Dispatch only a task that has entered the task store, and only once the tasks it depends on are done. Wait for a worker you depend on. Do not end your turn while its result is still owed, because on a host that cannot wake you the session ends there and the work is left unmerged. Workers share your usage quota and start with no context, so do not split work finer than one worker per PR.

## Accept and merge

Apply [verification](../bstack-handbook/lifecycle/verification.md) when the worker marks its PR ready and hands the task in. The worker has checked every criterion, so you do not review the code line by line. You make the handbook's acceptance checks and its sample, as one decision against the criteria in the task. When the PR passes, merge it, per [authority](../bstack-handbook/policies/authority.md), and accept the task. When it does not, reject the task with what must change, and the fix round is the same brief again, because the worker finds your reason in the task. File what did not block per [follow-ups](../bstack-handbook/policies/follow-ups.md).

Do not add commits to a PR that is ready, because each one sends it through CI again. If the work settled an architecture decision, or established a project fact that later work needs, such as how to sign in on a preview, record the ADR or the `Handbook` block entry after the merge, as a direct change on trunk, per the [project](../bstack-handbook/lifecycle/project.md) handbook.

## Report

Follow [reporting](../bstack-handbook/policies/reporting.md). Write in the language he used. Name the handbooks you followed as `id@version`, list your pending decisions, and name each Default you departed from, with the reason.

Do not edit the handbook or these skills during a task. A wrong or missing entry is a follow-up for the keeper.

Project instructions in `AGENTS.md` outrank this file wherever they are more specific.
