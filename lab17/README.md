# FIN 43900 — Lab 17: Point-in-Time Audit

**Selected FRED series: BAA — Moody's Seasoned Baa Corporate Bond Yield.** Selection confirmed October 29, 2026 for Lab 17 and the current Project 2 data-card evaluation; no earlier prework selection is claimed.

Andrew Pienkos · Fall 2026 · Professor Cinder Zhang

[Official assignment](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-10/lab-17-point-in-time.md); frozen Week 10 assignment, prework, README and handout are in `sources/`.

The app selects BAA, FEDFUNDS, DGS10 and MORTGAGE30US by default and shows names and native frequencies. Additional IDs accept comma or space separation, including PAYEMS. The chart start defaults to January 1, 2020; “As known on” defaults to today, as required by the official assignment. Set it to October 5, 2026 for the known answers or January 15, 2025 for PAYEMS. A refresh button clears both one-hour download caches.

Each series has a current-data line chart, the historical last measured date/value, actual download dates and source URLs. The comparison table links each ID to FRED and gives historical/current dates and values, later-observation counts and revision counts. Counts use the full history, independent of the chart start date. Dates added within earlier gaps are separately identified, rather than mislabeled revisions.

Current and historical data use separate cached functions, `download_current` and `download_vintage`. The parser requires the requested ID and, for historical data, ALFRED's exact vintage-suffixed column. It converts “.” to missing, validates dates and numbers, rejects duplicate dates and nonfinite values, sorts chronologically, and rejects historical rows after the cutoff. Only matching nonmissing dates enter revision comparisons. No frequency resampling or calendar-day guessing is used. Empty or malformed responses, invalid IDs, HTTP failures, timeouts, and redirects that change the endpoint/series/cutoff become per-series errors. Historical failure never triggers a current-data substitute. Other series continue to render.

Under the title, the app links FRED and ALFRED and discloses AI assistance, its learning purpose and that it is not investment advice. No API key is used. The current endpoint is `https://fred.stlouisfed.org/graph/fredgraph.csv?id=SERIES`; the historical endpoint is `https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=SERIES&vintage_date=YYYY-MM-DD`.

## Setup and run (Windows, from repository root)

```powershell
python -m pip install -r lab17/requirements.txt
python -m streamlit run lab17/asof_app.py
python -B -m unittest discover -s lab17 -p test_asof_app.py -v
python -B lab17/verify_live.py
```

This machine uses `project1/.runtime/python.exe` in place of `python` because Python is not on PATH. Existing dependencies were available; no installation was needed. For the app harness, first start the server on port 8517 with `--server.headless true --server.port 8517 --browser.gatherUsageStats false`, then run `python -B lab17/verify_app.py`. The normal run command uses the default browser/port. The network must allow HTTPS to FRED and ALFRED. A cached download may be up to one hour old; refresh explicitly when verifying.

## Known answers

Historical cutoff: **2026-10-05**. Downloaded **2026-10-29**. Monthly dates label the measured month; all yields/rates below are percent.

| Series | Actual latest observation | Actual | Expected | Result | Official vintage |
|---|---|---:|---:|---|---|
| BAA | 2026-09-01 | 6.47 | 6.47 | PASS | [CSV](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=BAA&vintage_date=2026-10-05) |
| FEDFUNDS | 2026-09-01 | 3.75 | 3.75 | PASS | [CSV](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=FEDFUNDS&vintage_date=2026-10-05) |
| DGS10 | 2026-10-02 | 5.28 | 5.28 | PASS | [CSV](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DGS10&vintage_date=2026-10-05) |
| MORTGAGE30US | 2026-10-01 | 7.28 | 7.28 | PASS | [CSV](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=MORTGAGE30US&vintage_date=2026-10-05) |

All four actual dates and values match. No discrepancies were found. Current downloads end at September 2026 for BAA (6.47) and FEDFUNDS (3.75), October 28 for DGS10 (5.05), and October 29 for MORTGAGE30US (7.24). New valid observations after each historical last date: 0, 0, 17 and 4 respectively; overlapping revised observations: 0 for each. Missing holiday/weekend cells are excluded from counts. Evidence: `evidence/live_results.json` and the corresponding raw CSV downloads. Expected answers occur only in the verification script and documentation.

## PAYEMS

At the **2025-01-15** cutoff, the latest available PAYEMS observation is **2024-12-01**, representing December 2024, at **159,536 thousand jobs**. The current download reports **158,316 thousand jobs for that same month**. The difference, current minus historical, is **158,316 − 159,536 = −1,220 thousand jobs** (1.220 million fewer).

