# Lab 14 — Portfolio Baselines

AI use: OpenAI Codex implemented, executed, tested and documented this work. Student review and the required independent/partner activities remain outstanding. This is a course exercise, not investment advice.

## Purpose and official sources

What does each simple portfolio earn and risk, and does any meet the Meridian mandate?

The official [Lab 14](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/lab-14-portfolio-baselines.md), [prework](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/student-prework.md), [handout](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/student-handout.md), weekly README, course README and Project 2 instructions were read by Codex on October 20, 2026. Frozen Week 9 sources are in `sources/`, at course commit `1b6c33a1d3c46ceb8657e85cdb4571c13e9cfcb6`. The weekly page identifies the grading key as instructor-only; no public separate key was available. Lab 14 is a Tuesday completion checkout, 25 or 0; Brightspace governs dates, grading and submission conflicts.

## Run and files

From the repository root, Python 3, standard library only:

```text
python -B lab14/portfolio.py
python -B lab14/mandate.py
python -B lab14/verify_preservation.py
python -B -m unittest discover -s lab14 -p test_portfolio.py -v
```

Actual interpreter: `C:/Users/acpie/Documents/Codex/amazon-report-upload/project1/.runtime/python.exe`, Python 3.13.7. `-B` avoids bytecode writes. Logs contain commands, exit codes and outputs. `portfolio.py` holds editable inputs and reusable functions; `mandate.py` is a Lab 14 copy with E added; `test_portfolio.py` validates both and the CSV. `original_mandate_output.txt` records the initial Lab 13 rerun; `portfolio_output.txt`, `mandate_output.txt` and `validation.txt` are final execution evidence. `preservation_manifest.json`, `preservation_check.txt`, `verify_preservation.py` and `preservation_validation.txt` document prior-work preservation. All 38,662 baseline files, including runtimes, passed the full hash check; the published manifest excludes runtime/cache entries. `SUBMISSION_CHECKLIST.md` contains checkout instructions and copy-ready links/disclosure. `fetch_prices.py`, `prices.csv` and the Yahoo JSON/provenance files provide reproducible proposed-universe data.

## Inputs and methodology

All Meridian inputs are fictional course-authored annual training values, not market estimates. Decimal returns/volatilities and fractional weights are used internally. CPI is a labeled 2.5% estimate; CPI + 4% gives the 6.5% objective.

| Asset, in engine order | Expected return | Volatility | Reserve eligible |
|---|---:|---:|---|
| Treasury bills | 3.5% | 0.5% | Yes |
| Treasury 10-year note | 4.3% | 7.0% | Yes |
| Investment-grade bond fund | 5.0% | 6.0% | No |
| Global equity index fund | 8.0% | 16.0% | No |

Correlation matrix, in that order:

```text
1.00  0.10  0.05  0.00
0.10  1.00  0.80 -0.10
0.05  0.80  1.00  0.25
0.00 -0.10  0.25  1.00
```

Covariance[i][j] = correlation[i][j] × volatility[i] × volatility[j]. Expected return sums weight × expected return. Portfolio variance sums weight[i] × weight[j] × covariance[i][j] over all pairs; volatility takes its square root. Reserve allocation sums bills and Treasury-note weights. Inverse volatility normalizes each 1 / volatility by their sum. Each calculation is a separate importable function; the main guard permits reuse without printing. Comparisons use full precision, with rounding only for display.

Dimensions, finite values, coefficient bounds, symmetry, a unit diagonal and long-only weights summing to one are checked. Inverse weighting requires positive volatilities. The engine does not certify positive semidefiniteness of arbitrary correlation matrices; it rejects materially negative computed portfolio variance. It is a training engine, not a general covariance estimator.

## Calculated results

| Portfolio | Weights: bills / 10-year / IG / equity (%) | Return | Volatility | Reserve | Meets 6.5%? |
|---|---|---:|---:|---:|---|
| Benchmark | 0.0 / 0.0 / 40.0 / 60.0 | 6.80% | 10.46% | 0.0% | Yes |
| Equal weight | 25.0 / 25.0 / 25.0 / 25.0 | 5.20% | 5.21% | 50.0% | No |
| Inverse volatility | 84.3 / 6.0 / 7.0 / 2.6 | 3.77% | 1.05% | 90.3% | No |

