#!/bin/bash
mkdir -p skills/changelog
cat > skills/changelog/SKILL.md <<'MD'
---
name: changelog
description: Writes the CHANGELOG entry for a release.
---

# Changelog

When a release is cut, add an entry to `CHANGELOG.md` for the new version.

## Steps

1. Read the merged PRs since the last tag.
2. Write one bullet per PR under the new version heading.
3. Group the bullets under Added, Changed, and Fixed.

## Notes

- IMPORTANT: Do not include PRs that only change CI or tests.
- Also, make sure to skip dependency bumps.
- Remember to write the bullets for users, not for developers.
- NOTE: dependency bumps that fix a security issue SHOULD be included under Fixed.
MD
