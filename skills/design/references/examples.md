# Worked examples

All examples are illustrative: the repo facts are invented to show shape and size. Match the proportion, not the content.

Never reuse names, paths, findings, or decisions from these examples. A real report contains only what you found and did in this repo.

## Contents
1. Small refine
2. Build with reuse decisions
3. Audit
4. The failure to avoid

## 1. Small refine

Request: "The Save button gives no feedback while saving."

```
Done: Save shows a pending state and an inline error with retry; success returns to the idle label.
Reused: existing Button (pending support) | Created: none
Verified: typecheck and lint pass; in the running app, saving disables the button and shows the pending label, a forced failure shows the error and retry works.
Not verified: narrow-width layout.
Adjacent findings: the display-name field uses a placeholder as its only label.
```

Why it is enough: one change, three checks, and the unrelated problem was reported, not fixed.

## 2. Build with reuse decisions

Request: "Add a recent-items list to the sidebar."

```
Done: the sidebar shows the five most recent items, with empty and error states; selecting one opens it.
Reused: existing List and Button components, the router for the selected item | Created: RecentItems (feature-local); nothing existing rendered a keyboard-navigable list with this data shape.
Verified: typecheck, lint, and the affected tests pass; keyboard navigation reaches each item and Enter opens it; empty and error states rendered and compared with the baseline.
Not verified: behavior with more than 100 items.
Adjacent findings: none.
```

Why it works: the reuse decision names what was checked, the new component is justified in one clause, and the gaps are stated.

## 3. Audit

Request: "Audit the settings page for accessibility and architecture. Do not change anything."

```
1. [high] settings-form.tsx:41 - a clickable div toggles notifications. Observed: it has no role or key handling, and Tab skips it. Fix: use a native button or the project's Switch.
2. [medium] settings-form.tsx:18 - display name is mirrored from props by an effect. Observed: reading the code; two renders per change. Fix: compute it during render.
3. [low] settings-form.tsx:77 - hard-coded color. Observed: a hex literal where a token exists. Fix: use the semantic token.
Not verified: screen-reader announcements (no assistive technology available).
```

Why it works: each finding has a location, something observed, and a fix, ordered by user impact, with no edits made.

## 4. The failure to avoid

A request to show a pending state on one button came back as a new shared button primitive, a motion preset module, a restructured settings folder, and a long report claiming everything was verified, while nothing had been run. If a change would not alter what the user asked for, leave it out; if a check did not run, say so.
