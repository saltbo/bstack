# README.md

A person reads this file to decide whether the project is what they need, and then to set it up and use it. They read it from the top and stop once they have what they came for. It is the face of the repository, and it is held to the same standard as `AGENTS.md`.

## Order

Each section answers the question a reader has at that point, in this order.

1. What it is and who it is for, in the name and the first one or two sentences.
2. How it works, when a reader has to understand the design to use it well, and only that far.
3. How to install it, then how to use it.
4. Configuration, layout, and development, as far as a user or a contributor needs them.

## What has to hold

- Every command and example runs exactly as written. Copy it from a run.
- It describes what exists now. Plans belong in issues, and changes in the changelog or the release notes.
- Each claim is one a reader can check. An adjective that only praises the project tells the reader nothing.
- Product behavior in detail, the reasons for a design, and instructions for agents each have their own place, in `spec/`, `docs/adr/`, and `AGENTS.md`. The README links to them.
- A table is for something a reader looks up, such as paths or options. Prose that explains goes in paragraphs.
- When a change makes the README untrue, the README changes in the same commit. A README that claims more than the code does is a defect in the README.
