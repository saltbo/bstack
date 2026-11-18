---
name: bstack-writing
description: How to write and revise a Markdown file that people or agents read,
  such as AGENTS.md, README.md, a skill, or any other .md file. Use it whenever
  you create or change a .md file, including when a correction to an agent's
  behavior leads to changing the Markdown that instructs it.
---

# Writing

A model changes a document by adding to it. Asked to fix a behavior, it appends a sentence that corrects the old text, and leaves the old text as it was. Each addition looks reasonable on its own. Together they make a document that contradicts itself, says one thing in three places, and hides the sentences that matter among the ones that patch them. This skill replaces that habit. It does not teach writing, which you already know.

## What has to hold

- **The document reads as if written in one pass**, by one writer who knew everything that is known today. It carries no trace of its history: no sentence that answers a past incident, no word added to steer an earlier sentence, no exception to an exception.
- **Each subject has one home.** A fact, decision, or rule is stated in one place, and every other place that needs it links there.
- **Each sentence earns its place, and stays true.** A reader would act differently, or misunderstand, without it. What a capable reader already knows is left out, and so is anything the repository or the machine shows, such as what a file lists or what a command runs, together with any sentence saying where to find it. A copy of such a fact goes stale on its own, because nothing tells the writer when its source changes. What stays is what the reader would get wrong without being told: a decision, a fact the environment does not show, an exception to the usual.
- **Who reads the document decides what goes in.** The pages for each kind of document below say who that is.

## Changing a document

1. Read the whole document first. Where a change belongs depends on what the rest already says.
2. Treat a correction as evidence that the text is wrong, not as a new requirement. Find the sentence that produced the wrong result, or the gap where no sentence existed. If the text already stated what was wanted, the text is not at fault, and it gets no new line.
3. Rewrite that sentence where it stands, so that it says the right thing the first time. Add a sentence only when nothing existing covers the case, and put it in the section its subject belongs to, not at the end and not under a heading for notes.
4. Where the new statement overlaps an old one, merge the two. Where it contradicts one, decide which is right and delete the other.
5. Read the whole document again as a newcomer would, against the signs below. A change that fixes a behavior usually leaves the document no longer than it was. If yours grew, name what the new lines say that nothing said before.

A new document starts the same way. Decide what each section is for before writing it, and give every subject one section.

## Signs of a patch

- A word that steers other text: note, important, also, remember, make sure, again, in addition, except when. Rewrite the sentence it steers, and the word goes with it.
- Emphasis that makes one rule weigh more than its neighbours, such as capitals. When a rule is ignored, its reason is missing or another sentence competes with it, and emphasis fixes neither.
- A prohibition that narrows a permission stated elsewhere, as in "do X" followed later by "do not do X when Y". Write one accurate statement of when to do X.
- A rule without its reason, where the reason is not obvious. A reader cannot judge a case the rule did not foresee, and the next failure gets another rule.
- The same subject in two places, or a summary that restates the body below it.
- A shape the content does not have: a heading over a single line, a list whose items are one chain of reasoning, a table whose rows are sentences.
- A sentence no reader would miss.

## By kind of document

| Document | Read |
| --- | --- |
| `AGENTS.md`, `CLAUDE.md`, and other instructions an agent reads on entering a repository | [agents-md](references/agents-md.md) |
| `README.md` | [readme](references/readme.md) |
| A skill, and other agent instructions kept as Markdown, such as a subagent or command definition | [skills](references/skills.md) |

Any other Markdown file follows this page alone. Where the [handbook](../bstack-handbook/lifecycle/project.md) gives a record its own place, such as product behavior in `spec/` or the reason for a design in `docs/adr/`, a document links to it instead of restating it.
