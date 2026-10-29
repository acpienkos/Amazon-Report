# FIN 43900 — Lab 17: Point-in-Time Audit

Andrew Pienkos · Fall 2026 · Professor Cinder Zhang

## Part 1 — Four known-answer checks

Historical cutoff: **2026-10-05**. Downloaded **2026-10-29**. Monthly dates label the measured month; all yields/rates below are percent.

| Series | Actual latest observation | Actual | Expected | Result | Official vintage |
|---|---|---:|---:|---|---|
| BAA | 2026-09-01 | 6.47 | 6.47 | PASS | [CSV](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=BAA&vintage_date=2026-10-05) |
| FEDFUNDS | 2026-09-01 | 3.75 | 3.75 | PASS | [CSV](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=FEDFUNDS&vintage_date=2026-10-05) |
| DGS10 | 2026-10-02 | 5.28 | 5.28 | PASS | [CSV](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DGS10&vintage_date=2026-10-05) |
| MORTGAGE30US | 2026-10-01 | 7.28 | 7.28 | PASS | [CSV](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=MORTGAGE30US&vintage_date=2026-10-05) |

All four actual dates and values match. No discrepancies were found. Current downloads end at September 2026 for BAA (6.47) and FEDFUNDS (3.75), October 28 for DGS10 (5.05), and October 29 for MORTGAGE30US (7.24). New valid observations after each historical last date: 0, 0, 17 and 4 respectively; overlapping revised observations: 0 for each. Missing holiday/weekend cells are excluded from counts. Evidence: `evidence/live_results.json` and the corresponding raw CSV downloads. Expected answers occur only in the verification script and documentation.

## Part 2 — PAYEMS revision probe

At the **2025-01-15** cutoff, the latest available PAYEMS observation is **2024-12-01**, representing December 2024, at **159,536 thousand jobs**. The current download reports **158,316 thousand jobs for that same month**. The difference, current minus historical, is **158,316 − 159,536 = −1,220 thousand jobs** (1.220 million fewer).

There are **381 revised observations among 1,032 matching nonmissing dates**, comparing full histories with `rtol=1e-9, atol=1e-8`. There are **21 newly available later observations**, which are excluded from the revision count. Today's latest PAYEMS observation is September 2026 at 159,044; that is a different month and is not the revision comparison. **The professor's probe passes.**

