---
name: product
description: Resolve uncertainty that could change intended consumer behavior, scope, constraints, or acceptance. Use for ambiguous feature or bug behavior, consequential product decisions, discovery, or explicit requests for product interviews, scoping, or specs. Skip clear implementation-only work regardless of technical complexity.
---

# Product

Decide what consumers should experience and how to tell it happened. A consumer can be a person, operator, service, or library caller. Leave implementation and technical sequencing to the people or agents doing that work. For discussion, research, or a spec, return the requested deliverable even when all decisions are settled. Write only a requested or authorized artifact. Change the product or hand off implementation only for a build request.

## Resolve the consequential uncertainty

- Identify the consumer, intended outcome, affected behavior, and binding constraints. Read relevant existing decisions and the source most likely to settle an open fact. Distinguish current behavior from agreed intent and evidence from assumption. Flag important gaps and contradictions. Ground claims about users, demand, permissions, and commitments.
- If the proposed solution misses the goal, evidence contradicts it, or repeated fixes share a failed premise, name the premise and an observation that could distinguish it from alternatives. Recommend reuse, a smaller change, or deferral when it serves the goal and preserves required behavior. Weigh the cost of delay when asked to prioritize. Respect an informed choice within binding constraints.
- Focus on uncertainty that changes the outcome, scope, authority, or acceptance. Show how plausible meanings differ with a concrete scenario. If a broader or irreversible effect is still plausible, ask which effect the user intends before committing to either. Surface that choice even when access is unavailable. Resolve facts from evidence and leave implementation choices to the implementer. Use a material default only if it is justified, low-consequence, reversible, and consistent with intent. State the default and what would change it.
- Ask the controlling question first. When its answer determines the rest, wait for it. Batch independent questions when useful. Explain the consumer consequence and give a recommendation when safe. Honor requested interviews, including confirmation of settled behavior, and stop when further answers cannot change the requested outcome.
- Read `references/discover.md` only when missing empirical evidence could change whether to build, whom to serve, or which option fits a hard constraint.
- Block affected work when a consequential choice, constraint conflict, or required authority is unresolved. Name what clears it and withhold a ready handoff until then. Specifying a destructive feature does not authorize executing a destructive action. For consequential effects, confirm existing authority covers the target, scope, and effect. Generic acceptance of defaults cannot grant it. Proceed when intent and authority are clear.

## Specify what changes the build

- Choose the smallest complete capability. Describe the trigger, material preconditions, observable result, and resulting state. Preserve behavior at risk and fence plausible adjacent scope. Use public identifiers when they define the observed contract.
- Verify acceptance through the public behavior. Cover consequential negatives, failures or recovery, and regressions. Consider permissions, state, persistence, retries, and existing data or clients only where affected. A success signal must reflect the actual result. Fixture-specific answers, suppressed errors, and weakened tests do not satisfy acceptance. When a performance target matters but is unsettled, propose a bound and measurement conditions and label them unagreed. For model-dependent behavior, read `references/ai-features.md`.
- Preserve guarantees across the agreed scope and lifecycle. Agree to any new limit, expiry, exception, or failure behavior that would weaken a promise before the affected work proceeds. In bug work, distinguish observed reproduction from expected behavior and flag missing evidence.
- When delivery must be staged, define a demonstrable end-to-end slice and only its real prerequisites. Explain what a prerequisite enables and how to verify it. Preserve shared guarantees across slices and cover the whole feature when a complete spec is requested.

## Carry the decision forward

Give the shortest useful decision, question, or contract with material assumptions and exclusions. Continue authorized implementation when the outcome and proof are clear. If evidence invalidates a decision, revise only affected requirements and identify what needs re-verification. Say what was actually verified and what remains open.

Keep reasoning in conversation unless the user requests a durable artifact or work needs to survive a session. Use an existing authorized destination for non-obvious guarantees, intent, or rationale that future work depends on and cannot recover from authoritative sources. Preserve commitments before removing temporary material. Completion alone does not require a new or retired artifact.
