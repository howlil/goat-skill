# Layout and composition

Use when a change affects page composition, hierarchy, grouping, density, responsive structure, or how information competes for attention. Do not load it for a local one-state tweak whose structure is unchanged.

## Goal

Turn product priority into a spatial structure that still makes sense when detail, viewport size, and sample content change.

Think in this order:

```text
priority -> reading order -> grouping -> structure -> rhythm -> density -> adaptation -> extremes
```

Do not begin with a dashboard grid, cards, columns, or a sidebar. Begin with the task and relationships those structures must express.

## 1. Establish the spatial thesis

Before moving UI, answer briefly:

- What must the user notice or do first?
- What information supports that primary path?
- Which items belong together, and which must feel separate?
- What density fits the task and frequency of use?
- What must remain stable when the container narrows or content grows?

If these are unclear because product behavior is unclear, return to the product contract. Layout must not invent product priority.

## 2. Reading order

The visual order should match the product priority.

Use a squint-style check: ignore detailed copy and decoration. You should still be able to distinguish the primary element, secondary element, and major groups in a sensible sequence.

Common failures:

- every region has equal visual weight;
- the largest object is not the most important one;
- supporting metadata competes with the primary action;
- DOM/focus order and visual order tell different stories.

Change hierarchy before adding effects.

## 3. Group by meaning

Use proximity and alignment before adding containers.

A card, panel, border, or background is justified when the boundary itself carries meaning: independent state, interaction, scrolling, selection, elevation, or a distinct surface. Do not wrap every semantic group merely to make the grouping visible.

Prefer the smallest cue that communicates the relationship:

```text
proximity -> alignment -> spacing contrast -> divider -> container
```

Avoid nested containers that exist only because the framework makes cards easy.

## 4. Build rhythm, not uniform gaps

Spacing encodes relationship. Repeating one gap everywhere flattens hierarchy.

Use the project's spacing scale, but vary roles deliberately:

- tight: parts of one control or datum;
- small: strongly related siblings;
- medium: one section or working group;
- large: separate concepts;
- strongest break: page regions or major task boundaries.

Do not invent arbitrary values to create variety. Contrast comes from semantic roles, not random spacing.

## 5. Choose density from the product

Minimal does not mean sparse. Dense does not mean cramped.

Infer the intended density from the existing product, frequency of use, information load, and task complexity. Preserve an established density unless the request explicitly changes it.

A high-frequency operational surface may need compact scanability. A low-frequency explanatory surface may earn more breathing room. The reference does not impose either.

## 6. Responsive behavior is a transformation

Do not define responsive behavior as "stack desktop vertically."

For each major region decide what happens as available space changes:

- stays fixed;
- reflows;
- reorders;
- collapses;
- becomes scrollable;
- moves behind disclosure;
- disappears because it is truly secondary.

Preserve the user's task, state, and familiarity. A narrower layout may expose less at once, but it should not silently change the workflow.

Prefer container-aware composition when a component appears in materially different parent widths.

## 7. Check realistic extremes

When relevant, inspect:

- narrowest supported container;
- normal and wide layouts;
- long and short valid text;
- empty and single-item states;
- many items;
- zoom;
- localization and RTL when the product supports them;
- overlays, sticky regions, safe areas, and focus order.

Use `references/stress.md` when these conditions need deliberate adversarial testing rather than a quick layout check.

## Layout gate

Before calling a structural change done:

1. Can primary -> secondary -> supporting hierarchy be understood without reading detailed copy?
2. Do related things group through proximity before decoration?
3. Does spacing create semantic rhythm instead of equal-weight repetition?
4. Does density fit the product rather than a generic aesthetic?
5. Does the structure preserve the task across supported widths and content extremes?

If a check fails, fix the structural cause before polishing.

## Influence

This reference is an original Goat Skill synthesis informed by Impeccable's layout reasoning, especially its separation of reading order, grouping, rhythm, density, adaptation, and extremes:
https://github.com/pbakaus/impeccable/blob/main/skill/reference/layout.md