Sources: [historical ALFRED CSV](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=PAYEMS&vintage_date=2025-01-15), [current FRED CSV](https://fred.stlouisfed.org/graph/fredgraph.csv?id=PAYEMS), [official PAYEMS page](https://fred.stlouisfed.org/series/PAYEMS). Raw downloads and JSON calculations are retained under `evidence/`.

Using today's lower December value in a January 15, 2025 decision would supply a later revision that was unavailable then. A backtest must request the vintage for each historical decision date; delaying today's finalized file by a fixed number of days does not remove revision leakage.

## Part 3 — Streamlit application

The app selects BAA, FEDFUNDS, DGS10 and MORTGAGE30US by default and shows names and native frequencies. Additional IDs accept comma or space separation, including PAYEMS. The chart start defaults to January 1, 2020; “As known on” defaults to today, as required by the official assignment. Set it to October 5, 2026 for the known answers or January 15, 2025 for PAYEMS. A refresh button clears both one-hour download caches.

Each series has a current-data line chart, the historical last measured date/value, actual download dates and source URLs. The comparison table links each ID to FRED and gives historical/current dates and values, later-observation counts and revision counts. Counts use the full history, independent of the chart start date. Dates added within earlier gaps are separately identified, rather than mislabeled revisions.

Current and historical data use separate cached functions, `download_current` and `download_vintage`. The parser requires the requested ID and, for historical data, ALFRED's exact vintage-suffixed column. It converts “.” to missing, validates dates and numbers, rejects duplicate dates and nonfinite values, sorts chronologically, and rejects historical rows after the cutoff. Only matching nonmissing dates enter revision comparisons. No frequency resampling or calendar-day guessing is used. Empty or malformed responses, invalid IDs, HTTP failures, timeouts, and redirects that change the endpoint/series/cutoff become per-series errors. Historical failure never triggers a current-data substitute. Other series continue to render.

Under the title, the app links FRED and ALFRED and discloses AI assistance, its learning purpose and that it is not investment advice. No API key is used. The current endpoint is `https://fred.stlouisfed.org/graph/fredgraph.csv?id=SERIES`; the historical endpoint is `https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=SERIES&vintage_date=YYYY-MM-DD`.

## Part 4 — Data card answers

## Series identification and selection

**Selected FRED series: BAA — Moody's Seasoned Baa Corporate Bond Yield.** Andrew confirmed this selection for Lab 17 and the current Project 2 data-card evaluation on October 29, 2026. This records the current choice; it does not claim an earlier prework selection. Series selection is confirmed, while admission to the Project 2 model remains subject to the timing checks below. There is no local Lab 15 folder; Lab 16's deterministic testing and explicit pending-activity documentation were reviewed. Existing Lab 13 untracked work was preserved.

[Official FRED page](https://fred.stlouisfed.org/series/BAA). Source organization: **Moody's**; distributor/archive: Federal Reserve Bank of St. Louis, FRED/ALFRED. Units: **percent, not seasonally adjusted**. Frequency: **monthly**. It measures yields on seasoned Baa corporate bonds; the source notes instruments with maturities of 20 years and above. Release listed by FRED: Moody's Daily Corporate Bond Yield Averages (Not a Press Release); the release name does not make this monthly series daily. Download date: **October 29, 2026**.

## Publication timing and historical availability

The monthly observation date, such as September 1, labels the month measured; it does not mean the complete monthly value was available on September 1. As of **September 30, 2026**, the latest BAA observation was **August 2026, 6.32%**. The current file's latest observation is **September 2026, 6.47%**. One observation is newly available after the historical endpoint.

The September observation is absent on the September 30 vintage and present on the October 1 vintage at 6.47; it also appears on October 2 and October 5. These adjacent date-level snapshots bracket its ALFRED availability to **October 1**, one calendar day after September month-end. This is evidence for that month's archive availability, not a universal release lag or an exact first-publication clock time at Moody's. The graph CSV has no per-row publication timestamps. We cannot establish source-first publication time, intraday availability, or a complete release schedule from these snapshots alone. September's value must not enter a September 30 trade.

Sources: [September 30 vintage](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=BAA&vintage_date=2026-09-30), [October 1 vintage](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=BAA&vintage_date=2026-10-01), [October 2 vintage](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=BAA&vintage_date=2026-10-02), [current CSV](https://fred.stlouisfed.org/graph/fredgraph.csv?id=BAA).

## Revisions and missing observations

Comparing September 30's vintage with the October 29 download gives **0 changed observations out of 1,292 overlapping nonmissing dates**, **1 newly available later month**, and **0 missing cells in either downloaded BAA history**. No observed revision is material because none was detected. This comparison does not prove that BAA has never been corrected or will never be revised. A future vintage must still be checked; the app uses matching observation dates and numeric tolerances rather than assuming immutability.

## Three-value verification

The following is **Codex-assisted verification**, independently comparing the graph CSV with FRED's separate official table response, not Andrew's required hand check.

| Observation month | Downloaded (%) | Official FRED table (%) | Match | Checked |
|---|---:|---:|---|---|
| 2026-07-01 | 6.19 | 6.19 | Codex-assisted match | 2026-10-29 |
| 2026-08-01 | 6.32 | 6.32 | Codex-assisted match | 2026-10-29 |
| 2026-09-01 | 6.47 | 6.47 | Codex-assisted match | 2026-10-29 |

For every row: [official FRED page](https://fred.stlouisfed.org/series/BAA), [official table](https://fred.stlouisfed.org/data/BAA), and [download CSV](https://fred.stlouisfed.org/graph/fredgraph.csv?id=BAA), verified October 29, 2026. The official table response is saved as `evidence/BAA_official_table.txt` (HTML despite the requested `.txt` endpoint). Andrew must personally read these three months on FRED and record his check; automation does not fulfill “yourself.” Codex independently rechecked both official URLs on October 29, 2026: July 6.19%, August 6.32% and September 6.47% all match on the FRED table and series page. This remains Codex-assisted verification; the student hand check is pending.

## Economic relevance and point-in-time risks

BAA reflects corporate borrowing costs and compensation for credit and interest-rate risk. That makes it a reasonable candidate for describing financing conditions around a long-only portfolio with liquidity constraints and issuer limits. A higher yield can affect discount rates and financing costs, but this evidence does not show that BAA reliably predicts stock returns or justify changing mandate constraints. No Project 2 holdings or specific strategy are assumed.

Risks include monthly publication lag, possible corrections, later vintages leaking into past trades, gaps in future downloads, and mismatch between monthly observations and daily portfolio decisions. Do not interpolate future monthly values backward into daily decisions. Carry forward only the latest admissible observation, identify stale values, and quarantine missing signals rather than replacing them with later data. Today's full file would incorrectly make September's completed value appear usable during September. Revisions could also change signals for older months.

## What is a data card, and which fields prevent leaks?

A data card records what a dataset measures and how it can be used responsibly: source and link, units, observation frequency, publication availability, revision behavior, download date and verification evidence. The series ID, measured date, decision-date vintage, availability evidence and download timestamp let me trace the value and stop future information entering a backtest. Units and frequency prevent incorrect joins and interpretations. “Cleaned the data” describes a processing step; it gives no evidence of when a value became knowable or whether it later changed.

## Part 5 — Partner preparation

## Historical download function: line-by-line preparation

The walkthrough below is study reference material. Andrew reports completing the partner code explanation, exchanged questions and role swaps; the actual discussion record appears below.

| Actual code | Explanation |
|---|---|
| `@st.cache_data(ttl=3600, show_spinner=False)` | Cache results by inputs for one hour; cutoff dates are separate cache keys. |
| `def download_vintage(series_id, decision_date):` | Inputs are a FRED ID and the historical decision date. |
| Docstring: download only the requested vintage; never fall back | States the historical provenance contract. |
| `series_id = validate_id(series_id)` | Strip whitespace, uppercase the ID and reject characters that could alter the URL query. |
| `decision_date = date.fromisoformat(str(decision_date))` | Normalize the date to a Python date from ISO text. |
| `if decision_date > date.today():` | Check that the requested historical date is not in the future. |
| `raise DataError('A future historical cutoff cannot be verified.')` | Stop rather than claiming knowledge of future data. |
| `url = (f'https://alfred.stlouisfed.org/graph/alfredgraph.csv?id={series_id}'` | Start the official historical CSV URL with the validated ID. |
| `f'&vintage_date={decision_date.isoformat()}')` | Add the exact historical date as `YYYY-MM-DD`. |
| `return request_csv(url, series_id, decision_date)` | Download and validate this historical response; return the parsed frame. |

The shared `request_csv` helper uses `requests.get` with connection/read timeouts and redirects enabled, checks HTTP status, and requires HTTPS, the official ALFRED host/path, unchanged ID and unchanged vintage date after redirects. `parse_csv` requires `ID_YYYYMMDD` as the value column, reads the CSV, converts dots to missing values and values to numbers, parses dates, rejects duplicates/nonfinite numbers, sorts dates and rejects rows after the cutoff. Empty/all-missing data raises `DataError`; it never calls `download_current` to fill a failure.

The function downloads the historical frame; it does not itself select the final row. In the app, `latest(historical, cutoff)` drops missing values, keeps dates at or before the cutoff, sorts and returns the last date/value. A cutoff filter on current FRED would be insufficient because older observations may contain later revisions. The explicit vintage request and vintage-column validation prevent that substitution. The per-series `try/except DataError` displays a failure and continues other series.

## Plausible partner challenges and sample responses

1. **Publication timing:** “Does September 1 mean 6.47 was known on September 1?” No: that labels the month, and the September 30 ALFRED snapshot still ends with August's 6.32. September's 6.47 appears in the October 1 vintage, so I cannot use it in a September 30 decision ([September 30](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=BAA&vintage_date=2026-09-30), [October 1](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=BAA&vintage_date=2026-10-01)).
2. **Revisions:** “Does zero revised prove BAA never changes?” No: it means zero changes in the 1,292 common nonmissing dates between these two snapshots. PAYEMS changes on 381 dates, illustrating why each series and decision date needs its own vintage check ([PAYEMS historical](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=PAYEMS&vintage_date=2025-01-15), [PAYEMS current](https://fred.stlouisfed.org/graph/fredgraph.csv?id=PAYEMS)).
3. **Units/frequency:** “Is 6.47 a monthly return, and can we join it directly to daily trades?” No: BAA is a monthly yield series in percent, not a monthly holding-period return. I would carry forward only the latest knowable observation to daily decision dates and retain its age ([FRED metadata](https://fred.stlouisfed.org/series/BAA)).

## Partner Challenge and Response

**Completed October 29, 2026, based on Andrew's supplied discussion notes and session date. Partner: John; surname requires confirmation because local Lab 16 records and their Git history do not establish it.** The opening rate explanation, code explanation exercise, exchanged questions, BAA data-card challenge and role swaps are complete as reported by Andrew. These are student-supplied records, not activities independently observed by Codex.

### Opening discussion

**Andrew asked John:** "Pick one of the four rates. What does it measure, and why would it matter to an investor?"

**John answered:** "I would choose FEDFUNDS. It measures the federal funds rate, which is the interest rate banks charge each other for overnight lending. Investors care because it affects borrowing costs throughout the economy and influences stock valuations, bond yields, and economic growth expectations. When the federal funds rate rises, financing generally becomes more expensive and investors may require higher returns from risky assets."

This is John's explanation, not Andrew's. [Official FEDFUNDS page](https://fred.stlouisfed.org/series/FEDFUNDS).

### Code discussion

**Andrew asked John:** "Can you explain how the download_vintage() function retrieves historical data and prevents future information from entering a backtest?"

**John answered:** "The function sends a request to ALFRED using a specific vintage date rather than downloading the current FRED dataset. Because the request is tied to a historical snapshot, it retrieves only the information that was available on that date. The function validates the response and rejects observations after the cutoff date. If the historical data are unavailable, it raises an error instead of substituting current values, which prevents look-ahead bias."

**Follow-up question:** "What happens if the historical vintage is unavailable?"

**John answered:** "The program reports an error and stops processing that historical request. It never replaces the missing vintage with today's data because doing so would introduce future information into the backtest."

### Actual BAA data-card challenge

**Andrew asked John:** "Looking at my BAA data card, which field do you trust the least, and what evidence would you need to trust it?"

**John challenged:** "The publication-timing section is the field I trust the least. The ALFRED snapshots show when the value appears in the archive, but they do not prove the exact time Moody's originally released the data. I would want additional evidence about publication timing before allowing the series into a trading model."

**Andrew's final two-sentence response:** "The September 30 ALFRED vintage contains August's BAA value of 6.32%, while September's 6.47% first appears in the October 1 vintage, confirming that September's value should not be used for a September 30 investment decision. However, these snapshots do not establish Moody's exact original publication time, so I would keep BAA quarantined until that timing is verified."

Supporting evidence: [September 30 ALFRED vintage](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=BAA&vintage_date=2026-09-30), [October 1 ALFRED vintage](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=BAA&vintage_date=2026-10-01), and the preserved CSV downloads in `evidence/`. "First appears" refers to the checked snapshots, not proof of Moody's original release time.

### John's question to Andrew

**John asked:** "Why does the code validate the vintage-specific column name instead of simply reading whatever column appears in the CSV?"

**Andrew answered:** "Validating the vintage-specific column confirms that ALFRED returned the exact historical snapshot requested. Without that check, an unexpected response, redirect, or malformed file could allow incorrect data to enter the analysis and potentially introduce look-ahead bias."

### Role swaps

Andrew reports that both partners completed the opening rate explanation, code explanation exercise, exchanged questions, discussed the BAA data-card challenge and swapped roles. No additional dialogue or separate activity is inferred from these notes.

## Part 6 — Project 2 decision

**Decision: Quarantine BAA for Project 2 model use pending sufficient publication-timing and trading-time verification.** BAA is economically relevant to borrowing costs and credit conditions. The audit detects no revisions in 1,292 matching dates, but the September value was not available on September 30 and date-level CSVs do not establish intraday source release times. The Week 10 handout says to quarantine when a publication date cannot be found; the limited availability bracket is insufficient for a complete trading-time policy across the backtest.

**Exact proposed as-of rule:** for a trade on date D, use the ALFRED vintage dated D−1 calendar day and select the latest nonmissing observation in that vintage, retaining its measured date and provenance. D−1 is a conservative whole-day buffer for daily trading; it is not a fixed lag applied to today's values. Never backfill from current FRED. A failed download, unavailable vintage, missing usable observation or unverified availability keeps that decision's signal quarantined. This rule would still require an explicit trading calendar and time-zone policy before admission. Archive the downloaded vintage and retrieval timestamp for each decision.

**What would change my call:** independently check the three values, document release/archival timing across the actual test period and trading time, and verify the rule on each decision date. If those checks pass, admit BAA as a contextual input under the vintage rule. Reject it if reliable historical availability cannot be established or it does not serve the eventual model. No predictive stock-return claim is needed for this decision.

## Part 7 — Reflection

BAA measures the yield on seasoned Baa corporate bonds. It is a monthly series in percent, so I need to distinguish the month it describes from the date investors could see the finished value. On September 30, the latest available month was August at 6.32%. September's 6.47% appears in the October 1 vintage. That comparison shows why the date on a monthly row is not enough to decide whether it belongs in a historical investment model.

I found no changed values among the 1,292 overlapping BAA observations in this comparison, but that does not prove the series can never be corrected. PAYEMS makes the revision risk clearer: December 2024 was 159,536 thousand jobs in the January 15, 2025 vintage and is now 158,316. A historical model using today's file would give past decisions information that arrived later.

A backtest using the finalized file would overstate how much information was available at the time. It could change signals and trades; whether it raises or lowers reported returns depends on the rule, so these checks do not prove a profit bias of a particular size. My takeaway from the audit is that I need the source, units, measured period, historical availability and revision evidence before using a dataset. BAA is my confirmed selected series, and I would keep it quarantined until its publication-timing and trading-time policy is sufficiently verified. This is an AI-assisted research reflection for review. The completed partner discussion is recorded above from my supplied notes.

## Part 8 — Remaining requirements

- Series selection completed: BAA is confirmed for Lab 17 and the current Project 2 data-card evaluation. Its model admission remains quarantined pending timing verification.
- Personally read July 6.19, August 6.32 and September 6.47 on FRED, recording the check date. Codex's separate-table checks do not satisfy the hand-verification requirement.
- Partner opening rate explanation and role swaps: completed October 29, 2026, per Andrew's notes. No separate partner-written opening reason is claimed; confirm that record if independently required.
- Partner code explanation, exchanged questions and role swaps: completed per Andrew's notes; the actual code question and answer are recorded in DATA_CARD.md and ANSWERS.md.
- Partner challenge and evidence-based two-sentence response: completed and recorded. Partner is John; surname remains for confirmation. Discussion date: October 29, 2026 (session context).
- Publication-timing challenge discussion: completed as documented. Review the reflection in your own words; complete any separately required explanation of why cleaning is not a data card and any personal reflection not covered by the supplied notes.
- GitHub links: **student-reported submitted to Brightspace**, reported October 29, 2026. Individual Lab 17 quiz/checkout completion is **unconfirmed**; check its submitted/completed status yourself. The links may be part of that quiz workflow, but submitting links alone does not establish quiz completion. Codex did not access Brightspace.
- Complete or confirm the assigned ALFRED reading and publication/trading-time policy before admitting BAA to a model. Confirm any private deadline and instructions.
