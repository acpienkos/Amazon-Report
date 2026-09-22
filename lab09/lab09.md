# Lab 09 — Pro-Forma Build: the Engine and the Known Answer

Educational Use Disclaimer: This analysis was prepared solely for educational purposes as part of Purdue University FIN 43900 coursework. It is a simplified valuation exercise and should not be relied upon for investment, trading, or other financial decisions. Nothing in this report constitutes financial or investment advice.

**ABG TRAINING / VALIDATION ONLY — this is not an Amazon valuation.** Prepared September 22, 2026. The required base case produces **$5,237.34 million of equity value, $291.75 per share, and 79.76% of value after 2030**. Every forecast balance sheet balances and cash stays above $25 million. The deliberate cash-link error stops valuation with the required FY2026E gap of **−$61.4 million**.

## Question and source of the assignment

The official research question is:

> What are five years of a company's statements worth, built from assumptions you can defend, and how do you know the statements are right?

The current [Lab 09 instructions][LAB] require the ABG engine and known-answer/break tests. [Week 5][WEEK] places the company-specific application in Lab 10. This submission continues the Amazon-Report repository after Lab 08, but uses the professor's ABG inputs because that is today's assignment. It adds only `lab09/`.

Materials reviewed: the complete Lab 09, [prework][PRE], [handout][HAND], [tutorial page][TUTORIAL], and the **complete Part 1 caption file**, from the opening disclaimer through the final reproducibility statement at 26:54 [CAPTIONS]. Useful transcript locators are 08:00–13:45 for assumptions, 13:48–17:45 for calculation order, 17:48–20:56 for checks and breaks, and 22:53–25:26 for valuation and terminal-growth restrictions. The course revision checked was `6bcbc3c929de59c547b2e421fe0f4ef2dc5d564f`. The public grading floor is the functioning known-answer engine and rejection of the broken balance sheet; Lab 09 is a 25-or-0 completion checkout. No private grading key or Brightspace content was accessed.

## Reopen the prior work without changing it

`python dcf.py` was executed from the existing repository root. That particular saved file is the **Lab 05 training DCF**, which still returns **$27.4974/share**, not the Amazon Week 3 result. It was not overwritten to hide this difference.

The saved Amazon model is `lab06/dcf.py`. Running that unchanged file reproduces **$5.9930/share**, the centered sensitivity range **$4.0382–$9.0873**, and the separate required fixed-grid range **$6.0937–$14.5950**. Its entire output was checked against `lab06/dcf_output_lab06.txt` after newline normalization. Both runs are recorded in [validation evidence](lab09_validation.txt). All 14 pre-existing tracked files were protected with SHA-256 checks. No earlier file was moved, renamed, or edited; earlier standalone Lab 03–05 folders do not exist in this checkout and were not invented.

## The three judgments that carry ABG's value

1. **Organic revenue growth — 1.8%.** Growth should come from the stores already owned. The tutorial distinguishes modest same-store growth from revenue added by acquisitions. Compounding acquisition-driven growth without also paying for acquisitions would overstate value. The base case assumes a modest improvement over the cited 1.2% same-store figure.
2. **Gross margin — 17.05%.** Holding margin close to the recent level is a choice. It assumes the unusually high vehicle-shortage margins have normalized, rather than extending either the peak or the entire decline forever.
3. **SG&A as a percentage of gross profit — 66.5%, 65.5%, then 64.5%.** This is the key operating recovery judgment. It assumes integration costs initially worsen the ratio, then efficiencies bring it back near recent normal. A lower ratio leaves more of each dollar of gross profit for interest, taxes, and owners. It is not SG&A divided by revenue.

These are the professor's teaching judgments, not newly researched student forecasts. They determine the operating path. The discount rate and terminal-growth judgment then strongly affect what that path is worth.

## Complete input register

All dollar totals are **USD millions**; shares are **millions**; percentages are annual unless noted. `INPUTS` at the top of [proforma.py](proforma.py) is the single model input register. Every entry has a value, one of the four labels, and a reason/source. Derived history ratios use the exact arithmetic below, not the rounded spoken percentages. The separate validation script repeats official inputs only as an independent test oracle, not as a second editable model input source.

