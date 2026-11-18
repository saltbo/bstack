#!/bin/bash
cat > package.json <<'JSON'
{
  "name": "shelf",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "test": "vitest run",
    "typecheck": "tsc --noEmit",
    "lint": "biome check .",
    "verify": "pnpm lint && pnpm typecheck && pnpm test"
  }
}
JSON
cat > AGENTS.md <<'MD'
# shelf

A small web app for keeping a reading list. It has no users yet.

## Scripts

- `pnpm dev` starts the dev server.
- `pnpm build` builds the app.
- `pnpm test` runs the unit tests.
- `pnpm typecheck` checks the types.
- `pnpm verify` is the gate: typecheck and test.

## Conventions

- Every change comes with a test.
MD
