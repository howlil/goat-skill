# Interface architecture

Choose the owner by following who can change the value, who needs it, and when it should reset. Derive values from authoritative state. Store a second value only when it has its own lifecycle, such as an editable draft or a snapshot that must survive changes to the source. Lift state only to the closest owner that coordinates the consumers and can clean it up when their shared task ends.

Keep similar surfaces local when their transitions, dependencies, or lifetimes differ. Share a stable primitive for the common part. Reuse or extract a behavior or invariant when real consumers must change together and divergence would cause a defect. Give the shared owner that common contract and keep each consumer's policy at its own boundary.

Use another feature's public contract. Separate presentation from infrastructure when either side needs independent authority, lifecycle, or verification. A new layer earns its place by making one of those guarantees easier to enforce. Verify that each consumer retains its behavior after moving ownership.

Use a real workload or a measured bottleneck to choose caching, memoization, virtualization, or other performance work. Check that it improves the affected path while preserving freshness, ordering, and access to results where relevant.
