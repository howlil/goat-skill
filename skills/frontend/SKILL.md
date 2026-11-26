---
name: frontend
description: "Design, implement, or review public interfaces and consumer-visible behavior in GUI, CLI, HTTP and events, SDKs and libraries, and device or agent interfaces. Skip mechanical edits and internal changes that preserve the public contract."
---

# Frontend

Find the actual consumer, normal entry point, and accepted behavior. Inspect the callers, contracts, neighboring surfaces, or tests that can settle a choice. For a mechanical edit, change only the affected surface and use its closest faithful check.

Use established primitives and the existing owner when their contracts fit. Give interaction state one owner and translate domain outcomes at the public boundary. Product owns intent, scope, and acceptance. The trusted implementation owns authoritative state, authorization, and domain invariants. Resolve local choices from evidence. Clarify ambiguity when the answer changes a consumer guarantee or the intended outcome.

Trace the changed action from entry and preconditions to the observable result and next available action. Preserve existing callers and consider reachable failure and recovery. For defects, reproduce cheaply through a boundary that fails for the same reason. Verify through the normal entry point with realistic inputs and check what a real consumer observes, including material failures or compatibility risks. Use a running UI when behavior or rendering needs direct proof. For an audit, report reachable defects with evidence and impact. State any material verification gaps.

Read a reference only when it can change a decision or a consequential check.

- [Architecture](references/architecture.md) for disputed state ownership, lifecycle, or whether to share behavior.
- [Interaction](references/interaction.md) for async flows, recovery, focus across layers, or interruptible motion.
- [Visual](references/visual.md) for composition, visual direction, or layout that must hold under realistic extremes.
- [Interface contracts](references/interface-contracts.md) for changes callers may depend on, including error and retry semantics.
