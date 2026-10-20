# Student-only Locked Changed-Input Record | archived pre-run instructions

Current status: the student independently completed the exercise. The preserved evidence is in project1/evidence/student-only/ and the compiled record is in project1/docs/validation-and-ai-use.md and its PDF. The original pre-run instructions below describe the earlier workflow; do not rerun or overwrite the completed experiment. Statements about an unfilled PDF below refer to that earlier stage.

This is a mechanical worksheet, not your prediction. **Codex has not executed this exercise, selected a new value, or written your expected direction or decision effect.** Turn off AI assistance before choosing the new value, writing the prediction, and executing the assessed run. If your instructor assigns a different perturbation, follow that instruction instead.

## Exact requirement

PROJECT-SUBMISSION-ARCHITECTURE.md lines88-94 requires a human-authored prediction before AI assistance on that prediction and before execution; input and old/new units; expected direction and decision effect; timestamp and repository commit; an AI-closed run; preserved before/after outputs; actual decision effect and mismatch/unchanged-action diagnosis. The validation template has the same precommit and execution tables. A local ZIP alone is not asserted to replace the required repository commit.

## 1. Inspect the input and choose your own change

- Input: `receivables_ratio` in the statement assumptions, applied to FY2026-FY2030 revenue. It proxies accounts receivable **and other current assets**, not pure customer receivables.
- Original value: **0.09447165947855003**, or **9.447165947855% of annual revenue**.
- Original source: FY2025 balance-sheet receivables/other current assets67729 divided by revenue716924, as documented in Lab10. Historical files must not be edited.
- Open `project1/data/student-change.json`. Independently choose a material new ratio and replace **only** `null` with that decimal. No new value is supplied here.

## 2. Author your prediction before any changed execution

Create `project1/evidence/student-only/prediction.md` yourself. Include your actual date/time/timezone; original and selected new value; units and years; expected direction for receivables, operating WC, FCFF, cash/funding and core value; finance reasoning; expected committee decision effect; and why this is a material challenge. Do not run the changed model before saving this record. Do not ask AI to write or improve this prediction.

If needed, create the directory yourself first with `New-Item -ItemType Directory -Force project1/evidence/student-only`, then use your editor to write the record. An empty directory is not prediction evidence.

Use your actual clock (`Get-Date -Format o` in PowerShell) when recording the time. Do not use a date supplied by a draft or folder name. Keep your exact original prediction even if it is wrong.

## 3. Freeze the record and model

The assistant has no permission to commit. If you personally choose to make the required **local** commit after review, from the repository root run:

```powershell
git add project1 README.md
git commit -m "Freeze Project 1 model and student pre-run prediction"
git rev-parse HEAD
```

Review the staged files before committing. Runtime/cache directories are ignored; do not stage credentials. This is not a push or submission. Record the actual resulting commit ID in a separate receipt note; do not amend the frozen prediction to pretend it already knew its own commit hash. The exercise runner verifies that the model, input JSON and prediction match that commit. If you do not commit, obtain the instructor's accepted alternative; do not claim the required commit evidence exists.

## 4. Execute independently, AI closed

From `C:\Users\acpie\Documents\Codex\amazon-report-upload`:

```powershell
project1/.runtime/python.exe -B project1/student_exercise.py --run
```

The runner uses an in-memory override. It does not modify baseline assumptions or historical labs. It saves actual before/after statements, inputs, cash flows, value, funding status, actual execution time, source hashes and repository commit in `project1/evidence/student-only/changed-result.json`. It refuses to overwrite an existing assessed output. Do not delete a surprising result or rerun until you get the answer you wanted.

Examine each year's receivables, change in operating WC, FCFF and cash; enterprise value, equity bridge and core per-share subtotal; funding failures; and the committee action. Distinguish arithmetic value from an investable result when funding fails. Compare actual outcomes with your own recorded predictions.

## 5. Restore and verify

The baseline files were never changed. Still run the separate restoration check yourself, AI closed:

```powershell
project1/.runtime/python.exe -B project1/student_exercise.py --restore-check
```

The output `restore-result.json` must show `restored_exact_match: true` and unchanged source hashes. Leave the student-change record intact as evidence of what was tested. Confirm the baseline dashboard/outputs remain unaltered. Do not edit historical files to restore a result.

## 6. Write the reconciliation yourself

In a new `reconciliation.md`, record the actual direction and magnitude, actual decision effect, agreement/disagreement with your prediction, and a finance-grounded explanation. Explain an unchanged recommendation rather than assuming a changed input must reverse the action. Preserve the failed prediction if applicable. Identify any problem, correction, or limitation. Record your own AI-off declaration truthfully.

Then incorporate the complete frozen prediction, commit evidence, outputs and reconciliation into Validation-and-AI-Use.pdf. The current generated PDF intentionally still marks this evidence incomplete; merely following this worksheet does not automatically update that PDF or certify compliance.
