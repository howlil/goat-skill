# Motion engineering

Use for anything beyond a simple state transition: layout or shared-element motion, enter and exit animation, looping or autoplaying motion, or scroll-linked effects.

## Contents
- Decide before animating
- Implementation rules
- Reduced motion
- Verify

## Decide before animating

Answer these in a line each. If you cannot, do not animate.

| Question | Example answer |
|---|---|
| Trigger | the user expands a panel |
| Purpose | show continuity from compact to expanded |
| Properties | position, scale, opacity |
| Interruption | can be reversed mid-way |
| Reduced motion | instant change or a short fade |
| Owner | shared preset or this feature |

Loading, feedback, and layout transitions do different jobs; do not give them all the same animation. Motion that answers a user's action is usually justified. Motion that plays unprompted needs a reason and should be rare.

## Implementation rules

- Reuse the project's presets (often a file such as a `motion` module) and the motion library already installed. Add timing and easing to the shared presets, not inline in components.
- Prefer animating `transform` and `opacity`. Animating layout properties (width, height, top, left) forces layout work; use it only when nothing else expresses the change, and measure on the target runtime.
- Make interactive transitions interruptible and reversible, so a second click mid-animation does not queue behind the first.
- Never block the next action until an animation finishes.
- Exits need a mechanism (the library's presence handling) so removed elements are not left in the tree.

## Reduced motion

Honor `prefers-reduced-motion`: reduce or replace non-essential movement (large travel, parallax, zoom, sliding panels) with an instant change or a short fade. The goal is less motion, not no feedback. Autoplaying or looping motion that lasts more than a few seconds also needs a pause control, which the media query alone does not provide.

## Verify

- Emulate reduced motion in the browser and check each animated state.
- Trigger the transition, then trigger it again or reverse it halfway.
- Confirm focus and keyboard behavior are unchanged during and after the animation.
- Report these as "not verified" if you had no way to run them.
