# Goat Skill

**Portable software-engineering skills for Codex, Claude Code, and Antigravity (Agy).**

> **First skill in development:** `product` (Direct / Shape / Discover). This branch is not a published plugin release.

## Design

- **One canonical skill source:** `skills/<skill-name>/SKILL.md` follows the Agent Skills specification.
- **Portable first:** root `plugin.json` is the canonical Agent Plugins manifest.
- **Compatibility without instruction duplication:** `.codex-plugin/plugin.json` is kept only as a Codex compatibility fallback and points back to the same `./skills/` directory.
- **Progressive disclosure:** references stay inside the skill and are loaded only when needed.
- **No premature runtime:** no hooks, MCP server, runtime dependency, generated skill copies, or extra agent layer.

## Repository layout

```text
goat-skill/
├── plugin.json                       # Canonical portable Agent Plugins manifest
├── .codex-plugin/
│   └── plugin.json                   # Codex compatibility fallback
├── skills/product/                   # Canonical product skill
│   ├── SKILL.md
│   └── references/
│       ├── discover.md
│       └── examples.md
├── .claude-plugin/
│   ├── plugin.json                   # Claude Code identity
│   └── marketplace.json              # Claude marketplace catalog
├── .antigravity-plugin/plugin.json   # Agy-specific overlay
├── .agents/plugins/marketplace.json  # Codex repo-local marketplace
├── scripts/validate.py               # Static packaging + skill validation
├── .github/workflows/validate.yml
├── AGENTS.md
└── README.md
```

## Manifest strategy

The current OpenAI portable format uses root `plugin.json`. OpenAI also continues to support `.codex-plugin/plugin.json` as a compatibility fallback. Goat Skill carries both so newer portable hosts and older Codex-compatible loaders resolve the same package without duplicating skill instructions.

The validator enforces that the compatibility manifest matches the canonical manifest for:

- plugin `name` and `version`
- author and repository
- OpenAI install-surface metadata
- `skills: "./skills/"`

The root manifest also supplies OpenAI presentation metadata for local install surfaces: display name, descriptions, developer, category, capabilities, and starter prompts.

## Validate

```bash
python3 scripts/validate.py
```

Successful static validation proves package structure and metadata consistency. It does **not** prove native client installation or model behavior.

When the respective clients are installed, run their native checks where available:

```bash
claude plugin validate .
agy plugin validate --strict .
```

For Codex, add the repo marketplace and verify discovery/install in a supported local client:

```bash
codex plugin marketplace add howlil/goat-skill
codex plugin marketplace list
```

## Install after the first skill release

These are future installation instructions, not a claim that the current branch is published:

```bash
# skills.sh / Skills CLI
npx skills add howlil/goat-skill

# Codex
codex plugin marketplace add howlil/goat-skill

# Claude Code
claude plugin marketplace add howlil/goat-skill
claude plugin install gs@goat-skill-marketplace

# Antigravity CLI
agy plugin install https://github.com/howlil/goat-skill
```

## Product skill

The canonical source is [`skills/product/SKILL.md`](skills/product/SKILL.md), with [Discovery](skills/product/references/discover.md) and [worked examples](skills/product/references/examples.md).

| Client | Explicit invocation |
| --- | --- |
| Claude Code plugin | `/gs:product` |
| Codex plugin or installed skill | `$product` |
| Antigravity plugin | `/product` |

`gs` is the plugin identity. `product` is the portable Agent Skill name. Invocation syntax remains host-native.

The skill chooses the lightest safe mode:

- **Direct** — behavior and done are already clear.
- **Shape** — outcome is clear but behavior, scope, or acceptance is underspecified.
- **Discover** — whether/what to build depends on evidence that is not yet available.
- **Blocked** — an unresolved choice is external, expensive, irreversible, privacy-sensitive, destructive, or otherwise unsafe to guess.

## Verification boundary

Static CI checks:

- portable manifest schema and identity
- Codex compatibility fallback and canonical `./skills/` path
- cross-host name/version consistency
- OpenAI interface metadata limits and consistency
- Codex marketplace policy/category/display name
- skill frontmatter and referenced Markdown files

Still requires native runtime evidence before claiming full multi-host verification:

- Claude discovers and runs `/gs:product`
- Codex discovers and runs `$product`
- Agy discovers and runs `/product`
- actual agent prompts exercise Direct / Shape / Discover / blocked-decision behavior

## Adding a skill later

Each skill must live at `skills/<skill-name>/SKILL.md`. Keep all reusable references/scripts/assets under that skill directory. Do not copy skill instructions into host-specific plugin folders.

Run `python3 scripts/validate.py` after every packaging or skill-layout change. Test native discovery before describing a new host as supported.

## Licensing

A license has not been selected. Choose and add a `LICENSE` file before public redistribution; a public GitHub repository does not automatically grant reuse rights.

## References

- [Agent Skills specification](https://agentskills.io/specification)
- [Skills CLI / skills.sh](https://skills.sh/docs)
- [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins)
- [Claude Code plugins](https://code.claude.com/docs/en/plugins)
- [Claude plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Antigravity plugin packaging](https://antigravity.google/docs/build-plugins)
