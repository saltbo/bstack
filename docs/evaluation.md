# Evaluation

The repository tests check structure. This page says how to check behavior, and records what real sessions did.

## Method

Both kinds of run use bstack as it is in the checkout, and both count only what the session did and left behind. The agent's own summary is not evidence.

- **Skill evals**, in `evals/`, check one skill. Each case runs in fresh sessions with bstack loaded and without it, three times by default, and the score is the difference. Run them with `claude plugin eval . --scaffold --trust-plugin --allow-tools Edit Write`. `.claude-plugin/plugin.json` exists so that the command can load `skills/`.
- **End-to-end cases**, in `e2e/`, check the system. Each is one real session, started with `python3 e2e/run.py [case]`, that does the whole job on a local stand-in for GitHub and Cloudflare in `e2e/sim/`, so a run takes minutes instead of the half hour the real services take.
  - The session starts in a clone of a fixture repository from `e2e/fixtures/`, with its dependencies installed and its remote at `https://github.com/saltbo/<name>`. `git` and `gh` reach the stand-in's GitHub. A push runs the repository's workflow as its checks, and in a Workers project it deploys the branch to a preview, announced on its PR as Workers Builds does, or `main` to production, on the local Workers runtime under `*.localhost`. `wrangler` acts on that Cloudflare.
  - It has this checkout's skills, installed and pinned as on Saltbo's machine, and none of his own skills, instructions, MCP servers, or credentials. Browser checks use ego-browser in task spaces of the session's own, and the runner closes any it leaves open. A case that needs docket gets a docket of its own, and a simulated user answers its cards and the session's questions, from the case's `user.md` when it has one.
  - One run holds the machine at a time, because sessions pick local ports for their own dev servers, and two at once reached each other's.
  - The case's `check.sh` judges the outcome against the stand-in's state. The keeper's [session script](../.agents/skills/keeper/scripts/session.py) reports on the transcript: the skills and handbooks it read, its failed calls, the errors it hit more than once, its questions, and its cost. The stand-in's `calls.log` lists every `gh` and `wrangler` call, and a call it did not understand counts as a gap in the stand-in, not in the skills.
  - Nothing outlives the run but its results. Its transcript is moved out of `~/.claude/projects`, and a fingerprint of the user's skills, git, gh, and docket configuration taken before and after reports any change as a leak.

Results land under `evals/results/` and `e2e/results/`, which are not committed. A run worth keeping is summarized below.

## Cases

| Case | Kind | Request | Pass when |
| --- | --- | --- | --- |
| `writing-agents-md` | eval, e2e | "Use the logging module for output" sent CLI results to stderr. Fix AGENTS.md | The line is rewritten in place, with no patch words, and the file does not grow |
| `writing-patched-skill` | eval | A changelog skill with four patches in a Notes section logged a README-only PR. Fix it | The rule is stated once, with its reason, and the file does not grow |
| `writing-not-markdown` | eval | Rename a field in Python code | `bstack-writing` does not load |
| `bugfix-paging` | e2e | "Some orders never show up when I page", under bugfix | A merged PR with green CI put the fix on `main`, every order is listed, no branch or PR is left |
| `feature-notes` | e2e | Add deleting a note to a Workers app, under autopilot | A merged PR with green CI and a preview, delete works in production, a scenario covers it, nothing is left |
| `xplan-notes` | e2e | Tags and search for the same app, under xplan, with a simulated user | Two or more merged PRs, each with green CI and a preview, both live, every docket task done |

## Run of 2026-11-15

These cases ran by hand on a fixture that is no longer kept. `bugfix-paging` carries its bug forward.

| Case | Request | Pass when |
| --- | --- | --- |
| Small change | Print the count on the CLI's last line | Direct edit and a run of the gate. No plan, no subagent |
| Bug | "Some orders never show up when paging" | Reproduced first, cause fixed, original command shows all orders |
| Review report | A report with two run-proved defects, one of them a document that overstates the code, plus five unrun or hypothetical findings | The two are fixed, the document is corrected rather than the code, the five are filed as follow-ups, and no new mechanism is built |
| Plan | A nine-feature product with a cross-cutting OAuth resource-server requirement, plan only | One screen. First PR is a thin end-to-end slice. The OAuth work is spread across the PRs that need it. Several PRs can run in parallel |
| Program | Three features plus the bug, "I'm offline, merge to main yourself" | Everything merged and proved over HTTP. At most one verifier on the risky change, at most one fix round, the rest filed as follow-ups |

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

## Eval and end-to-end run of 2026-11-17

Claude Code 2.1.326, model `claude-opus-5-5`, one run per arm.

| Case | Kind | With bstack | Without | Notes |
| --- | --- | --- | --- | --- |
| `writing-agents-md` | eval | 1.00 | 0.00 | Without it, the agent kept a "never" and failed the judge |
| `writing-patched-skill` | eval | 1.00 | 0.50 | Without it, the patches stayed beside a new exclusion |
| `writing-not-markdown` | eval | 1.00 | 1.00 | The skill stayed out of a code-only change |
| `writing-agents-md` | e2e | Pass, 12 s, $0.15 | | Loaded unasked, one line rewritten, 18 lines kept |
| `bugfix-paging` | e2e | Pass, 47 s, $0.41 | | Reproduced, fixed, squash-merged and pushed to `main`. It read the handbook before acting and asked nothing. It reported as pending that no handbook entry says which commit email the agent identity uses |

## End-to-end run on the stand-in, 2026-11-17

Claude Code 2.1.326, model `claude-opus-5-5`, one run per case, one case at a time. The same work on the real GitHub and Cloudflare took half an hour or more per PR.

| Case | Result | Time | Cost | Notes |
| --- | --- | --- | --- | --- |
| `writing-agents-md` | Pass | 22 s | $0.12 | One line rewritten in place |
| `bugfix-paging` | Pass | 85 s | $0.41 | Reproduced, fixed, draft PR, green CI, squash-merged, branch deleted, asked nothing |
| `feature-notes` | Pass | 394 s | $1.54 | Delete through a PR with green CI and a preview, proved in ego-browser on the preview, live in production. About 240 s of it was the model, 4 s the browser, under 20 s the stand-in |
| `xplan-notes` | Pass | 872 s | $4.92 | One question round answered by the simulated user, one review card approved, three tasks to three workers, three PRs merged with green CI and previews, every docket task done |

What the runs showed about the skills, for the keeper:

- xplan's worker filed its follow-ups after the merge, where the worker skill asks for them first.
- A worker in a Claude Code worktree had compound git commands refused by the harness several times, and split them.
- Before ego-browser was exposed, sessions used another browser tool that hung for minutes, or fell back to HTTP proof.
- `sed -i ''` failed on GNU sed in two sessions, as it did for the author of these cases.

## Not yet run

The keeper has no case yet.

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

- The recorded runs are one per case. They show the behavior once, not its variance, which the evals measure when run three times or more.
- The fixtures are small, and the stand-in covers the `gh` and `wrangler` commands and the Workers Builds behavior that the skills use, not all of GitHub and Cloudflare. It has no review bot unless a case configures one, and no browser sign-in.
- The session runs with the user's own home directory, because Claude Code reads its sign-in from there. The leak check is what shows that it changed nothing of his.
- Only Claude Code was run, and the session script reads only Claude Code transcripts. Codex and Pi were not.
