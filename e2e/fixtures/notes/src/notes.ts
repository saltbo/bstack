export const MAX_BODY = 500;

export type Note = { id: number; body: string; createdAt: number };

export type Parsed = { ok: true; body: string } | { ok: false; error: string };

/** The body of a new note, trimmed, or why it cannot be saved. */
export function parseBody(input: unknown): Parsed {
  if (typeof input !== "string") return { ok: false, error: "body must be text" };
  const body = input.trim();
  if (body.length === 0) return { ok: false, error: "body must not be empty" };
  if (body.length > MAX_BODY) return { ok: false, error: `body must be at most ${MAX_BODY} characters` };
  return { ok: true, body };
}

export interface NoteStore {
  list(): Promise<Note[]>;
  add(body: string, now: number): Promise<Note>;
}

export function d1Store(db: D1Database): NoteStore {
  return {
    async list() {
      const { results } = await db
        .prepare("SELECT id, body, created_at AS createdAt FROM notes ORDER BY created_at DESC, id DESC")
        .all<Note>();
      return results;
    },
    async add(body, now) {
      const row = await db
        .prepare("INSERT INTO notes (body, created_at) VALUES (?, ?) RETURNING id, body, created_at AS createdAt")
        .bind(body, now)
        .first<Note>();
      if (!row) throw new Error("insert returned no row");
      return row;
    },
  };
}

/** An in-memory store with the same contract, for tests. */
export function memoryStore(): NoteStore {
  const notes: Note[] = [];
  return {
    async list() {
      return [...notes].sort((a, b) => b.createdAt - a.createdAt || b.id - a.id);
    },
    async add(body, now) {
      const note = { id: notes.length + 1, body, createdAt: now };
      notes.push(note);
      return note;
    },
  };
}