There are **381 revised observations among 1,032 matching nonmissing dates**, comparing full histories with `rtol=1e-9, atol=1e-8`. There are **21 newly available later observations**, which are excluded from the revision count. Today's latest PAYEMS observation is September 2026 at 159,044; that is a different month and is not the revision comparison. **The professor's probe passes.**

Sources: [historical ALFRED CSV](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=PAYEMS&vintage_date=2025-01-15), [current FRED CSV](https://fred.stlouisfed.org/graph/fredgraph.csv?id=PAYEMS), [official PAYEMS page](https://fred.stlouisfed.org/series/PAYEMS). Raw downloads and JSON calculations are retained under `evidence/`.

Using today's lower December value in a January 15, 2025 decision would supply a later revision that was unavailable then. A backtest must request the vintage for each historical decision date; delaying today's finalized file by a fixed number of days does not remove revision leakage.

## Data card and call

See [DATA_CARD.md](DATA_CARD.md) and [ANSWERS.md](ANSWERS.md) for all written answers, timing limits, the completed October 29 partner discussion with John (surname unconfirmed), actual challenge/response, code question, role swaps and reflection.

**Decision: Quarantine BAA for Project 2 model use pending sufficient publication-timing and trading-time verification.** BAA is economically relevant to borrowing costs and credit conditions. The audit detects no revisions in 1,292 matching dates, but the September value was not available on September 30 and date-level CSVs do not establish intraday source release times. The Week 10 handout says to quarantine when a publication date cannot be found; the limited availability bracket is insufficient for a complete trading-time policy across the backtest.

**Exact proposed as-of rule:** for a trade on date D, use the ALFRED vintage dated D−1 calendar day and select the latest nonmissing observation in that vintage, retaining its measured date and provenance. D−1 is a conservative whole-day buffer for daily trading; it is not a fixed lag applied to today's values. Never backfill from current FRED. A failed download, unavailable vintage, missing usable observation or unverified availability keeps that decision's signal quarantined. This rule would still require an explicit trading calendar and time-zone policy before admission. Archive the downloaded vintage and retrieval timestamp for each decision.

**What would change my call:** independently check the three values, document release/archival timing across the actual test period and trading time, and verify the rule on each decision date. If those checks pass, admit BAA as a contextual input under the vintage rule. Reject it if reliable historical availability cannot be established or it does not serve the eventual model. No predictive stock-return claim is needed for this decision.

## Testing

**17 deterministic unit tests passed**: parsing/sorting, missing cells, empty/all-missing input, ID validation, inclusive cutoff, latest observation, revisions versus new observations, daily/weekly/monthly frequencies, floating-point tolerance, earlier missing-value fills, HTTP failures/timeouts, historical URL construction, unavailable vintages, redirect/current-substitution rejection, malformed inputs and future-row leakage. Mocked tests are separate from live evidence.

Live checks reproduce all four known answers and PAYEMS, with no errors in `evidence/live_results.json`. The independent FRED table matches all three BAA values. The live Streamlit AppTest results and server health are saved separately in `evidence/app_results.json`; startup output and execution results are in `validation.txt`. Browser inventory was empty, so no visual/browser verification is claimed. Streamlit's test harness exercises actual app widgets and rendering logic.

## Remaining personal requirements

- Series selection completed: BAA is confirmed for Lab 17 and the current Project 2 data-card evaluation. Its model admission remains quarantined pending timing verification.
- Personally read July 6.19, August 6.32 and September 6.47 on FRED, recording the check date. Codex's separate-table checks do not satisfy the hand-verification requirement.
- Partner opening rate explanation and role swaps: completed October 29, 2026, per Andrew's notes. No separate partner-written opening reason is claimed; confirm that record if independently required.
- Partner code explanation, exchanged questions and role swaps: completed per Andrew's notes; the actual code question and answer are recorded in DATA_CARD.md and ANSWERS.md.
- Partner challenge and evidence-based two-sentence response: completed and recorded. Partner is John; surname remains for confirmation. Discussion date: October 29, 2026 (session context).
- Publication-timing challenge discussion: completed as documented. Review the reflection in your own words; complete any separately required explanation of why cleaning is not a data card and any personal reflection not covered by the supplied notes.
- GitHub links: **student-reported submitted to Brightspace**, reported October 29, 2026. Individual Lab 17 quiz/checkout completion is **unconfirmed**; check its submitted/completed status yourself. The links may be part of that quiz workflow, but submitting links alone does not establish quiz completion. Codex did not access Brightspace.
- Complete or confirm the assigned ALFRED reading and publication/trading-time policy before admitting BAA to a model. Confirm any private deadline and instructions.

[Brightspace text](BRIGHTSPACE_SUBMISSION.md). AI disclosure: Codex implemented, researched, tested and drafted this package; student review, personal FRED checks and individual checkout remain necessary; partner activities are recorded from Andrew's supplied notes.
