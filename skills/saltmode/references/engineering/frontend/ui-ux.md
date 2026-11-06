# UI/UX Design And Components

Use these preferences for new design. Preserve existing architecture and supported
behavior unless the task includes changing them. Apply checks to the affected
capability; formal project-wide CI governance is a separate task.

## Organize Pages Around User Tasks

Make the page's purpose, current context, primary action, and next step legible.
Use a clear information hierarchy and consistent navigation. Group content and
controls by the user's task rather than backend modules or implementation details.
Reuse the project's design system and established interaction vocabulary.

Primary content pages prioritize browsing, scanning, and operating existing data.
Search, filters, sorting, and navigation controls may remain on these pages.
Create, edit, and configuration forms belong in a modal, drawer/sheet, or dedicated
secondary page. Use a contextual surface for short work and a secondary page for
long, multi-step, linkable, or recoverable tasks. This is a UI/UX design preference,
not a restriction on every HTML form element.

Apply this preference to every surface the change touches. Preserve supported
user workflows.

Adapt content and actions to narrow and wide viewports without losing hierarchy,
keyboard access, or task continuity. Preserve entered data through recoverable
failures and navigation where the workflow requires it. Size confirmation, undo,
and pending feedback to the consequences of the action.

## Build Coherent Components And Forms

Use semantic HTML and mature accessible UI primitives. Let `shared/ui` own
stable design-system behavior, semantic tokens, focus rules, and visual
contracts. Let feature components own domain meaning. Create a shared wrapper
only when it enforces real product semantics, accessibility, or repeated
interaction behavior; do not make one-to-one wrappers that merely rename a
native element or library primitive.

Keep component interfaces semantic and small. Prefer composition over a matrix
of styling and behavior booleans. Split a component when it owns unrelated
state, orchestration, or interaction responsibilities, not to satisfy a line
count. Keep feature data orchestration out of low-level visual components.

Use platform form behavior and direct state for a simple form. Use a mature form
library for dynamic fields, conditional sections, complex validation, or
multi-step recovery. Do not force every form through a universal abstraction.
Use the authoritative schema when its semantics match, map stable server errors
back to the relevant field or form, preserve input, and make pending and
duplicate-submission behavior explicit.

Choose the repository's styling technology, but keep stable visual decisions in
semantic design tokens. Scope feature styles locally. Do not introduce global
selectors that affect unknown surfaces or copy hard-coded values when an
appropriate token exists.

## Model Rendering And Failure Deliberately

Design applicable success, initial loading, background refresh, empty, stale,
partial, validation, authentication, authorization, conflict, offline,
uncertain-result, and unexpected-failure states with the feature. Do not add
them as generic spinners and error pages after implementation.

- keep usable content visible during background refresh when its age and stale
  state are explicit and safe;
- place field validation next to the field and actionable operation failure next
  to the operation;
- use a route or content-region failure state for failed loading while keeping
  unaffected content usable;
- preserve input after recoverable failure and move focus to useful feedback;
- prevent duplicate submission while allowing a deliberate retry after the
  previous outcome is known;
- size confirmation and undo behavior to the consequence of destructive work.

Use Toast only for a result with no natural persistent location, such as a
background action completed after its initiating surface disappeared. Do not
make Toast the default error channel. Use Error Boundaries for unexpected render
failures at a scope that can fail independently; do not route expected query or
mutation errors through them and do not wrap every component defensively.

## Verify Accessibility In The Changed Interface

Accessibility is part of the interface contract. Check the affected interface
locally and honor adopted release gates; do not require unrelated CI construction
for a local UI change. Use
[WCAG 2.2](https://www.w3.org/TR/WCAG22/) AA as the default conformance target
unless the product or regulation sets a stricter one. Require:

- semantic elements and native controls before custom widgets;
- programmatic labels, meaningful headings, visible focus, complete keyboard
  operation, and correct accessible names and states;
- deliberate focus restoration or movement after dialogs, route transitions,
  validation failure, and inserted content;
- appropriate announcements for dynamic content without noisy repetition;
- meaning that does not depend on color alone, sufficient contrast, usable
  target sizes, reduced-motion support, and user font-size resilience.

Run semantic lint, automated accessibility checks, and interaction tests through
roles, names, and keyboard behavior. Exercise focus, navigation, and critical
flows in a real browser. Manually inspect changed high-risk UI because automated
scans do not prove usability. Do not waive a failure because a third-party
component caused it; the product owns the delivered interface.
