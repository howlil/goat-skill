# UX flows and states

Use when adding navigation, a multi-step flow, or when an interaction question is unresolved. Skip it for a single-state change.

## Contents
- Model the flow only as far as needed
- State checklist
- Choosing a research method
- Interface wording

## Model the flow only as far as needed

Write the flow as a short table of trigger, state, outcome for the surfaces involved. Draw a sitemap only when the navigation structure changes. Stop once the next implementation decision is clear.

| Trigger | State | Outcome |
|---|---|---|
| user action or event | idle, pending, success, failure | what the user sees and can do next |

Decide the state owner and the surface (inline, panel, dialog, page) after the flow is clear, not before.

## State checklist

Cover the ones that apply, and skip the rest without comment:

- Loading: show structure or progress, and never block unrelated actions.
- Empty: say what belongs here and offer the action that fills it.
- Error: say what happened and how to fix it; offer retry when retry can work.
- Partial or stale data: show what is available and mark what is not.
- Destructive actions: allow undo, or confirm with the name of the thing being affected.
- Forms: validate where the mistake is made, keep what the user typed, and keep labels visible.
- Focus: after a dialog closes, an item is deleted, or a route changes, put focus somewhere sensible.
- Layout: check compact, expanded, and the narrowest supported width, and text longer than your sample.

## Choosing a research method

Choose by what is uncertain, not by habit:

- A visible usability problem: a heuristic review of the screen is enough.
- Unknown whether people can complete the task: a task-based usability test.
- Unknown whether the need exists: user research, which is a product question; flag it rather than inventing findings.

Never fabricate user feedback. If you did not observe it, it is an assumption.

## Interface wording

Words are part of the interface. Name actions by what happens ("Save changes", not "Submit"), keep one name for an action through the whole flow, and write errors that explain the cause and the fix without apologizing. Match the vocabulary already in the product.
