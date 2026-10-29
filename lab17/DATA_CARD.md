# FIN 43900 — Lab 17: Point-in-Time Audit

Andrew Pienkos · Fall 2026 · Professor Cinder Zhang

## Series identification and selection

**Provisional series: BAA — Moody's Seasoned Baa Corporate Bond Yield.** No recorded Lab 17 prework selection was found in the local repository. BAA is the user's fallback candidate, not a verified original choice. Andrew must confirm it. There is no local Lab 15 folder; Lab 16's deterministic testing and explicit pending-activity documentation were reviewed. Existing Lab 13 untracked work was preserved.

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

For every row: [official FRED page](https://fred.stlouisfed.org/series/BAA), [official table](https://fred.stlouisfed.org/data/BAA), and [download CSV](https://fred.stlouisfed.org/graph/fredgraph.csv?id=BAA), verified October 29, 2026. The official table response is saved as `evidence/BAA_official_table.txt` (HTML despite the requested `.txt` endpoint). Andrew must personally read these three months on FRED and record his check; automation does not fulfill “yourself.”

## Economic relevance and point-in-time risks

BAA reflects corporate borrowing costs and compensation for credit and interest-rate risk. That makes it a reasonable candidate for describing financing conditions around a long-only portfolio with liquidity constraints and issuer limits. A higher yield can affect discount rates and financing costs, but this evidence does not show that BAA reliably predicts stock returns or justify changing mandate constraints. No Project 2 holdings or specific strategy are assumed.

Risks include monthly publication lag, possible corrections, later vintages leaking into past trades, gaps in future downloads, and mismatch between monthly observations and daily portfolio decisions. Do not interpolate future monthly values backward into daily decisions. Carry forward only the latest admissible observation, identify stale values, and quarantine missing signals rather than replacing them with later data. Today's full file would incorrectly make September's completed value appear usable during September. Revisions could also change signals for older months.

## What is a data card, and which fields prevent leaks?

A data card records what a dataset measures and how it can be used responsibly: source and link, units, observation frequency, publication availability, revision behavior, download date and verification evidence. The series ID, measured date, decision-date vintage, availability evidence and download timestamp let me trace the value and stop future information entering a backtest. Units and frequency prevent incorrect joins and interpretations. “Cleaned the data” describes a processing step; it gives no evidence of when a value became knowable or whether it later changed.

## Project 2 decision

**Provisional decision: Quarantine BAA for Project 2 model use pending timing and selection confirmation.** BAA is economically relevant to borrowing costs and credit conditions. The audit detects no revisions in 1,292 matching dates, but the September value was not available on September 30 and date-level CSVs do not establish intraday source release times. The Week 10 handout says to quarantine when a publication date cannot be found; the limited availability bracket is insufficient for a complete trading-time policy across the backtest.

**Exact proposed as-of rule:** for a trade on date D, use the ALFRED vintage dated D−1 calendar day and select the latest nonmissing observation in that vintage, retaining its measured date and provenance. D−1 is a conservative whole-day buffer for daily trading; it is not a fixed lag applied to today's values. Never backfill from current FRED. A failed download, unavailable vintage, missing usable observation or unverified availability keeps that decision's signal quarantined. This rule would still require an explicit trading calendar and time-zone policy before admission. Archive the downloaded vintage and retrieval timestamp for each decision.

**What would change my call:** confirm BAA as the intended prework series, independently check the three values, document release/archival timing across the actual test period and trading time, and verify the rule on each decision date. If those checks pass, admit BAA as a contextual input under the vintage rule. Reject it if reliable historical availability cannot be established or it does not serve the eventual model. No predictive stock-return claim is needed for this decision.

## Historical download function: line-by-line preparation

This is study preparation. Andrew must explain it to his partner without AI during the actual six-minute exercise, answer the partner's code question, and swap roles.

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

- Actual partner name: **[pending; do not assume John Heins]**
- Actual challenge / least trusted field: **[pending]**
- Two-sentence response: **[write after the actual challenge]**
- Supporting app/FRED evidence: **[pending]**
- Date completed: **[pending]**
- Partner's code question and answer: **[pending]**

Also complete the opening five-minute no-screen explanation of one rate and why it matters, have the partner write the reason, and swap. The weekly instructions say to work with the same partner, but this package does not certify who participated. No partner interaction, role swap, or independent explanation is claimed.

## Reflection

BAA measures the yield on seasoned Baa corporate bonds. It is a monthly series in percent, so I need to distinguish the month it describes from the date investors could see the finished value. On September 30, the latest available month was August at 6.32%. September's 6.47% appears in the October 1 vintage. That comparison shows why the date on a monthly row is not enough to decide whether it belongs in a historical investment model.

I found no changed values among the 1,292 overlapping BAA observations in this comparison, but that does not prove the series can never be corrected. PAYEMS makes the revision risk clearer: December 2024 was 159,536 thousand jobs in the January 15, 2025 vintage and is now 158,316. A historical model using today's file would give past decisions information that arrived later.

A backtest using the finalized file would overstate how much information was available at the time. It could change signals and trades; whether it raises or lowers reported returns depends on the rule, so these checks do not prove a profit bias of a particular size. My takeaway from the audit is that I need the source, units, measured period, historical availability and revision evidence before using a dataset. I would keep BAA quarantined until its timing policy and my series selection are confirmed. This is an AI-assisted research reflection for review, not a claim that I completed the personal discussions.
