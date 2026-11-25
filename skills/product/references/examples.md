# Worked examples

These are fictional fixtures for choosing the amount of detail and the shape of a response.

Keep acceptance items independently checkable. Typically use one or two for small changes and three to seven for features. Use IDs when there are at least three items or another part of the task references them.

## Direct

The agreed behavior is that Clear filters restores the existing filter defaults and leaves the sort order alone.

> Direct. Restore the existing filter defaults and preserve the sort order.

Changing all the callers can be technically difficult while the product decision stays settled. If the request instead says “Reset the timer” and running timers can stop or continue, check the existing behavior or ask which state should follow reset.

## Shape a useful slice

Account holders need to save filtered activity. The activity list already supports a date filter and shows only the account holder's records. The first slice downloads one selected range. Repeated exports may follow once that workflow works.

```text
Outcome: Account holders can save activity for one selected date range.
Behavior: Select a range and download its activity as CSV.
Acceptance:
- A1 With matching records, the download contains all and only the account's records in the selected range.
- A2 With no matches, the app explains that there is nothing to download.
- A3 If preparation fails, the app reports the failure and preserves the selected range for retry.
Out of scope: Scheduled exports and delivery by email.
Constraints: Apply the same access rules as the activity list.
```

If older records lack reliable account ownership, establishing that ownership can be a prerequisite. Verify that affected records can be assigned reliably and that ambiguous cases remain inaccessible before shipping exports. Schema or UI work alone does not deliver the download.

## Shape the controlling choice

“Remove shared notes” is ambiguous when boards contain placements of the same note. Use the existing terms and a contrast.

> If note N is on boards A and B, should removing it from A leave B's placement intact? I recommend unlinking A's placement if the goal is board cleanup. Deleting N would remove it everywhere.

An explicit unlink request is ready without that question. Its acceptance checks that A stays unlinked after reopening while B still shows N. If unlinking fails, report it visibly and preserve A's placement.

## Block an irreversible action

“Plan cleanup of old user data” does not specify the retention policy or authorize deletion.

```text
Status: blocked for deletion. The target and retention rule are unresolved.
Question: Which data can expire, and what retention policy sets its cutoff?
Why: A cache and saved records have different recovery consequences.
Safe next step: Plan a read-only inventory and review of candidate data.
```

The plan can proceed within scope. Deletion needs explicit authorization of the selected data and effect.

## Discover whether work is warranted

Two support requests ask for easier downloads. Neither mentions recurring reporting. That supports looking at the download flow, but leaves demand for scheduled reports unverified. Recommend holding scheduled reports until direct evidence shows a repeated deadline and manual workflow. If a local prototype is authorized, bound it to sample data and check whether a user can specify the intended schedule. That result speaks to usability, not demand or production permission.

When two speed fixes leave report completion unchanged, check whether users reach the existing download in failed sessions. If they never reach it, another speed fix leaves that failure untouched.
