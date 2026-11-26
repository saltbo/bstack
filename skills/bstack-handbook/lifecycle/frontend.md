---
id: frontend
version: 2
audience: worker
applies: projects with a web frontend
---

# Frontend

## Decisions

- **Layout.** `src/app` for composition, providers, router, and shell. `src/routes` for thin entries. `src/features/<name>` for one capability each. `src/shared` for `api`, `config`, `observability`, `persistence`, `ui`, and `lib`. No global `components`, `hooks`, `services`, or `stores`. (2026-09)
- **Imports run one way.** Routes compose features through each feature's small public entry. Features do not import each other's internals, and `shared` imports no feature. An import lint that fails the build enforces this. (2026-09)
- **No backend-style layers for ordinary CRUD.** (2026-09)
- **Navigation state lives in the URL**, including search, filter, sort, page, tab, and the selected resource, so back, reload, and deep links work. (2026-09)
- **The query cache owns fetched data.** It is not copied into a store. A global store is only for state that truly crosses features. A multi-step flow is a reducer or state machine, not several booleans. (2026-09)
- **The typed client and its schemas are generated from the one contract** and never edited. Every runtime boundary is decoded with a schema, including API responses, URL state, and storage. No `as` or silent default gets past a failed check. (2026-09)
- **Updates wait for the server by default.** Optimistic updates are for low-risk reversible actions with a rollback. (2026-09)
- **UI is built from shadcn/ui at its latest version**, adapted where it is used and never by editing the installed component. Visual values come from tokens. `DESIGN.md`, in the [DESIGN.md format](https://github.com/google-labs-code/design.md), states them, and the theme's CSS variables carry the same values. (2026-07-31, 2026-09-08, 2026-11-26)
- **`UX.md` holds the product's own interaction rules**, which every page follows: which surface a task opens in, where global controls such as language and theme appear, what a list offers by default, how a destructive action is confirmed. General good practice comes from the UI skills in the [skill index](../policies/skills.md) and is not copied into it, so `UX.md` keeps only the choices a skill cannot make for this product, and where the two disagree `UX.md` wins. (2026-11-26)
- **Primary pages are for browsing and operating.** A create, edit, or settings form goes in a dialog, a drawer, or its own page. A list and a form do not share one dialog. (2026-05-24, 2026-09)
- **Errors appear where the user acted.** A field error sits by the field. A toast is for a result with no lasting place. A final error boundary catches the unexpected, so no page is ever blank. (2026-09-07)
- **User-facing text carries no technical detail**, stays short, and keeps button labels consistent. The layout explains, not extra labels. (2026-08-17, 2026-11-13)
- **Before a product has `UX.md` and `DESIGN.md`, apply a default quality bar**, so even a demo does not look like a draft. A redesign covers the whole component system across states and screen sizes. (2026-10-27, 2026-09-06)
- **A visual choice is shown as several complete variants side by side**, built in the project's real stack. (2026-07-31, 2026-07-09)
- **Sign-in is delegated to the OIDC provider.** The app builds no login or session layer. The access token stays in memory and is sent as Bearer. The ID token is never the API credential, and no token goes into browser storage. (2026-05-26, 2026-09)
- **Config comes from one backend endpoint**, not from build-time variables. (2026-06-28)
- **Stored browser data is versioned and decoded**, holds nothing sensitive, and is never silently replaced by defaults. (2026-09)
- **No raw HTML and no dynamic code.** Production sends a restrictive content security policy. (2026-09)
- **Accessibility target is WCAG 2.2 AA.** (2026-09)
- **An incomplete mock is completed in its own style**, without asking, and the PR shows the result. (2026-11-15)
