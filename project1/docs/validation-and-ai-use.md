# Validation and AI Use | reviewed package

## Decision, version, and as-of boundary

Do not initiate at September10 2026 reference price. Edition B frozen for the experiment at commit 99b99d0141f9a52510d71494943864c8cf4b6f71; subsequent documentation cleanup remains local and uncommitted; saved output metadata timestamp 2026-10-20T03:14:27.961562+00:00 (existing saved output; no new valuation execution during this finalization). Source availability is distinguished from later retrieval and retrospective judgments. The student confirms direct Brightspace submission of all three videos and transcripts; no receipt was independently inspected. No remaining-deliverable upload is claimed.

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

## Locked Changed-Input Record | completed student work

The student reports independently completing the prediction, input selection, execution, restoration check, and reconciliation with AI assistance off. Codex subsequently audited preserved artifacts and prepared this documentation. Automated tests, source hashes, timestamps, and Git history support technical consistency; they do not certify tool use or AI-OFF conduct.

Frozen repository commit: 99b99d0141f9a52510d71494943864c8cf4b6f71. Commit timestamp: 2026-10-19T16:20:47-04:00. The original prediction records October 19, 2026, 4:13 PM (GMT-04:00), before the commit and execution. The commit contains both project1/evidence/student-only/prediction.md and project1/data/student-change.json. Subsequent reconciliation is retained as post-run student evidence, not represented as part of that pre-run commit.

Material input: receivables_ratio, 0.09447165947855003 to 0.15, fraction of annual revenue applied FY2026-FY2030. The model aggregates receivables and other current assets; the frozen prediction's customer-receivables wording is preserved rather than corrected retroactively. The completed reconciliation identifies the broader asset definition.

Student execution commands (historical record; do not rerun or overwrite): project1/.runtime/python.exe -B project1/student_exercise.py --run and project1/.runtime/python.exe -B project1/student_exercise.py --restore-check. The runtime is the repository-local Python 3.13.7 embedded environment documented in README and requirements-lock.txt. The JSON records execution timestamps, commit, input, outputs, and source hashes; it does not independently attest the exact invoked executable.

Changed execution: 2026-10-19T20:39:58.537701+00:00. Restore check: 2026-10-19T20:40:16.206255+00:00. Both identify the frozen commit. restored_exact_match is true. The runner uses an in-memory override, leaving baseline assumption files intact; restoration verifies baseline reproducibility, not an on-disk edit reversal. All nine recorded source hashes match current bytes and both runs, and their contents match the frozen commit (normalizing Git line endings).

Expected directions: increased receivables/current assets and working-capital needs; lower FCFF, cash and valuation; greater funding pressure; likely unchanged recommendation. Actual committee action remains DO NOT INITIATE. The student explains that worsened liquidity and lower diagnostic valuation reinforce the original action. Both base and changed paths fail funding; positive base cash is not evidence of adequate funding.

Annual before/after record below is in USD millions. Complete statement, valuation and funding outputs remain in evidence/student-only/changed-result.json and restore-result.json.

| Year | Assets before / after | Change operating WC before / after | FCFF before / after | Cash before / after |
|---|---|---|---|---|
| 2026 | 78,565.64 / 124,744.78 | -9,807.43 / 36,371.71 | -82,622.75 / -128,801.89 | 31,778.41 / 25,000.00 |
| 2027 | 89,564.83 / 142,209.04 | -9,274.65 / -2,809.57 | -62,343.70 / -68,808.78 | 25,000.00 / -12,228.95 |
| 2028 | 100,312.61 / 159,274.13 | -8,667.02 / -2,349.71 | -22,043.82 / -28,361.13 | 13,815.67 / -47,839.60 |
| 2029 | 110,343.87 / 175,201.54 | -8,566.85 / -2,670.70 | 14,023.05 / 8,126.90 | 21,028.20 / -47,965.95 |
| 2030 | 119,171.38 / 189,217.67 | -7,279.22 / -2,090.61 | 46,585.21 / 41,396.60 | 45,819.10 / -14,978.14 |

