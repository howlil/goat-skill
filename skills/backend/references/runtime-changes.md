# Runtime changes

Use this when failures, retries, durable state, or rollout can change the outcome. Trace the real execution boundary and identify where the guarantee is enforced.

## State and effects

- Identify the authoritative record, the invariant it protects, and all writers that can affect it. Use the existing transaction, constraint, synchronization, or state transition when it can enforce the invariant. A check before a separate write may allow another operation to invalidate the check.
- Trace failure before and after each irreversible or externally visible effect. Decide whether retry is safe, how duplicate work is recognized, and where support can detect or recover incomplete work.
- For migrations, identify the versions of code and data that can coexist during deploy or rollback. Make migration steps resumable when they can be interrupted. Account for existing records with missing, unusual, or older shapes.
- For work across a trust boundary, validate inputs and protect credentials and sensitive data. Check authorization at the owner of the affected operation. Keep logs useful for diagnosis and exclude sensitive payloads they do not need.

## Verification and delivery

| Changed risk | Evidence to collect |
| --- | --- |
| Consistency or concurrency | Exercise competing writes or a failure at the commit boundary and verify the persisted invariant |
| Retries and external effects | Repeat delivery or interrupt the call around the effect and verify the final state and duplicate behavior |
| Compatibility or migration | Read representative old data with new code and exercise any supported mixed-version path |
| Latency or resource use | Measure the same workload before and after, with the input size and conditions recorded |
| Rollout or recovery | Identify the signal that tells an operator the change is healthy and exercise the relevant recovery step where practical |

Prefer existing tests and operational tooling. Use a focused new regression check when existing verification misses the failure. For an unresolved deployment or recovery condition, state what evidence is missing.
