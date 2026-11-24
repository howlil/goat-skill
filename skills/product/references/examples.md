# Worked examples

These scenarios are fictional. Use them to gauge how much detail a request needs.

## Contents
1. Tiny change -> Direct
2. Feature -> Shape contract
3. Too big -> blocked, then sliced
4. Irreversible effect -> blocked
5. "Should we build it?" -> Discover
6. The failure to avoid

## 1. Tiny change -> Direct

The request is to make Clear filters restore the default filters.

> Direct. Restore the existing filter defaults when Clear filters is pressed. Keep the current sort order.

The requester specified the behavior. Keeping the current sort order is a reversible default.

## 2. Feature -> Shape contract

The request is to let account holders download their filtered activity. In this scenario, the activity list already supports a date filter, and each account holder can view only their own records.

```text
Outcome: Account holders can save a copy of the activity that matches their selected date range.
Behavior: Choose a date range and select Download. The app prepares a CSV and starts the download.
Acceptance:
- A1 When the range matches records, the CSV includes every matching record and excludes records outside the range.
- A2 When the range matches zero records, the app shows that there is nothing to download.
- A3 If preparation fails, the app shows an error and the selected range remains available for retry.
Out of scope: Scheduled exports and delivery by email.
Constraints: The export follows the same account access rules as the activity list.
```

The acceptance checks cover matching records, an empty result, and a failed attempt. The access rule applies to the download as well as to the list.

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
1. Which data? [Regenerable cache files only. Preserve saved user data.]
2. What makes it old? [Not used for a period you choose; tell me the period]
3. Delete immediately or show first? [Show what would be removed and its size; delete only after you confirm]
Nothing is deleted until these are answered.
```

Why: third row of the decision table. A wrong guess here is not recoverable, so the contract blocks instead of choosing a default.

## 5. "Should we build it?" -> Discover

The request is to research whether customers need scheduled activity reports.

```text
Decision: Offer scheduled reports, improve manual downloads, or keep the current behavior.
Question: Do customers download reports on a recurring schedule?
Evidence: Two support requests ask for easier downloads. The frequency of downloads is unknown.
Assumptions: Repeated manual downloads indicate a recurring reporting need (unverified).
Recommendation: Do not build yet. Confidence: low.
What would change it: Several customers report a recurring deadline and describe the same manual steps.
Next smallest step: Ask customers who already use manual downloads how often and why they use them.
```

Why: evidence and assumptions are separated, the missing data is stated as missing, and the output is a recommendation with its flip condition, not a PRD.

## 6. The failure to avoid

A one-line bug fix expanded into four user stories carrying sixteen acceptance criteria, each restating that the system should be robust. Nothing in it changed what got built, and reviewing it cost more than the fix.
