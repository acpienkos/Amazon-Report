# Validation and AI Use | reviewed package

## Decision, version, and as-of boundary

Do not initiate at September10 2026 reference price. Local uncommitted Edition B; actual output timestamp 2026-10-19T19:48:15.443842+00:00. Source availability is distinguished from later retrieval and retrospective judgments. No upload or receipt is claimed.

## Data and convention ledger

data/assumptions.csv and data/source_register.csv retain source/units/classification records. New review facts and exact locators are in docs/financial-review.md, evidence/financial_review.json and data/financial-review-inputs.csv. The adapted statements.py leaves lab10 unchanged. The model is not an exact seasonal or September10 balance roll-forward; strategic cases are carrying references, not a net economic appraisal.

## Actual validation register

59 model tests executed: 59 passed, 0 failed, 0 errors, 0 skipped. Seven dashboard pages execute. Technical cold-run status PASS; see evidence/cold_run.md. Historical64-file hashes pass. Latest logs are evidence/validation_results.txt and validation_summary.json. No test is credited merely because code exists.

| Claim/failure | Test and actual result | Disposition/evidence |
|---|---|---|
| Legacy calculations | Original Lab10 outputs reproduce | Historical files unchanged |
| Arithmetic and definitions | Signed-flow, statement, WC/PPE/lease, WACC, bridge, shares, peer, scenario and solver tests pass | Automated evidence; not source truth |
| Review omission: cash investments | Known61067m enters other assets/CFI; does not enter FCFF | Funding pass withdrawn; tests50/52/57 |
| Review omission: July notes |25000m added to funding, bridge and debt weight | Test51 and known-cash bridge test58 |
| Terminal policy mismatch | Opening-asset D&A/rental schedules recomputed | Tests53/54; source-backed policies retained |
| Strategic-asset double count | Payment deducted once; gross assets added separately | Tests55/56/58; tax case explicitly hypothetical |
| Source correctness | Twelve annual statement rows matched in relevant table columns, EBIT identity reconciled | financial_review.json; AI-executed separate review |

Earlier actual development failures are retained in validation_first_run_failed.txt and environment_failures.md. The first49-test build passed despite financial omissions: that is why the source/economic review matters. No artificial failed tests or human checks are added for appearance.

## Locked Changed-Input Record | awaiting independent student work

Exact course requirement: human-authored prediction before AI assistance on it and before execution; timestamp/repository commit; exact old/new units; expected direction and decision effect; AI-closed run; actual before/after results and diagnosis. docs/student-ai-off-worksheet.md supplies mechanical instructions and an unexecuted runner. No new input value, prediction, precommit or assessed output has been filled in. Ordinary automated scenarios do not satisfy this record. The PDF must be updated with actual student evidence before claiming completion.

## Named AI-use and disposition register

| Tool/surface | Date | Material contribution | Check/disposition | Decision effect |
|---|---|---|---|---|
| Codex; underlying model/version not exposed in runtime evidence | October19 2026 | Initial implementation, research, tests, dashboard and drafts | Qualified; prior core subtotal was incomplete | Old headline withdrawn |
| Codex separate final review | October19 2026 | Filing-table/economic audit; known-transaction and terminal corrections; documents | Source-row checks, dual FCFF routes, targeted regressions; student review pending | Do not initiate; no verified full-company point value |
| Historical Codex disclosure | September1 draft metadata / lab records | Filing organization, original drafting and lab assistance | Preserve actual disclosures; no AI-free attestation | Accurate provenance |

| Material AI claim | Disposition | Evidence |
|---|---|---|
| $40.74 is an adequate company-value headline | Reject | Omitted strategic assets and funding cash flows |
| Funding passes under base | Correct | Include both investment61067m and July notes25000m; base fails2028-2029 |
| Terminal proportional D&A preserves original policy | Correct | Apply15% to opening net PPE and opening ROU/liability rent |
|22% of strategic gross assets is an actual tax liability | Reject | It is only a transparent haircut sensitivity; no tax basis appraisal |
| Original Edition A is AI-free/submitted | Reject | Historical checkout and absent receipt; later addition separately dated |

## Limits, monitoring and student evidence

Unlevered taxes are a provision-as-cash proxy; strategic tax/liquidity appraisal, actual/forecast stub and exact-date share bridge remain unresolved. Segment margins are not independently forecast. Full Brightspace assignment and analytic rubric were not accessible. Human source checks, assessed AI-off evidence, actual videos/transcripts and access checks remain pending. User-supplied October19 announcement is retained without inventing original posting access or recovery waiver.
