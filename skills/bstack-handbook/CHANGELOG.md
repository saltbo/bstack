# Handbook changelog

Each entry is a claim to check later. `Source` is the session, PR, or issue that
showed the problem. `Saw` is what went wrong. `Expect` is what the new text should
produce. `Outcome` is set to `held` or `recurred` once later work has run on that
version.

## all@1 (2026-11-15)

- Source: the Wordkith v1 session of 2026-11-15, which spent four review rounds on one PR and merged nothing.
- Saw: acceptance criteria were discovered during review, reviewers were asked to find problems, non-blocking findings entered fix rounds, and every fix restarted verification.
- Expect: criteria are fixed in the brief, acceptance is one decision on evidence, at most one fix round, and everything else is filed as a follow-up.
- Outcome: pending

## verification@2 (2026-11-15)

- Source: Saltbo, session of 2026-11-15, on the first playground task
- Saw: A one-line wording change was sent down the whole path of branch, draft PR, CI, preview proof, ready, and merge.
- Expect: A change that alters no behavior is made by the leader on trunk and pushed, with no branch, PR, preview, or worker.
- Outcome: held. On 2026-11-15 a title change on bstack-playground was committed on trunk with no branch or PR (commit 6ea8c7a), in 2 min 39 s against 10 min for a wording change on verification@1.

## pull-requests@2 (2026-11-15)

- Source: Saltbo, session of 2026-11-15, on the first playground task
- Saw: Every change, however small, required a pull request.
- Expect: A direct change is committed on trunk without a PR.
- Outcome: held. On 2026-11-15 a title change on bstack-playground was committed on trunk with no branch or PR (commit 6ea8c7a), in 2 min 39 s against 10 min for a wording change on verification@1.

## cf-workers@2 (2026-11-15)

- Source: bstack-playground PR 2 and issue 3, session of 2026-11-15
- Saw: The leader could not sign in on the preview, declined to touch the identity provider's settings because nobody asked for that, and proved the change on the preview only by reading the built bundle.
- Expect: A worker registers the preview's callback itself, signs in on the preview, and proves each criterion there.
- Outcome: held. On bstack-playground PR 6 the worker registered the preview's callback, signed in on the preview with a test account, and proved each criterion there.

## identity@2 (2026-11-15)

- Source: bstack-playground PR 6, session of 2026-11-15
- Saw: To sign in on a preview, the worker granted itself user, organization, and role-assignment scopes on the platform and made the test account a member of an organization that owns other private applications.
- Expect: A worker asks for the narrowest scopes, does not widen a test account's reach beyond the project, and reports when the task cannot be done inside that.
- Outcome: held. On 2026-11-15 the next leader on bstack-playground cited identity@2, removed the test account from the organization, and reported the grants that remained.

## agents@2 (2026-11-15)

- Source: Saltbo, session of 2026-11-15, after the second playground task cost 14 dollars
- Saw: Every worker and verifier ran on the leader's top-tier model.
- Expect: Workers, verifiers, and independent sessions start on Opus.
- Outcome: withdrawn in agents@3. It was not a decision of his.

## agents@3 (2026-11-15)

- Source: Saltbo, session of 2026-11-15
- Saw: agents@2 turned an instruction about one set of test runs into a standing decision and named a model in the handbook.
- Expect: The handbook names no model. agents@3 is agents@1 again.
- Outcome: pending

## Confirmation (2026-11-15)

Saltbo confirmed every entry under Decisions as it stood at this date, including those taken from his earlier sessions and from his older engineering references.

## follow-ups@2 (2026-11-15)

- Source: saltbo/bstack issue 7, from the bstack-playground PR 6 sessions
- Saw: The leader's session ended after the merge and nine follow-ups in the worker's report had not been filed.
- Expect: Follow-ups are filed before the merge.
- Outcome: pending

## identity@3 (2026-11-15)

- Source: saltbo/bstack issue 8, from the bstack-playground PR 6 sessions
- Saw: A test account could sign in to a private application only by joining its organization, which opened the organization's other applications to it.
- Expect: In a development project the application is made public and the account stays outside. In a live project the agent reports it.
- Outcome: pending

## identity@4 (2026-11-15)

- Source: Saltbo, session of 2026-11-15, confirmed as a standing decision
- Saw: Each project created its own test account. On bstack-playground that took a worker more than ten minutes and led it to grant itself user and organization write access.
- Expect: An agent signs in with the shared account and creates none.
- Outcome: pending

