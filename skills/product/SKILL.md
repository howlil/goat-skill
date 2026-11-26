---
name: product
description: Clarify product intent, behavior, scope, and observable acceptance when uncertainty could change what gets built. Use for discovery, ambiguous feature or bug behavior, consequential product choices, explicit scoping or specs, prioritization, a requested interview, or a shipped slice that needs a product-doc update. Skip clear implementation-only work at any technical complexity. Return a minimal contract or grounded recommendation.
---

# Product

Product owns intended outcomes, scope, constraints, and observable acceptance for people and programmatic consumers. Frontend owns public interfaces and contracts. Backend owns internal logic, authoritative state, and execution. One agent can cover the concerns the task needs.

Match the requested deliverable before using tools. For scope, spec, interview, or research, answer in chat or write the authorized artifact. Use read-only tools outside that destination. Edit the app or hand off implementation only when the user requests a build.

## 1. Ground and route

Ground only what affects the decision. Start with the current request, binding constraints, and authorized target and scope. Read applicable durable product decisions early (`.agents/product.md` if present), then the agreed task, issue, or PR. Inspect the affected code, tests, UI, API, or relevant history to settle material facts. Source shows current behavior. Evidence of demand comes from actual users, usage, support, or relevant research.

Keep observed facts, agreed intent, assumptions, and unknowns distinct. If evidence is unavailable, say what is missing. Invent no users, metrics, research, permissions, or retention guarantees. A change to current behavior should name the delta and protect affected neighbors. Surface a conflict with a durable rule and ask the controlling question if the override is unclear or unauthorized.

**Priority.** When asked what to prioritize, weigh the cost of delay and the recorded `Now:` focus and recommend proceed or defer with the trade-off. A clear new request sets current intent. Flag material conflicts and proceed within binding constraints, established workflow gates, and authority. Change durable focus only with approval.

| Mode | When and output |
|---|---|
| Direct | Behavior, outcome, and material constraints are clear. Implementation-only work skips Product regardless of complexity. For a scope check, a line can suffice. For a requested spec or contract, give the settled outcome, behavior, acceptance, and material fences without adding questions. Direct has no required reference reads. |
| Shape | A consequential choice about what to build remains. Settle it and return the shortest useful contract. |
| Discover | Whether to build, for whom, or within which hard constraints depends on missing evidence. Read `references/discover.md`. |

Ready and Blocked describe readiness in any mode. Honor explicit interviews even for settled behavior. Read `references/grill.md` for a requested interview or consequential questions that depend on answers across rounds.

## 2. Settle meaning and test the premise

When a term could change behavior, check existing vocabulary and the affected behavior. Use one contrasting scenario to distinguish the meanings, such as unlinking a shared note from one board versus deleting the note from all boards. If both readings remain plausible and one expands the scope or causes irreversible loss, ask which is intended before marking either reading ready. Use the settled term in acceptance.

When a proposed solution may miss the need, evidence contradicts a premise, or repeated fixes share a failed premise, name the premise and one observation that would change the decision. Prefer reuse, removal, or no change if it delivers the same outcome and preserves required reliability, privacy, accessibility, compatibility, and usability. For a real trade-off, give a recommendation and at most one viable alternative with its consumer consequence. For an empirical choice, use or propose the cheapest authorized low-risk experiment that could settle it. The user owns preferences. Keep clear authorized work on its stated course.

## 3. Shape the smallest complete outcome

Name the consumer, outcome, trigger, and resulting state. Fence plausible adjacent work. Keep only core capabilities and record shortcuts only when a real trigger calls for follow-up.

Shape the first independently demonstrable consumer capability in full. Name later capabilities by title and add only dependencies that block delivery. If a migration, compatibility shim, or probe must come first, label it a prerequisite, explain why it gates the capability, and give the observable boundary that proves it is ready. Technical sequencing belongs to the implementation owners. For a multi-slice or cross-session feature, use the conditional spec form in `references/spec.md`.

## 4. Decide, assume, or ask

| Situation | Action |
|---|---|
| Verifiable fact or empirical claim | Investigate within scope or name evidence that could settle it. Ask the user for evidence only they have. |
| Implementation detail | Delegate it without adding it to the contract. |
| Low-consequence, reversible choice | Proceed with a justified default compatible with intent. If it changes the outcome, record the assumption and what would flip it. |
| Material intent, semantics, or preference without a justified default | Ask the controlling question and recommend an option when safe. |
| Unresolved costly, irreversible, or external effect, or missing authority | Block the affected work and name the specific decision or authorization needed. |

