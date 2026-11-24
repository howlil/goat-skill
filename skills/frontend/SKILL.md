---
name: frontend
description: "Design, implement, or review how consumers use software. Use for graphical UI, CLI commands and output, HTTP or event contracts, SDK and library APIs, schemas exposed to consumers, and device or agent interfaces. Skip internal behavior changes that preserve the public contract."
---

# Frontend

Own the public surface and the behavior a consumer can observe at it. A consumer may be a person, a program, or another system. Find the boundary from the consumer's point of view.

## Trace the interaction

1. Start with the request, any product acceptance, and the existing interface. Read the affected call sites, tests, conventions, and consumer documentation. For a small refinement, trace only the affected action or state.
2. Identify the actual consumer, entry point, valid inputs, visible outcomes, and material failure or recovery paths. Account for existing consumers and supported versions when a contract changes.
3. Reuse the established interface patterns and primitives. Give presentation and interaction state a single owner. Let the implementation that owns domain state decide domain outcomes, and translate those outcomes into the public contract.
4. Resolve feasible interface choices with the existing conventions. Bring in Product only when the intended outcome or acceptance needs a decision. Bring in Backend when the internals need to change to fulfill the contract.

For a read-only review, trace the same path and report evidenced findings by impact. For a change, drive the changed entry point with realistic inputs and check relevant failure behavior or compatibility. Report the observable result and any material checks still open.

## Load guidance for the surface

- Read `references/interface-contracts.md` for a new or changed programmatic interface, or a compatibility question. Cover inputs, output shape and errors, side effects, and how consumers evolve.
- For graphical UI, start with existing brand or design guidance, tokens, components, and interaction patterns. Preserve native semantics, keyboard and focus behavior, and visible pending, empty, error, and recovery states where reachable. Inspect the running baseline and use the smallest faithful runtime check the host supports.
- Read `references/layout.md` for composition or responsive changes. Use `references/visual-quality.md` for design-system choices and `references/anti-slop.md` for a new visual direction or generic-looking work.
- Read `references/ux.md` for navigation, multi-step flows, destructive actions, or uncertain interaction. Read `references/motion.md` for nontrivial motion.
- Read `references/stress.md` for realistic data, content, or viewport extremes, and `references/hardening.md` for touched production risks. Apply only the relevant checks.
- Read `references/examples.md` when a build or audit needs an example of the appropriate depth.

For visual changes, render affected states at representative widths. For programmatic changes, exercise the public command, endpoint, or exported API as a real caller would. Review visual or textual output for the consumer who relies on it, including assistive technology or automation when applicable.
