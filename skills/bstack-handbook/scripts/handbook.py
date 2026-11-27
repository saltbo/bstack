#!/usr/bin/env python3
"""Keep the handbook's versions, lock, index, and changelog consistent.

  handbook.py check                      verify frontmatter, index, and lock
  handbook.py init                       lock handbooks that have no lock entry yet
  handbook.py bump <id> --source S --saw S --expect S [--owner]
                                         raise a changed handbook's version
"""

import argparse
import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "handbook.lock.json"
INDEX = ROOT / "SKILL.md"
CHANGELOG = ROOT / "CHANGELOG.md"
KEYS = ["id", "version", "audience", "applies"]
ORDER = ["project", "planning", "design", "openapi", "database", "backend", "frontend", "build", "testing", "verification",
         "versioning", "deploy", "release", "operate"]
START, END = "<!-- index:start -->", "<!-- index:end -->"


def handbooks():
    paths = []
    for group in ("lifecycle", "types", "policies"):
        paths += sorted((ROOT / group).glob("*.md"), key=lambda p: ORDER.index(p.stem) if p.stem in ORDER else len(ORDER))
    return [p for p in paths if p.is_file()]


def read(path):
    text = path.read_text()
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise SystemExit(f"{path.relative_to(ROOT)}: no frontmatter")
    meta = dict(line.split(": ", 1) for line in match.group(1).splitlines())
    return meta, text[match.end():]


def digest(path):
    _, body = read(path)
    h = hashlib.sha256(body.encode())
    detail = path.with_suffix("")
    if detail.is_dir():
        for extra in sorted(p for p in detail.rglob("*") if p.is_file()):
            h.update(extra.relative_to(detail).as_posix().encode())
            h.update(extra.read_bytes())
    return h.hexdigest()[:16]


def index_table():
    rows = ["| Handbook | Version | For | Applies to |", "| --- | --- | --- | --- |"]
    for path in handbooks():
        meta, _ = read(path)
        link = path.relative_to(ROOT).as_posix()
        rows.append(f"| [{meta['id']}]({link}) | {meta['version']} | {meta['audience']} | {meta['applies']} |")
    return "\n".join(rows)


def write_index():
    text = INDEX.read_text()
    a, b = text.index(START) + len(START), text.index(END)
    INDEX.write_text(text[:a] + "\n" + index_table() + "\n" + text[b:])


def check():
    problems, seen = [], set()
    lock = json.loads(LOCK.read_text()) if LOCK.exists() else {}
    for path in handbooks():
        meta, _ = read(path)
        name = path.relative_to(ROOT).as_posix()
        for key in KEYS:
            if key not in meta:
                problems.append(f"{name}: frontmatter lacks {key}")
        hid = meta.get("id")
        if hid != path.stem:
            problems.append(f"{name}: id {hid} does not match the file name")
        if hid in seen:
            problems.append(f"{name}: duplicate id {hid}")
        seen.add(hid)
        entry = lock.get(hid)
        if entry is None:
            problems.append(f"{name}: not locked; run handbook.py init")
        elif entry["hash"] != digest(path):
            problems.append(f"{name}: changed since {hid}@{entry['version']}; run handbook.py bump {hid}")
        elif str(entry["version"]) != meta.get("version"):
            problems.append(f"{name}: version {meta.get('version')} differs from lock {entry['version']}")
    for gone in set(lock) - seen:
        problems.append(f"lock lists {gone}, which no longer exists")
    text = INDEX.read_text()
    if START not in text or END not in text:
        problems.append("SKILL.md lacks the index markers")
    elif text[text.index(START) + len(START):text.index(END)].strip() != index_table():
        problems.append("SKILL.md index is out of date; run handbook.py bump or init")
    return problems


def save_lock(lock):
    LOCK.write_text(json.dumps(dict(sorted(lock.items())), indent=2) + "\n")


def init():
    lock = json.loads(LOCK.read_text()) if LOCK.exists() else {}
    for path in handbooks():
        meta, _ = read(path)
        lock.setdefault(meta["id"], {"version": int(meta["version"]), "hash": digest(path)})
    save_lock(lock)
    write_index()


def bump(args):
    path = next((p for p in handbooks() if p.stem == args.id), None)
    if path is None:
        raise SystemExit(f"no handbook named {args.id}")
    meta, _ = read(path)
    if meta.get("owner-only") == "true" and not args.owner:
        raise SystemExit(f"{args.id} is owner-only: only Saltbo changes it (pass --owner when he asked for the change)")
    lock = json.loads(LOCK.read_text())
    old = lock[args.id]["version"]
    if lock[args.id]["hash"] == digest(path):
        raise SystemExit(f"{args.id} has not changed since {args.id}@{old}")
    new = old + 1
    text = path.read_text()
    path.write_text(re.sub(r"(?m)^version: .*$", f"version: {new}", text, count=1))
    lock[args.id] = {"version": new, "hash": digest(path)}
    save_lock(lock)
    write_index()
    today = datetime.date.today().isoformat()
    entry = (f"\n## {args.id}@{new} ({today})\n\n- Source: {args.source}\n- Saw: {args.saw}\n"
             f"- Expect: {args.expect}\n- Outcome: pending\n")
    CHANGELOG.write_text(CHANGELOG.read_text().rstrip("\n") + "\n" + entry)
    print(f"{args.id}@{old} -> {args.id}@{new}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check")
    sub.add_parser("init")
    b = sub.add_parser("bump")
    b.add_argument("id")
    b.add_argument("--source", required=True, help="session, PR, or issue that showed the problem")
    b.add_argument("--saw", required=True, help="the behavior that was wrong")
    b.add_argument("--expect", required=True, help="the behavior the change should produce")
    b.add_argument("--owner", action="store_true", help="Saltbo asked for this change")
    args = parser.parse_args()
    if args.command == "check":
        problems = check()
        for line in problems:
            print(line, file=sys.stderr)
        print(f"{len(handbooks())} handbooks, {len(problems)} problems")
        sys.exit(1 if problems else 0)
    if args.command == "init":
        init()
    if args.command == "bump":
        bump(args)


if __name__ == "__main__":
    main()
