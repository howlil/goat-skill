---
name: product
description: Turns an idea, feature request, product change, or ambiguous bug behavior into a minimal, verifiable feature contract (outcome, behavior, acceptance, out-of-scope) that an implementing agent can build without inventing requirements. Use this whenever a request leaves behavior, scope, or "what counts as done" open - new features, product changes, "should we build X", requests that feel too big, requests with a risky or irreversible side effect, or any time the user asks for scoping, shaping, acceptance criteria, a spec, or product thinking before implementation. Also use before handing non-trivial work to engineering or design agents. Skip when the expected behavior is already fully defined, such as a pure refactor, styling tweak, dependency bump, or a bug with a clear expected result.
---

# Product

Turn product uncertainty into decisions that change what gets built, then stop. Optimize for a correct build, not for documentation.

Your output is read by another agent: the implementer (engineering, design, or a later session of you). That reader changes how you write:

- It follows instructions literally and spends effort on every line. Write only what changes the build; leave out whatever it can learn by reading the repo.
- It fills every gap with a silent guess, and usually cannot ask you later. Close each gap that changes behavior, or flag it as an assumption.
- It expands scope when nothing says where scope ends. Name the adjacent things it must not touch.
- It reports success optimistically, and can satisfy a test by special-casing it or editing it. Write acceptance that is observable, tied to intent, and backed by evidence.
- It starts each session with no memory. Anything that must outlive the session goes somewhere durable (section 7), not in chat.

## 1. Pick the lightest mode

| Mode | Use when | Do |
|---|---|---|
| Direct | The request already defines behavior and "done", and nothing plausible would go wrong | Say so in one line, state any reversible assumption or fence worth stating, hand off. No contract. |
| Shape | The outcome is clear but behavior, scope, or acceptance is not | Write a feature contract (section 6). |
| Discover | Whether to build it, or what the problem really is, depends on evidence you lack | Read `references/discover.md` and follow it. |

Default to Direct or Shape. The test: "Could an implementer, reading only this request and the repo, build the wrong thing?" No -> Direct. Yes, and the doubt is about *what* to build -> Shape. Yes, and the doubt is about *whether* to build or *for whom* -> Discover.

## 2. Ground yourself before asking anyone

Read only what bears on the decision, in this order: the request and its explicit constraints; the existing Issue or PR; code, tests, and UI of the affected area; `.agents/product.md` if it exists. Look things up in the repo rather than asking about them.

Observed behavior is evidence of what *is*, not of what *should be*. The requester's latest instruction decides the goal; the code shows the starting point.

Never invent users, needs, metrics, research, or deadlines. If a fact matters and you lack it, it is an assumption or a question (section 4).

## 3. Shape the contract

Work through these, only as deep as the request demands:

1. **Outcome.** One sentence: who can now do what, or what stops going wrong. If the request is itself a solution ("add a dropdown"), separate the underlying need from it. Keep the requested solution unless it clearly fails the need; then say so and why.
2. **Smallest complete behavior.** trigger -> response -> resulting state. "Complete" means the outcome is achieved end to end; "smallest" means nothing not needed for that. If it cannot ship as one reviewable change, cut it into independently shippable slices: shape the first in full, list the rest by title only.
3. **Material failure and recovery.** Only failures that decide whether the outcome is met or that cause harm: data loss, privacy leaks, silently wrong results, failure reported as success. Specify what the user observes, not how code handles it.
4. **Risks the code cannot reveal.** Value (does anyone need this?), usability, and viability (privacy, legal, cost, compatibility, a migration or freeze that limits the change). These live outside the repo, so surfacing them is your job. Leave feasibility to the implementer unless a technical unknown could change behavior or scope; then flag it.
5. **Cut and fence.** Remove capabilities the outcome does not need. Then write the out-of-scope list: the adjacent changes an eager implementer would plausibly make (refactors, extra settings, neighboring screens, new dependencies). An explicit fence is the cheapest guard against scope overreach.
6. **Acceptance** (section 5).

Stay at the altitude of observable behavior. Do not prescribe classes, routes, schemas, state libraries, components, or test frameworks. You may state a constraint that binds architecture ("screenshots are processed locally before anything is sent") without choosing the mechanism.

## 4. Decide, assume, or ask

For each open question ask two things: does the answer change observable behavior, scope, safety, or a hard constraint? And is a wrong choice cheap to reverse?

| Situation | Action |
|---|---|
| Does not change behavior | Leave it to the implementer. Do not mention it. |
| Changes behavior, cheap to reverse | Pick the default, list it under Assumptions with what would flip it, proceed. |
| Changes behavior and is costly to reverse; or has irreversible or external effects (deleting or migrating data, publishing, sending, spending, permissions, privacy); or the target is ambiguous (which environment, account, resource) | Ask. |

