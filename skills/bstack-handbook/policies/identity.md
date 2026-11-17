---
id: identity
version: 5
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
- **Sign-in checks use the shared test account at user level.** It exists already and the user-level agent instructions say where its credentials are. A separate account is made only when a test needs a specific identity, such as a paid plan or an admin role, and then its password is in a local env file noted in the project's instructions, never in source code. (2026-11-15, replacing the per-app rule of 2026-09-24)
- **An agent may complete a sign-in or approve its own access request in his logged-in browser** when the task needs it, unless he is testing that approval flow himself. (2026-09-05, 2026-11-15)

## Open

- How far may an agent widen its own access, or a test account's, to get a task done? Until decided, it requests only the scopes the task needs, for the shortest lifetime offered, and lists every grant in its report. It does not add a test account to an organization that owns other private applications, and it does not change who can reach anything other than the project it is working on. When the task cannot be done inside those limits, it reports that instead. (Seen on bstack-playground PR 6.)
- A test account has to sign in to an application that is private to an organization. Until decided, for a project in development the application is made public and the account stays outside the organization. For a live project the agent reports it and does neither. (saltbo/bstack issue 8.)
