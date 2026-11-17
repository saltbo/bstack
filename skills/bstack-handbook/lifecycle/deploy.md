---
id: deploy
version: 2
audience: leader
applies: services we run
---

# Deploy

Deploying means putting a service into an environment we run. Handing an artifact to someone else is [release](release.md).

## Decisions

- **A configured pipeline is standing permission.** When a merge deploys, merge. No pause, including for a redeploy that repairs a failed one.
- **Watch it land.** After the merge, confirm the pipeline finished and the target serves the new build.
- **Then the live check.** Confirm the target serves the intended build by its version, then exercise the changed behavior and the critical journey it belongs to. Use a dedicated test identity, and do not reset, seed, or change business data, send messages, or incur charges. (2026-09)
- **If it broke production**, follow [operate](operate.md).
- **A repository connected to a pipeline deploys through it.** The one other deploy is of a fix under debugging, sent directly to verify it before it is committed. Say in the report how a deploy happened. (2026-05-25, 2026-08-08)
- **Two environments.** Production, and one shared pre-release environment that branch previews connect to. A clean-slate acceptance runs locally. (2026-09-22, 2026-11-13)
- **Pre-release never touches real money or real payment networks**, and production never accepts sandbox funds. (2026-08-02)
- **After a refactor, check each environment variable and config file is still used** before the first deploy. (2026-07-30)
