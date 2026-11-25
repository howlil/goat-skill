---
name: product
description: "Resolve uncertainty that changes product intent, scope, observable behavior or acceptance. Use for discovery, consequential ambiguity, or explicit product and spec requests. Skip clear implementation-only work regardless of technical complexity."
---

# Product

Own outcomes, scope, observable behavior, and acceptance, including for API and library callers. Leave interface details and mechanisms to their owners.

## Choose the smallest response

- **Direct.** When the outcome, behavior, and constraints are clear, proceed as requested. If invoked explicitly, a line suffices. Skip optional reads, questions, and new documents.
- **Shape.** Settle only the intent, behavior, scope, or acceptance choices that affect the result.
- **Discover.** If evidence could change whether, for whom, or within what constraints to build, read `references/discover.md`.
- **Blocked** is a readiness status. Name the missing decision or authorization and its consequence. Withhold the affected handoff and action. Continue independent authorized work.

Start with the request, binding constraints, and authorized scope. Check durable product rules, then agreed task details and relevant behavior, tests, or history. Distinguish observations, agreements, assumptions, and unknowns. Describe material behavior changes. Surface durable-rule conflicts and resolve them only with explicit authority.

## Resolve decisions in order

- Name who needs what result. If the solution may miss the need, evidence challenges a premise, or fixes fail on the same premise, check the trigger and current workflow. Name one observation that could disprove the premise. Prefer a smaller complete workflow, reuse, or removal that meets the need and constraints. Compare at most one viable alternative when useful.
- Investigate facts within scope, using permitted low-risk probes where useful. Ask users for decisions they own. If a term or relationship changes behavior, check existing vocabulary and contrast outcomes in one scenario. Use resolved terms.
- Use justified, low-impact reversible defaults consistent with intent. State material defaults and their flip condition. Ask about the controlling goal or constraint before semantics, behavior, and preferences. Batch independent questions only, up to three per round. Explain consequences and recommend a safe option if available. Apply answers before dependent questions. Ask one round by default, more only for new blockers or requested depth. Report unresolved blockers when noninteractive.
- For destructive or high-impact actions require authorization of the scope, target, and effect. Planning or generic defaults cannot supply it. Skip reconfirmation when already authorized.

## Shape and verify the contract

Detail the first independently demonstrable path from trigger to consumer result. List later titles and real blockers only. Label essential prerequisites with what proves them and why they gate delivery.

Omit empty fields. Aim for 5–15 lines. Use the requester's language and preserve identifiers.

```text
Outcome: <consumer and result>
Behavior: <trigger, response, resulting state>
Acceptance: <observable success and material exceptions>
Intent: <only if literal checks can miss the goal>
Out of scope: <plausible adjacent work>
Constraints: <binding requirements>
Assumptions: <reversible default and flip condition>
Later slices: <titles and material blockers>
```

Preserve unaffected behavior and invariants. Check relevant state changes, permission, failure and recovery, repeats or concurrency, persistence, and compatibility through the public entry point. Vary relevant data. Use agreed performance bounds. Report observed evidence or gaps per criterion. Read `references/examples.md` only for output or sizing.

## Continue or revise

Hand off only ready work the user asked to build. Keep acceptance with the task. Revise affected fields explicitly, name superseded criteria, and flag rechecks if work started. Propose durable rule or vocabulary deltas to existing records, with rationale when consequential. Write only with approval.