| Named assumption | Value | Label | Reason / source |
|---|---:|---|---|
| `growth` | 1.8% each year | judgment | Modest organic improvement; exclude bought growth. |
| `gross_margin` | 17.05% | judgment | Hold normalized recent margin after shortage premiums faded. |
| `sga_ratios` | 66.5%, 65.5%, 64.5%, 64.5%, 64.5% | judgment | Initial integration pressure followed by limited cost recovery. |
| `depreciation_ratio` | 82.4 / 3,070.4 = 2.6836894216% | history | FY2025 depreciation divided by year-end PP&E, then applied to opening forecast PP&E. |
| `impairment` | 120/year | judgment | Keep recurring non-cash franchise write-downs; below recent average rather than zero. |
| `capex` | 250 in 2026 | guidance | Management's 2026 figure as identified in the tutorial. |
| `capex_after_2026` | 250/year, 2027–2030 | judgment | Extend guidance unchanged for the case; higher first-half spending challenges this simplification. |
| `tax_rate` | 25.5% of positive pretax income | judgment | Between the recent average and FY2025 effective rate; no tax benefit on losses in this case. |
| `inventory_days` | 2,135.8 / (17,999.0 − 3,071.7) × 365 = 52.2242468497 days | history | Carry the exact FY2025 inventory/cost-of-sales relationship. |
| `floor_plan_ratio` | 2,027.0 / 2,135.8 = 94.9058900646% | history | Carry the historical inventory funding ratio. |
| `other_wc_ratio` | 0.8% of revenue change | judgment | Small additional non-inventory working-capital investment. |
| `min_cash` | 25 | history | Course's cash-light dealer funding convention; official label retained. |
| `revolver_limit` | 850 | judgment | Finite liquidity safety net rather than unlimited borrowing. |
| `revolver_rate` | 6% | judgment | Assumed borrowing cost on the opening revolver balance. |
| `repayment` | 150/year | judgment | Steady term-debt reduction for the five explicit years; ceases in the terminal formula. |
| `buyback` | 150/year | judgment | Moderate owner distribution within recent experience, separate from FCFE. |
| `floor_plan_rate` | 4.67% | history | Tutorial's historical interest/opening floor-plan balance convention. |
| `debt_rate` | 5.44% | history | Tutorial's historical interest/opening term-debt convention. |
| `cost_of_equity` | 10% | judgment | Round base-case required return, not a newly measured beta estimate. |
| `terminal_growth` | 2.5% | judgment | Modest perpetual growth, strictly below the cost of equity. |
| `shares` | 17.951349 | fact | June 30, 2026 10-Q count supplied by Lab 09; fixed denominator, not a forecast of buyback shares. |
| `other_liability_growth` | 0% | judgment | Other liabilities stay flat under the simplified case instruction. |
| `first_year` / `last_year` | 2026 / 2030 | fact | Required five-year horizon; annual end-period cash-flow discounting. |
| `days_per_year` | 365 | fact | Required inventory-days convention. |

**Opening history and supporting ratio inputs**, supplied directly by [Lab 09][LAB]:

| Named input | FY2025 value | Label |
|---|---:|---|
| `revenue` | 17,999.0 | history |
| `gross_profit_2025` | 3,071.7 | history |
| `depreciation_2025` | 82.4 | history |
| `inventory` | 2,135.8 | history |
| `ppe` | 3,070.4 | history |
| `other_assets` | 6,371.6 | history |
| `cash` | 40.4 | history |
| `floor_plan` | 2,027.0 | history |
| `debt` | 3,572.0 | history |
| `other_liabilities` | 2,127.5 | history |
| `equity` | 3,891.7 | history |
| `revolver` | 0.0 | fact — no opening revolver specified in the teaching case |

The supplied opening assets and liabilities plus equity both equal **11,618.2**. The transcript mentions a −0.2 rounding gap in its displayed historical filing column; this implementation uses the exact opening numbers in the current lab, which already balance. It adds no rounding adjustment or hidden cash plug. `TOLERANCE = 0.0000001` million is a numerical checking tolerance, not a valuation assumption. Formatting never changes the unrounded calculations.

## Why cash comes last, and how the statements connect

The code follows this order each year:

1. Revenue, gross profit, SG&A, depreciation, impairment, and operating income.
2. Interest on opening floor-plan, term-debt, and revolver balances; pretax income, tax, and net income.
3. Inventory, floor-plan loans, PP&E, other assets, term debt, other liabilities, and equity, leaving cash unfilled.
4. FCFE from earnings, non-cash charges, investment, working-capital changes, inventory financing, and term-debt repayment.
5. Owner distributions and any revolver draw/repayment; then ending cash from the cash-flow roll-forward.

