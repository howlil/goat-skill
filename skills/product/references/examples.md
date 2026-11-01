# Worked examples

All examples are illustrative: the repo facts are made up to show shape and size. Match the proportion, not the content.

## Contents
1. Tiny change -> Direct
2. Feature -> Shape contract
3. Too big -> blocked, then sliced
4. Irreversible effect -> blocked
5. "Should we build it?" -> Discover
6. The failure to avoid

## 1. Tiny change -> Direct

Request: "tambah tombol reset timer"

Output (Indonesian, because the requester wrote Indonesian):

> Direct: perilaku sudah jelas, tidak perlu kontrak. Asumsi (mudah dibalik): reset mengembalikan timer ke durasi awal dan membiarkannya berhenti. Jangan ubah penyimpanan timer atau tambah dialog konfirmasi.

Why this is enough: one reversible assumption and one fence. Anything longer is ceremony.

## 2. Feature -> Shape contract

Request: "Build an AI screenshot feature triggered by a hotkey." Context found in the repo: a Windows desktop assistant that runs local CLI AI providers; `.agents/product.md` says never capture the screen without an explicit user action.

```text
Status: ready
Outcome: A user can ask the AI about the active screen from a shortcut, without opening the chat UI first.
Behavior: Hotkey -> capture the active screen -> submit it with the user's prompt -> show the response where other AI results appear.
Acceptance:
- A1 A valid shortcut starts exactly one analysis; pressing it again while one runs does not start a second.
- A2 When the analysis finishes, the result can be found in the usual results place.
- A3 If capture permission is denied, no image is sent anywhere and the user sees a message saying what to do next.
- A4 A failed analysis is shown as failed, never as success.
Intent: Capture happens only because the user pressed the shortcut.
Out of scope: OCR history, multi-monitor capture, annotation tools, new settings pages.
Constraints: Never capture without explicit user action (product.md). Process the image locally before it reaches the provider.
Assumptions: Active monitor only. The image is not kept after the request completes (safe default; flip only if the user wants history).
```

Why it works: each line changes what gets built. A3 and A4 cover the failures that matter; the Intent line blocks the cheap way to pass A1; the assumptions name the privacy defaults instead of leaving them implicit. No class names, no API routes, no test framework.

## 3. Too big -> blocked, then sliced

Request: "Redesign all the pages of the app."

```text
Status: blocked - the problem driving the redesign is unknown.
The app has several screens. Two questions (reply "defaults" to accept the bracketed answers):
1. What is wrong today that the redesign should fix? [Inconsistent spacing and controls across screens]
2. Which screen do people use most? [The main window]
Proposed cut: Slice 1 is the main window only, judged against the problem you name.
Later slices, by title: Settings, History, Onboarding. Each is shaped when reached.
```

Why: a redesign with no stated problem cannot be verified, and "all pages" invites an unreviewable change. Fence the scope, ask the one thing that decides it, and give a default.

## 4. Irreversible effect -> blocked

Request: "Clean up old user data so the app uses less disk space."

```text
Status: blocked - "old" and "user data" are undefined, and deletion cannot be undone.
Questions (reply "defaults" to accept):
1. Which data? [Cached screenshots and temp files only; never chats, settings, or history]
2. What makes it old? [Not used for a period you choose; tell me the period]
3. Delete immediately or show first? [Show what would be removed and its size; delete only after you confirm]
Nothing is deleted until these are answered.
```

Why: third row of the decision table. A wrong guess here is not recoverable, so the contract blocks instead of choosing a default.

## 5. "Should we build it?" -> Discover

Request: "Research whether OCR history is worth building."

```text
Decision: Build OCR history / do not build / build a smaller version.
Question: Do users come back to previously captured text, and does anything already serve that need?
Evidence: Two Issues ask for finding older results; none mention OCR. No usage data is available.
Assumptions: People who capture screens want to re-find the text later (unverified).
Recommendation: Do not build yet. Confidence: low.
What would change it: Repeated requests from frequent capturers, or data showing past results are reopened.
Next smallest step: Add a counter for reopened past results, or ask five active users.
```

Why: evidence and assumptions are separated, the missing data is stated as missing, and the output is a recommendation with its flip condition, not a PRD.

## 6. The failure to avoid

A one-line bug fix expanded into four user stories carrying sixteen acceptance criteria, each restating that the system should be robust. Nothing in it changed what got built, and reviewing it cost more than the fix.
