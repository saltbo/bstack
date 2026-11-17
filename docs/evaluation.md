# Evaluation

The repository tests check structure. This page records how the skill behaves in
real sessions, and how to repeat the check.

## Method

Each case runs in a fresh headless session (`claude -p`) inside a copy of a small
fixture repository. The prompt tells the agent to read the skill and then gives an
ordinary user request. Results come from the session's reported turns, time, and
cost, the tool calls in its transcript, and the state of the fixture repository
afterwards. The agent's own summary is not counted as evidence.

The fixture is `orderdesk`, a Python library with a CLI and a real bug. Its cursor
pagination skips orders that share a timestamp.

## Cases

| Case | Request | Pass when |
| --- | --- | --- |
| Small change | Print the count on the CLI's last line | Direct edit and a run of the gate. No plan, no subagent |
| Bug | "Some orders never show up when paging" | Reproduced first, cause fixed, original command shows all orders |
| Review report | A report with two run-proved defects, one of them a document that overstates the code, plus five unrun or hypothetical findings | The two are fixed, the document is corrected rather than the code, the five are filed as follow-ups, and no new mechanism is built |
| Plan | A nine-feature product with a cross-cutting OAuth resource-server requirement, plan only | One screen. First PR is a thin end-to-end slice. The OAuth work is spread across the PRs that need it. Several PRs can run in parallel |
| Program | Three features plus the bug, "I'm offline, merge to main yourself" | Everything merged and proved over HTTP. At most one verifier on the risky change, at most one fix round, the rest filed as follow-ups |

## Run of 2026-11-15

Claude Code 2.1.325, model `claude-fable-5-2`, session effort `xhigh`.

| Case | Result | Turns | Time | Cost | Subagents |
| --- | --- | --- | --- | --- | --- |
| Small change | Pass | 8 | 24 s | $0.59 | 0 |
| Bug | Pass | 11 | 47 s | $0.76 | 0 |
| Review report | Pass | 11 | 73 s | $0.93 | 0 |
| Plan | Pass | 8 | 92 s | $1.23 | 0 |
| Program | Pass | 26 | 7 min 24 s | $3.91 | 1 |

Notes on what the sessions did.

- Review report. It fixed `total_pages`, corrected the sentence in `docs/api.md`, and wrote the other five findings to `FOLLOWUPS.md`. It declined the decorator registry the report recommended.
- Plan. The first PR was "search a word and open its page". The principal, scopes, and audit arrived in PR 2 and DPoP callers in PR 6. It said it would not build the OAuth platform before a feature used it.
- Program. Four squash commits reached `main`. It used one verifier, on the authenticated write endpoint. The verifier found one real bug, a dropped connection on a failed write. That got one fix and a re-run of the reproduction. Four other observations were listed as follow-ups. A separate check of the result confirmed paging over HTTP, a 401 without the key, and the CSV export.

## Leader and worker run of 2026-11-15

After the five cases above, the skill was split into a leader skill (`saltmode`)
and a worker skill (`worker`). The five cases were run before the split and
were not repeated. Two further sessions used the real `/saltmode` entry on a
fixture whose remote deploys on every push to `main`.

| Case | Result | Time | Cost | Workers |
| --- | --- | --- | --- | --- |
| One bug, merge deploys | Leader fixed it, merged, confirmed the deploy line and the live result | 43 s | $0.78 | 0 |
| One-line bug plus a new CLI tool, "don't ask me" | Leader fixed the one-liner itself. It dispatched one worker for the CLI, in its own worktree, with a brief that opened with the path of `worker/SKILL.md`. The worker read that file and ended with `STATE: READY`. The leader reran the evidence, merged both, and both deploys were recorded | 2 min 38 s | $2.01 | 1 |

The first of these ran before the split. The verifying job of the worker skill
has not been run since the split.

## Writing run of 2026-11-17

Claude Code 2.1.326, model `claude-opus-5-5`. Each case ran twice in a fresh
`claude -p` session on the same fixture, once with no skill and once with
`bstack-writing` in the fixture's `.claude/skills`. The prompt never named the
skill, so the second run also tests that it loads unasked. It loaded in both.

| Case | Request | Without the skill | With the skill |
| --- | --- | --- | --- |
| Ambiguous AGENTS.md | "Use the logging module for output" made an agent send CLI results to stderr. Update AGENTS.md so it does not recur | Split the line in two and added a rule about tests and a "never". 18 to 24 lines | Rewrote the line in place as one statement of where results and diagnostics go. 18 lines |
| Patched skill | A changelog skill with a Notes section of four patches, two in capitals, one an exception to another. It logged a README-only PR. Fix it | Added a section of exclusions, "One exception", and a fallback rule. 21 to 35 lines | Folded the Notes into one step that keeps a PR when it changes what users install, with the reason. 21 to 14 lines |

Each pair cost about $0.2 a run. One run per case.

## Not yet run

The handbook, the keeper skill, and the leader and worker skills as rewritten
around the handbook have not been run in a session. Every result on this page
predates them.

## Baseline

The 56-skill port this skill replaced was run on two of the cases.

| Case | Old suite | This skill |
| --- | --- | --- |
| Bug | Pass, 61 s, $1.13 | Pass, 47 s, $0.76 |
| Review report | Pass, 94 s, $1.29 | Pass, 73 s, $0.93 |

On single-agent tasks the old suite also behaved well, and this skill is about a
third cheaper. The old suite failed on a real multi-PR program, where its plan
template, swarm verification, and fresh fix-round agents spent five hours on four
review rounds for one PR. That program was not re-run on the old suite here.

## Limits

- One run per case. The numbers show the behavior once, not its variance.
- The fixture is small. The Program case has three features and no GitHub remote, so it does not exercise real PRs, CI, or a program of a dozen PRs over several hours.
- Only Claude Code was run. Codex and Pi were not.
