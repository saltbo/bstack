# Skills and other agent instructions

This page covers a skill's `SKILL.md` and its references, a brief handed to another agent, and a system prompt. The reader is a capable model that follows the text closely, including the parts that were written carelessly.

## What goes in

- **Information**, meaning what the model cannot work out by itself: what the owner decided and why, facts about the environment, who holds which role, and the process the work moves through, that is, who hands what to whom and when something counts as done. A process is information, and it stays.
- **Goals**, meaning the results that have to hold, such as "nothing of the PR is left behind after a merge".

Execution is left to the model: which command to run, with which flags, in which order. A tool is named when the choice of tool is itself a decision, or a fact the model could not guess, and how to call it is still left to the model.

A rule carries its reason where the reason is not obvious, so the model can judge a case the rule did not foresee. A rule says what to do. A prohibition names the wrong path and leaves the right one to be guessed. A constraint that has to hold every time belongs in code, such as a hook, a schema, a validator, or a permission, and the text is left for what needs judgment.

## The description

The host reads only the description when it decides whether to load a skill. It says what the skill does and the situations it is for, in the words a user or an agent would use when such a situation comes up. It is not a summary of the body. A skill that is loaded only on request says so.

## Layout

`SKILL.md` holds what every use of the skill needs. A reference holds what one branch of the work needs, and `SKILL.md` says when to read it. References are linked from `SKILL.md` directly, never from one another in a chain. A skill links to another skill or to the handbook rather than restating it. In bstack, `tests/test_bundle.py` sets a line budget for each file, and a budget is raised only with a reason.

## Changing a skill

The evidence is what the skill made an agent do. Where there is a transcript, read which sentence the agent followed or cited, and revise that sentence as [the steps for changing a document](../SKILL.md#changing-a-document) describe. One bad run gets one corrected sentence, not a new rule for each thing that went wrong.

A revision is proved by behavior, not by reading it back. Run the case that failed again, in a fresh session, and see whether the behavior changed.
