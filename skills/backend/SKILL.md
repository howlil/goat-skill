---
name: backend
description: "Implement or review how software works behind its public interface. Use for domain rules, authoritative state, data storage and migrations, algorithms, concurrency, integrations, runtime execution, performance, reliability, and operating changes. Includes local tools, libraries, firmware, and infrastructure."
---

# Backend

Own internal behavior, authoritative state, and execution. Work from the requested outcome and the existing or agreed public contract. Start here for implementation work behind a fixed contract.

## Trace the changed path

1. Find the real entry point, relevant callers, authoritative state, and current behavior. Trace the inputs, decisions, state transitions, side effects, and result at the necessary depth.
2. For a defect, establish the failure with the cheapest faithful reproduction available. For a change, name the invariant, transition, or runtime guarantee that must hold.
3. Put the change in the existing owner. Reuse its established boundaries and mechanisms. Make invalid transitions hard to express and enforce authorization where protected state or capabilities are controlled.
4. Account for plausible failure and interruption. If the operation can be repeated, run concurrently, or fail partway, define what is committed, what a retry can do, and what the caller observes. Consider existing persisted data and supported versions.
5. Verify through the normal entry point or the closest boundary that can fail for the same reason. Exercise a material failure, retry, or concurrency case when the change affects it. Measure a baseline and rerun the same workload for performance claims.

Bring in Frontend when caller-visible inputs, outcomes, errors, or compatibility must change. Bring in Product when the intended outcome or acceptance needs a decision. Keep those decisions in the existing task when possible.

## Match the checks to the risk

Read `references/runtime-changes.md` when the change involves durable writes, concurrency, external effects, operational recovery, or a rollout. Check only the guarantees this change touches. Use operational evidence for operational claims.

For a review, report the reachable behavior, its impact, and the smallest fix direction. For implementation, report the changed behavior and proof observed, including any material verification limit.
