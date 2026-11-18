# notes

A small notes app on Cloudflare Workers, with Hono and D1.

```bash
pnpm install
pnpm db:migrate:local
pnpm dev
```

`pnpm verify` is the gate. It type-checks, checks that every scenario in `spec/` has a test, and runs the tests.