Core EV: $505.782bn to $462.406bn; core equity: $426.384bn to $383.008bn; per-share subtotal: $39.0450 to $35.0730. The baseline breaches its cash floor in 2028-2029; changed-case cash is negative in 2027-2030. Values remain diagnostic because funding fails and strategic investments are excluded from the core subtotal.

The original files below are reproduced verbatim as supplied student evidence. This compilation does not rewrite their contents or assert independent verification of authorship. Full machine-readable outputs remain repository evidence; the tables above preserve material before/after results in this PDF.

<!-- PAGEBREAK -->

### Frozen student prediction | verbatim

1. What is the current date and time?
 October 19, 2026, 4:13 PM (GMT-04:00).

2. What assumption did you change, and what are its original and new values?
 I changed the Accounts Receivable-to-Revenue ratio from 9.45% to 15%. This ratio is measured as a fraction of annual revenue and is applied to FY2026-FY2030.

3. Why did you choose that change?
 I increased the receivables ratio from 9.45% to 15% to test the effect of slower customer collections and higher amounts of revenue tied up in accounts receivable. This scenario assumes Amazon requires more time to convert sales into cash, resulting in greater working capital investment over FY2026-FY2030.

4. What do you expect to happen to receivables and working capital?
 I expect both accounts receivable and working capital to increase. Since receivables are modeled as a higher percentage of annual revenue, more cash becomes tied up in unpaid customer balances, increasing Amazon's working capital requirements.

5. What do you expect to happen to free cash flow, cash balances, and funding needs?
 I expect free cash flow to decrease because more cash is invested in working capital. Lower free cash flow would reduce projected cash balances, and Amazon may require greater external funding or use more of its existing cash resources to support operations and growth.

6. What do you expect to happen to Amazon's valuation?
 I expect Amazon's valuation to decrease. Higher receivables and working capital requirements reduce free cash flow, and lower future free cash flows result in a lower discounted cash flow (DCF) valuation.

7. Do you expect the investment recommendation to change? Why?
 I would not expect the investment recommendation to change significantly unless the decrease in valuation is large enough to materially reduce the stock's expected return. Although the higher receivables ratio negatively affects cash flow and valuation, Amazon's long-term outlook is still driven primarily by revenue growth, profitability, and operating performance. Therefore, the recommendation would likely remain unchanged unless the valuation decline substantially impacts the investment thesis.

### Student commit receipt | verbatim

# Student AI-OFF Commit Receipt

Date: October 19, 2026
Commit time: 2026-10-19T16:20:47-04:00

Git commit hash:
99b99d0141f9a52510d71494943864c8cf4b6f71

Commit message:
Freeze Project 1 model and student pre-run prediction

Changed input:
project1/data/student-change.json

Pre-run prediction:
project1/evidence/student-only/prediction.md

<!-- PAGEBREAK -->

### Completed student reconciliation | verbatim

# Reconciliation

I changed the receivables ratio from 0.09447 to 0.15. This assumption is measured as a fraction of annual revenue and applies to FY2026-FY2030.

As expected, receivables and other current assets increased substantially across all forecast years. FY2026 receivables increased from approximately $78.6 billion to $124.7 billion, and FY2030 receivables increased from approximately $119.2 billion to $189.2 billion. This reflects a larger portion of revenue being tied up in receivables and related current assets.

The higher receivables ratio increased working capital requirements. Operating cash flow decreased because more cash was tied up in working capital rather than being available for operations.

The reduction in operating cash flow negatively affected free cash flow. FCFF in FY2026 declined from approximately -$82.6 billion to -$128.8 billion. Future free cash flows were also generally lower throughout the forecast period.

Cash balances deteriorated significantly after the change. In the base case, projected cash remained positive, ending at approximately $45.8 billion in FY2030. After the change, projected cash became negative beginning in FY2027 and remained negative through FY2030. Funding stress also increased. The baseline model already showed funding-floor shortfalls in FY2028 and FY2029, but the modified case produced larger and more persistent shortfalls in FY2027 through FY2030.

The valuation was negatively affected. Enterprise value decreased from approximately $505.8 billion to $462.4 billion, while equity value decreased from approximately $426.4 billion to $383.0 billion. Estimated value per share declined from approximately $39.05 to $35.07.