## project@2 (2026-11-15)

- Source: bstack-playground PR 11, session of 2026-11-15; confirmed by Saltbo
- Saw: The leader added a one-line project fact to a PR that was ready, and the PR waited 2 min 12 s for a second CI run before it could merge.
- Expect: An ADR or a project fact is committed on trunk after the merge, and a ready PR gets no new commits.
- Outcome: held on bstack-playground PR 21: the ADR was committed on trunk after the merge.

## verification@3 (2026-11-15)

- Source: Saltbo, session of 2026-11-15, and bstack-playground PR 11
- Saw: Each browser check signed in from scratch in headed Chrome, and the same five scenarios were walked by hand four times: locally, on the preview twice, and in production. A 34-minute task had 7 minutes of building.
- Expect: Browser checks use ego-browser in the test profile and sign in without credentials. The worker does not repeat by hand locally what the end-to-end tests prove, and still looks at the pages it changed.
- Outcome: pending

## skills@2 (2026-11-15)

- Source: Saltbo, session of 2026-11-15
- Saw: The index sent browser work to playwright-cli.
- Expect: Browser work uses ego-browser.
- Outcome: pending

## build@2 (2026-11-15)

- Source: bstack-playground PR 15, session of 2026-11-15; confirmed by Saltbo
- Saw: The leader read the project as development-stage and took that as a reason to do less. It kept the old error format for the new endpoints to stay consistent with existing code that disagrees with the api handbook, and skipped the second check on a change to authorization and stored data.
- Expect: In a development project the code a task touches is brought into line with the handbook, and no decision is skipped.
- Outcome: held on bstack-playground PR 21: the API was moved to the handbook format and the second check ran.

## api@2 (2026-11-15)

- Source: Saltbo, session of 2026-11-15, after bstack-playground PRs 11 and 15 kept the old error format
- Saw: The error rule was one sentence. It did not say what a type URI looks like, whether status is included, or how a validation pointer is formed, and a project file that asked for error codes was followed in its place.
- Expect: An API returns problem+json exactly as the example shows, with a type URI and no code field.
- Outcome: held on bstack-playground PR 21: every error is problem+json with a type URI and no code field.

## agents@4 (2026-11-15)

- Source: Saltbo, session of 2026-11-15; confirmed as a standing decision
- Saw: Leaders running in T3 Code dispatched workers with the harness's native subagents. Saltbo could not watch a worker, a worker always ran on the leader's model, and one leader ended its turn while a verifier was still running.
- Expect: In T3 Code a leader dispatches with delegate_task and the worker is a visible child thread. In Herdr it uses hc.
- Outcome: pending

## project@3 (2026-11-15)

- Source: bstack-playground issue 20, session of 2026-11-15; confirmed by Saltbo
- Saw: A leader wrote into the project's Handbook block that Workers Builds does not apply migrations. It was a guess and it was false.
- Expect: A fact is checked before it is written into the block, and an inferred one is labelled as inferred.
- Outcome: pending

## cf-workers@3 (2026-11-15)

- Source: bstack-playground PR 15 and saltbo/bstack issue 15; confirmed by Saltbo
- Saw: Cloudflare's compression weakened the ETag on the preview, so an edit sent with If-Match was rejected. Local tests did not show it.
- Expect: Responses with an ETag send Cache-Control: no-transform and If-Match works behind Cloudflare.
- Outcome: pending

## verification@4 (2026-11-15)

- Source: Saltbo, review session of 2026-11-15; asked for by him
- Saw: Every method entry was a Decision that could not be skipped, so the freedom saltmode gives was empty. A large change that alters no behavior had no path, and a two-line fix after the fix round had to be cut or set aside.
- Expect: The leader picks among four paths by risk, builds a small change itself with the worker's checks, and departs from a Default with one stated line.
- Outcome: pending

## agents@5 (2026-11-15)

- Source: Saltbo, review session of 2026-11-15; asked for by him
- Saw: Every change in behavior was dispatched to a worker, also a small one the leader already held the context for.
- Expect: The leader builds a small change itself and dispatches when the work is large, parallel, or deserves a second reader.
- Outcome: pending

## skills@3 (2026-11-15)

