---
name: product
description: "Resolve uncertainty about what to build, why it matters, who needs it, or how to tell it works. Use for feature shaping, product discovery, unclear behavior or acceptance, and unresolved costly or irreversible choices. Skip work whose outcome and behavior are already clear."
---

# Product

Own the intended outcome, scope, observable behavior, and acceptance. Leave interface details and internal mechanisms to the concerns that own them. A contract can describe a binding constraint, such as offline use, without choosing the implementation.

## Choose the smallest useful response

| Situation | Response |
| --- | --- |
| The request and repo make behavior and done clear | **Direct.** Proceed with the requested work or answer. State a material reversible assumption only if one is needed. |
| The outcome is clear and scope, behavior, or acceptance could vary | **Shape.** Settle only the decisions that change the result. |
| Evidence could change whether to build it or whom it serves | **Discover.** Read `references/discover.md` and investigate the question most likely to change the decision. |
| A costly, irreversible, externally consequential, or authorization-sensitive choice is unresolved | **Blocked.** Ask for the missing decision and pause the dependent action. Keep any independent work moving. |

Read the request and its constraints, then inspect the relevant issue, existing behavior, tests, and product decisions. Treat current behavior as a baseline. Ground claims about users, demand, metrics, and feasibility in evidence. Record a material reversible assumption with the condition that would change it.

## Shape the work

- When evidence leaves a decision that would change the build, ask the highest-impact question whose prerequisites are settled. Stop asking once scope and acceptance are clear enough to build.
- State who needs what outcome or what failure stops. If a proposed solution obscures the user's job, identify what triggers the need and how they handle it today, if known.
- Describe the smallest complete path from trigger to observable result. Include the starting state in behavior and acceptance when it changes the result. For an existing product, cover only the changed path and states it touches. Split large work into independently useful slices.
- Cover material failure and recovery, binding constraints, and adjacent scope an implementer might reasonably include.
- Make acceptance observable through the public entry point. Cover the main path and meaningful failure or recovery. Use varied examples where behavior depends on data. State the intent if a literal check could be passed by special-casing its inputs.
- Ask what was observed for each material acceptance condition. Keep unknowns visible and distinguish evidence from assumptions.

Use only the fields that affect the decision or build.

```text
Outcome: <capability or corrected behavior>
Behavior: <trigger, response, result>
Acceptance: <observable evidence of success and material failure behavior>
Out of scope: <adjacent behavior beyond the request>
Constraints: <binding requirements>
Assumptions: <reversible default and what would change it>
Blocked on: <decision or authorization needed to continue>
```

## Continue at the relevant concern

When the user asks to build and the outcome is clear, carry it into the relevant interface or implementation work in the same task. When the user asks only for a decision or spec, deliver that. Revisit the affected decision if new evidence changes it.

Put durable product decisions in the project's existing product record when the user requests or authorizes a write. Keep feature-specific acceptance with the existing task. Read `references/examples.md` if the right amount of detail is unclear.
