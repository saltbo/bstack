#!/usr/bin/env python3
"""Entry point of the stand-in: the `gh` and `wrangler` shims, the push hook, and its background jobs."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import simcore  # noqa: E402


def main(argv):
    command, rest = argv[0], argv[1:]
    if command == "gh":
        import gh
        return gh.main(rest)
    if command == "wrangler":
        import wrangler
        return wrangler.main(rest)
    if command == "hook":
        simcore.hook(sys.stdin.read().splitlines())
    elif command == "pushed":
        simcore.pushed(*rest)
    elif command == "proxy":
        simcore.serve_proxy(int(rest[0]))
    else:
        print(f"unknown command {command}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
