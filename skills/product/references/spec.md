# Spec form

Use when a feature needs more than one shippable slice or will be built across sessions, so the contract must outlive the chat and keep the build honest. A change that fits in one PR keeps the plain contract (SKILL.md section 6) in the task or PR instead.

The spec is the contract the code is checked against, not a planning document. It holds product behavior only; implementation plans, data models, and task lists belong to the implementation owner when needed.

## Contents
- Where it lives
- Slicing
- Format
- Keeping it true, then making it disappear

## Where it lives

1. An existing Issue when the work uses an issue tracker: the spec is the Issue body; slices become sub-issues only if the workflow already does that.
2. Otherwise the repo's existing spec location; if there is none, `specs/<feature-slug>.md`.

Use the requested destination. Write or update a single spec when the request and existing workflow authorize the destination. Otherwise return it in the reply. Issue creation follows SKILL.md section 7.

## Slicing

- Shape only the next vertical slice in full. Give later slices a capability title and a blocker only when it gates delivery.
- If a necessary technical prerequisite blocks the next slice, show why and what observable evidence clears it. The implementer chooses how to deliver it.
- Every slice must be core to the outcome. A nice-to-have does not become a later slice; it is cut and not recorded.
- Appetite caps the work: the time or size the requester will spend (for example "one PR per slice, two weeks total"). Scope is shaped to fit the appetite, never the reverse. If a slice outgrows it during the build, the implementer stops and reports; re-shape by cutting, and extend only if the requester decides the remaining work is core.

## Format

Omit empty fields. Write acceptance as observable statements; use `When <event>, <result>.` / `If <unwanted condition>, <result>.` / `While <state>, <result>.` wherever the trigger is what makes the item testable.

```text
# <Feature name>
Status: draft | ready | in progress | blocked - <decision needed>
Outcome: <one sentence>
Appetite: <the budget the requester gave, if any>
Terms: <term = the one meaning used here, only for ambiguous or overloaded words>
Constraints: <binding ones only, including realistic scale>
Unchanged: <neighboring behavior at risk that must stay exactly as today>
Transition: <what happens to existing data, users, or clients at release; reversible or not>
Out of scope: <adjacent changes not to make>
Assumptions: <default chosen - what would flip it>
Open: [OPEN: <question> - default: <answer>]

## Slice 1: <title> - ready
Delivers: <the capability a user or caller gains>
Acceptance:
- A1 When <event>, <observable result>.
- A2 If <failure>, <visible, correct behavior; never reported as success>.
Intent: <only if acceptance can be met while missing the point>

## Slice 2: <capability title> - later
Blocked by: <only when a real blocker exists>
```

`Status: ready` requires no `[OPEN: ...]` item that would change the next slice. Open items that only affect later slices may stay.

Name what the owner or caller sees, in plain words. No code identifiers, routes, file paths, or stored state values: write "the subscription is past due", not the enum value. The implementer finds those in the code.

Budget: about 50 lines for the whole file. Terms and Assumptions take at most three lines each. If the file does not fit, the feature is too big: cut it or split it into separate features.

## Keeping it true, then making it disappear

A spec tracks remaining work and can hold durable constraints or rationale until their approved destination is updated.

- When intent or evidence changes during a build, update only affected criteria in the same change and flag what needs re-verification.
- The implementer may add acceptance items but never weakens or drops one; if an item is wrong, it proposes the contract change and says why.
- When a slice ships, collapse it to one line, `## Slice 1: <title> - done (<PR or commit>)`, and shape the next slice. Tests carry completed acceptance. Keep any unique durable decision or rationale until it reaches its approved source.
- Before retiring a completed spec, identify invariants, definitions, and consequential rationale that code and tests cannot reconstruct. Propose the smallest update to the existing authorized source per SKILL.md section 7. Preserve the decision in the spec until that update is approved and made, then retire through the authorized workflow. If code and tests already carry what matters, retire without a new record.
