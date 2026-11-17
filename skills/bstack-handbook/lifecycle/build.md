---
id: build
version: 3
audience: worker
applies: all
---

# Build

## Decisions

- **Analyzing a bug and fixing a bug are different jobs.** An analysis ends in a diagnosis with evidence and changes no product code. A fix starts from a reproduction and ends with that reproduction passing.
- **Reproduce before changing anything.** Keep the command. It is the first acceptance criterion of the fix.
- **Fix the cause.** When two fixes built on the same belief have failed, test the belief before writing a third.
- **The most correct change within the criteria.** Anything else noticed on the way is a follow-up. When the existing design is wrong for the task, refactor it instead of stacking on top. A refactor changes the design, and a mechanical move leaves it as it was. (repeated, 2026-06 to 2026-09)
- **No fallbacks.** One stable path, and a loud error when it fails. Do not hide a gap behind a default or a second attempt. (repeated, 2026-01 to 2026-08)
- **When code the task touches disagrees with the handbook, the stage decides.** In a development project, bring that code into line as part of the task and keep nothing of the old shape. In a live project, keep the existing shape for this task and file an issue so the migration is planned. A new piece is never written to match an old piece the handbook says is wrong. (2026-11-15)
- **Compatibility follows the project's stage.** In a development project, write none and delete the old path. In a live project, it is owed only to a released version that real users depend on, and it lives in one place that is easy to delete. (repeated, 2026-07-30, 2026-08-02)
- **Use mature libraries and the platform's own features** for standard protocols and common needs. Do not hand-roll them, and do not work around an outdated dependency when it can be upgraded. (repeated)
- **Stay inside what was asked.** Do not take on old unrelated problems or invent extra questions. (2026-09-04)
- **Keep configuration minimal.** Delete unused environment variables, keep fixed values in code, and use a secret only for a real secret. (2026-09-04)
- **Find the cause from real observed data**, not from a guess, and say whether it is one case or a systemic problem. (2026-07-24)
- **Reduce a bug to the smallest reproduction**, trace it through the real public seam, and remove temporary instrumentation before finishing. (2026-09)

## Measuring performance

Before reporting a performance number, write the claim in the words you would ship and answer each question from a run. A quick ballpark may be one run, says so, and still answers questions 4 and 7.

1. **What limits it?** Name the limiter, and profile in a run you do not report.
2. **Was each side tuned?** Both sides run the way production runs them, on the same data.
3. **Does it break a limit?** Do the arithmetic. A result past a physical limit measured something else.
4. **Did it error?** Count failures and check the outputs are correct.
5. **Does it reproduce?** At least five runs per side, alternating, reported as median and range.
6. **Does it matter?** Give a micro result as a share of the path a user waits on.
7. **Did the work happen?** Confirm the timed region did the work.

Lead with the verdict, which is faster, slower, no measurable difference, or inconclusive. Give the number with its unit, run count, range, and limiter. Try the cheap fixes first, which are to skip the work, do it once, do less, do it later, and do it concurrently.
