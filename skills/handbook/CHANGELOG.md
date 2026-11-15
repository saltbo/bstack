# Handbook changelog

Each entry is a claim to check later. `Source` is the session, PR, or issue that
showed the problem. `Saw` is what went wrong. `Expect` is what the new text should
produce. The keeper sets `Outcome` to `held` or `recurred` once later work has run
on that version.

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
- Outcome: pending
