# FIN 43900 Lab 06 - Amazon (AMZN)

Educational Use Disclaimer: This analysis was prepared solely for educational purposes as part of Purdue University FIN 43900 coursework. It is a simplified valuation exercise and should not be relied upon for investment, trading, or other financial decisions. Nothing in this report constitutes financial or investment advice.

**Date:** September 10, 2026. **Conditional call:** watch/defer.

The sourced-input model gives **$5.9930 per diluted share**, versus an observed
after-hours price of **$252.13**. This is outside the professor's reasonableness
band. The result exposes the limitations of applying a simple growth path to
investment-heavy cash flow; it is not a claim that Amazon should trade at $5.99.
It preserves the prior Amazon report's concern about AWS/AI investment turning
into sufficient future cash flow.

## 1. Inputs, dates, and exact source locators

Sources were read on September 10, 2026. [K] is Amazon's latest available **10-K**,
for FY2025, filed February 6, 2026 (accepted February 5), verified against its
[SEC filing index][KI]. [Q] is the newer June 2026 **10-Q**, used to update the
balance-sheet bridge and share count. The starting cash-flow scale remains the
latest audited annual figure, not a trailing-quarter figure or vendor FCF.
All rates are nominal annual USD rates. No training placeholders are used in the
Amazon run. Forecasts and estimates below are judgments, not reported facts.

| Input | Value | Unit | As-of / period | Status | Exact source locator |
|---|---:|---|---|---|---|
| Operating cash flow | 139,514 | USD million | FY ended 2025-12-31 | Reported | [K], Item 8, Consolidated Statements of Cash Flows, p. 36, operating-activities total |
| Debt interest paid, net of capitalized interest | 1,458 | USD million | FY2025 | Reported | [K], Note 1, Supplemental Cash Flow Information, p. 42, debt-interest row |
| Marginal tax shield rate | 21% | annual rate | Estimate made 2026-09-10; statutory basis FY2025 | Estimate | [K], Note 9, p. 65, federal statutory-rate reconciliation; used as a marginal-rate proxy |
| Gross cash capital expenditures | 131,819 | USD million outflow magnitude | FY2025 | Reported | [K], Item 8, cash-flow statement, p. 36, property/equipment purchases |
| **Starting FCFF** | **8,846.8200** | **USD million** | **FY2025 baseline** | **Calculated using estimated tax shield** | **OCF + interest paid x (1-tax) - gross capex; calculation below** |
| Year 1 FCFF growth | -50% | annual growth | Forecast made 2026-09-10; forward Year 1 | Forecast | Student scenario below; evidence [K] Item 7, pp. 20, 22-24; [R], Cash Flows and Shares, Q2 2026 column |
| Year 2 FCFF growth | +50% | annual growth | Forecast made 2026-09-10; forward Year 2 | Forecast | Same scenario/evidence; recovery from a depressed first year |
| Year 3 FCFF growth | +40% | annual growth | Forecast made 2026-09-10; forward Year 3 | Forecast | Same scenario/evidence; cash conversion improves |
| Year 4 FCFF growth | +25% | annual growth | Forecast made 2026-09-10; forward Year 4 | Forecast | Same scenario/evidence; recovery fades |
| Year 5 FCFF growth | +15% | annual growth | Forecast made 2026-09-10; forward Year 5 | Forecast | Same scenario/evidence; recovery fades further |
| **WACC** | **11.80145113%** | **annual discount rate** | **Estimate made 2026-09-10** | **Estimate** | **Component table and market-weighted calculation below; not a copied WACC** |
| Terminal growth | 3% | annual nominal rate | Chosen 2026-09-10; after Year 5 | Estimate | [F], Table 1, longer-run median real GDP 2.0% and PCE inflation 2.0%; choose a conservative rate below their roughly 4% nominal combination |
| Cash and equivalents | 78,213 | USD million | 2026-06-30 | Reported; treated as non-operating in this lab | [Q], Item 1, Consolidated Balance Sheets, cash/equivalents row; Note 2 cash reconciliation |
| Long-term debt face, including current maturities | 132,995 | USD million | 2026-06-30 | Reported | [Q], Note 5 - Debt, total face-value row; includes current portion |
| Other short-term borrowings | 325 | USD million | 2026-06-30 | Reported | [Q], Note 5, paragraph on other short-term credit facilities in accrued expenses |
| **Total debt deducted** | **133,320** | **USD million** | **2026-06-30** | **Calculated** | **132,995 + 325; [Q] Note 5** |
| Diluted weighted-average shares | 10,903 | million shares | Three months ended 2026-06-30 | Reported | [Q], Note 1 - Earnings Per Share, diluted EPS denominator, Q2 2026 column; not the cover-page basic count |
| **Reverse DCF target / observed price** | **252.13** | **USD/share** | **Quote: 2026-09-10 16:26 EDT; observed 16:44:44 EDT (20:44:44 UTC)** | **Observed after-hours quote** | **[P], AMZN overview, top quote block labeled After-hours; market-data vendors identified in page footer** |

