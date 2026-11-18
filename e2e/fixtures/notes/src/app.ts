import { Hono } from "hono";
import { type NoteStore, parseBody } from "./notes";

export function createApp(store: (env: Env) => NoteStore, clock: () => number = Date.now) {
  const app = new Hono<{ Bindings: Env }>();

  app.get("/api/notes", async (c) => c.json({ notes: await store(c.env).list() }));

  app.post("/api/notes", async (c) => {
    const input = await c.req.json<{ body?: unknown }>().catch(() => ({ body: undefined }));
    const parsed = parseBody(input.body);
    if (!parsed.ok) return c.json({ error: parsed.error }, 400);
    return c.json({ note: await store(c.env).add(parsed.body, clock()) }, 201);
  });

  app.get("/", async (c) => {
    const notes = await store(c.env).list();
    const items = notes.map((n) => `<li>${escape(n.body)}</li>`).join("");
    return c.html(`<!doctype html><html><head><meta charset="utf-8"><title>Notes</title></head><body>
<h1>Notes</h1>
<form method="post" action="/notes"><input name="body" aria-label="New note"><button>Add</button></form>
<ul id="notes">${items}</ul>
</body></html>`);
  });

  app.post("/notes", async (c) => {
    const form = await c.req.parseBody();
    const parsed = parseBody(form.body);
    if (parsed.ok) await store(c.env).add(parsed.body, clock());
    return c.redirect("/", 303);
  });

  return app;
}

function escape(text: string) {
  return text.replace(/[&<>"']/g, (ch) => `&#${ch.charCodeAt(0)};`);
}

export type Env = { DB: D1Database };
