# Video 2 | Technical ownership, reproduction and highest-risk validation

Hard maximum 5:00. Target 4:45; roughly 470 spoken words plus command execution and transitions.

These are AI-assisted preparation scripts, not actual transcripts. Review every statement and use your own delivery. Record personally with clear audio and a small webcam view unless an approved accommodation provides an equivalent. The times below are rehearsal targets, not recorded timestamps. Keep the hard limit; rehearse navigation and shorten pauses. Do not rerun student_exercise.py or edit any student-only evidence.

## Before recording | prepare the actual submitted checkout

Use a terminal at C:\Users\acpie\Documents\Codex\amazon-report-upload. Open project1/README.md, analysis.py, model.py, statements.py, config.py, tests/test_project.py and outputs/valuation-report.md. Use the final submitted checkout when available; the current documentation cleanup is not yet committed.

Run this read-only baseline reproduction on camera; it does not regenerate output:

```powershell
project1/.runtime/python.exe -B -c "import sys,json;sys.path.insert(0,'project1');import model;from pathlib import Path;saved=json.loads(Path('project1/outputs/valuation.json').read_text());actual=model.evaluate();assert actual==saved['base'];print('Saved baseline reproduced exactly');print('Core value per share:',actual['valuation']['per_share']);print('Funding feasible:',actual['funding_feasible'])"
```

Run the deliberate failure-detection tests on camera:

```powershell
project1/.runtime/python.exe -B -m unittest discover -s project1/tests -p test_project.py -k deliberate -v
```

Then run the full suite (normally takes less than a second on this runtime):

```powershell
project1/.runtime/python.exe -B project1/tests/test_project.py
```

The full suite refreshes only ordinary validation logs; it does not modify student-only evidence. For a new machine follow README setup first. Optional full output reproduction, outside the timed segment: project1/.runtime/python.exe -B project1/analysis.py. This regenerates ordinary outputs, so review resulting timestamps and final documents afterward. Do not use the assessed runner for a presentation demonstration.

## 0:00-0:40 | architecture and environment

Screen: README setup, requirements.txt, then repository map and analysis.py.

Speaking script:

This application supports an equity analyst advising a committee with no current Amazon position. The README documents Python setup, pinned dependencies and commands. This computer uses the isolated portable runtime; a clean user can create the documented environment. Analysis writes saved output, and the dashboard reads that output without a live market feed. Config holds dated inputs and scenario judgments; model contains valuation and scenarios; statements adapts the historical statement engine. Historical labs remain unchanged.

## 0:40-1:30 | financial logic and data flow

Screen: model.py forecast/value functions; statements.py cash articulation; FCFF reconciliation.

Speaking script:

Reported 2025 balances feed integrated 2026 through 2030 statements. Cash follows operating, investing and financing flows rather than plugging the balance sheet. Signed FCFF uses operating profit, qualified unlevered taxes, depreciation, investment and changes in operating working capital. Borrowing is financing; strategic asset purchases are investing cash uses. Neither is operating FCFF. Finance-lease asset additions count as investment and principal is financing. Operating leases remain rental economics, so their liability is not deducted again. Capital payables supply investment working-capital credit. WACC discounts signed cash flows, and the bridge moves enterprise value to equity and diluted per-share value.

## 1:30-2:15 | reproduce a saved result live

Screen: execute the read-only baseline command, then open valuation-report.md.

Speaking script:

I will reproduce the saved baseline directly from the current model and compare the complete result with the bundled JSON. The equality assertion checks all saved baseline fields, not just the rounded headline. The command reports an exact match, a core subtotal of approximately thirty-nine dollars and five cents, and funding feasible false. This is the September 10 comparison, not today's market price. The report makes these inputs, limitations and committee action visible without running code.

## 2:15-3:20 | highest-risk failure test

Screen: test_38_deliberate_high_risk_failure and test_39_deliberate_cash_failure; execute the two-test command.

Speaking script:

The highest-risk technical claim is that integrated investment and cash schedules articulate consistently. Test 38 deliberately removes financed asset additions from an in-memory copy. Diagnose must reject the accounting result, and valuation must raise an error. Test 39 corrupts cash continuity and must also be rejected. These tests passing means the detector caught the injected failures; it does not mean the corrupted forecast is acceptable. No source assumption or frozen evidence is edited. I can trace the discrepancy through investment, assets and cash rather than relying on the final price alone.

## 3:20-4:10 | full suite and economic completeness

Screen: run all model tests; highlight tests 50-59 and the known-transaction corrections.

Speaking script:

The complete suite has 59 tests, covering known answers, statement identities, FCFF routes, funding, scenarios and valuation boundaries. Targeted checks include investment cash uses, July borrowing, terminal depreciation and strategic-asset double counting. Earlier arithmetic tests passed despite economic omissions, so filing definitions and source evidence remain necessary. The independent changed-input record is separate student work. Its original prediction and results are preserved; this live demonstration is an ordinary technical check and does not replace that assessment.

## 4:10-4:45 | limitations and disclosure

Screen: validation PDF and financial-review.md limitations.

Speaking script:

The model uses a uniform remaining-year cash-flow stub, dated balance and dilution proxies, a twenty-two-percent tax proxy and an unproven terminal investment transition. Segment profitability and strategic-asset economic value are incomplete. The base fails funding, so its value is diagnostic. Codex assisted implementation and review; I must explain and verify consequential claims. Automated tests do not establish source truth or certify AI-off conduct.

## Personally complete

Run the commands yourself, understand the injected failure, and rehearse terminal and file navigation under 5:00. Record the actual walkthrough with webcam, correct project1/docs/transcript-video-2.txt from that recording, and supply its real URL, title, duration, evidence timestamps and access check. Refresh final validation logs and audit after any later changes.
