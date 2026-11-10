# Visual quality and the design system

Use when the surface has no established identity, when exploring a new visual direction, when auditing visual quality, or when creating or updating DESIGN.md.

## Contents
- Anchor to the identity that exists
- When no identity exists
- Review procedure
- DESIGN.md and tokens

## Anchor to the identity that exists

Order of authority: the user's brief, DESIGN.md, the token source in code, then the existing screens. Match them. Where they conflict, say so instead of choosing silently. Generic output comes from unanchored choices, so the fix is an anchor, not a longer list of bans.

## When no identity exists

Before styling, write a direction in at most six lines: the subject and audience, the primary job of the surface, four to six color roles, type roles, density, and one principle. Then ask whether the same direction would come out for any similar product. If it would, revise the parts that read as defaults and say what you changed.

Lists of banned fonts and colors are a weak control: models tend to move to the next most common choice. Specific choices tied to the subject work better than avoided ones. Spend boldness in one place and keep the rest quiet.

## Review procedure

Render the states you changed and compare each with the baseline: normal, empty, loading, error, compact and expanded, and the widths the app supports. Score five things:

| Dimension | Check |
|---|---|
| Specificity | reflects this product, not a template |
| Hierarchy | primary action and key information are obvious |
| Composition | proportion, alignment, density, and whitespace look intentional |
| Consistency | type, radius, spacing, color, icons, and motion follow the system |
| Behavior | every interaction has feedback and a recovery path |

Fix in this order: hierarchy, composition, consistency, and only then effects. Effects do not repair weak structure.

## DESIGN.md and tokens

DESIGN.md (an open format from Google Labs, currently alpha) pairs machine-readable tokens in YAML front matter with prose explaining why they exist. Treat it as optional and unstable: do not make it a hard dependency, and do not adopt the full schema on a project that has not.

- Code is authoritative for token values. If the project already defines tokens (a theme file, CSS variables, a Tailwind theme), DESIGN.md points to them rather than repeating them. Two editable copies of a value will drift.
- If the project's DESIGN.md uses the Google format and the tooling is available, validate it after editing: `npx @google/design.md lint DESIGN.md`. The tool can also export tokens to Tailwind or DTCG formats; use that instead of hand-syncing.
- Keep it short: identity, where tokens and components live, layout and density principles, interaction and motion rules, accessibility rules, and a few anti-patterns specific to the product. Leave out per-screen specs.
- Each line should change what an agent does. If removing it would not change behavior, leave it out.