The quote is a timestamped observation, not a continuously updating live feed.
The page also displayed a $251.89 regular-session close at 16:00 EDT. The target
is explicitly the newer **after-hours $252.13** observation, not the close or an
unverified price-history table entry.

### FCFF definition and recent history

```text
After-tax debt interest = 1,458 x (1 - 0.21) = 1,151.82 USD million
Starting FCFF = 139,514 + 1,151.82 - 131,819 = 8,846.82 USD million
```

Capex is **gross cash purchases**. Amazon's published FCF nets property-sale
proceeds/incentives against purchases and does not add back after-tax debt
interest, so it is not substituted for the required formula. The consistently
calculated annual history, using the same 21% shield proxy, is:

| Fiscal year ended December 31 | OCF | Debt cash interest | Gross capex | Calculated FCFF |
|---|---:|---:|---:|---:|
| 2023 | 84,946 | 2,608 | 52,729 | 34,277.32 |
| 2024 | 115,877 | 1,858 | 82,999 | 34,345.82 |
| 2025 | 139,514 | 1,458 | 131,819 | 8,846.82 |

All historical amounts are USD million; reported components: [K] pp. 36 and 42,
respective annual columns. FCFF is calculated, not reported. In the newer Q2
release, TTM OCF is 161,403 and net capex is 169,007, leaving reported FCF of
-7,604 USD million ([R], Supplemental Financial Information, Cash Flows and
Shares, Q2 2026 column, TTM ended 2026-06-30). That reported FCF is a warning
about current cash conversion, **not** the starting FCFF inserted into this model.

**Forecast rationale:** the first-year 50% decline represents continuing capital
spending pressure. Subsequent 50%, 40%, 25%, and 15% growth assumes that added
capacity begins converting demand into cash while the recovery slows. These are
transparent student scenario choices, not management FCFF guidance or a fitted
market-price forecast. Even Year 5 FCFF of 13,353.17 remains far below the
2023-2024 calculated level. A recovery is plausible, but neither its timing nor
magnitude is established by the filings. The base remains positive; a negative
starting-FCFF model would need an explicit recovery path instead of growing a loss.

**Timing convention:** Years 1-5 are five forward annual model periods from the
valuation date, with cash flows at each year-end. The 2025 figure supplies their
starting scale; no stub-period or midyear convention is introduced. Gordon value
uses Year 6 FCFF but is located at Year 5 and discounted exactly five periods.

### WACC estimated from components

