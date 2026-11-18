#!/usr/bin/env python3
"""Turn a Claude Code session into evidence of what an agent did and which text it followed.

The script reads a session transcript, its subagents included, and prints a
numbered timeline and the signals worth a look: skills loaded, handbooks cited,
failed and repeated calls, questions to the user, long waits, and totals. It
judges nothing. The agent that runs it decides what the evidence means.

  session.py report <session-id or .jsonl> [--json]
  session.py events <session-id or .jsonl> [--from N] [--to M]
"""

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
HANDBOOK = REPO / "skills/bstack-handbook"
CITATION = re.compile(r"\b([a-z][a-z-]*)@(\d+)\b")
SKILL_SHOW = re.compile(r"\bskills\s+show\s+([\w:-]+)")
TEXT_PATH = re.compile(r"([\w-]+/SKILL\.md|(?:[\w-]+/)?(?:lifecycle|policies|types|references)/[\w-]+\.md)")
SKILL_BODY = re.compile(r"^Base directory for this skill: (\S+)")
# A compound shell command can fail midway and still exit 0, so its output is read too.
ERROR_LINE = re.compile(r"(?im)^.*(?:^FAILED:|\berror:|\bfatal:|^Traceback|No such file or directory|"
                        r"command not found|Permission denied|unrecognized arguments|Exit code [1-9]).*$")
WAIT_SECONDS = 300
SHORT = 160


def projects_dir():
    return Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude") / "projects"


def locate(target):
    path = Path(target).expanduser()
    if path.suffix == ".jsonl" and path.exists():
        return path
    found = sorted(projects_dir().glob(f"*/{target}.jsonl"))
    if not found:
        sys.exit(f"no transcript for session {target} under {projects_dir()}")
    return found[0]


def records(path):
    with path.open() as stream:
        for line in stream:
            line = line.strip()
            if line:
                yield json.loads(line)


