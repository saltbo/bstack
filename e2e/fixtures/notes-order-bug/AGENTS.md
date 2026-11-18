# notes

A small notes app on Cloudflare Workers. People add short notes on one page and see them newest first. It has no real users yet.

## Commands

The gate is `pnpm verify`, the same locally and in CI. `pnpm dev` runs the app on the Workers runtime after `pnpm db:migrate:local`.

## Handbook

Types: cf-workers
Stage: development
Facts: gate `pnpm verify`; Worker `notes` with D1 `notes` (production) and its preview database shared by previews; Workers Builds applies D1 migrations itself before it deploys, so do not apply them by hand; there is no sign-in
Preview: Workers Builds deploys every branch other than `main` and posts its address on the branch's PR, in the form `http://<branch>-notes.localhost:{{PROXY_PORT}}`
Production: http://notes.localhost:{{PROXY_PORT}}, deployed by Workers Builds on every push to `main`
Exceptions: none