| Component | Value | Unit | As-of date | Status / exact locator |
|---|---:|---|---|---|
| Risk-free rate | 4.95% | annual nominal yield | 2026-09-10 | Reported; [T], Daily Treasury Par Yield Curve Rates, 09/10/2026 row, 10 Yr column |
| Beta | 1.44 | dimensionless | Observed 2026-09-10 | Vendor estimate; [B], Stock Price Statistics, Beta (5Y); vendor sampling method not separately verified |
| Equity risk premium | 5% | annual return premium | Lab 06 assumption, used 2026-09-10 | Assumption; [L], R - WACC row |
| Pretax debt rate | 5.341% | annual yield | Issue pricing 2026-07-07; proxy used 2026-09-10 | Estimate using reported issue YTM; [D], Fixed Rate Notes, Yield to Maturity, 2036 Notes |
| Tax rate | 21% | annual tax-shield rate | Estimated 2026-09-10 from FY2025 statutory rate | Estimate; [K], Note 9, p. 65; ignores jurisdiction-specific marginal differences |
| Cost of equity | 12.15% | annual return | Estimated 2026-09-10 | Calculated: 4.95% + 1.44 x 5% |
| After-tax debt cost | 4.21939% | annual return | Estimated 2026-09-10 | Calculated: 5.341% x (1 - 0.21) |
| Point-in-time common shares for WACC only | 10,783 | million shares | 2026-06-30 | Reported; [Q], balance sheet, common-stock shares outstanding parenthetical |
| Market equity proxy | 2,718,717.79 | USD million | Estimated at 2026-09-10 quote; June share count | 252.13 x 10,783; price [P], shares [Q] |
| Notes market value | 123,800 | USD million | 2026-06-30 | Reported approximate fair value; [Q], Note 5, paragraph below debt table |
| Non-note long-term debt proxy | 855 | USD million | 2026-06-30 | Reported carrying/face amount used as fair-value estimate; [Q], Note 5, other long-term debt row |
| Short-term debt proxy | 325 | USD million | 2026-06-30 | Reported carrying amount used as fair-value estimate; [Q], Note 5, short-term facilities paragraph |
| Market debt proxy | 124,980 | USD million | June values used in 2026-09-10 estimate | 123,800 + 855 + 325; estimate, not today's traded debt value |
| Equity / debt weights | 95.605018% / 4.394982% | capital weights | Estimated 2026-09-10 | E/(E+D) and D/(E+D) from preceding rows |

```text
WACC = [2,718,717.79 x 0.1215 + 124,980 x 0.0421939]
       / [2,718,717.79 + 124,980]
     = 0.11801451134756481 = 11.80145113%
```

The code retains full precision. It uses market equity rather than book equity;
the diluted EPS share count is reserved for value per share. Debt is weighted
using disclosed note fair value plus explicit carrying-value estimates for the
small remaining facilities. The July issue yield is a borrowing-cost proxy,
not a September bond quote. This is an approximate WACC with dated components.

**Scope limitations:** cash and debt are the same June reporting snapshot; the
bridge uses debt face value (including current debt), while WACC uses the market
proxy. Subsequent borrowing is not silently added to debt without its cash/use
of proceeds: [Q] Note 5 discloses $25,000 million of July notes, so June balances
are not claimed to be today's balances. The lab's simple cash/debt bridge omits
separate valuation of marketable/strategic investments and assumes all included
cash is excess. Only debt cash interest is unlevered; separate leases/financing
obligations are not fully recast. These are limitations of this simplified lab
model, not adjustments made to reach the market price.

## 2. Training validation before the company run

The unmodified Lab 05 file was run first and all twelve outputs matched to four
decimals. After extending that same calculation, `--validate-training` passed
before the first Amazon run. Complete original and new check records are in
`lab06_validation.txt`.

| Training WACC / terminal growth | 2% | 3% | 4% |
|---|---:|---:|---:|
| 9% | 28.60 | 32.94 | 39.02 |
| 10% | 24.36 | **27.50** | 31.69 |
| 11% | 21.06 | 23.41 | 26.44 |

All nine cells match the professor's table. The middle is the training base,
value falls down each column and rises across each row. The $30 training reverse
DCF solves to **+1.777948 percentage points** on each growth rate and reprices to
$30 within $0.0000001. Tests cover INVALID cells, an unreachable target, growth
at/below -100%, true endpoint solutions, and unchanged base inputs.

## 3. Amazon results

The twelve standard output lines are preserved in `dcf_output_lab06.txt`.

| Result | Value | Unit |
|---|---:|---|
| FCFF Years 1-5 | 4,423.4100; 6,635.1150; 9,289.1610; 11,611.4513; 13,353.1689 | USD million |
| PV explicit FCFF | 30,988.2064 | USD million |
| Terminal value at Year 5 | 156,267.0041 | USD million |
| PV terminal value | 89,460.2450 | USD million |
| Enterprise value | 120,448.4515 | USD million |
| Equity value: EV + 78,213 - 133,320 | 65,341.4515 | USD million |
| Base value per diluted share | **5.9930** | USD/share |
| PV terminal value / EV | 0.7427 (74.27%) | ratio |
| Observed market price | **252.13** | USD/share, quote 2026-09-10 16:26 EDT |

