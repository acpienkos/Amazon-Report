# Amazon | FIN 43900 Project 1 Edition B

An AI-assisted, provisional committee application with integrated FY2026-2030 statements, signed FCFF, explicit funding failures, EV/equity multiples and visible outputs. The dated market comparison is **September 10, 2026**, not a live price. Read `outputs/valuation-report.md` before using a number.

## Run from the repository root

On standard Python 3.13, create an isolated environment and install the pinned direct dependencies:

```powershell
py -3.13 -m venv project1/.venv
project1/.venv/Scripts/python.exe -m pip install -r project1/requirements.txt
project1/.venv/Scripts/python.exe -B project1/analysis.py
project1/.venv/Scripts/python.exe -B project1/tests/test_project.py
project1/.venv/Scripts/python.exe -m streamlit run project1/app.py --server.address 127.0.0.1 --server.port 8501 --browser.gatherUsageStats false
```

The standard-venv creation command is provided for normal Python installations; this host uses the separately tested portable-runtime route below because its existing Python is embedded.

## Tested portable runtime route

The local `.runtime/python.exe` is isolated inside this workspace. It is ignored by Git and is not a submission artifact. With this runtime already provisioned:

```powershell
project1/.runtime/python.exe -B project1/analysis.py
project1/.runtime/python.exe -B project1/tests/test_project.py
project1/.runtime/python.exe -B project1/test_app.py
project1/.runtime/python.exe -m streamlit run project1/app.py --server.address 127.0.0.1 --server.port 8501 --browser.gatherUsageStats false
```

Open http://127.0.0.1:8501. The dashboard reads saved JSON; it does not fetch prices or alter assumptions. To provision Python and packages on another Windows machine with Python available, use `python project1/setup_runtime.py --destination .runtime`. It downloads the official Python 3.13.7 embedded archive and pip bootstrap, then installs the pinned requirements. Internet is needed for setup and optional source refresh; the model and tests run offline using bundled source snapshots. Full installed versions are in `requirements-lock.txt`.

## Reproduce documents

After analysis and tests, run `project1/.runtime/python.exe -B project1/build_documents.py`. This renders the reviewed Markdown into PDFs and matching local submission copies without regenerating authored prose or student evidence. The review_documents.py compatibility command uses the same renderer; neither command regenerates prose. Re-render and review PDFs after changes. The committee memo must stay at two pages or less. Run `project1/.runtime/python.exe -B project1/audit_package.py` last.

## Repository map

- `model.py`: read-only reuse of `../lab10/amazon_proforma.py`, signed FCFF, WACC, terminal, bridge, scenarios, reverse solver and comparables.
- `config.py`: dated inputs and explicit analyst scenario judgments.
- `analysis.py`: output generation; `data/` contains inherited history and generated assumption/source/normalization registers.
- `outputs/`: statements, FCFF reconciliation, scenarios, sensitivity, bridge, comparables and visible JSON/Markdown.
- `sources/`: public downloaded evidence; `evidence/source_downloads.json` records successful and failed retrievals.
- `tests/`: deterministic regression, identity, boundary and fault-injection tests. `exercise_audit.py` checks frozen evidence without executing the assessed runner.
- `docs/`: research evolution, memo, validation/AI record, video outlines and explicitly incomplete transcript templates.
- `docs/historical/`: byte-identical original Edition A, later completed copy and checkout disclosure.
- `submission/`: local PDF drafts and the official 12-row manifest; no upload or submission is implied.

## Final financial review

Read `docs/financial-review.md` before recording. The prior $40.74 headline is superseded. The corrected core subtotal is $39.05 and the base fails funding after known investment uses and July issuance are included. A sourced FTC-settlement normalization is separately attributed. Strategic carrying references are $57.06-$61.59 under explicit diagnostic haircut cases; these are not verified fair-value bounds. The reviewed committee action is **do not initiate at the dated comparison price**. There is no comprehensive verified point value or complete investable scenario range.

The independent Locked Changed-Input Record is complete as reported by the student. The original prediction and `data/student-change.json` are frozen in commit `99b99d0141f9a52510d71494943864c8cf4b6f71`; the five preserved files in `evidence/student-only/` contain prediction, receipt, changed output, restoration output and completed reconciliation. The input increased from 0.09447165947855003 to 0.15; core value declined from $39.0450 to $35.0730 and the action remains DO NOT INITIATE. Restoration matches exactly. Codex audited technical consistency after completion; automated checks do not certify AI-OFF conduct. See `docs/validation-and-ai-use.md` and its PDF for the compiled record. Do not rerun the assessed runner or edit its artifacts during recording.

The pre-run worksheet and empty template retain historical instructions; they are not current completion reports. The source model, input and original prediction remain frozen; later documentation and audit improvements remain local and uncommitted. Current post-run evidence is not yet in a final committed package; the public repository was verified October 20, 2026. Final local revisions await approval to commit and push.

## Finance conventions and limitations

USD millions, shares in millions, nominal annual rates. Operating leases remain operating; finance leases and facilities financing are debt-like. Asset additions include financed investment; capital AP supplies investment working-capital credit and is not separately deducted as debt. Negative FCFF is retained. Borrowing and securities liquidation are not FCFF. Required operating cash is separated from excess cash. The diluted share denominator is a disclosed point-in-time/award proxy.

Annual forecast seasonality is not available: 2026 remaining FCFF is prorated by 112/365, and June30 bridge balances proxy September10. Strategic investments and their related tax/commitment claims are unvalued. Normalized taxes and terminal capital ratios are judgments. Values are provisional and may materially understate equity value; a source-backed exact-date bridge remains unresolved. See `evidence/convention_decisions.md` and the full limitations in the visible report.

The original Edition A is not represented as AI-free or submitted. Dr. Z's October19 announcement is recorded as supplied by the student; separate early-AI recovery clarification is unresolved. The original is preserved, October19 additions remain later developments. No receipts, human predictions, precommits, conversations or recordings are invented.

## Student-only work before submission

1. Review the compiled Locked Changed-Input Record in the validation PDF against your preserved independent work; no new assessed run is needed.
2. Personally review sources, definitions, major judgments and the final decision. Obtain the full Brightspace brief/rubric and clarify any remaining early-AI recovery requirements.
3. Perform or obtain any required human README-only cold-run observation. The included technical cold run is AI-executed and labeled.
4. The student confirms all three videos and transcripts were submitted directly through Brightspace. No public URLs or submission timestamps were provided; receipts and instructor access were not independently inspected. Repository transcript templates remain historical preparation files.
5. Review final PDFs and the completed manifest, approve the final Git commit/push, then submit remaining PDF/repository/output/manifest deliverables personally and retain receipts. See `docs/final-submission-checklist.md`.

No credentials are required. No deployment is required by the inspected shared architecture. No trades, commits, pushes or submissions are performed by these commands.

## October 20 finalization status

See `docs/finalization-review.md` for the current delivery review. October 19 audit/checklist and recording scripts describe their historical inspection state; they are not evidence that the already-submitted Brightspace videos or transcripts must be repeated. No final commit or push has been performed.