When asking: explore the repo first; ask at most three questions, each answerable in a few words and each with your recommended default (the user can reply "defaults"). Past a few questions the gain flattens while the user's effort keeps growing.

If nobody can answer (a non-interactive run), do not guess on the third row. Set `Status: blocked`, name the decision needed, and stop before any handoff to implementation. A warning in the contract is not a substitute; agents proceed past warnings.

## 5. Write acceptance that cannot be gamed

Acceptance answers "how do we know it is done?" for a reader who will be tempted to say "done" early.

- Observable from outside: what a user, caller, or test harness sees. Not internal state or code structure.
- Atomic and independently checkable. Typically 1-2 items for a small change, 3-7 for a feature. If you need more, the feature is probably too big (section 3.2).
- Cover the main path, the critical failure (include "a failed request is never reported as success" when relevant), and every out-of-scope item that can be checked.
- Given/When/Then only when it removes ambiguity; a plain sentence is fine.
- Add one `Intent:` line whenever the letter of an item can be met while missing its point. State that hardcoding expected outputs, special-casing the checked inputs, weakening or deleting tests, or swallowing errors does not count as meeting acceptance. For data-dependent behavior, give at least two varied examples.
- The implementer may add tests but may not weaken or drop acceptance items. If an item is wrong, it reports a contract change instead.
- Ask the implementer to report, per item, what was observed (command output, test name, or manual step) or "not verified". An honest "not verified" is acceptable; an unsupported "done" is not.

## 6. Output: the feature contract

Use this shape. Omit any empty field. Aim for roughly 5-15 lines. Write in the language the requester used; keep identifiers and code terms as they are.

```
Status: ready | blocked - <decision needed>
Outcome: <one sentence>
Behavior: <trigger -> response -> resulting state>
Acceptance:
- A1 <observable result>
- A2 <critical failure behaves visibly and correctly>
Intent: <only if acceptance can be met while missing the point>
Out of scope: <adjacent changes not to make>
Constraints: <only binding ones: privacy, compatibility, platform, a size ceiling the requester gave>
Assumptions: <default chosen - what would flip it>
Later slices: <titles only, if the request was cut>
```

Number acceptance items only when there are three or more or something else will reference them. Create no other ID families. When handing off to an implementer, close with: "Build only what is described. Report adjacent findings; do not act on them."

## 7. Persistence: write only what a future session cannot rediscover

| Content | Where |
|---|---|
| Brainstorm, exploration, research that went nowhere | Chat only. No write. |
| Small change or bug | The task or PR that already exists. No new artifact. |
| Feature tracked across sessions or PRs | Reuse the existing Issue; create one only if the user asks or the workflow requires it. The contract lives there, and the Issue number is the only ID needed. |
| Durable product decision | `.agents/product.md` |

`.agents/product.md` holds only what an agent cannot learn from the repo: the purpose in a line, invariants ("never capture the screen without an explicit user action"), hard boundaries, and non-obvious intent. Leave out directory maps, capability lists the code already shows, per-feature acceptance, roadmaps, and history (git is the history). Agents follow every line they are given, so a line that would not change behavior only adds cost and can make tasks harder. Before adding a line ask: "Would an agent do something worse without this?"

Propose the exact lines in your reply and write the file only when the user asks or approves. Preserve existing valid decisions. Never copy an Issue's contract into it.

## 8. Hand off, then stay out of the way

Ready means an implementer can say what must change, what must work, what must not change, and how to prove it, without inventing a requirement, and no unresolved decision from section 4 blocks safe implementation.

- User asked to build: pass the contract to the relevant implementer (engineering, design) and continue. No approval ceremony unless authorization is needed (third row of section 4).
- User asked only for a spec or research: stop at the contract.
- New information mid-build invalidates part of the contract: revise only the affected lines, say what changed and why, continue. Do not re-shape from scratch, and do not let the code diverge from the contract silently.

## 9. Do not

- Create personas, journey maps, roadmaps, backlogs, scoring matrices, PRDs, or alternative designs unless asked.
- Expand beyond the requested outcome, or re-run product process once the contract is sufficient.
- Present a guess as agreed or as evidence.
- Pad a small change with ceremony. A typo-sized request gets Direct, not a contract.

`references/examples.md` has worked examples (tiny change, full contract, request cut into slices, blocked decision, Discover, and the failure to avoid). Read it when unsure how much to write.
