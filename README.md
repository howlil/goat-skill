# Goat Skill

**Portable software-engineering skills for Codex, Claude Code, Antigravity (Agy), and Agent Skills-compatible hosts.**

> **Current development catalog:** `product` + `design`. This branch is not a published plugin release.

## Design

- **One canonical skill source:** every skill lives at `skills/<skill-name>/SKILL.md`.
- **Portable first:** root `plugin.json` is the canonical Agent Plugins manifest.
- **Compatibility without instruction duplication:** `.codex-plugin/plugin.json` points to the same `./skills/` directory.
- **Progressive disclosure:** references live inside the skill and load only when needed.
- **Clear ownership:** `product` decides product behavior/scope; `design` implements or audits frontend behavior without redefining product acceptance.
- **No premature runtime:** no hooks, MCP server, runtime dependency, generated host-specific skill copies, or extra agent layer.

## Repository layout

```text
goat-skill/
├── plugin.json
├── .codex-plugin/
│   └── plugin.json
├── skills/
│   ├── product/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── discover.md
│   │       └── examples.md
│   └── design/
│       ├── SKILL.md
│       └── references/
│           ├── anti-slop.md
│           ├── examples.md
│           ├── hardening.md
│           ├── layout.md
│           ├── motion.md
│           ├── stress.md
│           ├── ux.md
│           └── visual-quality.md
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── .antigravity-plugin/plugin.json
├── .agents/plugins/marketplace.json
├── scripts/validate.py
├── .github/workflows/validate.yml
├── AGENTS.md
└── README.md
```

## Skill catalog

### `product`

Turns product uncertainty into the smallest verifiable contract an implementer can build without inventing requirements.

Modes:

- **Direct** — behavior and done are already clear.
- **Shape** — outcome is clear but behavior, scope, or acceptance is underspecified.
- **Discover** — whether/what to build depends on evidence.
- **Blocked** — an unresolved choice is external, expensive, irreversible, privacy-sensitive, destructive, or otherwise unsafe to guess.

Canonical source: [`skills/product/SKILL.md`](skills/product/SKILL.md).

### `design`

Frontend architect and design engineer for an existing codebase. It builds, refines, and audits UI while preserving the product contract.

Modes:

- **Refine** — smallest fix or improvement to an existing surface.
- **Build** — new screen, feature UI, or component; trace flow, reuse, implement, verify.
- **Audit** — reconstruct behavior and report evidence-backed findings; change nothing unless asked.

Core rules:

- search and reuse before creating components;
- one authoritative owner per state;
- native/accessibility-first interaction;
- explicit loading/empty/error/recovery behavior;
- product-priority layout, grouping, spacing rhythm, and responsive transformation;
- product-specific visual direction without style blacklists or template defaults;
- purposeful, interruptible, reduced-motion-aware animation;
- realistic stress testing and production UI hardening;
- verification in proportion to the change;
- report only what was actually observed.

References:

- [Layout and composition](skills/design/references/layout.md)
- [Anti-slop and visual specificity](skills/design/references/anti-slop.md)
- [UX flows and states](skills/design/references/ux.md)
- [Motion engineering](skills/design/references/motion.md)
- [Visual quality and design system](skills/design/references/visual-quality.md)
- [UI stress testing](skills/design/references/stress.md)
- [UI hardening](skills/design/references/hardening.md)
- [Worked examples](skills/design/references/examples.md)

Canonical source: [`skills/design/SKILL.md`](skills/design/SKILL.md).

## Ownership boundary

```text
product
  ↓ observable behavior / acceptance / scope
design
  ↓ frontend implementation / interaction / visual system / audit
repo code + tests + running UI
  ↓ evidence
report only what was actually verified
```

`design` may make a reversible implementation assumption when necessary, but it does not silently change product scope or acceptance.

## Invocation

| Skill | Claude Code | Codex | Antigravity |
| --- | --- | --- | --- |
| Product | `/gs:product` | `$product` | `/product` |
| Design | `/gs:design` | `$design` | `/design` |

`gs` is the plugin identity; `product` and `design` are portable Agent Skill names. Literal invocation syntax remains host-native.

## Manifest strategy

Root `plugin.json` is the portable source of truth. The Codex compatibility manifest contains packaging metadata plus `skills: "./skills/"` but never duplicates skill instructions.

The validator keeps these synchronized:

- plugin name, version, and description;
- author and repository;
- OpenAI interface metadata;
- Codex repo marketplace category/display name;
- canonical skill layout and referenced Markdown files.

Current development version: **0.4.0**.

## Validate

```bash
python3 scripts/validate.py
```

The PR gate runs the same command. Successful static validation proves package structure and metadata consistency; it does **not** prove native client discovery or model behavior.

When clients are installed, run native checks where available:

```bash
claude plugin validate .
agy plugin validate --strict .

codex plugin marketplace add howlil/goat-skill
codex plugin marketplace list
```

## Install after release

These are future installation instructions, not a claim that the current branch is published:

```bash
# Skills CLI / skills.sh
npx skills add howlil/goat-skill

# Codex
codex plugin marketplace add howlil/goat-skill

# Claude Code
claude plugin marketplace add howlil/goat-skill
claude plugin install gs@goat-skill-marketplace

# Antigravity CLI
agy plugin install https://github.com/howlil/goat-skill
```

## Verification boundary

Static CI verifies:

- portable manifest schema and identity;
- Codex compatibility fallback and canonical `./skills/` path;
- cross-host manifest consistency;
- OpenAI interface metadata constraints;
- Codex marketplace policy/category/display name;
- each skill's frontmatter;
- every referenced Markdown resource.

Still requires native runtime evidence before claiming multi-host verification:

- Claude discovers `/gs:product` and `/gs:design`;
- Codex discovers `$product` and `$design`;
- Agy discovers `/product` and `/design`;
- actual agent sessions exercise Product Direct / Shape / Discover / Blocked;
- actual frontend sessions exercise Design Refine / Build / Audit plus conditional layout / specificity / stress / hardening references.

## Adding a skill later

Each skill must live at `skills/<skill-name>/SKILL.md`. Keep reusable references, scripts, and assets under that skill directory. Do not copy skill instructions into host-specific plugin folders.

Run `python3 scripts/validate.py` after every packaging or skill-layout change. Test native discovery before describing a host as verified.

## Licensing

A license has not been selected. Choose and add a `LICENSE` file before public redistribution; a public GitHub repository does not automatically grant reuse rights.

## References

- [Agent Skills specification](https://agentskills.io/specification)
- [Skills CLI / skills.sh](https://skills.sh/docs)
- [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins)
- [Claude Code plugins](https://code.claude.com/docs/en/plugins)
- [Claude plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Antigravity plugin packaging](https://antigravity.google/docs/build-plugins)
