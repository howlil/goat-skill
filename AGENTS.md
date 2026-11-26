# Engineering

Deliver the simplest complete, correct, maintainable change with evidence.

- Product owns intent and expected behavior. Frontend owns public interfaces and contracts. Backend owns internal logic, authoritative state, and execution. Use the concerns the task actually changes.
- Preserve compatibility and keep responsibilities with existing owners that can support the required behavior. Add an architectural boundary only when state, lifecycle, authority, or a public contract needs independent management. Reuse existing primitives, fix root causes, and encode invariants at the boundary that owns them. Remove obsolete paths when the change replaces them.
- Understand the relevant behavior, make the smallest complete change, and verify it through its normal entry point. Resolve uncertainty when it changes the outcome or risk.
- Read selectively and report the evidence you observed. Capture durable decisions and turn recurring failures into enforceable checks.