### Required fixed-rate sensitivity grid

Everything except WACC and terminal growth is fixed at the Amazon base inputs.

| WACC / terminal growth | 2% | 3% | 4% |
|---|---:|---:|---:|
| 9% | 9.64 | 11.70 | 14.59 |
| 10% | 7.64 | 9.14 | 11.13 |
| 11% | 6.09 | 7.21 | 8.65 |

Fixed-grid range is **$6.0937-$14.5950** from the 11%/2% and 9%/4% corners.
Its middle is a 10% WACC scenario, not the estimated Amazon base WACC.

### Amazon grid with the actual base in the center

To satisfy the center-cell merit criterion without pretending that WACC is 10%,
this additional grid uses estimated WACC minus/plus one percentage point and
terminal growth minus/plus one point. Exact rates are used; headings are rounded.

| WACC / terminal growth | 2% | 3% | 4% |
|---|---:|---:|---:|
| 10.801451% | 6.37 | 7.56 | **9.09** |
| 11.801451% | 5.08 | **5.99** | 7.13 |
| 12.801451% | **4.04** | 4.75 | 5.63 |

**Lowest corner: $4.0382** at WACC 12.80145113%, g 2%.
**Highest corner: $9.0873** at WACC 10.80145113%, g 4%.
**Base: $5.9930**, in the center. Direction and corner checks passed on unrounded
values. No displayed cell is invalid, but the code prints `INVALID` for g >= WACC.

### Reverse DCF: required bracket, then a disclosed wider experiment

The solved variable is **one uniform additive percentage-point shift** to
[-50%, 50%, 40%, 25%, 15%], not five independently solved rates.

- Required shift bracket **[-5, +10] percentage points**: endpoint values are
  **$3.6173 and $12.1885**. The $252.13 target is outside them. Result:
  **no solution in bracket**. There are no solved growth rates within this bracket;
  neither bound is returned as a solution.
- To show the growth implied by the observed price, a separately labeled
  supplementary bracket **[-5, +150] points** is explicitly specified at the top
  of the same file. Bisection solves **+96.978684 points**, implying growth of
  **46.978684%, 146.978684%, 136.978684%, 121.978684%, 111.978684%** in Years 1-5.
  Repriced value is **$252.12999999**. This is outside the required bracket and
  is an extreme mathematical scenario, not the adopted forecast.

Both searches hold fixed: **starting FCFF 8,846.82 USD million; WACC
11.80145113%; terminal growth 3%; cash 78,213 USD million; debt 133,320 USD million;
diluted shares 10,903 million; five annual year-end periods; terminal discount
of five years**. WACC and its initial market-value weights are not recalculated
while solving. Only explicit FCFF growth rates change; terminal growth does not.
The wider solution is one set of assumptions consistent with the price under
these fixed inputs, **not proof of mispricing**.

## 4. Reasonableness and conditional call

**$5.9930 / $252.13 = 0.023769x**, outside the required **0.5x-2.0x** band
of **$126.065-$504.260**. I did not change the forecast, WACC, or starting FCFF
to force the result inside the band. Widening the diagnostic reverse-search
bracket does not change the base valuation.

**The one input I distrust most is the five-year FCFF growth forecast.** In
particular, the Year 1 -50% assumption and subsequent recovery are not company
guidance: the recent cash-flow evidence shows investment pressure, but it cannot
establish how quickly new capacity earns cash returns. Percentage growth applied
to a temporarily depressed annual base can badly represent Amazon's investment
cycle. The extreme implied recovery and large terminal share reinforce that
uncertainty; a richer investment/cash-conversion model would be needed before
using this number for a real decision.

