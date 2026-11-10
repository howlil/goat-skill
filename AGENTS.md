# Goat Skill — repository instructions

## Purpose
Maintain one portable library of software-engineering agent skills. The canonical library currently includes the `product` skill; add others only on explicit request.

## Structure
- `skills/<name>/SKILL.md`: canonical instructions; optional resources live within the same skill.
- `plugin.json`: canonical portable Agent Plugins identity and OpenAI metadata.
- `.codex-plugin/plugin.json`: Codex compatibility fallback only; it must point to the canonical `./skills/` directory and stay synchronized with root metadata.
- `.claude-plugin/`, `.antigravity-plugin/`: host-specific distribution metadata.
- `.agents/plugins/marketplace.json`: Codex repo-local marketplace.
- Project constraints: `.agents/product.md`; architecture and verification: `.agents/engineering.md`; UI: `.agents/DESIGN.md`.

## Commands
- Validate: `python3 scripts/validate.py`
- Host checks (when CLIs are present): `claude plugin validate .`, `agy plugin validate --strict .`
- Codex discovery: `codex plugin marketplace add howlil/goat-skill`, then `codex plugin marketplace list`
- No install, build, or application test command is needed.

## Boundaries
- Root `plugin.json` is the portable source of truth; compatibility manifests may mirror metadata but never skill instructions.
- Do not create extra skills, placeholders, MCP servers, hooks, agents, or runtime dependencies without a requirement.
- Do not duplicate canonical skill content into host-specific directories.
- Use the Agent Skills specification for required skill frontmatter and relative resource paths.
- Keep `name` and `version` consistent across all plugin manifests.
- Keep changes small; add validation only for real failure modes.
- No secrets. Never publish, tag, or merge without explicit approval.
