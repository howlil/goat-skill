# Engineering

## System
Static GitHub repository. Agents load canonical `skills/<name>/SKILL.md` according to the Agent Skills specification. Plugin manifests provide host-specific discovery; they do not contain instruction copies.

## Structure & responsibility
- `skills/`: sole owner of skill instructions and per-skill resources.
- Root `plugin.json`: portable Agent Plugins / Codex manifest.
- `.claude-plugin/`: Claude Code manifest and marketplace.
- `.antigravity-plugin/`: Agy manifest override.
- `.agents/plugins/marketplace.json`: Codex local catalog.
- `scripts/validate.py`: metadata consistency and basic skill layout checks.

## State & contracts
No runtime or persisted user state. All manifests share the same plugin name and version. Skill folder and YAML `name` must match. The plugin is named `gs` (Claude command `/gs:product`); other hosts use their own invocation syntax.

## Verification
Local: `python3 scripts/validate.py`; CI: same command on push/PR.
Static validation also enforces required Codex marketplace policy/category metadata.
Host smoke checks are pending: `claude plugin validate .` and `agy plugin validate --strict .`.
A passing static check is not proof of plugin installation or working skill behavior.

## Release
Do not publish or tag before deliberate release approval. Before first public release: choose a license, run host-specific installation checks and product-skill behavior evaluations.
