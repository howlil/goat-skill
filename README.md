# Goat Skill

**Portable software-engineering skills for Codex, Claude Code, and Antigravity (Agy).**

> **First skill in development:** `product` (Direct / Shape / Discover). This branch is not a published plugin release.

## Design

- **One canonical source:** `skills/<skill-name>/SKILL.md` follows the [Agent Skills specification](https://agentskills.io/specification).
- **No duplicated skills:** Codex, Claude Code, and Agy consume the same `skills/` folder. Platform-specific files contain distribution metadata only.
- **Progressive disclosure:** Keep the entrypoint focused. Add `references/`, `scripts/`, or `assets/` inside a skill only when needed.
- **No premature runtime:** No hooks, MCP servers, Node.js dependency, or generated platform-specific variants.

## Repository layout

```text
goat-skill/
├── skills/product/                  # Canonical product skill
│   ├── SKILL.md
│   └── references/{discover,examples}.md
├── plugin.json                       # Portable Agent Plugins / Codex
├── .claude-plugin/
│   ├── plugin.json                   # Claude Code identity
│   └── marketplace.json              # Claude marketplace catalog
├── .antigravity-plugin/plugin.json   # Agy-specific overlay
├── .agents/plugins/marketplace.json  # Codex repo marketplace
├── scripts/validate.py               # Lightweight metadata validation
├── .github/workflows/validate.yml
├── AGENTS.md
└── README.md
```

## Validate the skill

```bash
python3 scripts/validate.py
```

Once you have installed the respective clients, use their native validation commands:

```bash
claude plugin validate .
agy plugin validate --strict .
```

These host-specific checks have **not** yet been run as part of the repository scaffold.

## Install after the first skill release

These commands are **future installation instructions**, not a claim that a usable skill is available now:

```bash
# skills.sh / Skills CLI — portable skill installation
npx skills add howlil/goat-skill

# Codex — register the repository marketplace
codex plugin marketplace add howlil/goat-skill

# Claude Code — register marketplace and install plugin
claude plugin marketplace add howlil/goat-skill
claude plugin install gs@goat-skill-marketplace

# Antigravity CLI — install GitHub plugin bundle
agy plugin install https://github.com/howlil/goat-skill
```

## Product skill

The canonical source is [`skills/product/SKILL.md`](skills/product/SKILL.md), with [Discovery](skills/product/references/discover.md) and [worked examples](skills/product/references/examples.md) loaded only as needed.

| Client | Explicit invocation |
| --- | --- |
| Claude Code plugin | `/gs:product` |
| Codex plugin or installed skill | `$product` |
| Antigravity plugin | `/product` |

`gs` is the **plugin identity**, `product` is the **portable Agent Skill name**. The literal syntax `gs:product` is not universal across hosts.

Use **Direct** for clear, low-risk work; **Shape** for underspecified behavior; **Discover** when evidence is needed to decide whether to build. Critical irreversible decisions remain blocked until answered. Skill-specific behavior evaluations and native host-install smoke checks have **not** run.

## Adding a skill later

Each skill must live at `skills/<skill-name>/SKILL.md` with a valid YAML frontmatter `name` (equal to the directory name) and `description` (what it does and when to use it). Additional resources remain inside that skill directory. Do not write placeholder skills or duplicate platform-specific copies.

Run `python3 scripts/validate.py`, then test skill discovery and relevant behaviors in actual target clients before describing it as supported. Release versions in all three plugin manifests must stay in sync; bump them when publishing a new plugin release.

## Licensing

A license has not been selected. Choose and add a `LICENSE` file before public redistribution; a public GitHub repository does not automatically grant a reuse license.

## References

- [Agent Skills specification](https://agentskills.io/specification)
- [Skills CLI / skills.sh](https://skills.sh/docs)
- [Codex plugin packaging](https://developers.openai.com/plugins/build/plugins)
- [Claude Code plugins](https://code.claude.com/docs/en/plugins)
- [Claude plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Antigravity plugin packaging](https://antigravity.google/docs/build-plugins)
