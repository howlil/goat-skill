# Visual quality and the design system

Use when checking consistency with an established visual system, creating a restrained direction where no identity exists, or updating DESIGN.md. Layout structure belongs to `references/layout.md`; generic/template risk belongs to `references/anti-slop.md`.

## Contents
- Authority
- System consistency
- When no identity exists
- Final visual review
- DESIGN.md and tokens

## Authority

For visual implementation, use this order:

```text
user brief
-> DESIGN.md / brand guidance
-> token and component source in code
-> existing screens
-> generic Goat guidance
```

Where these conflict, say so instead of silently picking a new style. Code remains authoritative for actual token values.

## System consistency

Check the visual vocabulary that the project already owns:

- typography roles and scale;
- semantic color roles;
- spacing scale;
- radius and shape language;
- borders/elevation/depth;
- icon family and sizing;
- component states;
- density;
- motion vocabulary.

Reuse the established role before inventing a new one. A one-off value is justified only when the existing system cannot express the requirement.

Do not normalize deliberate exceptions merely to make the system look mathematically uniform.

## When no identity exists

Before styling, write a direction in at most six lines:

- subject and audience;
- primary job of the surface;
- four to six semantic color roles;
- typography roles;
- density;
- one visual principle.

Then run `references/anti-slop.md` before implementation. The direction should be specific enough that replacing only the logo and copy would not make it equally suitable for an unrelated product.

Do not create a complete brand system for a feature that only needs a local interface.

## Final visual review

Render only the states and widths affected by the change. Review:

| Dimension | Check |
|---|---|
| System fit | tokens, components, type, icons, shape, and depth follow the project |
| Hierarchy | priority remains obvious after the actual content is rendered |
| Composition | proportion, alignment, and density feel deliberate |
| Consistency | repeated roles look and behave consistently |
| State quality | loading, empty, error, disabled, focus, and selected states belong to the same system |

If hierarchy/composition fail, go back to `references/layout.md`. If the result feels interchangeable with another product, use `references/anti-slop.md`. Effects are not a repair strategy.

## DESIGN.md and tokens

DESIGN.md (an open format from Google Labs, currently alpha) may pair machine-readable tokens with prose explaining why they exist. Treat it as optional and unstable; do not make it a hard dependency on projects that do not use it.

- Code is authoritative for token values. When tokens already live in a theme file, CSS variables, or framework config, DESIGN.md points to that source rather than becoming a second editable copy.
- If the project's DESIGN.md uses the Google format and the tooling is available, validate it after editing with the cross-platform entrypoint: `npx -p @google/design.md designmd lint DESIGN.md`.
- Keep DESIGN.md short: identity, token/component sources, layout/density principles, interaction/motion rules, accessibility rules, and project-specific anti-patterns. Leave out per-screen specifications and transient decisions.
- Each line must change what an implementing agent does. If removing a line would not alter behavior, remove it.

Reference:
https://github.com/google-labs-code/design.md