**Initiate if a refreshed, filing-supported FCFF forecast produces a DCF value at
least 20% above the observed share price and the required growth is supported by
AWS cash conversion; otherwise watch/defer.** The 20% cushion is my decision
rule, not a reported fact. At the current target, that requires a defensible
value of at least **$302.556**. With the current unchanged base, the corresponding
price ceiling is **$4.9941**; this is a mechanical condition, not a price target.
The evidence needed to change the call is a sustained, sourced improvement in
cash conversion, not merely a higher assumed growth rate.

**Monitor:** the next earnings release's trailing-twelve-month operating cash
flow minus **gross cash property/equipment purchases**, and whether it turns
sustainably positive as AWS/AI capacity ramps. This directly tests the concern
in the earlier watch/defer report.

## 5. Reproduce, quality checks, and checkout

One DCF file, standard library only:

```powershell
python dcf.py                      # Amazon: twelve lines + grids + reverse DCF
python dcf.py --training           # Training: twelve lines + grid + $30 reverse DCF
python dcf.py --lab05              # Exactly the original twelve training lines
python dcf.py --validate-training  # Training checks only
python dcf.py --validate           # Training checks, then Amazon checks
```

Python 3.13.7 was used. If `python` is unavailable on PATH in this session, the
tested executable is `C:\Users\acpie\AppData\Local\Temp\fin439-python-3.13.7\python.exe`;
invoke it with PowerShell's `&` followed by the same file and arguments.
The older `validate_dcf.py` is retained unchanged as Lab 05 coursework; use the
new embedded `--validate` checks for the updated Lab 06 interface.

| Floor / merit item | Evidence and status |
|---|---|
| Sourced Amazon inputs | Values, units, dates, locators, and estimate/forecast labels above; complete |
| Amazon value | Twelve outputs, bridge, and diluted-share denominator; complete |
| Grid and direction | Required grid plus centered company grid, corner ranges and tested directions; passed |
| Reverse DCF / price-implied growth | Training shift reproduced; required bracket honestly unbracketed; separate wider solution and all fixed inputs stated; passed |
| Reasonableness | Outside-band result retained; single least-trusted input and reason stated; complete |
| Conditional call | Initiate-if/otherwise rule, measurable trigger, and one monitoring metric; complete |

Both instruction pages were reread after the work. All computational tests
passed; the grade remains the instructor's judgment. Previous Lab 03/04/05
notes, filings, and saved outputs are preserved. Only `dcf.py` is updated.

**Files to upload later:** `dcf.py`, `lab06.md`, `dcf_output_lab06.txt`, and
`lab06_validation.txt`. In **Brightspace > Quizzes > Lab 06**, paste the four
GitHub file-page links after upload and finish the individual checkout. Repository
URL/branch are not available here, so actual remote links cannot yet be supplied.
No Git repository was created and no upload or submission was performed.

Classroom actions remain personal: discuss the hardest input to source (90
seconds each), complete any instructor-directed quiz, and the optional anonymous
temperature check. The linked open challenge is optional depth, not an additional
floor deliverable. AI assistance: Codex helped draft the code, sourcing table,
and explanations and executed the validations; review the judgments before submission.

## Sources

[K]: https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm
[KI]: https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/0001018724-26-000004-index.htm
[Q]: https://www.sec.gov/Archives/edgar/data/1018724/000101872426000026/amzn-20260630.htm
[R]: https://ir.aboutamazon.com/news-release/news-release-details/2026/Amazon-com-Announces-Second-Quarter-Results/default.aspx
[P]: https://stockanalysis.com/stocks/amzn/
[B]: https://stockanalysis.com/stocks/amzn/statistics/
[T]: https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2026
[D]: https://www.sec.gov/Archives/edgar/data/1018724/000110465926081334/tm2619352d3_fwp.htm
[F]: https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260617.htm
[L]: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-03/lab-06-sensitivity-and-reverse-dcf.md

- [Amazon 2025 10-K][K] and [filing index][KI]
- [Amazon Q2 2026 10-Q][Q] and [earnings release][R]
- [AMZN quote][P] and [beta statistics][B]
- [Treasury yields][T], [Amazon July pricing term sheet][D], [Federal Reserve projections][F]
- [Lab 06][L] and [Session 6 slides](https://cinderzhang.github.io/FIN43900-Fall2026/lessons/week-03/slides-session-06.html)
