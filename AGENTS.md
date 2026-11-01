# Goat Skill — repository instructions

## Purpose
Maintain one portable library of software-engineering agent skills. This repository is in scaffold-only state until a skill is explicitly requested.

## Structure
- `skills/<name>/SKILL.md`: canonical instructions; optional resources live within the same skill.
- `plugin.json`: portable Codex/Agent Plugins identity.
- `.claude-plugin/`, `.antigravity-plugin/`: host-specific distribution metadata.
- `.agents/plugins/marketplace.json`: Codex local marketplace.
- Project constraints: `.agents/product.md`; architecture and verification: `.agents/engineering.md`; UI: `.agents/DESIGN.md`.

## Commands
- Validate: `python3 scripts/validate.py`
- Host checks (when CLIs are present): `claude plugin validate .`, `agy plugin validate --strict .`
- No install, build, or application test command is needed.

## Boundaries
- Do not create a skill, placeholder `SKILL.md`, MCP server, hook, agent, or runtime dependency without a requirement.
- Do not duplicate canonical skill content into host-specific directories.
- Use the Agent Skills specification for required skill frontmatter and relative resource paths.
- Keep `name` and `version` consistent across all plugin manifests.
- Keep changes small; add validation only for real failure modes.
- No secrets. Never publish, tag, or merge without explicit approval.
