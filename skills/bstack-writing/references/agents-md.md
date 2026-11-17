# AGENTS.md

Every agent that works in the repository reads this file at the start of every session, before it knows what its task is. So each line costs every session, and a wrong line misleads all of them. It is held to a higher standard than any other document in the repository.

The reader is a capable model that can read the code, run it, and look things up. It needs only what none of that would tell it.

## What goes in

- What the repository is for, in a few sentences, and what it is easily mistaken for.
- Decisions its owner made that the code does not show, each with its reason.
- Facts about its environment: where it runs, what deploys it, which commands make up the gate, the names of its resources. A fact is checked against the running system or its configuration before it is written.
- Where things are, when the layout does not explain itself.
- In a project under the handbook, the `## Handbook` block that its [index](../../bstack-handbook/SKILL.md) describes. The block carries facts, and the rules stay in the handbook.

## What stays out

- Method the agent already knows, such as language idioms, git usage, general engineering practice, or the steps of routine work.
- Any rule a tool enforces. A linter, formatter, type checker, hook, or test holds a rule more reliably than a sentence does, so the file names the command and leaves the rule to the tool.
- Records that have a place of their own: product behavior in `spec/`, the reason for a design in `docs/adr/`, a rule that holds across projects in the handbook. The file links to them.
- The description of the project for a person, which is in `README.md`.
- History, meaning what was tried, what changed, and why an old rule was dropped. Git keeps it.
- Guidance for one task.

## Shape

Open with what the repository is for. Give every other section a heading named after the question it answers, so an agent can find it without reading the rest. Write commands in code blocks, exactly as they run. A host that reads its own file name, such as `CLAUDE.md`, is a symlink to `AGENTS.md` or holds only `@AGENTS.md`, never a second copy.

## When an agent got something wrong here

The question is whether the agent lacked a fact about this repository that the file should have held. A missing fact goes in, in the section where it belongs. A missing method does not, because the agent could have worked it out, and a sentence telling it how would cost every later session to fix one.
