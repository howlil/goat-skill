# AI features

Use when observable behavior depends on a model's output: LLM generation, extraction, classification, ranking, or an agent that calls tools. The same input can give different outputs, so "returns X" cannot be the acceptance. The contract must say what "good enough" means, how it is judged, and what the user sees when the model is wrong.

Everything in SKILL.md still applies. This file changes only acceptance, failure behavior, and a few constraints.

## Contents
- Acceptance becomes an eval set
- Failure, uncertainty, and actions
- Constraints worth stating
- Acceptance that cannot be gamed
- Example

## Acceptance becomes an eval set

1. **Cases.** A small set of real or realistic inputs, usually 5-20: typical ones, hard ones (messy, ambiguous, long, other languages the product supports), and ones where the right answer is "nothing" or "I can't". Take them from the requester or from real data within privacy rules; write them together if neither exists. A set of synthetic happy cases proves nothing.
2. **Pass bar.** An observable threshold over the set: "total and date match exactly on at least 10 of 11 invoices". Harm is zero-tolerance, not a percentage: leaking private data, acting without confirmation, following instructions hidden in the input.
3. **Grading.** How each case is judged: exact match, a rule, a human check, or a model grader. If a model grades, write its rubric in the contract and have a human spot-check a few grades.
4. **Runs.** Outputs vary, so the bar holds across repeated runs (state how many, usually 3) at the settings production uses.

The eval cases live with the tests, wherever the implementer keeps test data. They are the acceptance; do not copy them into the spec or `.agents/product.md`.

## Failure, uncertainty, and actions

- Say what the user sees when the model times out, refuses, returns malformed output, or is unsure: an empty field marked for review, "couldn't read this", a request to confirm. A guess is never shown as fact, and malformed output never reaches stored data silently.
- If model output triggers a side effect (send, delete, pay, write records, call an external tool), require an explicit user confirmation or make the step reversible. The eval includes cases where it must not act.
- Text from users, files, web pages, or tool results is data, not instructions. Include at least one case whose input contains instructions aimed at the model, and require that they are ignored.

## Constraints worth stating

Only when binding: a latency or cost ceiling per request the requester gave; where data may go (local only, no provider retention, a region); what must never be sent to a model. The model and provider choice belongs to the implementer unless one of these forces it.

## Acceptance that cannot be gamed

- Tuning prompts, examples, or rules to the exact eval inputs, hardcoding their answers, or removing hard cases does not count as meeting the bar.
- When the set is large enough, hold out a few cases the implementer does not tune on and report their score separately.
- Report the score per run, the number of runs, and every failed case, not only the pass rate.
- A later prompt or model change is re-run against the same set before it merges. A drop below the bar is a regression.

## Example

Request: "foto nota supplier, isi otomatis total dan tanggalnya".

```text
Status: ready
Outcome: Pemilik bisa memotret nota supplier dan langsung mendapat total, tanggal, dan nama supplier terisi untuk dicek.
Behavior: Unggah foto -> model membaca field -> form terisi -> pemilik konfirmasi -> baru disimpan.
Acceptance:
- A1 Pada eval set 12 foto (8 jelas, 3 buram atau miring, 1 bukan nota), total dan tanggal cocok persis pada minimal 10 dari 11 nota, di setiap 3 kali run.
- A2 If sebuah field tidak terbaca, field dibiarkan kosong dan ditandai; tidak pernah ditebak.
- A3 When foto bukan nota, pemilik melihat bahwa tidak ada yang terbaca dan tidak ada data yang dibuat.
- A4 Tidak ada yang tersimpan sebelum pemilik konfirmasi.
- A5 If teks di foto berisi instruksi untuk model, instruksi itu diabaikan.
Intent: Menyetel prompt khusus untuk 12 foto itu tidak dihitung; 3 foto cadangan dilaporkan terpisah.
Unchanged: Input nota manual tetap bekerja seperti sekarang.
Constraints: Foto nota tidak boleh disimpan oleh provider model.
```

Why: the bar is measurable over a varied set, the "nothing to read" case is explicit, guessing is forbidden, and saving still waits for a human.
