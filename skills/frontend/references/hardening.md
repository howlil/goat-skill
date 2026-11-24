# UI hardening

Use near the end of a non-trivial Build, or during a production-readiness Audit. It checks whether a correct-looking interface is fragile in implementation.

Hardening does not choose a visual direction, redesign layout, or replace the project's normal lint/test tools.

## Goal

Catch defects that commonly survive a visual pass: broken focus, unsafe async behavior, overflow, fragile form semantics, accidental motion, invalid responsive assumptions, and platform-specific edge cases.

## 1. Start from the changed risk

Do not run every rule on every component. Inspect only categories the diff can affect.

A local text-color change does not need form or async review. A new data table, dialog, or responsive workflow may need several sections.

## 2. Semantic interaction and accessibility

Check applicable behavior:

- actions use the platform's native/established interactive primitive;
- navigation remains real navigation, not click-only text;
- icon-only controls have an accessible name;
- keyboard users can reach and operate every action;
- focus is visible and is not hidden behind sticky/overlay UI;
- dialogs and transient layers restore focus sensibly;
- ARIA state matches real behavior rather than decorating markup;
- gestures have an alternate interaction unless the gesture is essential.

Automated accessibility tooling is evidence, not proof. Keyboard and focus behavior still need observation when the host allows it.

## 3. Async and state feedback

For changed async actions:

- pending state is visible;
- repeated activation cannot create an unintended duplicate effect;
- failure is never reported as success;
- recovery exists when retry can work;
- stale/partial data is marked when it changes a decision;
- unrelated actions remain usable unless the contract requires blocking them.

Product semantics such as retry count or automatic retry belong to the product/engineering contract, not this reference.

## 4. Forms

When forms change:

- labels remain visible and associated with controls;
- errors appear near the source and explain the next useful action;
- submitted failure preserves entered data when safe;
- input type, autocomplete, and platform keyboard hints match the field where relevant;
- paste is not blocked without a product/security requirement;
- submit/loading behavior is unambiguous.

## 5. Content and layout mechanics

Inspect the implementation for fragility:

- flex/grid children can shrink where text is expected to wrap or truncate;
- overflow is intentional, not hidden to conceal a layout bug;
- fixed heights have a real invariant behind them;
- text wrapping/truncation is deliberate;
- empty strings/arrays do not leave broken chrome;
- images/media reserve appropriate space to avoid unnecessary layout shift;
- layout relies on native layout primitives before JS measurement.

Framework-specific fixes are examples, not universal rules. Follow the target stack.

Use `references/layout.md` when the underlying structure is wrong and `references/stress.md` when realistic data is needed to reproduce the failure.

## 6. Motion

Defer detailed motion decisions to `references/motion.md`.

For hardening, only confirm:

- reduced-motion behavior exists where movement is non-essential;
- interactive motion can be interrupted or reversed when the interaction requires it;
- animation does not block the next valid action;
- broad "animate everything" transitions are not masking unrelated property changes.

## 7. Locale, theme, and platform boundaries

Only when supported by the product, check:

- date/number/currency formatting follows locale-aware platform APIs;
- translated text can grow without breaking layout;
- RTL keeps reading/focus semantics sensible;
- theme changes preserve contrast and native control legibility;
- safe areas/insets are respected for full-bleed or native-like layouts;
- zoom remains usable and is not disabled as a workaround.

## 8. Performance checks when the UI path changed

Do not speculate about scale.

Check only concrete hot paths:

- large rendered collections use an existing pagination/virtualization strategy when volume warrants it;
- render paths do not perform repeated layout measurements unnecessarily;
- expensive controlled inputs or derived calculations do not run more work than the interaction needs;
- image/media strategy fits the project's established performance pattern.

Performance optimizations require evidence of a relevant workload or existing project rule.

## Hardening gate

Before a non-trivial Build is reported as production-ready:

1. changed interaction semantics are keyboard/focus safe;
2. changed async/form behavior has honest pending/failure/recovery handling;
3. content and layout mechanics survive the valid input space;
4. relevant motion/theme/locale/platform behavior is checked or explicitly not verified;
5. no hardening rule introduced a new dependency or architecture without a requirement.

## Influence

This reference is an original Goat Skill synthesis informed by Vercel's Web Interface Guidelines and WCAG-style semantic/focus principles:
https://github.com/vercel-labs/web-interface-guidelines/blob/main/command.md
https://www.w3.org/TR/WCAG22/
