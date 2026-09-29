# Lab 11 — Amazon.com, Inc. (AMZN)

**Research question: Which assumptions drive my company's forecast and value, and what explains their effects?**

**Status: computational analysis, student review, and student-confirmed reciprocal partner evidence complete.** The higher-capex case is invalid because it exhausts funding. Its value is unavailable; its statement outputs are diagnostics, not a usable forecast or ranked endpoint.

## Official materials and preservation

Materials read at current course revision `69eac1e8cbd63b35e801d48d990c4b594bfdbbc8`:

- [Official Lab 11](https://github.com/CinderZhang/FIN43900-Fall2026/blob/69eac1e8cbd63b35e801d48d990c4b594bfdbbc8/lessons/week-06/lab-11-proforma-what-if.md)
- [Student handout](https://github.com/CinderZhang/FIN43900-Fall2026/blob/69eac1e8cbd63b35e801d48d990c4b594bfdbbc8/lessons/week-06/student-handout.md)
- [Prework](https://github.com/CinderZhang/FIN43900-Fall2026/blob/69eac1e8cbd63b35e801d48d990c4b594bfdbbc8/lessons/week-06/student-prework.md)
- [Week 6 README](https://github.com/CinderZhang/FIN43900-Fall2026/blob/69eac1e8cbd63b35e801d48d990c4b594bfdbbc8/lessons/week-06/README.md)
- [Part 2 captions](https://github.com/CinderZhang/FIN43900-Fall2026/blob/69eac1e8cbd63b35e801d48d990c4b594bfdbbc8/lessons/week-05/pro-forma-abg-tutorial/video-2-captions.vtt), especially 09:15–13:22: one-at-a-time operating assumptions, full statement reruns, liquidity effects and interactions. The current worksheet governs; wider tutorial scenarios are not added to this assignment.


The current official Lab 11 worksheet was reread after execution on September 29, 2026. The worksheet requires pre-run partner review, unlike the original request to defer every partner note until after computation. The student has now supplied a real pre-run discussion and confirmed the partner agreed on ranges, units and one-input-at-a-time design. The account identifies the **student** as the questioner; it is not rewritten as a question received from the partner. Remaining reciprocal checks are not inferred. The worksheet requests closing AI to write the prediction; no unconfirmed claim about doing so is made.

The existing Amazon-Report `main` was pulled before work. Starting commit: `d3991925d141bb3896f2c0059e4bc43eac14e4c5`. SHA-256 fingerprints of all **27** existing tracked files are in [preservation_manifest.json](preservation_manifest.json). Every prior file remains unchanged. All additions are inside `lab11/`. Lab 10 already contains earlier sensitivity tests; the locked record is a pre-run record for this Lab 11 analysis, not a claim that sensitivity results never existed before.

## Unchanged base

`python -B lab10/amazon_proforma.py` reproduces [base_output.txt](base_output.txt) and the saved Lab 10 output exactly after newline decoding. [base_snapshot.json](base_snapshot.json) contains all 62 independent base inputs, full-precision statement rows and checks. Source labels and reasons remain in [Lab 10 assumptions](../lab10/amazon_assumptions.csv).

| Base metric | Value |
| --- | ---: |
| FY2030 operating income, USD million | 132,404.53 |
| FY2030 FCFE, USD million | 38,251.88 |
| Equity value, USD million | 352,422.75 |
| Value per share, USD | 32.67 |
| Value after FY2030 | 92.11% |
| Shares, millions | 10,786.313572 |
| Equity return / terminal growth | 10% / 2.5% |
| Accounting and liquidity | PASS, all five years |

Base FCFE (USD million) in 2026–2030: **−20,787.84; −42,339.39; −28,972.61; +5,957.06; +38,251.88**. Negative signs are retained in every statement and check.

FCFE = net income + depreciation − operating working-capital investment − net cash capex − other net-asset investment + net term borrowing − finance-lease/facility principal + net revolver borrowing. Sales of the existing securities reserve fund cash but are excluded from FCFE. Valuation retains the original course **positive-only** explicit-flow convention, full-year discounting from December 31, 2025, and fixed shares. The terminal proxy removes temporary revolver movements and new term borrowing. A failed check or nonpositive sustainable terminal FCFE prevents valuation. Nothing in Lab 10 is rewritten.

## Selected operating drivers and exact paths

The student approved the AI-proposed candidates and supplied the ranges and reasons. No ABG endpoints are used. Revenue growth, SG&A/gross profit, residual operating costs, depreciation and inventory days were considered as alternatives; gross margin and post-2026 reinvestment directly address Amazon's profit conversion and uncertain infrastructure-spending taper. Selection is not evidence of universal importance.

| Independent register key | Units | Years | Lower | Base | Higher |
| --- | --- | --- | --- | --- | --- |
| `gross_margin` | Percent of sales (stored as decimal ratios) | 2026; 2027; 2028; 2029; 2030 | 50%; 51%; 52%; 52.5%; 53% | 51%; 52%; 53%; 53.5%; 54% | 52%; 53%; 54%; 54.5%; 55% |
| `capex_later` | USD million, net cash capital spending | 2027; 2028; 2029; 2030 | 207,000; 198,000; 189,000; 180,000 | 230,000; 220,000; 210,000; 200,000 | 253,000; 242,000; 231,000; 220,000 |

Margin changes are **±1 percentage point** in each year (±0.01 in decimal form), not ±1% relative. The relative changes have magnitudes 1.960784%, 1.923077%, 1.886792%, 1.869159%, and 1.851852% respectively. Capex changes are **±10% relative**, or ±23,000 / 22,000 / 21,000 / 20,000 USD million. The separate **2026 capex remains 220,000 USD million**. The executed output prints each path, units, years and signed input differences.

**Student's range evidence:** historical cost-of-sales margins of 46.98%, 48.85%, 50.29% support a meaningful but not extreme one-point test around the forecast. Historical net cash capex of 48,133 / 77,658 / 128,320 USD million supports questioning the timing and size of the spending taper. The endpoint widths are labeled student judgments, not guidance, probabilities or forecasts. [History and exact filing locators](../lab10/amazon_history.csv); [2025 SEC filing, Operations p.37 and Cash Flows p.36](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm).

Gross margin here is calculated as (sales − cost of sales)/sales, not AWS margin or a separately reported Amazon subtotal. The post-2026 capex taper is a judgment. The separate 2026 guidance input remains the dated Lab 10 input, whose secondary-carrier provenance is disclosed in [Lab 10 sources](../lab10/sources.md); it has not been refreshed.

## Genuine locked prediction

Saved at actual UTC time **2026-09-29T21:04:48.155628+00:00**, before execution began at **2026-09-29T21:05:33.216405+00:00**. The [verbatim locked response](locked_prediction.md) retains every prediction and the actual partner discussion. The pre-run record SHA-256 is `d3f6f8b3d8581ca9f373499491bc93de8f0fe38ed29a287e62bb668885758a18`. No backdated timestamp or Git commit is claimed. Reconciliation below supplements rather than replaces the predictions.

## Sensitivity results

Every row reruns the complete five-year model from a fresh independent input copy. Only the named register entry changes; all other assumptions reset to base. Expense ratios remain fixed but their dollar expenses recalculate. Full statements and all 15 annual accounting/liquidity checks are visible in [lab11_output.txt](lab11_output.txt); full precision and inputs are in [sensitivity_results.json](sensitivity_results.json).

All income and FCFE figures and their differences below are **USD million**; value and its difference are **USD/share**. Differences use unrounded changed minus unrounded base; small displayed rounding differences are possible.

### Gross margin

| Case | FY2030 operating income | Δ income | FY2030 FCFE | Δ FCFE | Value/share | Δ value | Checks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| lower | 121,707.43 | -10,697.11 | 15,598.46 | -22,653.42 | 23.87 | -8.81 | PASS: accounting/liquidity |
| base | 132,404.53 | +0.00 | 38,251.88 | +0.00 | 32.67 | +0.00 | PASS: accounting/liquidity |
| higher | 143,101.64 | +10,697.11 | 47,038.38 | +8,786.50 | 40.59 | +7.92 | PASS: accounting/liquidity |

### Post-2026 net cash capex

| Case | FY2030 operating income | Δ income | FY2030 FCFE | Δ FCFE | Value/share | Δ value | Checks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| lower | 141,318.25 | +8,913.71 | 57,815.69 | +19,563.81 | 50.49 | +17.82 | PASS: accounting/liquidity |
| base | 132,404.53 | +0.00 | 38,251.88 | +0.00 | 32.67 | +0.00 | PASS: accounting/liquidity |
| higher **diagnostic only** | 123,490.82 | -8,913.71 | 18,388.73 | -19,863.16 | Unavailable | Unavailable | **INVALID: liquidity FAIL; valuation refused** |

The higher-capex path still satisfies the balance identities, but this does not establish solvency. FY2028 cash is **1,309.67** against a **25,000** minimum, a **−23,690.33** headroom, with the **15,000** revolver fully drawn and securities exhausted. FY2029 cash becomes **−13,569.92**, and FY2030 remains below the cash minimum at **4,818.81**. Its later arithmetic includes effects of an infeasible cash balance, so all final-year amounts are diagnostics only. No extra debt is introduced to rescue the case; no price is forced.

## Output spans and qualified comparison

Spans are maximum minus minimum among **usable** lower/base/higher results, including base. Failed higher capex is excluded for every output.

| Driver | Operating-income span, USD million | FCFE span, USD million | Value span, USD/share | Valid observations |
| --- | ---: | ---: | ---: | --- |
| gross_margin | 21,394.21 | 31,439.92 | 16.73 | 3/3 |
| capex_later | 8,913.71 | 19,563.81 | 17.82 | 2/3; higher invalid |

**Over these ranges**, gross margin has the larger **observed valid-output span** for operating income and FCFE; capex has the larger observed valid-output span for value per share. This is a comparison of the available valid subsets, **not a complete ranking across both full approved ranges**: the failed capex endpoint is never ranked, and the program marks that driver's full-range ranking ineligible. The higher-capex failure is itself evidence that funding constraints matter. A larger span can reflect a wider tested input range; it does not prove inherent importance. Endpoints carry no probabilities.

## Causal trace: lower gross margin

FY2030 gross margin moves from 54% to 53%, with the approved one-point reduction also applied in 2026–2029. Revenue stays at 1,261,451.11. Gross profit falls **12,614.51**; SG&A falls **1,917.41** because its base ratio of 15.2% applies to lower gross profit. Thus operating income falls **10,697.11**, not the entire gross-profit loss. Depreciation, capex and residual cost ratios remain unchanged.

The higher cost of sales increases FY2030 inventory **1,356.43** and trade payables **3,359.10** relative to base. Their year-to-year movements reduce operating working-capital investment by **148.35**. Net income falls **9,205.17**, reflecting operating profit, **356.59** less interest income, **747.81** additional revolver interest, and **2,596.33** less tax. Operating cash flow therefore falls **9,056.83**.

Earlier shortages exhaust securities and draw the revolver: 11,387.49 in 2028 and another 2,209.10 in 2029. In 2030, FCFE before revolver repayment is **29,195.05**; repayment of **13,596.59** leaves final FCFE of **15,598.46**. Its change is −9,056.83 in operating cash minus 13,596.59 in repayment = **−22,653.42**. FY2030 ending cash is **40,598.46**, equity **786,947.30**, and the balance and cash links pass. FY2029 FCFE is effectively zero within the $1 tolerance; its tiny negative floating-point residue is not an economic negative cash flow.

Value falls from **32.67** to **23.87** per share, a **−8.81** change. The terminal proxy uses **29,195.05** sustainable FCFE, excluding temporary revolver repayment, rather than perpetuating the 15,598.46 reported final-year FCFE. This distinction explains why the percentage drop in final FCFE does not translate directly into the same percentage drop in value.

### Reinvestment cross-check: lower capex

FY2030 spending falls **20,000**, capital AP falls **4,208.23**, and cumulative net PP&E falls **70,300.63**. Opening-PPE depreciation falls **8,913.71**, so operating income rises by that amount. Net income rises **8,477.53**, but depreciation's addback falls **8,913.71**, giving **−436.19** CFO change. Working capital is unchanged. The 20,000 cash investment saving yields **+19,563.81** FCFE and **+17.82/share** course value. It does not create extra modeled sales: investment and revenue are independent in this exercise.

## Prediction reconciliation — AI-assisted arithmetic and explanation

Each cell shows **predicted signed change → actual signed change (actual minus prediction)**. The original estimates remain intact in the lock.

| Case | Operating income, USD million | FCFE, USD million | Value/share, USD |
| --- | ---: | ---: | ---: |
| gross_margin lower | -12,000.00 → -10,697.11 (+1,302.89) | -9,500.00 → -22,653.42 (-13,153.42) | -7.50 → -8.81 (-1.31) |
| gross_margin higher | +12,000.00 → +10,697.11 (-1,302.89) | +9,500.00 → +8,786.50 (-713.50) | +7.50 → +7.92 (+0.42) |
| capex_later lower | +6,000.00 → +8,913.71 (+2,913.71) | +18,000.00 → +19,563.81 (+1,563.81) | +14.00 → +17.82 (+3.82) |
| capex_later higher (invalid diagnostics) | -6,000.00 → -8,913.71 (-2,913.71) | -18,000.00 → -19,863.16 (-1,863.16) | -14.00 → Unavailable; error unavailable |

The valid directions agree with the student's estimates. Margin's operating-income effect is smaller than predicted because SG&A dollars also move. Lower-margin FCFE is much worse than predicted because of accumulated financing needs and final-year revolver repayment; higher-margin FCFE does not carry the same repayment burden, so effects are asymmetric. Lower-capex depreciation savings exceed the predicted 6,000 because they accumulate across asset balances and capital AP; cash interest and taxes also recalculate. The higher-capex price prediction is **not testable as a valid price**: funding fails before valuation. Its diagnostic income/FCFE directions do not make that scenario usable.

The student's expected direct importance of gross margin for operating income is consistent with its larger valid span. The expectation that capex would dominate FCFE is not supported by the observed valid spans, substantially because lower-margin FCFE includes debt repayment. The expectation for capex's value effect is consistent with the available valid-subset span, but the full-range ranking remains unresolved because higher capex fails. These are AI-assisted comparisons, not a substituted personal reflection.

## Restored base and independent validation

Initial and ending assumptions, all five-year rows, all checks, and all valuation fields match **exactly**, including full-precision 32.67314175381166/share and 38,251.882151184334 FY2030 FCFE. Maximum difference is **0**. Tolerance: 0.000001 USD million ($1) for statement amounts and 0.000001 USD/share for price; inputs must be exactly equal.

[validate_lab11.py](validate_lab11.py) independently rebuilds every financial line with [40-digit Decimal arithmetic](independent_reference.py), adapted from Lab 10's separate reference validator. It does not use the production calculation for expected rows. It checks all approved inputs, actual run object isolation, every unchanged assumption, linked recalculation, signs, units, valid spans, refusal gates, rerun reproducibility, output/report agreement and the 27 original hashes. Refusal tests are marked synthetic checks, not additional sensitivity endpoints. [Executed validation log](lab11_validation.txt) gives the final count and status. Automated checks do not certify human review.

## Student conclusion: watch-defer and research priority

The following conclusion and reflections were supplied by the student after reviewing the results:

> My final conclusion is watch-defer.
>
> Amazon’s base modeled value remains $32.67 per share, compared with the previously recorded market price of $249.38. Even the highest valid sensitivity value, $50.49 under lower capex, remains substantially below the market price. In addition, 92.11% of the base valuation comes from value after 2030, while the higher-capex case exhausts available funding and fails the model’s liquidity checks. These results do not provide enough support to initiate a position.
>
> What surprised me most was the severity of the lower-margin effect on FCFE. I predicted a $9,500 million reduction, but FCFE fell by $22,653.42 million. The model’s repayment of $13,596.59 million in revolver borrowing during 2030 explains much of the miss and shows that operating assumptions also affect financing flows. I was also surprised that the higher-capex scenario failed completely instead of merely producing a lower value.
>
> My next research priority is Amazon’s ability to fund its capital-investment program internally. I would investigate the expected timing of the capex slowdown, the amount of incremental operating cash flow produced by that spending, and whether Amazon can avoid depending on revolving credit under a less favorable operating scenario.

The $249.38 comparison is the preserved September 24, 2026 market observation, not a newly retrieved price. Post-2026 capex combines demonstrated model impact with weak forward evidence: its taper remains judgment rather than management guidance. The student retains watch-defer and directs further research toward internal funding and investment cash conversion.

## Actual partner evidence

**Exchange 1:** the student asked the partner, “Why are those ranges reasonable, and how do you know we are changing only one assumption at a time?” The partner initially did not know. The student explained the one-point margin range, 10% post-2026 capex range, and reset of every other independent input. The partner agreed the ranges were reasonable and the cases used percentage and USD-million units with one input changed at a time. The exact account is preserved in [the pre-run lock](locked_prediction.md). The student was the questioner; no partner-originated question or independent verification is inferred.

**Exchange 2 — student-supplied account:**

> I showed my partner the lower-capex case and asked: “Can you recompute the differences from the base case for operating income, FCFE, and value per share? Also confirm that only the 2027–2030 capex path changed.”
>
> We reviewed the following differences:
>
> - FY2030 operating income: $141,318.25 million − $132,404.53 million = +$8,913.72 million
> - FY2030 FCFE: $57,815.69 million − $38,251.88 million = +$19,563.81 million
> - Value per share: $50.49 − $32.67 = +$17.82
>
> We also reviewed the lower-capex path of $207,000 million, $198,000 million, $189,000 million, and $180,000 million for 2027–2030, with units stated in USD millions. Gross margin and the other independent assumptions remained at their base values.
>
> I asked my partner whether anything about the result concerned or surprised them. My partner said no, although I was not completely confident that they had independently checked every part of the analysis.
>
> Because of that uncertainty, I performed my own specific check. I independently subtracted each base result from the lower-capex result and confirmed all three differences. I also checked the case inputs and confirmed that only the 2027–2030 net-cash-capex path changed while the other independent assumptions stayed at their base values.

**Rounding reconciliation:** the student's subtraction of displayed income figures is correct: 141,318.25 − 132,404.53 = **8,913.72**. The model subtracts unrounded figures, 141318.24643612953 − 132404.53372571804 = 8913.712710411492, displayed as **8,913.71**. The 0.01 USD-million difference is rounding, not a model mismatch. Both are labeled correctly here; the original account is not altered. These checks concern the student's own Amazon model, not the partner's separate analysis. The report does not claim the partner independently verified every calculation.

**Exchange 3 — student-supplied account:**

> I explained that gross margin affects profit across Amazon’s entire revenue base and can also change its financing requirements. Capex directly affects FCFE and the terminal cash-flow base, making valuation especially sensitive to the capex assumption. The higher-capex case exhausted available funding and failed liquidity checks, so it correctly produced no valuation.
>
> I asked my partner: “Why did gross margin create the larger valid FCFE span, while capex created the larger valid value-per-share span?”
>
> I answered that gross margin produced the larger observed valid FCFE span because it affected company-wide profitability and revolver activity. Capex produced the larger valid value-per-share span because it directly changed cash flow and FY2030 terminal cash flow. However, this comparison is incomplete because the higher-capex case failed, and the tested ranges were not identical in economic magnitude.
>
> My partner summarized the explanation in simpler terms: gross margin mainly changes how much profit Amazon earns, while capex mainly changes how much cash Amazon has available and therefore has a large effect on its valuation.
>
> Our companies’ most important drivers differ because they have different business models, operating-cost structures, investment requirements, and financing needs. Amazon’s valuation is especially affected by its unusually large capital-spending program, cash conversion, and terminal-year financing requirements. Therefore, a driver that materially affects Amazon may not have the same effect on my partner’s company.

No partner-company identity or company-specific findings were supplied; this cross-company explanation remains general. The later reciprocal exchange below supplies only the partner’s revenue-growth paths. The question and answer above were supplied as the student's own, not attributed to the partner. No attendance or session token is claimed.

### Final reciprocal exchange — supplied and confirmed by the student

**Partner's question:** “Why did your higher-capex case produce no valuation instead of just a lower valuation?”

**Student's response:** “Higher capex exhausted the model’s available funding and caused its liquidity checks to fail. Because the model is designed to refuse valuation whenever a required check fails, it correctly reported no valuation instead of producing an unreliable number.”

**Specific check of the partner's analysis — student's account:**

> For my specific check of my partner’s analysis, my partner showed me a revenue-growth base path of 1%, 2%, and 1% across the three applicable forecast periods. We considered a lower path of 0%, 1%, and 0% and a higher path of 2%, 3%, and 2%.
>
> I independently checked the range by subtracting one percentage point from every base value for the lower case and adding one percentage point to every base value for the higher case:
>
> - Base: 1%, 2%, 1%
> - Lower: 0%, 1%, 0%
> - Higher: 2%, 3%, 2%
>
> I confirmed that the units were percentage growth rates, that the adjustments were percentage-point changes rather than percentage changes, and that every sensitivity endpoint was calculated consistently. I also confirmed that this design changes only the revenue-growth path while the partner’s other independent assumptions remain at their base values. I considered the range reasonable because it tests a consistent one-percentage-point change in each direction without using an extreme or negative growth assumption.

This is the confirmed reciprocal input-range and isolation check, separate from the Amazon self-check in exchange 2. No partner company, calendar forecast years, valuation result, output recomputation or additional partner activity is inferred. The range-reasonableness statement is the student's judgment, not externally verified company evidence. These actual question/response and reciprocal-check details satisfy the previously missing documented completion-floor items. The evidence is the student's explicit account; automated validation checks its inclusion, not attendance or human behavior.

## Limitations

Financing dependence, assumed 2027 debt issuance, securities liquidation and revolver renewal remain. Negative early FCFE remains signed; positive-only valuation omits its economic charge. Heavy terminal dependence persists. Fixed shares, cash replacement of stock compensation, aggregate depreciation, cash-tax approximations, fixed residual balances and omitted strategic investments remain Lab 10 simplifications. The dated market comparison and December 2025 valuation convention are unchanged. Growth does not respond to investment in this one-at-a-time model, and real-world correlations are absent. No endpoint is a forecast probability; an invalid liquidity case cannot support a price or full-range ranking.

## Completion floor and execution

| Requirement | Status |
| --- | --- |
| Two driver tables and visible output | Complete; invalid higher capex clearly flagged |
| Restored-base check | PASS, exact equality |
| Locked prediction reconciled | Complete numerical comparison and student reflection |
| Main-driver explanation | Valid-subset comparison over these ranges; full-range ranking unavailable |
| Actual partner question/response received and partner-analysis check | Complete; final reciprocal exchange supplied by student |
| Student review and final judgment | Complete; student retains watch-defer |
| GitHub checkout files | Report, program, visible output, locked prediction, and validation linked below |

```text
python -B lab11/amazon_sensitivity.py --run-approved
python -B lab11/validate_lab11.py
python -B lab11/validate_lab11.py --submission-ready
```

The default command tests computation; the final command additionally checks that required student-confirmed evidence is documented. The runtime used here is portable Python 3.13.7. The runner prints full output; the saved text is the actual executed stdout.

## AI-use disclosure

**AI-use disclosure:** I used Codex to inspect and extend my existing Amazon pro-forma, construct and debug the one-at-a-time sensitivity analysis, create and run independent validation tests, calculate results, trace mechanisms, and help document this report. I approved the AI-proposed sensitivity drivers, selected the ranges, supplied and recorded my pre-run predictions and reasons, participated in the partner exchanges described above, reviewed the results, and made the final watch-defer judgment. Codex saved my prediction before changed Lab 11 cases ran. My account includes uncertainty about my partner's independent checking; the final reciprocal question/response and input-range check are included as I supplied them. No additional partner activity, verification or attendance is claimed. I remain responsible for the work, judgments, any errors, final interpretation and submission.

## Brightspace checkout links

- [Report](https://github.com/acpienkos/Amazon-Report/blob/main/lab11/lab11.md)
- [Sensitivity program](https://github.com/acpienkos/Amazon-Report/blob/main/lab11/amazon_sensitivity.py)
- [Executed output](https://github.com/acpienkos/Amazon-Report/blob/main/lab11/lab11_output.txt)
- [Locked prediction and reconciliation](https://github.com/acpienkos/Amazon-Report/blob/main/lab11/locked_prediction.md)
- [Validation script](https://github.com/acpienkos/Amazon-Report/blob/main/lab11/validate_lab11.py)
- [Executed validation](https://github.com/acpienkos/Amazon-Report/blob/main/lab11/lab11_validation.txt)
- [Complete Lab 11 folder and supporting artifacts](https://github.com/acpienkos/Amazon-Report/tree/main/lab11)
