"""The user of an end-to-end session: answers docket cards while the session runs, and its questions when it stops.

The case's `user.md` says who the user is and what they want. Without one, the
user approves every card and answers every question with "go with your
recommendation". With one, a separate model plays the user from that text,
seeing only the question, as a person would.
"""

import json
import sqlite3
import subprocess
import sys
import threading
import time
import urllib.request
from pathlib import Path

import simcore

USER_MODEL = "sonnet"
DEFAULT_REPLY = "按你推荐的来，不用再问我。"


class Docket:
    """A client of the stand-in's own docket server, speaking MCP over HTTP like a card would."""

    def __init__(self, url, token, db):
        self.url, self.token, self.db, self.session = url, token, Path(db), None

    def rpc(self, method, params=None, notify=False):
        body = {"jsonrpc": "2.0", "method": method, **({"params": params} if params is not None else {})}
        if not notify:
            body["id"] = int(time.time() * 1000)
        headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream",
                   "Authorization": f"Bearer {self.token}"}
        if self.session:
            headers["Mcp-Session-Id"] = self.session
        req = urllib.request.Request(self.url, data=json.dumps(body).encode(), headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=30) as resp:
            self.session = resp.headers.get("Mcp-Session-Id") or self.session
            text = resp.read().decode()
        for line in text.splitlines():
            if line.startswith("data:"):
                return json.loads(line[5:])
        return json.loads(text) if text.strip() else None

    def connect(self):
        self.rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                                "clientInfo": {"name": "e2e-user", "version": "1"}})
        self.rpc("notifications/initialized", notify=True)

    def pending(self):
        if not self.db.exists():
            return []
        with sqlite3.connect(self.db) as con:
            rows = con.execute("SELECT id, template, data FROM asks WHERE answer IS NULL ORDER BY created_at").fetchall()
        return [{"id": r[0], "template": r[1], "data": json.loads(r[2])} for r in rows]

    def submit(self, ask_id, answer):
        return self.rpc("tools/call", {"name": "submit", "arguments": {"id": ask_id, "answer": answer}})


class User:
    def __init__(self, persona, log):
        self.persona, self.log = persona, log

    def note(self, kind, question, answer):
        with open(self.log, "a") as f:
            f.write(json.dumps({"at": time.strftime("%H:%M:%S"), "kind": kind, "question": question,
                                "answer": answer}, ensure_ascii=False) + "\n")

    def decide(self, prompt, fallback):
        """What the user would say. Without a persona, the fallback."""
        if not self.persona:
            return fallback
        text = (f"You are this user:\n\n{self.persona}\n\nThe coding agent working for you asks:\n\n{prompt}\n\n"
                "Reply as the user, in one to three sentences, in the language of the question. "
                "Decide what is yours to decide. Where you have no preference, accept the agent's recommendation.")
        result = subprocess.run(["claude", "-p", text, "--model", USER_MODEL, "--setting-sources", "",
                                 "--strict-mcp-config", "--no-session-persistence", "--tools", ""],
                                capture_output=True, text=True, timeout=120, env=simcore.outside_env(), stdin=subprocess.DEVNULL)
        return result.stdout.strip() or fallback

    def answer_card(self, ask):
        data = ask["data"]
        if ask["template"] == "review":
            items = []
            for item in data.get("items", []):
                entry = {"id": item["id"], "verdict": "ok"}
                question = item.get("question")
                if question:
                    text = question if isinstance(question, str) else question.get("text", "")
                    options = [] if isinstance(question, str) else question.get("options", [])
                    recommended = None if isinstance(question, str) else question.get("recommended")
                    fallback = recommended or (options[0] if options else DEFAULT_REPLY)
                    entry["answer"] = self.decide(f"{item.get('title', item['id'])}: {text}\nOptions: {options}\n"
                                                  f"Recommended: {recommended}", fallback)
                items.append(entry)
            answer = {"round": data.get("round", 1), "items": items}
        elif ask["template"] == "choice":
            options = data.get("options", [])
            pick = next((i for i, o in enumerate(options) if o.get("recommended")), 0)
            label = options[pick].get("label") if options else ""
            if self.persona and options:
                said = self.decide(f"{data.get('question', '')}\nOptions: {[o.get('label') for o in options]}", label)
                pick = next((i for i, o in enumerate(options) if o.get("label") and o["label"] in said), pick)
                label = options[pick].get("label")
            answer = {"choice": options[pick].get("value", pick) if options else None, "label": label}
        else:
            answer = {"text": self.decide(json.dumps(data, ensure_ascii=False)[:2000], DEFAULT_REPLY)}
        self.note(f"card:{ask['template']}", data, answer)
        return answer

    def reply(self, message):
        said = self.decide(message[-3000:], DEFAULT_REPLY)
        self.note("chat", message[-3000:], said)
        return said


def watch_cards(docket, user, stop):
    """Answer each docket card shortly after it appears, as the user would."""
    connected = False
    while not stop.is_set():
        try:
            for ask in docket.pending():
                if not connected:
                    docket.connect()
                    connected = True
                docket.submit(ask["id"], user.answer_card(ask))
        except Exception as exc:  # a failed answer is recorded, and the next poll tries again
            user.note("error", "", repr(exc))
        stop.wait(3)


def asks_user(final_text):
    """Whether the session stopped to wait for the user, judged as a person reading its last message would."""
    text = final_text.strip()
    if not text:
        return False
    if any(line.rstrip().endswith(("?", "？")) for line in text.splitlines()[-6:]):
        return True
    prompt = ("A coding agent ended its turn with the message below. Does it wait for the user to answer, "
              "confirm, or choose something before it continues? Reply with yes or no only.\n\n" + text[-3000:])
    result = subprocess.run(["claude", "-p", prompt, "--model", USER_MODEL, "--setting-sources", "",
                             "--strict-mcp-config", "--no-session-persistence", "--tools", ""],
                            capture_output=True, text=True, timeout=120, env=simcore.outside_env(), stdin=subprocess.DEVNULL)
    return result.stdout.strip().lower().startswith("yes")


if __name__ == "__main__":
    print(asks_user(sys.stdin.read()))
