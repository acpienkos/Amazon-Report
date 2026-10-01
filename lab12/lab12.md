# Lab 12 — Amazon: present and review my full analysis

**My conclusion remains watch-defer.** My existing model does not yet establish that Amazon's investment program will generate enough sustainable cash for shareholders. The next research priority remains internal funding of capital investment and the operating cash flow that investment produces.

This is a written learning-partner review under the instructor clarification supplied by me: my partner may be my AI partner. “Partner” identifies that permitted role throughout this exchange. My answers below are drafted from my existing analysis, not a transcript of new spoken answers. The [current worksheet](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-06/lab-12-proforma-present.md) was read in full. Its classroom instructions describe reciprocal company presentations; this permitted adaptation contains both presenter and reviewer work on the available Amazon evidence, including my questions back to Partner. There is no separate Partner-owned company analysis in the supplied evidence. No second-company presentation, human classmate exchange, attendance, elapsed classroom time, or session token is claimed.

## Stop 1 — Target selection

I selected Amazon because it gives me a concrete question to investigate: can a growing retail and cloud business convert its large infrastructure investment into cash that supports its price? Its public filings, distinct operating segments, and capital-intensive growth make it suitable for tracing evidence into a forecast. **Partner's interpretation:** this selection rationale reconstructs the economic motivation in my [company report](../Amazon_2026-09-03_report.md); the repository does not contain a separate original selection diary proving why I first chose the ticker.

My initial documented view was already watch-defer. I liked the operating progress, especially AWS, but questioned the return on investment. I now understand that stronger operating income alone does not answer that question: funding, depreciation, capital spending, and terminal cash flow also matter. I have become more specific about what would change my mind, rather than changing the call simply because one method produces a higher value.

## Stop 2 — Company and evidence

Amazon earns money from products it sells itself, third-party seller and fulfillment services, AWS cloud services, advertising, subscriptions, and digital content. North America, International, and AWS are its reported segments. Retail scale, seller activity, delivery efficiency, cloud customer usage, service mix, and infrastructure utilization are company-specific drivers; consolidated sales growth alone cannot distinguish them. The [company report](../Amazon_2026-09-03_report.md) and [peer research](../lab08/lab08.md) cite the annual filing's business description and segment note.

The most useful historical contrast is FY2025 revenue of **$716,924 million**, consolidated operating income of **$79,975 million**, and AWS operating income of **$45,606 million**, against net cash capex of **$128,320 million** and reported free cash flow of **$11,194 million**. These are fiscal-year figures, not a quarterly run rate. AWS revenue was **$128,725 million**. The source is the [FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm): Operations p.37, Cash Flows p.36, MD&A pp.23–27 and pp.29–30, and segment information. I use the existing source transcriptions; this review's new evidence check is a calculation, not a fresh audit of every filing.

| Historical evidence, USD million except margins | FY2023 | FY2024 | FY2025 |
| --- | ---: | ---: | ---: |
| Revenue | 574,785 | 637,959 | 716,924 |
| Calculated gross margin | 46.98% | 48.85% | 50.29% |
| Gross cash PP&E purchases | 52,729 | 82,999 | 131,819 |
| PP&E proceeds/incentives | 4,596 | 5,341 | 3,499 |
| Net cash capex | 48,133 | 77,658 | 128,320 |

The [history CSV](../lab10/amazon_history.csv) identifies each own-year filing, statement, period, unit, and calculation; [sources](../lab10/sources.md) records definitions and comparative checks. Gross margin means sales less cost of sales divided by sales, not an Amazon-reported subtotal or AWS margin. Net capex subtracts proceeds/incentives from gross cash purchases; it is not total asset additions. The provider's CapEx row matched this net definition in the saved source comparison. Reported and constant-currency growth are not automatically organic growth: a true consolidated organic/same-store percentage was not disclosed in the reviewed history.