def clip(text, limit=SHORT):
    text = " ".join(str(text).split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def result_text(content):
    if isinstance(content, list):
        return " ".join(c.get("text", "") for c in content if isinstance(c, dict))
    return str(content or "")


def call_summary(name, args):
    if name == "Bash":
        return args.get("command", "")
    if name in ("Read", "Write", "Edit", "NotebookEdit"):
        return args.get("file_path", "")
    if name == "Skill":
        return args.get("skill", "")
    if name == "Agent":
        return f"{args.get('subagent_type', '')}: {args.get('description', '')}"
    if name == "AskUserQuestion":
        return " | ".join(q.get("question", "") for q in args.get("questions", []))
    return json.dumps(args, ensure_ascii=False)


def stamp(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00")) if value else None


def parse(path, actor):
    """Yield events in transcript order. A tool result is folded into its call."""
    events, calls, when = [], {}, None
    for rec in records(path):
        kind, when = rec.get("type"), stamp(rec.get("timestamp")) or when
        message = rec.get("message") or {}
        if kind == "pr-link":
            events.append({"at": when, "actor": actor, "kind": "pr", "text": rec.get("prUrl", "")})
        elif kind == "cost-state":
            events.append({"at": when, "actor": actor, "kind": "cost", "usd": rec.get("totalCostUSD")})
        elif kind == "assistant":
            for block in message.get("content") or []:
                if block.get("type") == "text" and block.get("text", "").strip():
                    events.append({"at": when, "actor": actor, "kind": "say", "text": block["text"]})
                elif block.get("type") == "tool_use":
                    event = {"at": when, "actor": actor, "kind": "call", "tool": block.get("name"),
                             "input": call_summary(block.get("name"), block.get("input") or {}),
                             "error": None, "output": ""}
                    calls[block.get("id")] = event
                    events.append(event)
        elif kind == "user":
            content = message.get("content")
            blocks = [{"type": "text", "text": content}] if isinstance(content, str) else content or []
            for block in blocks:
                if block.get("type") == "tool_result":
                    call = calls.get(block.get("tool_use_id"))
                    if call is not None:
                        call["output"] = result_text(block.get("content"))
                        shell = call["tool"] == "Bash"
                        match = ERROR_LINE.search(call["output"]) if shell and not block.get("is_error") else None
                        call["error"] = "failed" if block.get("is_error") else "error in output" if match else None
                        call["error_line"] = (match.group(0) if match else call["output"].strip().split("\n")[0])[:200]
                        call["done"] = when
                elif block.get("type") == "text":
                    text = block.get("text", "")
                    body = SKILL_BODY.match(text)
                    if body:
                        events.append({"at": when, "actor": actor, "kind": "skill",
                                       "name": Path(body.group(1)).name, "via": "Skill tool"})
                    elif not rec.get("isMeta") and not text.startswith("<"):
                        role = "user" if actor == "main" else "brief"
                        events.append({"at": when, "actor": actor, "kind": role, "text": text})
    return events


def load(target):
    path = locate(target)
    events = parse(path, "main")
    for sub in sorted((path.parent / path.stem / "subagents").glob("agent-*.jsonl")):
        meta_path = sub.with_suffix(".meta.json")
        meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
        events += parse(sub, f"{meta.get('agentType', 'agent')}:{sub.stem[6:14]}")
    events = [e for e in events if e["at"]]
    events.sort(key=lambda e: e["at"])
    for index, event in enumerate(events):
        event["i"] = index
    return path, events


def handbook_ids():
    return {p.stem for group in ("lifecycle", "types", "policies") for p in (HANDBOOK / group).glob("*.md")}


def bstack_at(start):
    """The commit of bstack's main that was current when the session started."""
    if start is None:
        return None
    for ref in ("origin/main", "main"):
        out = subprocess.run(["git", "-C", str(REPO), "log", "-1", f"--before={start.isoformat()}",
                              "--format=%h %cs %s", ref], capture_output=True, text=True)
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip()
    return None


def signature(event):
    """What a failure says, without the arguments that differ between attempts: its first two words and its last clause."""
    line = event.get("error_line", "").strip()
    words, clause = line.split()[:2], line.rsplit(": ", 1)
    tail = clause[1] if len(clause) == 2 and len(clause[1]) > 3 else ""
    return clip(re.sub(r"\d+", "N", " ".join(words) + (" … " + tail if tail else "")), 80)


def signals(path, events):
    calls = [e for e in events if e["kind"] == "call"]
    times = [e["at"] for e in events if e["at"]]
    start, end = (min(times), max(times)) if times else (None, None)
    known = handbook_ids()

    skills = [{"i": e["i"], "name": e["name"], "via": e["via"], "actor": e["actor"]}
              for e in events if e["kind"] == "skill"]
    for e in calls:
        if e["tool"] == "Bash":
            for name in SKILL_SHOW.findall(e["input"]):
                skills.append({"i": e["i"], "name": name, "via": "skills show", "actor": e["actor"]})
    texts = [{"i": e["i"], "path": path, "via": e["tool"], "actor": e["actor"]}
             for e in calls if e["tool"] in ("Read", "Bash") for path in TEXT_PATH.findall(e["input"])]

    cited = Counter()
    for e in events:
        if e["kind"] == "say":
            cited.update(f"{a}@{v}" for a, v in CITATION.findall(e["text"]) if a in known)

    failed = [e for e in calls if e["error"]]
    by_signature = defaultdict(list)
    for e in failed:
        by_signature[signature(e)].append(e["i"])
    repeated = [{"error": k, "events": v} for k, v in by_signature.items() if len(v) > 1]

    streaks, run = [], []
    for e in calls:
        if e["error"]:
            run.append(e["i"])
        else:
            if len(run) >= 3:
                streaks.append(run)
            run = []
    if len(run) >= 3:
        streaks.append(run)

    questions = [{"i": e["i"], "text": clip(e["input"])} for e in calls if e["tool"] == "AskUserQuestion"]
    main = [e for e in events if e["actor"] == "main"]
    for prev, nxt in zip(main, main[1:]):
        if prev["kind"] == "say" and nxt["kind"] == "user":
            asked = [line for line in prev["text"].splitlines() if line.rstrip().endswith(("?", "？"))]
            if asked:
                questions.append({"i": prev["i"], "text": clip(asked[-1])})

    waits = []
    for prev, nxt in zip(events, events[1:]):
        if prev["at"] and nxt["at"] and nxt["kind"] != "user":
            gap = (nxt["at"] - prev["at"]).total_seconds()
            if gap >= WAIT_SECONDS:
                waits.append({"after": prev["i"], "minutes": round(gap / 60, 1)})

    costs = [e["usd"] for e in events if e["kind"] == "cost" and e["usd"] is not None]
    return {
        "session": path.stem,
        "transcript": str(path),
        "start": start.isoformat() if start else None,
        "minutes": round((end - start).total_seconds() / 60, 1) if start else None,
        "bstack": bstack_at(start),
        "user_messages": [{"i": e["i"], "text": clip(e["text"])} for e in events if e["kind"] == "user"],
        "skills": skills,
        "texts_read": texts,
        "handbooks_cited": dict(cited),
        "tool_calls": dict(Counter(e["tool"] for e in calls)),
        "subagents": sorted({e["actor"] for e in events if e["actor"] != "main"}),
        "failed_calls": [{"i": e["i"], "tool": e["tool"], "how": e["error"], "input": clip(e["input"]),
                          "error": clip(e["error_line"])} for e in failed],
        "repeated_failures": repeated,
        "failure_streaks": streaks,
        "questions_to_user": questions,
        "waits": waits,
        "pull_requests": sorted({e["text"] for e in events if e["kind"] == "pr"}),
        "cost_usd": costs[-1] if costs else None,
    }


def render(s):
    out = [f"# Session {s['session']}", "",
           f"- Transcript: `{s['transcript']}`",
           f"- Started {s['start']}, ran {s['minutes']} min, cost {s['cost_usd']} USD",
           f"- bstack main at the start: {s['bstack'] or 'unknown'}",
           f"- Tool calls: {s['tool_calls']}",
           f"- Subagents: {', '.join(s['subagents']) or 'none'}",
           f"- Pull requests: {', '.join(s['pull_requests']) or 'none'}",
           f"- Handbooks cited: {s['handbooks_cited'] or 'none'}"]

    def section(title, rows):
        out.extend(["", f"## {title}", ""])
        out.extend(rows or ["None."])

    section("User messages", [f"- [{m['i']}] {m['text']}" for m in s["user_messages"]])
    section("Skills loaded", [f"- [{k['i']}] {k['name']} via {k['via']} ({k['actor']})" for k in s["skills"]])
    section("Skill and handbook files read", [f"- [{x['i']}] {x['path']} via {x['via']} ({x['actor']})" for x in s["texts_read"]])
    section("Questions to the user", [f"- [{q['i']}] {q['text']}" for q in s["questions_to_user"]])
    section("The same error more than once", [f"- `{r['error']}` at {r['events']}" for r in s["repeated_failures"]])
    section("Failure streaks", [f"- events {r}" for r in s["failure_streaks"]])
    section("Failed calls", [f"- [{f['i']}] {f['tool']} ({f['how']}) `{f['input']}`: {f['error']}" for f in s["failed_calls"]])
    section("Waits of five minutes or more", [f"- after [{w['after']}]: {w['minutes']} min" for w in s["waits"]])
    out.extend(["", "Read any event in full with `session.py events <session> --from N --to M`."])
    return "\n".join(out)


def show_events(events, start, stop):
    for e in events[start:stop + 1]:
        head = f"[{e['i']}] {e['at'].strftime('%H:%M:%S') if e['at'] else '--'} {e['actor']} {e['kind']}"
        if e["kind"] == "call":
            flag = f" ({e['error']})" if e["error"] else ""
            print(f"{head} {e['tool']}{flag}: {e['input']}")
            if e["output"]:
                print("    " + clip(e["output"], 1200))
        elif e["kind"] in ("say", "user", "brief", "pr"):
            print(f"{head}: {e['text']}")
        elif e["kind"] == "skill":
            print(f"{head}: {e['name']} via {e['via']}")
        elif e["kind"] == "cost":
            print(f"{head}: {e['usd']} USD")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    report = sub.add_parser("report", help="signals and totals for a session")
    report.add_argument("session")
    report.add_argument("--json", action="store_true")
    events = sub.add_parser("events", help="the numbered timeline, or a slice of it")
    events.add_argument("session")
    events.add_argument("--from", dest="start", type=int, default=0)
    events.add_argument("--to", dest="stop", type=int, default=10**9)
    args = parser.parse_args()

    path, timeline = load(args.session)
    if args.command == "events":
        show_events(timeline, args.start, args.stop)
        return
    result = signals(path, timeline)
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else render(result))


if __name__ == "__main__":
    main()
