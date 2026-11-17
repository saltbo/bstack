---
name: bstack-handbook
description: Saltbo's handbook. Versioned decisions that agents follow instead of
  asking him, by lifecycle stage and project type, with an index of specialist
  skills. Read by autopilot, bugfix, xplan, worker, and keeper. Explicit entry only.
disable-model-invocation: true
---

# Handbook

Each handbook records what Saltbo has already decided for one kind of situation, so an agent can act without asking him again. A handbook states decisions and their reasons. It does not teach method, which the agent already knows.

## Look here before asking

When you are about to ask Saltbo something, look it up first, in this order.

1. The project's exceptions, in its `AGENTS.md`.
2. The handbook for the project's type.
3. The lifecycle handbooks for the stage you are in.
4. The policy handbooks.

If a **Decisions** entry answers it, follow it and do not ask. A decision is not skipped because a step looks costly or the project is small. The only way to depart from one is an entry under `Exceptions` in the project's `Handbook` block, with its reason. If a **Defaults** entry covers it, do that, unless in this case it would cost more than the risk it removes. Then do what fits and say so in one line of your report, naming the entry. If an **Open** entry covers it, use the interim default it gives, and list the question under "pending" in your report. If nothing covers it, decide the reversible ones yourself and list them as pending. Ask him only what [planning](lifecycle/planning.md) and [authority](policies/authority.md) reserve for him.

Cite what you followed as `id@version`, for example `verification@1`, in your report and in the PR. That is how a later reader tells which text produced a decision.

Do not edit a handbook during a task. A task runs on one version from start to finish. Report a gap or a wrong entry per [follow-ups](policies/follow-ups.md), and the keeper revises it afterwards.

## Handbooks

<!-- index:start -->
| Handbook | Version | For | Applies to |
| --- | --- | --- | --- |
| [project](lifecycle/project.md) | 3 | leader | all |
| [planning](lifecycle/planning.md) | 1 | leader | all |
| [design](lifecycle/design.md) | 2 | worker | all |
| [openapi](lifecycle/openapi.md) | 3 | worker | projects with an HTTP API |
| [backend](lifecycle/backend.md) | 1 | worker | projects with a backend |
| [frontend](lifecycle/frontend.md) | 1 | worker | projects with a web frontend |
| [build](lifecycle/build.md) | 2 | worker | all |
| [testing](lifecycle/testing.md) | 1 | worker | all |
| [verification](lifecycle/verification.md) | 5 | leader, worker | all |
| [versioning](lifecycle/versioning.md) | 1 | leader, worker | all |
| [deploy](lifecycle/deploy.md) | 1 | leader | services we run |
| [release](lifecycle/release.md) | 1 | leader | artifacts others install |
| [operate](lifecycle/operate.md) | 1 | leader | all |
| [docker-service](types/docker-service.md) | 1 | leader, worker | projects that declare this type |
| [client-app](types/client-app.md) | 1 | leader, worker | projects that declare this type |
| [cf-workers](types/cf-workers.md) | 3 | leader, worker | projects that declare this type |
| [go-cli](types/go-cli.md) | 1 | leader, worker | projects that declare this type |
| [authority](policies/authority.md) | 1 | leader | all |
| [resources](policies/resources.md) | 1 | leader | all |
| [follow-ups](policies/follow-ups.md) | 3 | leader, worker | all |
| [identity](policies/identity.md) | 4 | leader, worker | all |
| [reporting](policies/reporting.md) | 1 | leader | all |
| [pull-requests](policies/pull-requests.md) | 3 | leader, worker | all |
| [skills](policies/skills.md) | 6 | leader, worker | all |
| [agents](policies/agents.md) | 6 | leader | all |
<!-- index:end -->

## What a project declares

A project's instructions file carries facts, not rules.

```
## Handbook
Types: cf-workers, docker-service
Stage: live
Facts: production https://example.com; D1 database example-prod
Preview: each PR gets https://<branch>.example.workers.dev (or: none, and why)
Exceptions: none
```

`Types` selects the type handbooks. `Stage` is `development` when nothing is released and nobody depends on the project, and `live` once real users do. Development means there is no history to preserve, so whatever is wrong is changed to the right shape directly. It does not lower any standard: design and verification ask the same of both stages. Live means real users depend on what exists, so a change to it is planned and migrated. `Facts` are names, addresses, and identifiers. `Preview` says where a PR's preview environment appears, or that there is none. An exception names the handbook entry it departs from and gives the reason.

## What an entry looks like

An entry says what has to be true or what to do, never how to do it. It names the outcome and leaves the commands and steps to the agent. A **Decisions** entry is a bold one-line rule, its reason where it needs one, and the date Saltbo said it. A **Defaults** entry has the same form and records his usual way of working, which an agent may depart from with a stated reason. Standards, authority, and anything that guards against an irreversible mistake are Decisions, not Defaults. An **Open** entry is a question Saltbo has not answered, followed by the default to use until he does.

## Changing a handbook

Only the keeper changes handbooks, in the `saltbo/bstack` repository where the keeper skill lives, and only Saltbo changes one marked `owner-only`. An entry becomes a Decision only after he has confirmed it as one. Every change goes through `scripts/handbook.py`, which raises the version and adds a [changelog](CHANGELOG.md) entry saying what was seen and what the change should produce.
