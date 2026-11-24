---
name: frontend
description: "Design, implement, or review how consumers use software. Use for graphical UI, CLI commands and output, HTTP or event contracts, SDK and library APIs, schemas exposed to consumers, and device or agent interfaces. Skip internal behavior changes that preserve the public contract."
---

# Frontend

Own the public interface and observable behavior for people, programs, and other systems. Find the boundary from the consumer's point of view.

## Trace the interaction

1. Start with the request, acceptance, and current interface. Read the callers, tests, conventions, and docs that affect the change.
2. Identify the consumer, entry point, inputs, outcomes, and material failure or recovery paths. Account for existing callers and supported versions when a contract changes.
3. Reuse interface patterns and primitives. Give presentation and interaction state one owner. Translate domain outcomes at the public boundary.
4. Resolve feasible interface choices with the existing conventions. Bring in Product only when the intended outcome or acceptance needs a decision. Bring in Backend when the internals need to change to fulfill the contract.

For a review, report observed findings by impact. For a change, exercise the public entry point with realistic inputs and verify relevant failure behavior and compatibility. Report what was observed and any material gaps.

For a local tweak, inspect the affected surface and use its closest faithful check. Use a running UI when the rendered result or interaction needs direct proof. Check representative widths when layout or responsiveness changes.

## Load guidance for the surface

Start with the reference that answers the most important open question. Read another when a separate decision or verification risk still needs guidance.

- Read `references/interface-contracts.md` for a new or changed programmatic interface, or a compatibility question. Cover inputs, output shape and errors, side effects, and how consumers evolve.
- For graphical UI, reuse established components, tokens, and interaction patterns. Preserve native semantics, keyboard and focus behavior, and visible pending, empty, error, and recovery states where reachable.
- Read `references/layout.md` for composition or responsive changes. Use `references/visual-quality.md` for design-system choices and `references/anti-slop.md` for a new visual direction or generic-looking work.
- Read `references/ux.md` for navigation, multi-step flows, destructive actions, or uncertain interaction. Read `references/motion.md` for nontrivial motion.
- Read `references/stress.md` when realistic extremes pose a material risk to the changed surface, and `references/hardening.md` for a specific implementation risk that needs another check.
- Read `references/examples.md` when a build or audit needs an example of the appropriate depth.

Review output as the actual consumer would, including assistive technology or automation when applicable.
