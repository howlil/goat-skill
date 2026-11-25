# Discover mode

Use when evidence could change whether to build, whom to serve, or which options fit. Use Shape when only the exact behavior is open.

## Frame the decision

Check binding constraints and authorized scope first. Rule out options that violate them. Compare viable choices, including a smaller scope or no change. Name the question and the observation that would change the decision. Skip investigation if no plausible answer would change it.

Check four risks. Start with the decisive unknown and revisit another only if it could block the decision or a safer option.

- Value. Does the intended consumer have the need?
- Usability. Can they complete the workflow?
- Viability. Does it fit privacy, legal, cost, support, and product constraints?
- Feasibility. Can the outcome fit the constraints? Leave the implementation to its owner.

## Gather sufficient evidence

Start with relevant observations such as usage, support reports, current behavior, and agreed decisions. Ask for evidence the user has when it can resolve the choice. Cite public sources for relevant external facts. Code and prototypes can establish behavior or feasibility within limits. Demand needs evidence from or about the intended users.

State what each observation supports and where it stops. Keep assumptions separate. Say when evidence is missing and use a decision-relevant threshold or qualitative result grounded in the goal.

If a probe would settle the uncertainty, propose the smallest safe, time-bounded experiment with a scoped audience or fixture and a result criterion. Say if it has yet to run. Obtain authorization for production experiments, instrumentation, spending, or data collection. Experiments cannot settle preferences the user owns.

## Output

```text
Decision: <viable options>
Question: <decisive uncertainty>
Evidence: <source, observation, limitation>
Assumptions: <unverified premises, if material>
Recommendation: <build / smaller / do not build yet and confidence>
What would change it: <decision-relevant observation>
Next smallest step: <only when needed>
```

A recommendation supplies neither readiness nor permission. Shape ready build work only when the decisive evidence supports its intended scope, or when an explicitly authorized, safely scoped experiment is itself the work. Keep experiment findings within that scope. Otherwise stop at a recommendation or next step. If implementation was requested, mark the unresolved work blocked.
