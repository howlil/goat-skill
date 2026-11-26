# Discover mode

Use when whether to build, for whom, or whether the option can meet a hard constraint depends on evidence.

## Decide what evidence matters

1. Check binding constraints and authority first. Consider only options within them. If an option is prohibited, assess an allowed alternative or return blocked. A value result cannot override a binding constraint. State the decision and the observation that would change it. Skip investigation when no plausible result would change the decision.
2. Pick the uncertainty most likely to change the decision. Check another risk only if it blocks the decision or a viable alternative.
   - **Value.** Who needs this enough to use it?
   - **Usability.** Can the consumer complete the workflow?
   - **Viability.** Can it meet privacy, legal, cost, support, and product constraints?
   - **Feasibility.** Can it work within those constraints? Engineering owns the method.

## Gather the cheapest sufficient evidence

Start with relevant usage, support, requests, existing behavior, or evidence the requester supplied. Source and tests can establish behavior or feasibility. Demand needs demand evidence. Use public sources for relevant external facts and cite them. State what each observation supports and where it falls short.

If evidence is missing, name the smallest time-bounded experiment and the observable result that would change the recommendation. Use qualitative criteria unless a threshold is grounded. Run it only within authorized scope. Production exposure, real-user instrumentation, spending, or data collection needs explicit authorization. If proposing an experiment, say it has yet to run.

## Output and readiness

```text
Decision: <options under consideration>
Question: <decisive uncertainty>
Evidence: <source, observation, limitation>
Assumptions: <unverified premises>
Recommendation: <build / smaller / do not build yet>, confidence <low / medium / high>
What would change it: <decision-relevant observation>
Next smallest step: <if needed>
```

Shape a ready contract only when the decisive uncertainty is resolved for the intended scope, or the requester explicitly authorized a safe, bounded experiment as the deliverable. Give an experiment its own result criterion. A recommendation grants no execution authority. If production evidence or a hard constraint is unresolved, return the recommendation and mark the affected implementation blocked if requested.