These match all official displayed values. Rounded inverse-volatility weights total 99.9%; unrounded weights total 100%.

Benchmark meets the expected-return objective but fails the 3% reserve minimum. Equal weight and inverse volatility satisfy that reserve minimum but miss the return objective. None satisfies both. Expected annual return does not establish the client's rolling-five-year objective net of costs or guarantee future returns.

## AI-generated study notes

These explanations are study assistance, not the student's independent by-hand work or personal reflections.

Diversification spreads exposure across investments that do not move identically. With positive weights, correlation below +1 reduces the covariance contribution relative to perfect positive correlation. It can lower portfolio risk, but does not guarantee volatility below each constituent: the benchmark remains riskier than the bond fund alone. Common market risk remains, and correlations can increase in stress.

Benchmark covariance = 0.25 × 0.06 × 0.16 = 0.0024. Variance = (0.4² × 0.06²) + (0.6² × 0.16²) + (2 × 0.4 × 0.6 × 0.0024) = 0.000576 + 0.009216 + 0.001152 = 0.010944. Square root = 0.1046135746, or 10.46%. Omitting covariance incorrectly gives 9.90%. The student must separately perform the assigned by-hand calculation.

The benchmark has the highest expected return and volatility here but no eligible reserves. Equal weight is simple and transparent; equal dollars do not imply equal risk, and its return misses the objective. Inverse volatility gives bills the largest weight because 1 / 0.005 = 200 dominates the reciprocals. It produces low volatility but misses the objective and concentrates capital in cash exposure. Its weighting ignores correlations and returns; it is not full risk parity or minimum-variance optimization. These are trade-offs, not a supplied personal CIO recommendation.

## Validation results

All five automated tests pass, exit 0 (including exact consecutive monthly dates): known answers and objective boundaries; sensitivity/restoration; invalid inputs; A–D preservation and E; CSV-to-raw-source verification. `validation.txt` contains actual results.

Symmetric IG/equity correlation 0.25 → 0.50 moves benchmark volatility 10.46135746% → 10.99818167% (11.00% rounded); restoring 0.25 returns 10.46135746%. A temporary copied matrix is used; both final production entries remain 0.25. Invalid 1.3 is rejected with a bounds message, asymmetry with a symmetry message, and a 1×1 table with a dimension message. Wrong-length, negative, nonunit and NaN weights are rejected, as is zero volatility for inverse weighting. No invalid production values remain.

The original Lab 13 checker was rerun before implementation. A/D pass; B fails three rules; C fails one. The Lab 14 copy retains all A–D holdings and verdicts. Candidate E is 40% IG bonds and 60% equity, zero elsewhere. It has 0% reserves against 3% required and fails only that rule; liquidity is 100% within five days and nonexempt single-company exposure is 0%. Failure counts A/B/C/D/E are 0/3/1/0/1. A benchmark is a comparison reference, not necessarily an admissible client portfolio. The calendar-year loss promise still requires CIO clarification.

## Project 2 preparation — PROPOSED universe

The existing personal mandate in `../lab13/lab13.md` was inspected before selecting suggestions: a 25-year-old with $50,000 toward a first home in five years, a 4–5% annual net-return goal, at least 20% low-risk liquid reserves, a 10% corporate-issuer cap, at least 90% accessible within five business days, no borrowing/shorting/derivatives, and declining equity exposure.

| Ticker | Fund name (Yahoo metadata) | Proposed role and rationale |
|---|---|---|
| BIL | State Street SPDR Bloomberg 1-3 Month T-Bill ETF | Short Treasury cash/reserve proxy for the liquidity floor |
| IEF | iShares 7-10 Year Treasury Bond ETF | Government bond exposure; duration risk means it is not treated as cash for the personal reserve floor |
| LQD | iShares iBoxx $ Investment Grade Corporate Bond ETF | Corporate fixed income, with credit and duration risks |
| VT | Vanguard Total World Stock Index Fund ETF Shares | Broad global growth exposure; home-purchase timing limits acceptable equity losses |

These are proposals, not confirmed personal choices or allocations. Prospectus/holdings, look-through issuer treatment, accessibility and suitability still need review. Do not transfer Meridian's 6.5% objective or Treasury-note reserve rule automatically to this client. Proposed numerical objective: 4.5% net, midpoint of the existing range, pending the student's decision. Starting hard constraint: at least 20% in low-risk liquid reserves. The client's willingness to delay the home purchase and the equity glide path remain unresolved.

