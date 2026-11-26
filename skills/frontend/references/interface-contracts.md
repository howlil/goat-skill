# Programmatic interfaces

Trace an actual call through the public entry point. Look at released types or schemas, examples, and real callers to distinguish existing guarantees from new choices. Preserve accepted inputs, defaults, output and error shapes, side effects, resource lifetime, and compatibility where consumers rely on them. Check ordering, units, timeout, or cancellation where they affect a caller's next action.

- CLI: Check flags, exit status, and both streams. Keep stdout machine-readable where scripts consume it and send human diagnostics to the established error channel.
- HTTP and events: Preserve schema and error discriminants. Check pagination and ordering when promised, and delivery, retries, or repeated effects when a request or event can recur.
- SDK and library: Check exports, public types, synchronous or asynchronous behavior, and failure and disposal semantics.
- Devices and agents: Check advertised capabilities, commands and signals, acknowledgement, units, observable failure, and recovery.

Reuse the surface's error convention. Give automated callers a stable way to distinguish failures that require different recovery. Preserve existing side effects on success and make any work committed before failure intelligible to a retrying caller. The implementation that controls the protected resource enforces its authorization and invariants.

If a break is necessary, identify affected callers and the explicit change path. Exercise the real CLI, production router, or public library export. When compatibility is the risk, run an existing consumer with realistic input through both success and the affected failure.
