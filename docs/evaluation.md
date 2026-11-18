# Evaluation

The repository tests check structure. This page says how to check behavior, and what the last runs showed. Earlier runs are in the history of this file.

## Method

Both kinds of run use bstack as it is in the checkout, and both count only what the session did and left behind. The agent's own summary is not evidence.

- **Skill evals**, in `evals/`, check one skill. Each case runs in fresh sessions with bstack loaded and without it, three times by default, and the score is the difference. Run them with `claude plugin eval . --scaffold --trust-plugin --allow-tools Edit Write`. `.claude-plugin/plugin.json` exists so that the command can load `skills/`.
- **End-to-end cases**, in `e2e/`, check the system. Each is one real session, started with `python3 e2e/run.py [case]`, that does the whole job on a local stand-in for GitHub and Cloudflare in `e2e/sim/`, so a run takes minutes instead of the half hour the real services take.
  - The session starts in a clone of a fixture repository from `e2e/fixtures/`, with its dependencies installed and its remote at `https://github.com/saltbo/<name>`. `git` and `gh` reach the stand-in's GitHub. A push runs the repository's workflow as its checks, and in a Workers project it deploys the branch to a preview, announced on its PR as Workers Builds does, or `main` to production, on the local Workers runtime under `*.localhost`. `wrangler` acts on that Cloudflare.
  - It has this checkout's skills, installed and pinned as on Saltbo's machine, and none of his own skills, instructions, MCP servers, or credentials. Browser checks use ego-browser in task spaces of the session's own, and the runner closes any it leaves open. A case that needs docket gets a docket of its own, and a simulated user answers its cards and the session's questions, from the case's `user.md` when it has one.
  - One run holds the machine at a time, because sessions pick local ports for their own dev servers, and two at once reached each other's.
  - The case's `check.sh` judges the outcome against the stand-in's state. The [session script](../.agents/skills/revise-from-evidence/scripts/session.py) reports on the transcript: the skills and handbooks it read, its failed calls, the errors it hit more than once, its questions, and its cost. The stand-in's `calls.log` lists every `gh` and `wrangler` call, and a call it did not understand counts as a gap in the stand-in, not in the skills.
  - Nothing outlives the run but its results. Its transcript is moved out of `~/.claude/projects`, and a fingerprint of the user's skills, git, gh, and docket configuration taken before and after reports any change as a leak.

Results land under `evals/results/` and `e2e/results/`, which are not committed. The last run of each case is summarized below and replaces the one before it.

## Cases

| Case | Kind | Request | Pass when |
| --- | --- | --- | --- |
| `writing-agents-md` | eval, e2e | "Use the logging module for output" sent CLI results to stderr. Fix AGENTS.md | The line is rewritten in place, with no patch words, and the file does not grow |
| `writing-patched-skill` | eval | A changelog skill with four patches in a Notes section logged a README-only PR. Fix it | The rule is stated once, with its reason, and the file does not grow |
| `writing-not-markdown` | eval | Rename a field in Python code | `bstack-writing` does not load |
| `writing-copied-facts` | eval | AGENTS.md copies every script from package.json. "I added `lint`, update AGENTS.md" | Only the gate command stays, with no copy of the scripts or of what the gate runs, and no line saying where the scripts are |
| `bugfix-paging` | e2e | "Some orders never show up when I page", under bugfix | A merged PR with green CI put the fix on `main`, every order is listed, no branch or PR is left |
| `feature-notes` | e2e | Add deleting a note to a Workers app, under autopilot | A merged PR with green CI and a preview, delete works in production, a scenario covers it, nothing is left |
| `xplan-notes` | e2e | Tags and search for the same app, under xplan, with a simulated user | Two or more merged PRs, each with green CI and a preview, both live, every docket task done |

## Last runs

Claude Code 2.1.326, model `claude-opus-5-5`, 2026-11-17. Evals ran once per arm. End-to-end cases ran once each, one at a time, on the stand-in. The same work on the real GitHub and Cloudflare took half an hour or more per PR.

| Case | Kind | Result | Time | Cost | Notes |
| --- | --- | --- | --- | --- | --- |
| `writing-agents-md` | eval | 1.00 with bstack, 0.00 without | | | Without it, the agent kept a "never" and failed the judge |
| `writing-patched-skill` | eval | 1.00 with bstack, 0.50 without | | | Without it, the patches stayed beside a new exclusion |
| `writing-not-markdown` | eval | 1.00 with bstack, 1.00 without | | | The skill stayed out of a code-only change |
| `writing-copied-facts` | eval | 1.00 with bstack, 0.00 without, five runs per arm | | | Without it, `lint` was added to the copied list every time. Before the gate fact read "which command is the gate", one run in five restated what the gate runs |
| `writing-agents-md` | e2e | Pass | 23 s | $0.12 | One line rewritten in place |
| `bugfix-paging` | e2e | Pass | 97 s | $0.37 | Reproduced, fixed, draft PR, green CI, squash-merged, branch deleted, asked nothing |
| `feature-notes` | e2e | Pass | 320 s | $1.37 | Delete through a PR with green CI and a preview, proved in ego-browser on the preview, live in production. Most of the time is the model, seconds the browser and the stand-in |
| `xplan-notes` | e2e | Pass | 872 s | $4.92 | One question round answered by the simulated user, one review card approved, three tasks to three workers, three PRs merged with green CI and previews, every docket task done |

## Not yet run

The worker's verifying job and `revise-from-evidence` have no case yet.

## Limits

- The recorded runs are one per case. They show the behavior once, not its variance, which the evals measure when run three times or more.
- The fixtures are small, and the stand-in covers the `gh` and `wrangler` commands and the Workers Builds behavior that the skills use, not all of GitHub and Cloudflare. It has no review bot unless a case configures one, and no browser sign-in.
- The session runs with the user's own home directory, because Claude Code reads its sign-in from there. The leak check is what shows that it changed nothing of his.
- Only Claude Code was run, and the session script reads only Claude Code transcripts. Codex and Pi were not.