The [June 2026 10-Q](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000026/amzn-20260630.htm) supports the later share count, observed financing, and interim operating evidence. The **$220,000 million FY2026 cash-capex input** is the dated guidance recorded in the [assumption register](../lab10/amazon_assumptions.csv), carried by a management-call transcript and cross-checked with AP in the source register. That is secondary-carrier provenance, not an annual-filing forecast. The later taper is my scenario judgment, not management guidance. The saved Stock Analysis observation supplies the market comparison; none of these dated observations is represented as refreshed today.

## Stop 3 — My pro-forma

I start from the audited FY2025 balances and build FY2026–FY2030 statements in [the existing model](../lab10/amazon_proforma.py). The root DCF is training work; [Lab 09](../lab09/lab09.md) is the ABG engine exercise, not Amazon evidence. My Amazon forecast is in Labs 10–11. The [assumption register](../lab10/amazon_assumptions.csv) separates history, facts, guidance, and judgments, and the [executed base](../lab11/base_output.txt) shows the linked statements.

| Forecast assumption | FY2026 | FY2027 | FY2028 | FY2029 | FY2030 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Sales growth, judgment | 16% | 14% | 12% | 10% | 8% |
| Gross margin, judgment | 51% | 52% | 53% | 53.5% | 54% |
| SG&A / gross profit, judgment | 16% | 15.8% | 15.6% | 15.4% | 15.2% |
| Net cash capex, USD million | 220,000 | 230,000 | 220,000 | 210,000 | 200,000 |

