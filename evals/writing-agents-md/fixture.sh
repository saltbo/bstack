#!/bin/bash
cat > AGENTS.md <<'MD'
# orderdesk

A Python library and a CLI for managing orders in a small shop.

## Commands

Run the tests with `python3 -m unittest`. The CLI is `python3 -m orderdesk`.

## Conventions

- Write tests for every change.
- Keep commits small, one concern each.
- Use the logging module for output.
- Configuration comes from environment variables prefixed `ORDERDESK_`.

## Release

Bump the version in `pyproject.toml`, then tag it as `vX.Y.Z`.
MD
