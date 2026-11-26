# Worked examples

These fixtures are synthetic. Match their form and length to the request.

## Direct and material ambiguity

Request: "Tolong scope saja: ubah label Start menjadi Resume saat timer dijeda." The paused state already exists and the click behavior stays the same.

> Direct: Saat timer dijeda, labelnya menjadi Resume. Perilaku tombol tetap sama.

With "tambah tombol reset timer" and no reset convention, ask whether resetting a running timer stops it or starts a fresh countdown. Either result can surprise the user. Existing reset-and-stop behavior on the same timer would settle that choice.

## Shape a shared-note contract

A reusable Note can appear on several Boards. "Delete this note from the board" could mean removing the placement or erasing the shared Note. Ask which effect the editor intends. Recommend removing the placement because it preserves the other Boards. Global deletion needs explicit authorization for that scope.

After the user chooses unlinking:

```text
Status: ready
Outcome: A board editor can remove a Note from this Board and keep it available elsewhere.
Behavior: The editor removes a placement and the Note disappears from this Board.
Acceptance:
- A1 With the Note on two Boards, removal affects only the selected Board.
- A2 After reopening the selected Board, the placement is still absent.
- A3 If removal fails, the placement remains or is restored and the editor sees the failure.
- A4 Someone without editing rights cannot remove a placement.
Out of scope: Global deletion, trash, new note types.
```

## Blocked destructive scope

Request: "Plan how to clean up old user data and use less disk space." The app stores caches and user history.

```text
Status: blocked - deletion target and retention rule are open.
Known: Caches and user history have different consequences if removed.
Question: Which data is eligible for cleanup? I suggest checking caches first.
Why: That choice determines the retention rule and what a purge could erase.
Safe next step: If authorized, list candidate cache sizes without changing them.
```

A reply accepting defaults settles only a safe planning choice. Before any purge, get explicit authorization for the specified target, criteria, and effect.

## Challenge a premise

Two changes to hover delays failed to stop an unexpected dock opening. Both assumed the hover timer initiated the open. Check whether a failing open occurred without a hover event. If it did, another delay control cannot fix that failure. Preserve the agreed activation behavior and leave diagnosis and mechanism to the implementation owner.

## Discover demand

Request: "Research whether OCR history is worth building." Two issues ask for finding old results. Neither identifies OCR results. Existing search establishes that retrieval is possible.

```text
Decision: OCR history, reuse existing results, or defer.
Question: Do people need to retrieve captured text that current results cannot help them find?
Evidence: Two issues mention finding results. They show retrieval friction. OCR-specific demand is unknown.
Assumptions: OCR users experience that same friction.
Recommendation: Defer OCR history, low confidence.
What would change it: Reports from capture users that they repeatedly lose text they need later.
Next smallest step: Review existing capture-related requests for that pattern.
```

## Grill in rounds

Request: "aku mau fitur langganan di app kasir ini, belum tahu detailnya". The app has store owners and cashiers and already handles one-time payments.

> Q1 Langganan ini untuk pemilik toko membayar penggunaan aplikasi, atau pelanggan toko membayar pembelian rutin? Saya sarankan mulai dari pemilik toko karena itu sesuai alur yang sudah ada.

If the user chooses store owners, resolve which capability lapses and protect selling. If they choose store customers, owner report access is irrelevant. Ask the next question only if its answer changes the outcome.

## Spec with a real dependency

The requester has chosen monthly owner subscriptions to unlock reports. They require that selling always works and approved a three-day grace period. The first slice lets the owner subscribe and see reports unlock only on payment confirmation. Verify that reports stay locked and failure is visible when payment fails, sales still work, and cashiers cannot subscribe. Later slices can be listed as:

```text
## Renewal with a three-day grace period - later
Blocked by: Subscribe and unlock reports

## Cancel and keep access until the paid period ends - later
Blocked by: Subscribe and unlock reports
```

If an existing client needs compatible identifiers before that first capability can work, describe the compatibility proof as a prerequisite. The implementer chooses the mechanism.

## Off-focus request

Recorded focus: "owner subscription renewal." Request: "tambahin dark mode dong".

> Status: blocked - bukan prioritas. Fokus sekarang perpanjangan langganan. Dark mode layak didahulukan jika tampilan saat ini menghambat kasir di toko yang gelap, atau jika kamu menetapkannya sebagai fokus.

## Bug form

Request: "A refund should reduce the report total on the day of the refund." Daily reports are computed when opened.

```text
Status: ready
Current: Sell 100, refund it on the same day, then open the report. It shows 100.
Expected: The same report shows 0.
Unchanged: Totals for days without refunds and existing CSV columns.
Transition: Past reports reflect the corrected totals on open.
Acceptance:
- A1 The sell-and-refund reproduction fails before the fix and passes after.
- A2 Refunding 240 on the following day leaves the sale day total intact and reduces the refund day total by 240.
- A3 Existing fixture data without refunds produces the same totals.
Intent: The calculation must hold for other amounts and dates.
```
