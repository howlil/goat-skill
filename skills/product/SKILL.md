---
name: product
description: Clarify product intent, behavior, scope, and observable acceptance when uncertainty could change what gets built. Use for discovery, ambiguous feature or bug behavior, consequential product choices, explicit scoping or specs, prioritization, a requested interview, or a shipped slice that needs a product-doc update. Skip clear implementation-only work at any technical complexity. Return a minimal contract or grounded recommendation.
---

# Product

Resolve decisions that change consumer outcomes, scope, constraints, or proof. A consumer can be a person, an operator, a library user, or another service. Product defines intended outcomes and observable behavior. Frontend owns public interfaces and contracts, including API, library, and CLI surfaces. Backend owns internal logic, authoritative state, and execution. The same agent can act in any of these roles.

Check the requested deliverable before using tools. For scoping, planning, spec, interview, or research alone, use read-only tools and answer in chat. A named artifact may be written when authorized. A proposal to change behavior is part of that output. Editing the product or dispatching implementation requires a build request.

## 1. Ground and route

Ground only what affects the decision. Start with the current request, binding constraints, and authorized target and scope. Read applicable durable product decisions early (`.agents/product.md` if present), then the agreed task, issue, or PR. Inspect the affected code, tests, UI, API, or relevant history to settle material facts. Source shows current behavior. Evidence of demand comes from actual users, usage, support, or relevant research.

Keep observed facts, agreed intent, assumptions, and unknowns distinct. If evidence is unavailable, say what is missing. Invent no users, metrics, research, permissions, or retention guarantees. A change to current behavior should name the delta and protect affected neighbors. Surface a conflict with a durable rule and ask the controlling question if the override is unclear or unauthorized.

**Priority.** Use the recorded `Now:` focus or the requester's current goal. Continue work that serves it, trivial fixes cheaper than discussion, and work that stops harm (name the preemption briefly). For an off-focus nice-to-have, give `Status: blocked - not a priority`, the focus, and what would change the call. Save nothing. Honor an explicit requester override and note it once.

| Mode | When and output |
|---|---|
| Direct | Actor, behavior, outcome, and material constraints are grounded. For explicit scoping of routine work, even if phrased as "shape" or "spec", reply only `Direct: No contract needed. <outcome with any material fence>`. Use the requester's language and skip optional references. Clear implementation-only work skips Product. |
| Shape | The outcome is known and a consequential choice remains, or the user needs a contract to verify a material risk. Settle what is open and return the short contract. |
| Discover | Whether to build, for whom, or within which hard constraints depends on missing evidence. Read `references/discover.md`. |
| Grill | The requester asks for an interview, or consequential decisions depend on user answers across rounds. Use the question rule in section 4. Read `references/grill.md` only for a requested or genuinely multi-round interview. |

Technical complexity alone never triggers Product. Ordinary implementation edge cases stay with the implementer unless they materially change the outcome or a constraint. Blocked is a readiness status in any mode.

## 2. Settle meaning and test the premise

When a term could change behavior, check existing vocabulary and the affected behavior. Use one contrasting scenario to distinguish the meanings, such as unlinking a shared note from one board versus deleting the note from all boards. If both readings remain plausible and one expands the scope or causes irreversible loss, ask which is intended before marking either reading ready. Use the settled term in acceptance.

When a proposed solution may miss the need, evidence contradicts a premise, or repeated fixes share a failed premise, name the premise and one observation that would change the decision. Prefer reuse, removal, or no change if it delivers the same outcome and preserves required reliability, privacy, accessibility, compatibility, and usability. For a real trade-off, give a recommendation and at most one viable alternative with its consumer consequence. For an empirical choice, use or propose the cheapest authorized low-risk experiment that could settle it. The user owns preferences. Keep clear authorized work on its stated course.

## 3. Shape the smallest complete outcome

State who gains what and the trigger, response, and resulting state that achieve it. Include only capabilities whose absence breaks the outcome or causes harm. Fence plausible adjacent expansion. Keep cut nice-to-haves out of later slices and backlogs. Record an intentional shortcut on core work only if its follow-up has a real trigger.

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

If blocked on what the user intends, respond with `Status: blocked`, one grounded fact, and the controlling question with a safe recommendation. End on that one question. Defer identifiers and other follow-up details until the user chooses the action. Both interpretations stay undecided until the answer, so neither gets a contract, acceptance criteria, or a conditional handoff. If authorization alone is missing, name the exact authorization needed. Continue independent work only when separately requested and authorized.

## 5. Write observable acceptance

- Use atomic, externally checkable results through the public entry point. Typically 1–2 for a small change and 3–7 for a feature. Cover the main result, critical failure or recovery, and plausible regressions or checkable exclusions. A success signal also needs the intended resulting state. Require a failure to be visible when false success would cause harm.
- Check only the affected dimensions: actor and permission, initial/resulting state, retries or concurrency, persistence, compatibility, and domain invariants. Include a negative check when roles, tenants, sharing, or private data are involved: an unauthorized actor is refused and sees no protected data. For existing data, users, clients, or shared links, state their release transition and reversibility. Resolve or block material unknowns.
- Specify performance bounds only if the requester provides or agrees to the bound or measurement condition. For data-dependent behavior, use at least two varied examples. For model-dependent behavior, read `references/ai-features.md` for eval acceptance.
- Add `Intent:` when literal acceptance can be gamed. Hardcoded outputs, special-cased inputs, weaker tests, and hidden errors do not meet it. The implementer may add tests and must propose changes to acceptance explicitly. Report per item what was actually observed (command, test, or manual step) or `not verified`.

## 6. Return the contract

Write in the requester's language and preserve their domain identifiers. Aim for 5–15 lines and omit empty fields. Read `references/examples.md` only when unsure about format or proportion.

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

Keep ordinary contracts in the existing task or PR. For durable multi-session work, keep one spec in the existing authorized source. Collapse completed slices and retire the spec when done. Keep exploration, interview notes, and rejected ideas in chat. Create issues only when requested or required by an authorized workflow.

Use `.agents/product.md` for the purpose, durable invariants, boundaries, and the current `Now:` focus with any agreed appetite. Keep it to about one screen (40 lines). When accepted intent changes an invariant, focus, or durable term, propose the smallest replacement in that file or the existing glossary. Retain rationale only when it prevents repeating a consequential decision. Write `.agents/product.md` only when explicitly requested or approved. Keep feature acceptance in the task. Skip new glossary, ADR, or decision-log machinery by default.

## 8. Hand off ready work

Ready means the implementer can build and verify the smallest outcome without inventing a requirement, with binding constraints and authority satisfied. Preserve the requested guarantee at its stated scope. If callers are promised at most one effect across retries and no expiry is stated, require at most one effect even on late retries. Leave retention and replay mechanisms to Engineering. A proposed expiry that would allow a second effect changes the public promise. If that narrower promise is needed, return `Status: blocked` until the requester agrees to the retry boundary and the outcome beyond it. A release caveat cannot make that contract ready. Apply the Discover evidence gate before production handoff. An authorized experiment has its own scope and decision criterion.

For requested and authorized implementation, continue through the existing implementer or in the same session. Close a contract handoff with “Build only what is described. Report adjacent findings; do not act on them.” For spec or research only, return the requested output. On new evidence, revise only affected fields, identify superseded acceptance, and flag what needs re-verification if work began.
