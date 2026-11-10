# Product

## Purpose
Reusable software-engineering agent skills installable across Codex, Claude Code, Agy, and skills.sh without duplicated platform-specific instructions.

## Invariants
- The canonical skill contents live under `skills/<name>/`; manifests only package them.
- The plugin identity is `gs`; the canonical catalog currently contains `product` and `design`.
- `product` owns product uncertainty, scope, acceptance, and evidence-driven discovery.
- `design` owns frontend implementation/refinement/audit and consumes product scope rather than redefining it.
- `product` minimizes specification overhead; never invent evidence, stakeholders, metrics, or decisions.
- When an external, irreversible, or expensive product choice is unresolved, block rather than assuming.
- No publication, installation claim, or new skill without the required evidence and authorization.

## Open decision
Select a distribution license before public release.
