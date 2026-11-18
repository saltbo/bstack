import { describe, expect, it } from "vitest";
import { createApp } from "../src/app";
import { MAX_BODY, memoryStore, parseBody } from "../src/notes";

describe("parseBody", () => {
  it("trims the body [notes-add-a-note]", () => {
    expect(parseBody("  buy milk ")).toEqual({ ok: true, body: "buy milk" });
  });

  it("refuses an empty or too long body [notes-refuse-an-empty-note]", () => {
    expect(parseBody("   ").ok).toBe(false);
    expect(parseBody("x".repeat(MAX_BODY + 1)).ok).toBe(false);
  });
});

describe("notes API", () => {
  it("lists the newest note first [notes-list-newest-first]", async () => {
    const store = memoryStore();
    let now = 1000;
    const app = createApp(() => store, () => now++);
    for (const body of ["first", "second"]) {
      await app.request("/api/notes", { method: "POST", body: JSON.stringify({ body }), headers: { "Content-Type": "application/json" } });
    }
    const res = await app.request("/api/notes");
    const { notes } = (await res.json()) as { notes: { body: string }[] };
    expect(notes.map((n) => n.body)).toEqual(["second", "first"]);
  });
});