Growth fades as the business scales; better service/AWS mix supports the margin hypothesis; modest scale efficiencies reduce SG&A relative to gross profit. These are educated forecasts, not measured future outcomes. Historical inventory and operating-balance ratios are carried forward as judgments. Depreciation is **15% of opening net PP&E**, supported as a rough scenario by the saved interim evidence, not an equipment-vintage model; tax is **22%**, a provision-as-cash-tax approximation. See [Lab 10's rationale](../lab10/lab10.md).

Sales and margins determine gross profit; SG&A, residual operating costs, depreciation, and lease expense determine operating income. Interest and tax determine net income. Sales and cost of sales drive operating working capital. PP&E rolls forward using net cash capex, changes in capital payables, and noncash financed additions, less depreciation. Capital payables stay outside operating working capital. Equity rolls forward from retained income; cash is opening cash plus operating, investing, and financing flows, never a balance-sheet plug.

FCFE equals net income plus depreciation, less operating working-capital investment, net cash capex and other net-asset investment, plus net term borrowing, less finance-lease/facility principal, plus net revolver borrowing. Sales of the existing securities reserve support cash but are excluded from FCFE. Financing is explicit: **$25,000 million** additional net term borrowing in FY2027 is assumed; the cash floor is **$25,000 million** and revolver limit **$15,000 million**, with renewal beyond its November 2028 term assumed. The base needs securities sales and term financing but no revolver draw. It therefore does not demonstrate internal self-funding.

Before valuation, every opening balance must match the previous close; assets must equal liabilities plus equity; cash, FCFE, securities, PP&E, capital payables, debt, leases, equity, and revolver roll-forwards must reconcile. Asset and financing balances must be finite and nonnegative, cash must meet its floor, and revolver use must stay within its limit. Tolerance is **$0.000001 million ($1)**. The [saved validation](../lab11/lab11_validation.txt) also tests refusal when a required check fails. Accounting balance does not imply available funding.

## Stop 4 — Valuation

My current **$32.67 per share** is in **USD**, valued at **December 31, 2025** with five full year-end cash flows through FY2030, using information recorded September 24, 2026. It is not a September stub-period valuation. The fixed denominator is **10,786.313572 million common shares**, the **July 22, 2026** cover-page count, not a diluted weighted-average EPS denominator. The nominal equity return is **10%** and perpetual growth **2.5%**, both judgments. This is an equity FCFE DCF, so I do **not** add cash and subtract debt again; financing already enters the cash flows, and no separate opening excess-cash or strategic-investment value is added. [Valuation conventions and output](../lab10/lab10.md).

| Base valuation component | Existing result |
| --- | ---: |
| FY2030 operating income, USD million | 132,404.53 |
| FY2030 FCFE / sustainable terminal proxy, USD million | 38,251.88 |
| PV of positive explicit FCFE, USD million | 27,820.16 |
| Terminal value at year-end FY2030, USD million | 522,775.72 |
| PV of terminal value, USD million | 324,602.59 |
| Equity value, USD million | 352,422.75 |
| Value after FY2030 | 92.11% |

The terminal formula is sustainable terminal-year FCFE times one plus terminal growth, divided by equity return less terminal growth, then discounted back over the forecast horizon. Temporary revolver movements and new term borrowing are removed from the terminal proxy. The proxy must be positive and the discount rate must exceed growth. Those conditions permit the calculation but do not prove a sustainable steady state.

Base signed FCFE for FY2026–FY2030 is **−20,787.84; −42,339.39; −28,972.61; +5,957.06; +38,251.88 USD million**. The course's positive-only explicit valuation omits **$75,656.81 million** of discounted negative flows, while statements and liquidity checks retain them. This is a material limitation, not a complete signed-flow intrinsic valuation. The [saved market price](../lab10/sources.md) is **$249.38 per share on September 24, 2026, 16:00 EDT**, a regular-session close. Both the different date and the model convention limit that comparison. The price is not live.

My earlier [Lab 06 FCFF DCF](../lab06/lab06.md), dated **September 10, 2026**, gave **$5.9930 per diluted share**, in USD. It used starting FY2025 FCFF **$8,846.82 million**, growth **−50%, +50%, +40%, +25%, +15%**, estimated WACC **11.80145113%**, and terminal growth **3%**. Five forward annual periods were discounted from that valuation date. Unlike the FCFE model, it required an enterprise-to-equity bridge: **$120,448.4515 million EV + $78,213 million cash − $133,320 million debt = $65,341.4515 million equity**, divided by **10,903 million Q2 2026 diluted weighted-average shares**. Cash/debt were the June 30, 2026 inputs. This preserves the older gross-capex, simplified FCFF scenario rather than quietly substituting the later FCFE assumptions.

The older WACC combines a Treasury risk-free rate, vendor beta and assumed equity premium with an after-tax issue-yield debt-cost proxy, using estimated market capital weights. Its bridge assumes the included cash is excess, uses debt face value, and does not separately value strategic investments or fully recast leases. These dated approximations differ from the current model's judgmental required equity return; the two rates are not interchangeable. [Component sources and bridge limits](../lab06/lab06.md).

The existing [reverse DCF output](../lab06/dcf_output_lab06.txt) targets **$252.13**, the **September 10, 2026, 16:26 EDT after-hours** quote. A uniform growth-rate shift of **−5 to +10 percentage points** found **no solution in bracket**. The explicitly wider **−5 to +150 percentage-point** experiment solved at **+96.978684 percentage points**, implying annual FCFF growth **46.978684%, 146.978684%, 136.978684%, 121.978684%, 111.978684%**. Held fixed were the starting FCFF, WACC, terminal growth, cash, debt, shares, five year-end flows, and terminal discount horizon just stated; WACC weights were not recalculated. This is conditional arithmetic under extreme growth, not evidence those outcomes are feasible. It is not a reverse DCF for the newer saved market price or the current pro-forma; that remains an unresolved extension.

The actual Amazon peers are **Walmart and Microsoft**, qualified partial matches in [Lab 08](../lab08/lab08.md). Walmart represents retail/distribution and membership; Microsoft represents cloud infrastructure and enterprise ecosystems. Neither replicates Amazon's combined economics. The [Lab 07](../lab07/lab07.md) dealership exercise is training, not an Amazon peer set.

| Peer comparison: September 10, 2026 closes, USD/share | Price | Annual GAAP diluted EPS | Earnings period end | P/E |
| --- | ---: | ---: | --- | ---: |
| Walmart | 105.73 | 2.73 | January 31, 2026 | 38.728938× |
| Microsoft | 492.44 | 17.95 | June 30, 2026 | 27.433983× |
| Amazon target | 251.89 | 7.17 | December 31, 2025 | 35.131102× |

Applying the peer multiples to Amazon's annual diluted EPS gives **$196.70–$277.69 per share**, with **$237.19** median-implied value; removing either peer moves the midpoint **17.07%**. These are USD equity-per-share references with contemporary split bases, not enterprise values; no cash/debt bridge applies. The annual earnings periods differ and investment gains affect recurring earnings quality. [Sources, qualification decisions and executed arithmetic](../lab08/lab08.md); [output](../lab08/lab08_output.txt).

The methods disagree because P/E capitalizes accounting earnings and embedded market expectations, whereas DCF charges the chosen investment path against cash flow. Capex reduces cash immediately but reaches earnings through depreciation; investment gains can also raise EPS without operating cash generation. The newer pro-forma additionally changes margins, financing, net-versus-gross capex, discounting, shares, and the treatment of negative flows. Averaging the methods would conceal these differences without evidence-based weights. A peer range containing a market quote does not validate my cash-flow forecast.

## Stop 5 — Sensitivity and drivers

The [locked prediction](../lab11/locked_prediction.md) remains intact. The existing run changes one independent assumption path at a time and restores every other input. Margin is tested at **±1 percentage point**, not a relative percent; post-FY2026 net cash capex is tested at **±10% relative**. FY2026 capex stays **$220,000 million**. The widths are judgments, not confidence intervals. [Approved ranges](../lab11/approved_ranges.json).

| Input path | Lower | Base | Higher |
| --- | --- | --- | --- |
| Gross margin, FY2026–FY2030 | 50%; 51%; 52%; 52.5%; 53% | 51%; 52%; 53%; 53.5%; 54% | 52%; 53%; 54%; 54.5%; 55% |
| Net capex, FY2027–FY2030, USD million | 207,000; 198,000; 189,000; 180,000 | 230,000; 220,000; 210,000; 200,000 | 253,000; 242,000; 231,000; 220,000 |

| Case | FY2030 operating income, USD million | FY2030 FCFE, USD million | USD/share | Status |
| --- | ---: | ---: | ---: | --- |
| Base | 132,404.53 | 38,251.88 | 32.67 | Valid |
| Lower gross margin | 121,707.43 | 15,598.46 | 23.87 | Valid |
| Higher gross margin | 143,101.64 | 47,038.38 | 40.59 | Valid |
| Lower capex | 141,318.25 | 57,815.69 | 50.49 | Valid |
| Higher capex | 123,490.82 | 18,388.73 | Unavailable | Invalid; statement amounts are diagnostics only |

All prices use the same December 31, 2025 valuation convention, USD currency, and fixed common-share basis stated above. The valid sensitivity values span **$23.87–$50.49**. [Saved full-precision results](../lab11/sensitivity_results.json) and [executed statements/checks](../lab11/lab11_output.txt) support the table.

Lower margin reduces gross profit, partly offset by lower SG&A dollars. It also changes inventory/payables, tax, interest income, and borrowing. In the lower-margin case, FY2030 FCFE before revolver repayment is **$29,195.05 million**; repayment of **$13,596.59 million** leaves **$15,598.46 million**. The terminal proxy removes that temporary repayment. This explains why the final-year FCFE decline is not proportional to the value decline. My locked estimate of a **$9,500 million** FCFE reduction missed the actual **$22,653.42 million** reduction, largely because financing responded. [Causal trace and prediction reconciliation](../lab11/lab11.md).

Lower capex reduces PP&E and later depreciation, increasing operating income. Lower depreciation also reduces its cash-flow addback; tax and interest effects recalculate, so operating cash flow need not rise. The direct spending saving dominates FCFE in the tested lower-capex case. The model holds revenue growth fixed: it does not prove that Amazon could cut investment without losing future sales. The calculation check below traces this mechanism using unrounded results.

Higher capex exhausts the securities reserve and available revolver funding. FY2028 cash is **$1,309.67 million**, below the **$25,000 million** floor; cash headroom is **−$23,690.33 million**, with the **$15,000 million** revolver fully drawn. The balance identities can still reconcile, but the funding plan fails. Consequently **higher capex has no valuation**. Its later statement amounts are infeasible-path diagnostics, excluded from valid ranges and rankings; they are not rescued with invented borrowing. [Failure evidence](../lab11/lab11.md).

| Observed valid-output span | Gross margin | Post-FY2026 capex |
| --- | ---: | ---: |
| FY2030 operating income, USD million | 21,394.21 | 8,913.71 |
| FY2030 FCFE, USD million | 31,439.92 | 19,563.81 |
| Value/share, USD | 16.73 | 17.82 |

**Over these tested ranges**, gross margin has the larger valid operating-income and FCFE span, while capex has the larger valid value span. This compares available valid subsets: the failed capex endpoint prevents a full-range ranking. Different widths and units can change the ranking. **Impact** is the modeled change conditional on a specified input change; **uncertainty** is how poorly I know the input, its probability, persistence, or correlations. A large impact does not establish high uncertainty, and these endpoints carry no probabilities. **Partner's interpretation:** capex remains the main research driver because its taper is weakly evidenced and its adverse endpoint exposes a funding boundary, not because it wins every output ranking.

## Stop 6 — Interpretation

I keep **watch-defer**. The model and valid sensitivities do not support initiating a position at the saved price, but the limitations also prevent me from declaring a precise intrinsic value or treating the gap as proof the market is wrong. The earlier concern about AWS investment returns now has a specific financing mechanism behind it.

Evidence that could change my view would be a defensible investment timetable, sustained operating cash conversion after cash capex and recurring financing principal, and a credible funding plan under weaker operating conditions. I would track operating cash flow less net cash PP&E purchases and finance-lease/facility principal alongside new borrowing and securities sales, checking whether improvement is recurring rather than working-capital timing or delayed investment. I would then reassess the terminal cash-flow assumption and value on a consistent date. This is a proposed research test, not a claim that those checks or a model repair have already been completed.

The largest limitation is the uncertain connection between investment, sustainable cash generation, and financing. Heavy terminal dependence amplifies it. Fixed shares with cash replacement of stock compensation, aggregate depreciation, tax approximations, omitted strategic investments, and fixed residual balances further limit the model. Passing accounting checks establishes internal consistency, not forecast accuracy. [Existing limitations](../lab10/lab10.md).

## Reciprocal written review

### Selection and evidence

**Partner:** Why choose Amazon if AWS profitability does not establish investment returns, and which evidence supports that distinction?

**My evidence-based answer:** My company report already pairs improved AWS/consolidated operating income with rising cash capex and weaker reported free cash flow. The annual filing locators and history register above support that contrast. It makes Amazon useful to analyze, but does not prove project returns. The specific unresolved gap is a reliable link from infrastructure additions and utilization to incremental operating cash flow; I need segment investment/returns evidence, not just another consolidated growth figure.

**My question back to Partner:** Does that justify saying AWS is the main valuation driver?

**Partner:** **Partner's interpretation:** AWS is an important operating hypothesis in the company report. The consolidated sensitivity does not isolate an AWS valuation contribution. Keep that distinction and call capex/cash conversion the research priority, with gross margin the stronger observed driver of final operating income and FCFE over the tested valid ranges.

### Model and valuation

**Partner:** If the base passes its liquidity checks, has the model demonstrated internal funding, and can the peer midpoint resolve the DCF gap?

**My evidence-based answer:** No. The base uses assumed term issuance and securities liquidation. The course valuation also omits negative explicit flows and depends heavily on terminal value. The peers price different earnings streams and periods, so averaging does not fix the financing or cash-conversion assumptions. A common-date, sustainable signed-flow assessment remains unresolved; I have not run that repair here.

**Partner follow-up:** What supports the later capex taper and continued financing access?

**My evidence-based answer:** The assumption register labels the taper and future borrowing as judgments. Historical investment growth and observed financing give context, but no cited evidence establishes the full future path or guarantees refinancing. I need updated capital-spending evidence, maturities/facility availability, and cash-generation evidence before claiming that path is feasible beyond the conditional scenario.

### Sensitivity and interpretation

**Partner:** Would capex still rank first if the input widths changed, and what does the invalid higher-capex endpoint tell you?

**My evidence-based answer:** The existing runs cannot answer another set of widths. Capex leads only the observed valid price span here; gross margin leads the valid operating-income and FCFE spans. Higher capex tells me the stated funding policy is insufficient under that path. It supplies no price and no complete capex range. I should research both spending uncertainty and available funding rather than treat sensitivity as a probability forecast.

**My question back to Partner:** Why did the lower-margin case undermine my expected FCFE ranking?

**Partner:** The existing trace shows that the margin change affects financing as well as profit. Final-year revolver repayment magnifies the reported FCFE decline, while the terminal proxy excludes that temporary repayment. **Partner's interpretation:** this is the question that causes reconsideration of the simple claim that capex must dominate every cash-flow measure.

### Evidence check performed for this review

**My review question:** Can Partner trace the approved lower-capex input through the statement effects, FCFE, and value without relying only on the rounded comparison table?

**Partner:** I opened the existing input register, approved paths, model code, and saved full-precision results. The new [validation script](validate_lab12.py) reruns the unchanged model in memory and independently recomputes the following links; it does not save new sensitivity results over the old ones.

For the FY2030 lower-capex case, net cash capex changes **$200,000 → $180,000 million**. Across the approved path, accumulated lower PP&E reduces FY2030 depreciation by **$8,913.71 million**, so operating income rises by **$8,913.71 million**. The recomputed net-income change is **+$8,477.53 million**, depreciation addback change **−$8,913.71 million**, and operating working-capital change is unchanged. Therefore CFO changes **−$436.19 million**. The cash investment saving **$20,000 million** produces an FCFE increase of **$19,563.81 million**, from **$38,251.88 to $57,815.69 million**. Discounting the permitted positive explicit flows and sustainable terminal proxy reproduces **$32.67 → $50.49 per share**, a **+$17.82** change. All amounts use full precision until display, so subtracting rounded cells can differ in the last displayed decimal.

**Result: supported.** The unchanged revenue path is also verified. This proves the internal arithmetic of the conditional case; it does not establish that lower investment would preserve real-world revenue or that its terminal cash flow is sustainable. The [passing log](lab12_validation.txt) records the actual execution. This is a Partner-performed computational check within our written exchange, not a claim that I separately performed an unaided manual calculation.

### Partner explains back; my response

**Partner — conclusion:** You retain watch-defer because the available modeled values and funding limitations do not support initiation, while the scenario's limitations prevent a precise fair-value claim.

**Partner — main driver:** Your research driver is the capex-to-cash-conversion path and its funding. Margin has the stronger valid final-income and FCFE span; capex has the stronger valid price span over the selected ranges. These are different statements.

**Partner — largest limitation:** The model does not establish sustainable post-forecast cash generation from its investment program; terminal dependence, financing assumptions, and positive-only valuation make that unresolved link consequential. **Partner's interpretation:** this is the central economic limitation, even though the calculations reconcile.

**My response:** That explanation matches my saved conclusion. I would correct any shorthand that says “capex is always the biggest driver” or “the base is internally funded.” Neither is supported by these runs.

**Partner — evidence-backed strength:** Your higher-capex case is allowed to fail. The visible cash-floor failure and valuation refusal prevent a balanced but unfunded forecast from becoming a misleading price. The preserved input paths and restored base make the comparison auditable.

**Partner — actionable improvement:** Build an evidence-led funding and reinvestment reconciliation next: separate operating cash generation, net cash capex, recurring financing principal, new debt, and reserve liquidation; tie the spending taper to current disclosures and infrastructure utilization evidence. Then assess whether a sustainable terminal case survives weaker cash conversion. This is a proposed next investigation, not a new valuation model claimed as completed here.

**My reviewer response to Partner:** I accept the improvement because it directly addresses the observed funding dependence. I would challenge any stronger assertion that investment can fall without affecting growth: our fixed-growth sensitivity does not test that. Partner's interpretation is useful as a scoped research judgment, not new numerical evidence. There is no independent Partner-company model to review, so no findings about another company are invented.

## What I keep, revise, and investigate

- **Keep:** watch-defer, the source-linked assumptions, signed cash-flow statements, explicit financing, and refusal gates. They preserve the distinction between consistent arithmetic and a defensible investment conclusion.
- **Revise:** my explanation of the main driver. State the output being ranked and the tested range, qualify the incomplete capex range, distinguish AWS operating importance from an isolated valuation contribution, and keep valuation dates/share bases beside the values. These explanatory revisions are made in this note; prior files and model assumptions are unchanged.
- **Investigate:** internal funding and incremental operating cash generated by investment, especially the evidence for the capex taper, financing availability, and sustainable terminal cash flow. A common-date signed-flow assessment and a current-model reverse DCF remain future work.

**Question that caused reconsideration:** “If the base passes its liquidity checks, has the model demonstrated internal funding?” My answer is no: passing with financing is different from funding investment out of operations. **Partner's interpretation:** this sharpens the next research question without supplying new evidence that would reverse the decision.

**Effect on conclusion and priority:** neither changes. The review supports watch-defer and the same internal-funding/cash-conversion priority because it verifies the conditional arithmetic while identifying unresolved economic assumptions. It does not supply the missing evidence needed to initiate.

## Validation, preservation, and checkout

The [validation script](validate_lab12.py), [executed log](lab12_validation.txt), [audit manifest](audit_manifest.json), and [publication check record](publication_checks.json) check the content, numerical evidence, calculation trace, prior-file hashes, and publication URLs. Run `python -B lab12/validate_lab12.py --published --write-log` from the repository root to reproduce the full check (Python standard library and Windows PowerShell; live GitHub access required). Automated checks establish artifact coverage and reproducibility; they do not certify truth of forecasts, personal understanding, attendance, or instructor grading. Narrative attribution and limitations were reviewed by Partner; unsupported original selection history and the absence of a separate partner-company analysis are explicitly scoped above.

The request referred to **27** prior tracked files. That is the pre-Lab-11 inventory recorded in its preservation manifest. At the start of this review there were **40** tracked files, including **13** Lab-11 files. All are preserved byte-for-byte and checked against the starting commit; additions are confined to `lab12/`. Earlier disclosures and partner accounts remain historical records, not new interactions asserted by this review. The repository has no separate Lab-03/04 notes: the company report is the available earlier research, and the root DCF is the preserved training exercise.

Publication checks cover every GitHub link in this new report, including relative file links resolved to their published GitHub URLs. The link log records actual HTTP responses after publication; reachability does not independently verify an external source's financial content. Brightspace submission itself is not performed here.

## AI disclosure

Codex served as my permitted learning partner, identified as “Partner” in this written review, and assisted with organizing, checking, validating, and documenting the analysis. The explanations and evidence-based answers were drafted from my existing repository; interpretive judgments are labeled, and no human classmate interaction, attendance, session token, or separate partner-company presentation is claimed. I remain responsible for reviewing the work, understanding the analysis, the final conclusion, and any errors.
