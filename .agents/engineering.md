# Engineering

## System
Static GitHub repository. Agents load canonical `skills/<name>/SKILL.md` according to the Agent Skills specification. The root portable manifest is authoritative; host-specific metadata must not duplicate skill instructions.

## Structure & responsibility
- `skills/`: sole owner of skill instructions and per-skill resources.
- `plugin.json`: canonical portable Agent Plugins manifest and OpenAI presentation metadata.
- `.codex-plugin/plugin.json`: Codex compatibility fallback; points to the canonical `./skills/` directory.
- `.claude-plugin/`: Claude Code manifest and marketplace.
- `.antigravity-plugin/`: Agy manifest override.
- `.agents/plugins/marketplace.json`: Codex repo-local catalog and install policy.
- `scripts/validate.py`: cross-manifest, marketplace, interface, path, and skill-layout checks.

## State & contracts
No runtime or persisted user state. All plugin manifests share `name=gs` and `version=0.2.0`. Root `plugin.json` owns portable identity. The Codex compatibility manifest must match its identity, author, repository, and OpenAI interface metadata and must expose `./skills/`. Skill folder and YAML `name` must match.

## Verification
Local and PR gate: `python3 scripts/validate.py`.
The gate verifies portable schema/identity, Codex compatibility fallback, OpenAI interface metadata, repo marketplace policy/category/display name, host manifest identity/version, skill frontmatter, and referenced Markdown paths.
Native host discovery remains release evidence: Claude `/gs:product`, Codex `$product`, and Agy `/product`.
Model behavior remains separate evidence: Direct / Shape / Discover / blocked-decision prompts must be exercised in an actual agent runtime.

## Release
Do not publish or tag before deliberate release approval. Before first public release: choose a license, run native host installation/discovery checks, run behavior evaluations, and complete any directory listing/legal metadata required by the target host.
