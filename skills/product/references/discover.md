# Discover mode

Use only when the right decision depends on evidence you do not have: whether the problem is real, who has it, or whether the proposed solution is worth its cost. If the open question is only *what exactly to build*, use Shape instead.

## Contents
- Frame the decision
- Find the riskiest unknown
- Gather the cheapest sufficient evidence
- Output

## Frame the decision

Write the decision in one line: "Build X / do not build / build smaller Y." Then write the question that evidence would answer, and which result would change the decision. If no plausible result would change it, skip discovery and decide.

## Find the riskiest unknown

Check the four product risks and pick the one most likely to sink the work. Be honest about which is hardest: it is easy to over-examine whatever is easiest to examine.

- Value: does anyone need this enough to use it?
- Usability: can they work out how to use it?
- Viability: does it fit privacy, legal, cost, support, and product direction?
- Feasibility: can it be built within the constraints? Name it only if the answer could change the behavior or scope; the implementer owns the detail.

Value and viability are not in the code. Do not answer them from code.

## Gather the cheapest sufficient evidence

In this order, stopping as soon as the decision is clear:

1. The repo and what the requester gave you: Issues, support threads, usage logs, existing behavior, prior decisions in `.agents/product.md`.
2. Things the user can tell you in one answer.
3. Public sources via web search, for market or technical facts. Cite them.
4. A cheap experiment the user can run: a usage counter, a fake-door button, five short conversations.

Spend effort only on the one risk you picked. Do not survey the market for its own sake.

## Output

```text
Decision: <the one-line decision>
Evidence: <each item with its source>
Assumptions: <treated as true without evidence>
Recommendation: <build / do not build / build smaller>, confidence low | medium | high
What would change it: <the result that flips the recommendation>
Next smallest step: <only if evidence is still short>
```

Keep Evidence and Assumptions visibly separate. If you found nothing, write "no evidence found" instead of filling the gap with plausible user stories, statistics, or quotes. If the recommendation is to build, finish with a Shape-mode contract (SKILL.md section 6).
