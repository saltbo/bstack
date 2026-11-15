---
id: identity
version: 2
audience: leader, worker
applies: all
---

# Identity and accounts

## Decisions

- **Write as the agent.** Commits, pushes, and other writes use the agent identity from `realmroot agent whoami` when it is available. Reads may use his credentials.
- **Disclose his credentials.** Whenever his credentials were used, the report says which identity, why, and for what.
- **Realmroot first, then his account.** When Realmroot has no integration for a service, use his developer account without asking and say so in the report. (2026-09-07)
- **Agents hold only short-lived tokens.** A grant may persist. The token does not. (2026-08-03)
- **Use the CLI access that exists**, such as `wrangler` and `gh`, instead of asking him for a token or a login. (2026-05-05)
- **One dedicated test account per app**, created by the agent. Its password is in the local env file and noted in the project's instructions, never in source code. (2026-09-24, 2026-06-04)
- **An agent may complete a sign-in or approve its own access request in his logged-in browser** when the task needs it, unless he is testing that approval flow himself. (2026-09-05, 2026-11-15)

## Open

- How far may an agent widen its own access, or a test account's, to get a task done? Until decided, it requests only the scopes the task needs, for the shortest lifetime offered, and lists every grant in its report. It does not add a test account to an organization that owns other private applications, and it does not change who can reach anything other than the project it is working on. When the task cannot be done inside those limits, it reports that instead. (Seen on bstack-playground PR 6.)