- Source: Saltbo, session of 2026-11-15; he moved his skills into the skills store and ego-browser dropped its skill
- Saw: The index sent agents to SKILL.md files in globally installed directories that no longer hold them, and to an ego-browser skill that no longer exists.
- Expect: An agent finds a skill with skills list, loads it with skills show, and reads the ego-browser and Herdr guides from the tools.
- Outcome: pending

## skills@4 (2026-11-15)

- Source: Saltbo, session of 2026-11-15
- Saw: skills@3 dropped the App Store Connect row because the asc skills were missing from the store.
- Expect: With the asc skills reinstalled, an agent doing App Store Connect work finds them through the index.
- Outcome: pending

## follow-ups@3 (2026-11-15)

- Source: Saltbo, session of 2026-11-15; confirmed by him; saltbo/bstack issue 14
- Saw: A missing Realmroot feature was filed in saltbo/bstack because a handbook entry mentioned the subject, although realmroot/realmroot issue 264 already tracked it.
- Expect: A product or tool problem is filed with that product, and saltbo/bstack receives only problems with handbook or skill text.
- Outcome: pending

## pull-requests@3 (2026-11-15)

- Source: Saltbo, session of 2026-11-15; confirmed by him; saltbo/bstack issue 9
- Saw: A merged PR's remote branch survived, and the entries around it named commands where they should name the outcome.
- Expect: After a merge the agent leaves no branch or worktree behind, by whatever means, and the entries state outcomes only.
- Outcome: pending

## api@3 (2026-11-15)

- Source: Saltbo, session of 2026-11-15; confirmed by him as the writing principle of the repository
- Saw: The entry gave the path checker's full invocation.
- Expect: The handbook names the checker and its profile and leaves the call to the agent.
- Outcome: pending

## skills@5 (2026-11-15)

- Source: Saltbo, session of 2026-11-15; confirmed by him as the writing principle of the repository
- Saw: The index spelled out the store's commands for each row.
- Expect: The index names what to load, and the agent loads it from the store.
- Outcome: pending

## design@2 (2026-11-15)

- Source: Saltbo, session of 2026-11-15; asked for by him
- Saw: The API handbook was named api.
- Expect: It is named openapi, with its version carried over as openapi@3, and this handbook links to it under that name.
- Outcome: pending

## verification@5 (2026-11-15)

- Source: Saltbo, session of 2026-11-15; asked for by him
- Saw: The API handbook was named api.
- Expect: It is named openapi, with its version carried over as openapi@3, and this handbook links to it under that name.
- Outcome: pending

## planning@2 (2026-11-16)

- Source: session 2026-11-16, PR #28
- Saw: Large plans were written into docs/plans in each repository and repeated in worker briefs and a trail file, while the tasks themselves already lived in docket
- Expect: A leader plans a large change as docket tasks under the project, posts them to Saltbo as one review card, and keeps their state in the task history
- Outcome: pending

## agents@6 (2026-11-17)

- Source: Saltbo, 2026-11-17: saltmode split into autopilot, bugfix, and xplan
- Saw: The entry named saltmode, which no longer exists
- Expect: Agents name xplan as the leader a session in another repository runs, and load autopilot, bugfix, and xplan from the store
- Outcome: pending

## skills@6 (2026-11-17)

- Source: Saltbo, 2026-11-17: saltmode split into autopilot, bugfix, and xplan
- Saw: The entry named saltmode, which no longer exists
- Expect: Agents name xplan as the leader a session in another repository runs, and load autopilot, bugfix, and xplan from the store
- Outcome: pending

## project@4 (2026-11-17)

- Source: Saltbo, 2026-11-17: asked that every description be stated positively
- Saw: Entries stated a rule, then corrected or restated it with a negative sentence
- Expect: Each entry states what holds, once and positively, with its meaning unchanged
- Outcome: pending

## planning@3 (2026-11-17)

- Source: Saltbo, 2026-11-17: asked that every description be stated positively
- Saw: Entries stated a rule, then corrected or restated it with a negative sentence
- Expect: Each entry states what holds, once and positively, with its meaning unchanged
- Outcome: pending

## verification@6 (2026-11-17)

- Source: Saltbo, 2026-11-17: asked that every description be stated positively
- Saw: Entries stated a rule, then corrected or restated it with a negative sentence
- Expect: Each entry states what holds, once and positively, with its meaning unchanged
- Outcome: pending