Cash is the **result** of the income statement, balance-sheet movements, financing, investment, and distributions. It should expose an omitted flow or broken link. Solving cash as the amount needed to force assets to equal liabilities plus equity would hide the error being tested.

For FY2026, rounded for explanation:

```text
FCFE = 413.6 + 82.4 + 120.0 - 250.0 - 38.9 - 2.6 + 36.9 - 150.0
     = 211.4 million
Ending cash = 40.4 + 211.4 - 150.0 = 101.8 million
```

The model uses unrounded values, so rounded display rows need not sum perfectly in every year. Impairment reduces net income and other assets but is added back as non-cash in FCFE. Depreciation reduces PP&E and earnings, then is added back to cash flow. Buybacks reduce equity and cash **after FCFE**; subtracting them inside FCFE and again in the cash roll-forward would double-count the distribution.

## Floor-plan financing in plain language

A dealer borrows from manufacturers' finance arms or banks to fund vehicles held for sale. The vehicles provide collateral. More inventory requires more financing; when the inventory loan is repaid, cash goes out. This model treats that financing consistently in three places: opening floor-plan loans generate interest, closing loans equal inventory times the historical funding ratio, and the change in loans enters operating cash flow and FCFE.

In FY2026, inventory grows by about $38.9 million and floor-plan funding grows by $36.9 million. The dealer therefore does not fund the entire inventory increase out of its own cash. The independent omission test sets the future funding ratio to zero, which requires repaying the **$2,027 million opening loan**. Even drawing the full **$850 million revolver** leaves FY2026 cash at **−$1,112.0 million**. The balance sheet still ties, but the cash-floor check correctly refuses valuation. This is why a balance check alone is insufficient. This extra test is a teaching diagnostic, not an alternative investment recommendation.

## Known-answer validation

All official checkpoint displays match. Full statements with years across appear in [executed output](lab09_output.txt).

| Checkpoint | FY2026 official | FY2026 actual | FY2030 official | FY2030 actual |
|---|---:|---:|---:|---:|
| Revenue | 18,323.0 | 18,323.0 | 19,678.3 | 19,678.3 |
| Operating income | 844.2 | 844.2 | 971.4 | 971.4 |
| Net income | 413.6 | 413.6 | 527.5 | 527.5 |
| FCFE | 211.4 | 211.4 | 342.3 | 342.3 |
| Ending cash | 101.8 | 101.8 | 719.8 | 719.8 |
| Assets − liabilities − equity | 0.0 | 0.0 | 0.0 | 0.0 |

| Every-year check | 2026 | 2027 | 2028 | 2029 | 2030 |
|---|---:|---:|---:|---:|---:|
| Balance gap, USD m | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Cash-flow linkage gap, USD m | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| PP&E roll-forward gap, USD m | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Debt roll-forward gap, USD m | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Cash above $25m floor, USD m | 76.8 | 181.9 | 331.6 | 502.5 | 694.8 |
| Status | PASS | PASS | PASS | PASS | PASS |

`assert_balanced` recomputes gaps from the actual lines and raises an error naming the year, failed check, and gap. `value_equity` calls it before discounting anything. It also rejects a terminal growth rate at or above the cost of equity. Tests independently reconstruct the base case with 40-digit Decimal arithmetic and independently sum assets and claims; they do not just ask the model whether it thinks it passed.

## Required break, refusal, and restoration

Executed `python -B lab09/proforma.py --break-cash`. The flag temporarily changes **only the FY2026 balance-sheet cash line** from its computed result to opening cash of 40.4. The cash-flow calculation stays intact, making this a controlled broken-link test rather than a new forecast. The program returned exit code **1**, with:

```text
ERROR: FY2026E balance_gap = -61.4 million; valuation refused
```

The balance and cash-link gaps both become **−61.4**, because `40.4 − 101.8 = −61.4` at the displayed precision. Assets are short by exactly the year's omitted cash increase. Cash still exceeds the minimum, so the balance/link check, not the floor, identifies this particular error. No valuation section or value per share is printed in the failed run.

The override was then removed by running the normal command again. All checks passed and **$291.75** returned. The validation script captures both actual process runs, checks their exit codes, confirms the error text, and verifies the source file is unchanged. This reversible runtime override performs the requested replacement and undo without leaving broken code in the submitted file. It was performed by AI on this model; no partner swap is claimed.