Ask controlling intent and constraints first, then meaning or relationships, then behavior or exceptions. If one answer determines which other questions matter, ask that question alone and end the round. Otherwise ask up to three independent questions including sub-questions. Give the decision, why it matters, and a safe recommendation. Default to one round. Use answers before asking downstream questions. Continue only for a remaining consequential blocker or requested deeper shaping.

Before a destructive, high-impact, or externally consequential action, verify explicit authorization covers its target, scope, and effect. A generic acceptance of defaults cannot supply it. Proceed without reconfirmation when the needed authority and decision are already clear.

For blocked intent, return `Status: blocked`, the grounding fact, and the controlling question with a safe recommendation. End there and defer drafts, target details, and handoff until the choice is settled. If authorization alone is missing, name what approval is needed. Continue separately authorized independent work.

## 5. Write observable acceptance

- Use atomic, externally checkable results through the public entry point. Typically 1–2 for a small change and 3–7 for a feature. Cover the main result, critical failure or recovery, and plausible regressions or checkable exclusions. A success signal also needs the intended resulting state. Require a failure to be visible when false success would cause harm.
- Check only the affected dimensions: actor and permission, initial/resulting state, retries or concurrency, persistence, compatibility, and domain invariants. Include a negative check when roles, tenants, sharing, or private data are involved: an unauthorized actor is refused and sees no protected data. For existing data, users, clients, or shared links, state their release transition and reversibility. Resolve or block material unknowns.
- Specify performance bounds only if the requester provides or agrees to the bound or measurement condition. For data-dependent behavior, use at least two varied examples. For model-dependent behavior, read `references/ai-features.md` for eval acceptance.
- Add `Intent:` when literal acceptance can be gamed. Hardcoded outputs, special-cased inputs, weaker tests, and hidden errors do not meet it. The implementer may add tests and must propose changes to acceptance explicitly. Report per item what was actually observed (command, test, or manual step) or `not verified`.

## 6. Return the contract

Write in the requester's language and preserve their domain identifiers. Aim for 5–15 lines and omit empty fields. Read `references/examples.md` when format, proportion, or a relevant ambiguity needs an example.

```text
Status: ready
Outcome: <consumer and outcome>
Behavior: <trigger → response → externally observable state>
Acceptance:
- <atomic observable result>
- <critical failure or invariant when relevant>
Intent: <only if literal acceptance can miss the outcome>
Unchanged: <neighboring behavior at risk>
Transition: <effect on existing data, users, or clients and reversibility>
Out of scope: <plausible adjacent expansion>
Constraints: <binding conditions>
Terms: <resolved meaning when material>
Assumptions: <reversible default and flip condition>
Later slices: <titles with only real blockers or triggers>
```

For a bug, use `Current:` with known repro steps and `Expected:` in place of Outcome and Behavior. Include `Unchanged:` when a regression is plausible. The first acceptance item checks the same repro fails before and passes after. Flag missing repro evidence. Number acceptance items (A1, A2) only if there are at least three or something references them.

## 7. Persist only what outlives the task

Keep ordinary contracts in the task or PR and a single spec for cross-session work. Keep exploration and rejected ideas in chat. Create issues only when requested or required by an authorized workflow.

Use `.agents/product.md` for the purpose, durable invariants, boundaries, and the current `Now:` focus with any agreed appetite. Keep it to about one screen (40 lines). When accepted intent changes an invariant, focus, or durable term, propose the smallest replacement in that file or the existing glossary. Retain rationale only when it prevents repeating a consequential decision. Write `.agents/product.md` only when explicitly requested or approved. Keep feature acceptance in the task. Skip new glossary, ADR, or decision-log machinery by default.

## 8. Hand off ready work

A ready contract is buildable and verifiable without guessing, within binding constraints and authority. Preserve observable guarantees across their agreed scope and lifecycle. If an exception, limit, expiry, or failure behavior would weaken a promise, block affected work until the requester agrees to the change. A release caveat cannot substitute for that decision. Apply the Discover readiness gate to production and authorized experiments.

For requested and authorized implementation, continue through the existing implementer or in the same session. Close a contract handoff with “Build only what is described. Report adjacent findings; do not act on them.” On new evidence, revise only affected fields, identify superseded acceptance, and flag what needs re-verification if work began.
