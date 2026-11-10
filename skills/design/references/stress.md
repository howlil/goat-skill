# UI stress testing

Use when a surface is data-driven, content-heavy, responsive, localized, or explicitly needs edge-case testing. Also use during an Audit when normal demo data can hide layout or state failures.

This is adversarial verification, not a redesign mode.

## Goal

Feed the interface the hardest data a real user or real system can plausibly produce, then observe what fails.

The standard is realism, not absurd length.

## 1. Derive extremes from the domain

Inspect the actual source of rendered values:

- schema or type;
- API contract;
- database or validation limits;
- whether the field is optional;
- representative existing data;
- product-supported locales and writing directions.

Prefer a plausible extreme or a real contract limit.

Bad:

```text
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
999999999999999999999999999999
```

Better:

```text
a legitimate long organization/person/file name
the maximum meaningful count or amount for this domain
an empty optional field
exactly one result
a localized label that is materially longer than the sample
```

Never change component markup just to manufacture a failure. Change data or environment at the real input boundary.

## 2. Cover the dimensions that apply

### Content

- empty;
- minimum valid;
- normal;
- long but plausible;
- maximum contract-backed;
- missing optional value;
- unusual but valid script, punctuation, or emoji when allowed.

### Cardinality

- zero;
- one;
- few;
- many;
- maximum practical page/batch where the product defines one.

### State

- loading;
- partial or stale data;
- success;
- recoverable error;
- retrying;
- disabled or permission-limited state when applicable.

### Layout and environment

- narrowest supported width;
- normal width;
- widest meaningful layout;
- browser or OS zoom when applicable;
- localization;
- RTL only when the product supports it;
- dark/light themes when both are supported;
- reduced motion for animated surfaces.

Do not run irrelevant dimensions merely to complete a checklist.

## 3. Exercise one variable at a time first

A single "worst case" fixture can hide root causes.

Start by varying the field or condition most likely to break the interface. Once individual failures are understood, combine realistic extremes to check interaction between them.

This keeps the finding attributable.

## 4. What counts as a break

Report observable failures such as:

- clipped or unreachable content;
- actions pushed out of a usable region;
- overlap;
- accidental horizontal scrolling;
- hierarchy collapsing under long content;
- orphaned punctuation or labels when optional data disappears;
- misleading truncation;
- unusable controls at narrow widths;
- loading/error states changing layout unpredictably;
- focus or keyboard order no longer matching the visible interface.

Aesthetic dislike alone belongs to visual review, not stress testing.

## 5. Fix the underlying contract

Prefer fixes that make the component robust for the valid input space:

- allow the intended region to shrink/wrap;
- define deliberate truncation;
- stabilize action regions;
- change the responsive transformation;
- paginate/virtualize only when volume actually requires it;
- handle absence explicitly;
- keep state transitions structurally consistent.

Do not special-case only the fixture value.

## 6. Report

For each material break:

```text
[severity] <surface/location>
Input: <realistic extreme>
Observed: <what breaks>
Fix: <smallest structural direction>
Verified: <what was rerun>
```

Also state which stressed conditions held up so the test does not encourage unnecessary change.

## Robustness gate

A data-driven or responsive surface is not robust merely because demo data renders. When stress is material to the request, verify at least one realistic extreme from the changed risk and report the rest as not verified.

## Influence

This reference is an original Goat Skill synthesis informed by worst-case-data methods from Emil Kowalski's Break UI skill and mblode's UI Design Break mode:
https://github.com/emilkowalski/skills/blob/main/skills/break-ui/SKILL.md
https://github.com/mblode/agent-skills/blob/main/skills/ui-design/SKILL.md
