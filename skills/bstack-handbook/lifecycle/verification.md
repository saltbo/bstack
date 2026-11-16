---
id: verification
version: 4
audience: leader, worker
applies: all
---

# Verification

How a change is verified on its way from "built" to "merged", without the two sides arguing. Each check has one owner, one moment, and one way to pass. Only CI and the leader's acceptance can stop a merge.

| Check | Who | When | Passes when |
| --- | --- | --- | --- |
| Tests | The worker writes them, CI runs them | Every push | The project gate is green |
| Local proof | The worker | Before it opens the PR | The feature runs locally and every criterion was seen working |
| Preview proof | The worker | After CI is green | Every criterion was seen working on the preview, with the evidence in the PR |
| Acceptance | The leader | When the PR is marked ready | See "The leader's acceptance" |
| Second check | One verifier | Only for a high-risk change | It reports what it found. It has no vote |
| Live check | The leader | After a deploy | The changed behavior works in production |

## Decisions

- **The path is sized to the change's risk.** There are four paths, and the leader picks one before starting. (2026-11-15)
  - **Direct.** A small change that a plain revert undoes, such as wording, styling, a config value, or a doc. The leader makes it on trunk, runs the tests that cover it, commits, and pushes. There is no branch, PR, preview, scenario, or worker. After the push it watches CI and the deploy, and looks at the result once.
  - **Maintenance.** A change that alters no behavior but is too large to be direct, such as a refactor, a dependency upgrade, or a CI change. It goes through a PR and merges when the gate is green. It has no scenario. Its criteria are that the gate passes and that the behavior it touches still works on the preview.
  - **Standard.** A change in behavior. Everything in the table applies.
  - **High-risk.** A standard change that also gets the second check.
- **A change is direct only when all of these hold.** No scenario in `spec/` is affected. It touches no API contract, schema, migration, authentication, or stored data. A plain revert undoes it. It is small enough that the leader reads the whole diff before pushing. When in doubt it is standard. A repository that requires pull requests gets a PR for a direct change too, merged as soon as CI is green, with no preview proof. (2026-11-15)

- **The bar is written before the work starts.** The leader's brief carries a closed list of acceptance criteria, usually three to seven, each pointing at its scenario. Every check uses that list and nothing else. A bar discovered during review is what turns one review into four. (2026-11-15)
- **Every change in behavior starts as a scenario in `spec/`**, written by the leader in product language. A change that alters no behavior, such as a refactor or a config value, needs none. A project without `spec/` gets one for the area being changed, without backfilling the whole product first. (2026-06-27, 2026-11-15)
- **The leader writes the bar and the worker writes the tests.** The worker does not change a scenario's text or weaken an existing test. If one is wrong, it says so in its report and the leader decides. (2026-11-15)
- **A leader that builds a change itself does the worker's checks.** It proves every criterion locally and on the preview, and that walk stands in for the acceptance sample. A high-risk change it built still gets the second check. (2026-11-15)
- **The worker is exhaustive.** It proves every criterion locally, opens the PR as a draft, gets CI green, proves every criterion again on the preview, and only then marks the PR ready. Ready means exactly that, so the handoff is one visible event. (2026-11-15)
- **The leader's acceptance is a sample and a judgment, not a code review.** It does not read the whole diff. It checks four things. The changed files stay inside the brief. Every change in behavior has its scenario, and no test, spec file, or gate setting was weakened without a stated reason. Each new API and new table follows the [api](api.md) and [design](design.md) handbooks. Every criterion has preview evidence. Then it walks the main path of the feature on the preview once, or for an API sends one or two requests, and merges. (2026-11-15)
- **Code quality is held by the project's gate, not by reading.** A quality rule worth having is written as a check in CI. (2026-08-30, 2026-11-15)
- **A new API or a new table needs no approval.** It is the one part of the code the leader reads, and the report lists each one. (2026-11-15)
- **A project that can have a preview environment has one.** A web project can, and a Cloudflare Workers project always can. The project's `Handbook` block says where it is. A missing one is a gap, not an exemption, and for a web project the default is to build it as its own PR first. (2026-11-15)
- **Without a preview**, as for a command line tool or a client app, local proof stands in for preview proof, and the leader's sample is to build the artifact from the PR's commit and run the main path. (2026-11-15)
- **What blocks.** A finding stops a merge only when something run on the commit as written shows a criterion that does not hold, a bug a user of the change would hit, a failed project gate, or a document the change made false. When a document claims more than the code does, the fix is the document. (2026-11-15)
- **Everything else is a follow-up**, filed per [follow-ups](../policies/follow-ups.md). That covers a gap that needs code the change does not contain, anything read but not run, style, naming, and ideas. (2026-11-15)
- **Second check.** Use one verifier when the change touches authentication or authorization, money, persisted data or a migration, a public contract, or concurrency, or when Saltbo asks. It walks every criterion on the preview in place of the leader's sample and is asked which criteria do not hold, not to find problems. The leader still makes its four checks and decides. (2026-11-15)
- **Checking costs less than building.** When checking a PR has taken longer than building it, stop and rethink its size or its criteria. (2026-11-15)
- **A browser is driven with ego-browser**, in the test profile that the user-level agent instructions name. The shared test account is already signed in there, so a sign-in needs no credentials and no human check. (2026-11-15)
- **Proof is from a user's point of view**, through the real UI, CLI, or API with real data. It does not depend on reading the database or the source, and a timeout is never a pass. (2026-07-30)
- **Verification is not skipped.** A blocker met while proving is investigated and fixed. A skip is allowed only after several different attempts, and the report names what was skipped, why, and the evidence. (2026-05-05)
- **Normal flows.** Extreme edge cases are not part of acceptance unless the criteria name them. (2026-09-05)
- **A bug fix shows red, then green.** The report carries the new test's failing output before the fix and its passing output after. (2026-06-06)
- **The leader does the final acceptance of a whole program itself**, against real upstream services, not fakes. (2026-07-07, 2026-11-15)
- **Saltbo is not the tester.** Work is not handed back for him to try. (repeated since 2026-05)
- **Live check.** After a deploy, exercise the changed behavior on the live system once, per [deploy](deploy.md). A failure is handled per [operate](operate.md) and never reopens the PR. (2026-11-15)
- **A change to what users see does not wait for him.** Day-to-day UI and UX work follows the product's standard and style, and the PR carries screenshots. (2026-11-15)

## Defaults

- **One fix round.** It contains only the blocking findings, and the leader rechecks those once. If something still blocks, the leader cuts that part out, or merges with a follow-up when the finding does not meet the rule, or sets the PR aside, and says which. A further round is the departure, taken when the remaining fix is plainly cheaper than any of those. (2026-11-15)
- **A large new feature is split in two.** One worker builds. A second writes the end-to-end tests from the spec alone, without reading the implementation. They run in parallel and meet in CI. This needs the spec or the API contract to fix the interface first. (2026-11-15)

## Open

- When the project's end-to-end tests cover the scenarios, does the worker still walk every criterion by hand locally? Until decided, no. Locally the gate and the end-to-end tests prove the criteria. When the change alters what users see, the worker also looks at the pages it built and fixes what looks wrong, which stays required. The full walk under real sign-in happens once, on the preview. (Seen on bstack-playground PR 11, where the same five scenarios were walked four times.)
- Where do a PR's screenshots go? Until decided, they stay local, the worker's report lists their paths, and the PR says in words what was seen. No image host is set up for them.