## Equity valuation and what 80% means

The five unrounded annual FCFE amounts are discounted at 10%. Terminal cash flow adds back the final $150 million repayment because the case does not assume that annual deleveraging continues forever:

```text
TV at end of 2030 = (FCFE_2030 + repayment_2030) × (1 + 2.5%) / (10% - 2.5%)
Equity value = sum(FCFE_t / 1.10^t, t = 1..5) + TV / 1.10^5
Value/share = equity value / 17.951349 million shares
```

| Output | Executed result |
|---|---:|
| PV of five explicit FCFE | $1,059.87 million |
| Terminal cash flow, 2031 | $504.59 million |
| Terminal value at end of 2030 | $6,727.85 million |
| PV of terminal value | $4,177.46 million |
| Equity value | **$5,237.34 million** |
| PV terminal / equity value | **79.76%**, or approximately 79.8% |
| Value per share | **$291.75** |

This is an equity cash-flow valuation, so there is no second cash/debt bridge. The fixed June 2026 share count and FY2025 opening sheet follow the frozen teaching instructions; this is not presented as a fresh market valuation. About four-fifths of the result comes from cash flows after the explicit forecast. That makes the terminal growth, required return, repayment convention, and sustainable operating assumptions important. Matching the known answer proves implementation, not that the assumptions predict the future. No buy/sell recommendation or invented sensitivity range is attached to the training answer.

## Run commands, review, and disclosure

From the repository root, with Python available:

```text
python -B dcf.py
python -B lab06/dcf.py
python -B lab09/proforma.py
python -B lab09/validate_lab09.py
```

The working executable used here was `C:\Users\acpie\AppData\Local\Temp\fin439-python-3.13.7\python.exe` (Python 3.13.7). Both new scripts use only the standard library. `validate_lab09.py` exits nonzero on any failed check and invokes the break/restore commands itself. **All 158 checks passed.** The only expected nonzero model run is the deliberately broken subprocess, which the validator confirms was refused.

Final review against the current official instructions:

| Requirement | Evidence / status |
|---|---|
| Correct case, research question, and three judgments | ABG identified as training; question and operating reasoning above. |
| Complete labeled assumptions in one place | `INPUTS`; exact history ratios; every judgment has a reason, including the guidance extension. |
| Required calculation order and cash last | `project`; FCFE/cash walkthrough; no balancing plug. |
| Consistent floor-plan financing | Interest, debt balance, operating cash flow/FCFE; omission test also executed. |
| Three readable statements and every-year checks | `lab09_output.txt`; all five forecast years, one-decimal statements. |
| Refusal before valuation | `assert_balanced` inside `value_equity`; broken CLI exits 1 without value. |
| Known answers and terminal formula | All endpoint, handout, balance, minimum-cash, and valuation tests passed. |
| Required break and undo | FY2026 −61.4 error, no valuation, followed by normal $291.75 run. |
| Prior work preserved | All pre-existing files hashed and unchanged; root training and saved Amazon DCF both rerun. |
| Honest process disclosure | No unverified attendance, partner exchange, or session token claimed. |

**AI-use disclosure:** Codex read the official materials and full captions, wrote the model and independent tests, drafted this report, executed the runs, and checked the files. The explanations are AI-assisted coursework for student review, not a claim of unaided authorship. Reading captions is not a claim that the student watched the video. The required personal explanation, partner exchange, swap-and-break exercise with an actual partner, and any in-class checkout remain student activities; none is certified here.

**Individual checkout:** use the five GitHub file links in `lab09/` when the instructor directs the Brightspace attempt. Review the three judgments, explain why cash is last, and be able to identify −61.4 as the omitted cash increase. Follow any private Brightspace requirements. No attendance or session token was supplied or invented, and no Brightspace submission was made. For Lab 10, bring Amazon's three most recent 10-Ks and identify its company-specific modeling issue; that future assignment is outside this ABG build.

[LAB]: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-05/lab-09-proforma-build.md
[WEEK]: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-05/README.md
[PRE]: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-05/student-prework.md
[HAND]: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-05/student-handout.md
[TUTORIAL]: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-05/pro-forma-abg-tutorial.md
[CAPTIONS]: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-05/pro-forma-abg-tutorial/video-1-captions.vtt