`prices.csv` has 60 completed monthly adjusted-close price levels per fund, October 2021–September 2026, date first and oldest first, then BIL/IEF/LQD/VT. Yahoo monthly timestamps label the start of the month; source dates are retained, not asserted to be trading/availability dates. Partial October 2026 is excluded. Sixty price levels yield 59 within-sample monthly returns. No filling/interpolation/fabrication occurred. Every value matches the saved raw `indicators.adjclose` data. Adjustments include payouts/splits and may be revised; these data are history, not forecasts or point-in-time signal evidence.

For each BIL/IEF/LQD/VT, the source was Yahoo Finance's chart endpoint `https://query1.finance.yahoo.com/v8/finance/chart/TICKER?range=10y&interval=1mo`, downloaded October 20, 2026 UTC. Exact URLs, names and retrieval times are in `sources/price_provenance.json`; raw responses are `sources/TICKER_monthly.json`. `fetch_prices.py` reproduces retrieval (network required; rerunning replaces the snapshots and CSV). Student visual review of Yahoo Historical Data → Monthly → Adj Close remains outstanding.

Before Thursday: confirm funds, objective and constraint; review the assigned Streamlit install page and Basic concepts through Data flow, install Streamlit in a separate environment and run its demo. The app, search/stress, later signal/holdout/cost analysis, memo and videos are future Lab 15/Project 2 work, not claimed completed here.

## Official requirement status

| Requirement | Status |
|---|---|
| Read official sources and inspect existing mandate | Completed by Codex |
| Rerun original mandate before implementation | Completed; output retained |
| Standard-library reusable engine and three baselines | Completed |
| Known answers, sensitivity, restoration, invalid-input refusal | Completed |
| Candidate E reserve failure, original candidates retained | Completed |
| Written methodology, comparison, study explanations, tests and disclosure | Completed; AI-authored |
| Own-universe proposal and real five-year monthly adjusted-close CSV | Prepared; student selection/review required |
| Personal reading, by-hand arithmetic, quiz, explanation and reflection | STUDENT ACTION REQUIRED |
| No-AI code explanation and partner swap/break | STUDENT ACTION REQUIRED |
| Thursday Streamlit reading, installation and demo | STUDENT ACTION REQUIRED / later preparation |
| GitHub delivery | See final publication report and SUBMISSION_CHECKLIST.md links |
| Brightspace deadline/fields, individual checkout and attendance | External verification/student action required |

## STUDENT ACTION REQUIRED

- Personally read the assigned diversification material (the handout is the allowed alternative), work the benchmark by hand, and give the five-minute no-screen explanation to the Lab 13 partner, then swap.
- Read and run the code. Choose the line you understand least; answer an AI quiz before receiving its explanation. No student answer is invented. Unanswered suggested quiz: in the variance sum, why do both (i,j) and (j,i) appear?
- Follow the exact official instruction, **“Explain the code (six minutes, no AI)”**: explain the volatility block line by line to the partner; answer their question; swap. No submission-ready personal response is supplied.
- Run the partner's script, reproduce their values, change IG/equity correlation to 1.3, verify refusal and undo. Automated local tests do not fulfill partner participation.
- Give your partner the two personal reflections: why inverse volatility piles into bills, and which baseline you would show the CIO first and why. AI study notes above are not your response.
- Confirm personal funds/objective, inspect Yahoo monthly adjusted closes, resolve the home-purchase question, and prepare Streamlit for Thursday.
- Verify the live Brightspace header, deadline and fields, complete individual checkout/any attendance verification, and submit individually. No Brightspace access, submission, attendance or partner activity is claimed.

## AI disclosure

I used OpenAI Codex to read official course materials; inspect my existing mandate; implement and run the portfolio engine and a separate mandate-checker copy; validate known answers, correlation sensitivity, invalid inputs and candidate E; draft documentation and study explanations; propose a fund universe; retrieve and verify Yahoo monthly adjusted-close data; and prepare the GitHub submission package. Codex executed the scripts and tests. Student review and required independent/partner activities remain outstanding. No personal reflection, partner participation, attendance, individual checkout or Brightspace submission is represented as completed by AI.
