# Goat Skill

Three composable engineering skills for coding agents. Each owns a part of the work and can start wherever the task needs it.

| Skill | Responsibility | Examples |
| --- | --- | --- |
| [Product](skills/product/SKILL.md) | Intent, scope, observable behavior, and acceptance | Evaluate an idea, shape a feature, clarify an ambiguous failure |
| [Frontend](skills/frontend/SKILL.md) | Public interfaces and contracts for people, programs, and devices | Web or desktop UI, CLI flags and output, SDK exports, HTTP endpoints, device signals |
| [Backend](skills/backend/SKILL.md) | Internal logic, authoritative state, and execution | Domain rules, algorithms, migrations, runtime behavior, jobs, firmware |

The boundary depends on who consumes the software. For a CLI, commands and output belong to Frontend and command execution belongs to Backend. For a database, the query contract belongs to Frontend and the storage engine belongs to Backend. Product owns the outcomes and guarantees that both deliver.

## Choose the concerns the task changes

| Request | Skills |
| --- | --- |
| Evaluate whether to build an idea | Product |
| Improve keyboard interaction on an existing screen | Frontend |
| Fix a slow database query behind a stable interface | Backend |
| Implement an already-defined API behavior | Backend |
| Design and implement a new API contract | Frontend + Backend |
| Build a new application from an unshaped idea | Product + Frontend + Backend |
| Rename a private variable | None |

Architecture, testing, security, performance, observability, review, and delivery belong to the concern that owns the change. For example, Product defines the observable acceptance, Frontend verifies the public interaction, and Backend proves the relevant state or execution invariant. Load each skill's references when their guidance changes what you do.

`AGENTS.md` holds shared engineering principles for projects whose host loads it. The installed skills are self-contained so they also work when installed individually.

## Install and invoke

The current development version is **0.5.0**. The commands below install from the repository. Existing `design` users should invoke `frontend`, which includes the visual design guidance and covers programmatic interfaces too.

### Codex

```bash
codex plugin marketplace add howlil/goat-skill
codex plugin add gs@goat-skill-marketplace
```

Invoke `$gs:product`, `$gs:frontend`, or `$gs:backend` from the plugin. Marketplace snapshots may need an upgrade to pick up repository changes.

### Claude Code

```bash
claude plugin marketplace add howlil/goat-skill
claude plugin install gs@goat-skill-marketplace
```

The expected plugin commands are `/gs:product`, `/gs:frontend`, and `/gs:backend`.

### Antigravity

```bash
agy plugin install https://github.com/howlil/goat-skill
```

The expected commands are `/product`, `/frontend`, and `/backend`.

### Skills CLI

```bash
npx skills add howlil/goat-skill
```

Select the skills you want. Individual installations use the plain skill names.

## Verify

```bash
python3 -m pip install -r scripts/requirements.txt
python3 scripts/validate.py
python3 scripts/test_validate.py
```

CI validates the portable manifest against a checked-in schema, parses skill frontmatter as YAML, and checks the catalog, reference paths, and shared packaging metadata. Regression tests exercise the same validation command on clean and broken packages. Verify native installation and discovery in each host separately.

### Compare agent behavior

Use a clean, signed-in Codex CLI profile and the same model for both sides of each pair. The runner installs the relevant skill in one copy of the fixture.

```bash
python3 evals/run.py --model gpt-5.4-mini
```

The default eval runs a UI label fix, a CLI error contract change, and a database retry fix in disposable projects. Each case runs once with a skill and once without it. Use `--case` to run one pair.

Add `--routing` to compare a mechanical edit and an ambiguous deletion request. The skill-enabled runs make all three skills available and let Codex choose what to use. Results include first-attempt correctness, token usage, elapsed time, and skill file paths visible in successful shell commands.

## Licensing

Distribution license selection is pending.

## Influences

The independent skills draw on Matt Pocock's emphasis on small, composable guidance. Runtime checks draw on Lauren Tan's PStack emphasis on reproducing failures and proving behavior at the boundary. [Matt Pocock's skills](https://github.com/mattpocock/skills) · [Lauren Tan's PStack](https://github.com/poteto/plugins/tree/HEAD/pstack)