## deploy@2 (2026-11-17)

- Source: Saltbo, 2026-11-17: asked that every description be stated positively
- Saw: Entries stated a rule, then corrected or restated it with a negative sentence
- Expect: Each entry states what holds, once and positively, with its meaning unchanged
- Outcome: pending

## operate@2 (2026-11-17)

- Source: Saltbo, 2026-11-17: asked that every description be stated positively
- Saw: Entries stated a rule, then corrected or restated it with a negative sentence
- Expect: Each entry states what holds, once and positively, with its meaning unchanged
- Outcome: pending

## cf-workers@4 (2026-11-17)

- Source: Saltbo, 2026-11-17: asked that every description be stated positively
- Saw: Entries stated a rule, then corrected or restated it with a negative sentence
- Expect: Each entry states what holds, once and positively, with its meaning unchanged
- Outcome: pending

## follow-ups@4 (2026-11-17)

- Source: Saltbo, 2026-11-17: asked that every description be stated positively
- Saw: Entries stated a rule, then corrected or restated it with a negative sentence
- Expect: Each entry states what holds, once and positively, with its meaning unchanged
- Outcome: pending

## identity@5 (2026-11-17)

- Source: Saltbo, 2026-11-17: asked that every description be stated positively
- Saw: Entries stated a rule, then corrected or restated it with a negative sentence
- Expect: Each entry states what holds, once and positively, with its meaning unchanged
- Outcome: pending

## build@3 (2026-11-17)

- Source: Saltbo, 2026-11-17: asked that every description be stated positively
- Saw: Two entries contradicted each other: 'Smallest change that meets the criteria' and 'The most correct change, not the smallest'
- Expect: One entry: the most correct change within the criteria, with anything else as a follow-up and a refactor when the design is wrong for the task
- Outcome: pending

## agents@7 (2026-11-17)

- Source: Saltbo, 2026-11-17: the three leader skills start only by hand, except autopilot for a session in another repository
- Saw: A session in another repository was told to run xplan, so an agent started a skill the user starts by hand
- Expect: A session in another repository is started with autopilot, carrying the goal and acceptance criteria the first leader gives it
- Outcome: pending

## skills@7 (2026-11-17)

- Source: session 2026-11-17, Saltbo
- Saw: Agents revised Markdown and skills by appending sentences that patched earlier ones, so documents grew, contradicted themselves, and buried the rules that mattered.
- Expect: An agent writing or revising Markdown loads bstack-writing and rewrites the sentence at fault instead of adding a patch.
- Outcome: pending

## skills@8 (2026-11-17)

- Source: session 2026-11-17, Saltbo
- Saw: The bstack-writing row named prompts, so the skill read as covering briefs and system prompts that are not Markdown files.
- Expect: Agents load bstack-writing for Markdown files only.
- Outcome: pending

## follow-ups@5 (2026-11-17)

- Source: session 2026-11-17, Saltbo
- Saw: Issues in saltbo/bstack named a session or a PR loosely, so the keeper could not find the transcript that showed the problem.
- Expect: Every issue in saltbo/bstack carries the host and session ID, and the keeper reads it with session.py.
- Outcome: pending

## authority@2 (2026-11-17)

- Source: session 2026-11-17, Saltbo
- Saw: The handbook named a keeper role that no agent took: the maintenance skill was invisible to Claude Code and explicit-only, so problems were left for nobody.
- Expect: Any agent may propose a change to this file; only Saltbo applies one.
- Outcome: pending

## reporting@2 (2026-11-17)

- Source: session 2026-11-17, Saltbo
- Saw: Pending decisions were addressed to a keeper role that no agent took.
- Expect: Pending decisions are listed so that they can become handbook entries, by whichever agent maintains saltbo/bstack.
- Outcome: pending

## follow-ups@6 (2026-11-17)

- Source: session 2026-11-17, Saltbo
- Saw: The rule for issues in saltbo/bstack named a keeper role that no agent took.
- Expect: An issue carries the session ID so that whoever works on it can trace the problem through the transcript.
- Outcome: pending

## build@4 (2026-11-17)

- Source: session 2026-11-17, Saltbo
- Saw: build.md carried a general checklist for measuring performance, condensed from the port this system replaced: method a capable model already knows, and the last text that needed that port's MIT notice.
- Expect: build.md holds Saltbo's decisions only, and the repository carries no text derived from the port, and no notice for it.
- Outcome: pending

