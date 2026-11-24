# Engineering

The `gs` plugin distributes three Agent Skills from `skills/product/`, `skills/frontend/`, and `skills/backend/`. Each skill can be installed on its own and all of its resources live inside its directory. Shared project guidance lives in `AGENTS.md`, which applies where the host loads it. Each installed skill carries the instructions it needs to work independently.

## Packaging

- Root `plugin.json` is the portable source of truth. The Codex fallback manifest mirrors the identity and OpenAI interface metadata and points to the canonical `./skills/` directory.
- Claude Code, Antigravity, and marketplace manifests package the same library. Keep the plugin name, version, and description in sync.
- The package consists of static instructions and metadata. Keep specialized testing, architecture, security, operations, review, and delivery guidance within the concern that owns the work.
- The change from `design` to `frontend` is an invocation rename. The current development version is 0.5.0.

## Verification and release

- Run `python3 scripts/validate.py`. CI runs the same check for the exact catalog, skill names and required fields, direct Markdown references, and manifest consistency.
- Check installation and discovery in the target hosts before claiming native support. Run representative tasks to verify that each concern can operate independently and that combined changes respect the public contract.
- Choose a distribution license before the first public release. Publishing, tagging, and merging require explicit approval.