Despite these negative effects, the investment committee recommendation did not change. The original recommendation was DO NOT INITIATE, and it remains DO NOT INITIATE after the assumption change. The higher receivables ratio reduced free cash flow, worsened liquidity, increased funding pressure, and lowered valuation, which reinforces rather than reverses the original conclusion.

I verified the restoration step using restore-result.json. The field "restored_exact_match" was set to true, confirming that the model returned exactly to its original state after the assumption was restored.

<!-- PAGEBREAK -->

### Recorded source hashes | SHA256

project1/model.py
85b7be73d829688328a352fdd9bcd01f3ea822d3f5d2018d4fd1c452489c6a2b

project1/statements.py
38a4f64fbb3609788e42f4569d87efff69512ed9ff45da06a81a7a88746a3097

project1/config.py
6e63287fb0897fb5d6ea7727e6f6751945611bbe80a26a28b7b96549e19dcabc

project1/student_exercise.py
d0bee2a35eee3009cbc82ffb324d68848ff983b31f8ed15fe2dab6de81385bf3

project1/data/legacy_assumptions.csv
cbe5b8b189db6aba1f78797429c2934af731e310f525af84aed108cdb753673b

lab10/amazon_proforma.py
f0c0058578dce0c7c787e71cb1339d1705fb72a3722c625ffe0629502209650a

lab10/amazon_assumptions.csv
cbe5b8b189db6aba1f78797429c2934af731e310f525af84aed108cdb753673b

project1/data/student-change.json
9138aa6c027798bd0255bfed6c3056f54fd58af43c119686ae9e639999f92d63

project1/evidence/student-only/prediction.md
d04b1dfe969a6364a95c03ba7ff2244ea397d1fefb2dc24c08d0b849ba8ed617

<!-- PAGEBREAK -->

## Named AI-use and disposition register

| Tool/surface | Date | Material contribution | Check/disposition | Decision effect |
|---|---|---|---|---|
| Codex; underlying model/version not exposed in runtime evidence | October19 2026 | Initial implementation, research, tests, dashboard and drafts | Qualified; prior core subtotal was incomplete | Old headline withdrawn |
| Codex separate final review | October19 2026 | Filing-table/economic audit; known-transaction and terminal corrections; documents | Source-row checks, dual FCFF routes, targeted regressions; student review pending | Do not initiate; no verified full-company point value |
| Codex documentation cleanup | October 19, 2026 | Audited completed student artifacts; compiled this record; revised audit, scripts and packaging | Preserved student files and frozen model; technical tests do not prove AI-OFF conduct | No change to the model or recommendation |
| Codex submission preparation | October 20, 2026 | Reconciled manifest and delivery status using student confirmation; checked saved documents and output without rerunning the exercise | Brightspace submission is student-reported; public GitHub checked separately; final commit/push requires approval | No financial change |
| Historical Codex disclosure | September1 draft metadata / lab records | Filing organization, original drafting and lab assistance | Preserve actual disclosures; no AI-free attestation | Accurate provenance |

| Material AI claim | Disposition | Evidence |
|---|---|---|
| $40.74 is an adequate company-value headline | Reject | Omitted strategic assets and funding cash flows |
| Funding passes under base | Correct | Include both investment61067m and July notes25000m; base fails2028-2029 |
| Terminal proportional D&A preserves original policy | Correct | Apply15% to opening net PPE and opening ROU/liability rent |
|22% of strategic gross assets is an actual tax liability | Reject | It is only a transparent haircut sensitivity; no tax basis appraisal |
| Original Edition A is AI-free/submitted | Reject | Historical checkout and absent receipt; later addition separately dated |

## Limits, monitoring and student evidence

Unlevered taxes are a provision-as-cash proxy; strategic tax/liquidity appraisal, actual/forecast stub and exact-date share bridge remain unresolved. Segment margins are not independently forecast. Full Brightspace assignment and analytic rubric were not accessible. The independent assessed record is complete as student-reported and technically verified. Personal source review remains pending. The student confirmed on October 20, 2026 that all three videos and transcripts were submitted directly through Brightspace. No video URLs or submission timestamps were supplied; receipts and instructor access were not independently inspected. Repository transcript templates are historical preparation files. User-supplied October19 announcement is retained without inventing original posting access or recovery waiver.