## agents@8 (2026-11-17)

- Source: session 2026-11-17, Saltbo
- Saw: Agents created branches and worktrees by hand, next to the repository and under codex/ and agent/ names, where the environment's delegation could have given them a working copy.
- Expect: Work takes the directory and branch the environment's tool gives it, and branches and worktrees are made by hand only where no tool gives them.
- Outcome: pending

## pull-requests@4 (2026-11-17)

- Source: session 2026-11-17, Saltbo
- Saw: Branches outlived their work: closed or dropped work, branches checked out to review or verify a PR, and local branches whose remote was deleted at merge. The rule covered only merges.
- Expect: Whatever an agent created by hand is gone when its work ends, however it ends; what an environment's tool created is left to that tool.
- Outcome: pending

## planning@4 (2026-11-26)

- Source: Saltbo, Edith's session of 2026-11-26, on zpan PR #622
- Saw: A contributor's sign-in language menu (PR #622) waited days for Saltbo's go because every new feature waited for him, and no project wrote down what its product is for.
- Expect: A feature inside a project's positioning is built and merged without asking him. Only a change of direction, such as a change to the positioning or to a global UX rule, waits for him.
- Outcome: pending

## project@5 (2026-11-26)

- Source: Saltbo, Edith's session of 2026-11-26, on zpan PR #622
- Saw: No project recorded its positioning, so an agent could not tell an expected feature from a change of direction, and no record had a place for the UX rules every page follows.
- Expect: Each project keeps its positioning at the top of spec/README.md, and a product with a UI keeps UX.md and DESIGN.md at its root; spec scenarios carry no screen mechanics.
- Outcome: pending

## frontend@2 (2026-11-26)

- Source: Saltbo, Edith's session of 2026-11-26, on zpan PR #622
- Saw: The written UI standard every product needed had no name or place, so neither zpan nor zpan-cloud had one, and a small UI change such as where a language menu goes had nothing to be judged against.
- Expect: A product's UI work follows its UX.md and DESIGN.md, with general practice from the UI skills, and a missing one is drafted rather than asked about change by change.
- Outcome: pending

## skills@9 (2026-11-26)

- Source: Saltbo, Edith's session of 2026-11-26, on zpan PR #622
- Saw: The installed UI skills, ui-ux-pro-max and web-design-guidelines, were not in the index, and ui-ux-pro-max writes its own design-system files that would duplicate DESIGN.md.
- Expect: UI work loads ui-ux-pro-max while building and web-design-guidelines before ready, and no design-system/ folder appears beside DESIGN.md.
- Outcome: pending

## backend@2 (2026-11-27)

- Source: Saltbo, session of 2026-11-27, reviewing the zpan schema
- Saw: The rule for which fields are real columns sat in backend, the only place any table design was written down.
- Expect: Schema rules have one home in database; backend keeps only how repositories are shaped.
- Outcome: pending

## design@3 (2026-11-27)

- Source: Saltbo, session of 2026-11-27, reviewing the zpan schema
- Saw: design named the area handbooks a design is judged by, and none covered a relational schema.
- Expect: A table design is judged by database alongside openapi, backend, and frontend.
- Outcome: pending

## verification@7 (2026-11-27)

- Source: Saltbo, session of 2026-11-27, reviewing the zpan schema
- Saw: The leader was told to check each new table against design, which has no rule about tables, so zpan's tables were accepted with three time units, path references, no foreign keys, and per-feature config tables.
- Expect: The leader checks each new table against database.
- Outcome: pending

## database@1 (2026-11-27)

- Source: Saltbo, session of 2026-11-27, reviewing the zpan schema
- Saw: No handbook said how a table is designed, so each zpan table followed the habit of the moment: seconds and milliseconds mixed in one table, folders referenced by path, foreign keys only on new tables, five ways to mark a delete, tenant ids copied into child tables, one config table per feature, and indexes nobody's query needed.
- Expect: A new table is named for its entity in the one word the code and API use, with no vendor or protocol in the name, and has UUIDv7 ids, UTC millisecond times, created_at, updated_at, and deleted_at with soft delete, foreign keys to ids, a tenant id only on top-level resources, one source per fact, reused shared structures, and an index only for a named query.
- Outcome: pending
