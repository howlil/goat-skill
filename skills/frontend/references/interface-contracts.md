# Programmatic interfaces

Open this when designing or changing a contract used by programs or devices. Read callers and existing contracts first. Use a small example call to make the intended consumption clear.

## Define what callers can rely on

- Name the entry point, the public input types, required fields or flags, defaults, and the success result. Include only guarantees callers need, such as ordering, units, schema stability, or timeout behavior.
- Define what invalid input, authorization failure, unavailable data, and partial results look like where applicable. Give automated consumers stable error codes or discriminants and useful guidance for recovery.
- Make side effects and retry expectations explicit. Carry validated inputs and caller context to the implementation boundary. The owner of protected state enforces its own authorization and invariants.
- Preserve existing callers. Check released schemas, public types, flags, and outputs before removing or changing them. Plan an explicit change path for compatibility breaks.

## Apply the surface's conventions

| Surface | Contract details that often matter |
| --- | --- |
| CLI | Flags, exit status, stdout for results, stderr for diagnostics, and machine-readable output when scripts rely on it |
| HTTP or events | Input and output schema, errors, pagination, versioning, and delivery or retry semantics |
| SDK or library | Exported names and types, caller defaults, errors, and resource lifetime |
| Device or agent | Commands or signals, declared capabilities, acknowledgements, units, and externally visible failure behavior |

Use the smallest test that exercises the real boundary. For example, run an actual command and assert its exit status and output streams, or send a request through the production router and assert the public response. Exercise an existing caller when compatibility is at risk.
