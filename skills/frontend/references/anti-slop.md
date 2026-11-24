# Anti-slop and visual specificity

Use when creating a new visual direction, materially restyling a surface, or when the result risks looking like a reusable AI template. Skip it when the project's established identity already determines the visual choices and the change does not challenge them.

## Goal

Avoid generic output by grounding free visual decisions in this product, not by maintaining a blacklist of fashionable fonts, colors, effects, or layouts.

## 1. Respect the authority chain

For visual decisions, use this order:

```text
explicit user brief
-> project DESIGN.md / brand guidance
-> code tokens and established components
-> existing product surfaces
-> generic design guidance
```

If an established product deliberately uses cards, gradients, monochrome typography, or any other common pattern, do not remove it merely because the pattern is common.

Anti-slop applies to decisions that are still free.

## 2. Specificity test

Ask:

> Could this composition plausibly belong to an unrelated product if only the logo and copy were replaced?

If yes, identify which choices are generic:

- information hierarchy;
- composition;
- typography roles;
- color roles;
- shape or surface treatment;
- density;
- icon treatment;
- interaction pattern;
- decorative motif.

Revise the smallest set of choices that can be tied more clearly to the product's subject, audience, task, or existing identity.

## 3. Detect default clusters, not isolated styles

A common-looking element is not automatically a problem. Genericness usually appears as a cluster of unearned defaults.

Examples of warning clusters:

- equal rounded cards for every section;
- muted metadata plus oversized heading plus decorative eyebrow on every surface;
- repeated pills or badges with no information role;
- gradients, glass, shadows, or floating chrome added before hierarchy is settled;
- a new typography/color personality that does not exist elsewhere in the product.

Do not "deslop" by swapping one cliché for another. Changing the costume while preserving the same generic structure is not progress.

## 4. Spend the design-decision budget deliberately

Every new visual decision increases inconsistency risk.

Use this order:

```text
reuse existing token
-> reuse existing component/pattern
-> extend an established visual rule
-> introduce a new choice only when it adds identity, hierarchy, usability, or meaning
```

A new decision needs a reason visible in the brief or product. "Looks modern" is not a reason.

## 5. Concentrate boldness

If the surface needs stronger personality, put the strongest expression in one coherent place and let the rest support it.

Possible signature axes include:

- typography;
- composition;
- imagery;
- interaction;
- shape language;
- information density.

Do not maximize all axes simultaneously. A distinctive interface still needs calm areas for comprehension and repeated use.

## 6. Self-critique before polish

For a new or materially restyled direction, answer:

1. Which choices came from the product or user brief?
2. Which choices came from the existing system?
3. Which choices are arbitrary?
4. Do the arbitrary choices resemble recurring template defaults?
5. Which one or two changes would make the result more specific without adding noise?

Then render again. Do not solve genericness by adding decoration to weak hierarchy; use `references/layout.md` first if structure is the problem.

## Specificity gate

Before calling a new direction complete:

- the primary composition reflects this product's job;
- at least the consequential visual decisions have an explicit anchor;
- no cluster of arbitrary defaults dominates the surface;
- the design still belongs to the project after removing decorative effects;
- established project decisions were preserved unless the request explicitly changed them.

## Influence

This reference is an original Goat Skill synthesis informed by Anthropic's frontend-design guidance on subject-specific, deliberate visual direction:
https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md
