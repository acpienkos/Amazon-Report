# FIN 43900 Lab 07 — Comparable-Company Policy and Implied Range

Educational Use Disclaimer: This analysis was prepared solely for educational purposes as part of Purdue University FIN 43900 coursework. It is a simplified financial analysis and should not be relied upon for investment, trading, or other financial decisions. Nothing in this report constitutes financial or investment advice.

**Prepared:** September 15, 2026. **Course company:** Amazon (AMZN).

## Assignment and scope

The current [Lab 07 instructions][L7] and [Session 07 slides][S7] require the **Asbury Automotive training case**, checked P/E calculations, explained peer decisions, and interpretation of a peer removal. Lab 07 is a Tuesday completion checkout, **25 or 0**. The [Week 4 README][W4] explicitly assigns the independently sourced own-company peer comparison to [Lab 08][L8]. Its five merit criteria belong to Lab 08, not Lab 07. No chart, deal model, DCF extension, or new scenario forecast is required for Lab 07.

Accordingly, section A below uses the professor's frozen inputs **only as TRAINING / VALIDATION**. Section B contains the separate Amazon analysis: the existing DCF discussion and an independently sourced annual-earnings diagnostic. No Asbury, AutoNation, or Group 1 value is presented as an Amazon input or peer valuation. A complete Amazon peer selection exercise belongs to Lab 08.

Materials reviewed: Lab 07, Session 07 markdown and rendered-slide HTML source, Week 4 README, [worked case][CASE], [handout][HAND], [prework][PRE], Lab 08 for the scope boundary, and both optional-reading pages. The latter explicitly exclude advanced multiples and acquisition exercises from the labs. The written case/handout route substitutes for the optional video route. There is no Lab 07 starter or separate public grading key in this package; the build specification and floor are in Lab 07. Course snapshot: `6b259a25e194b1d56e08dbf2502373ba334b22a0`. Brightspace remains authoritative for deadlines and any private instructions; its contents were not accessed.

**AI-use disclosure and personal work:** Codex reviewed materials and sources, drafted this report and calculator, and executed checks. These are AI-assisted explanations for student review, not a claim of unaided authorship. The required before-AI explanation, personal prediction, hand calculation, and partner discussion cannot be reconstructed after the fact. The notes below prepare those discussions but do not certify that they occurred. No classroom conversation, instructor demonstration, or Brightspace attempt is claimed as completed.

## Reopen and explain — Amazon DCF context

The existing `dcf.py`, `lab06.md`, `dcf_output_lab06.txt`, and `lab06_validation.txt` were reviewed. The unchanged DCF was rerun, reproducing the saved output. [Lab 06 report][PRIOR] retains the detailed sources, dates, component WACC calculation, and limitations.

| Saved Amazon input/result | Value and units | Classification and locator |
|---|---:|---|
| FY2025 starting FCFF | $8,846.82 million | Calculated; Lab 06 §1: OCF 139,514 + debt cash interest 1,458 × (1 − 21%) − gross cash capex 131,819 |
| Five annual FCFF growth rates | −50%, +50%, +40%, +25%, +15% | Lab 06 forecasts, not management guidance |
| WACC / terminal growth | 11.80145113% / 3% | Lab 06 estimated WACC / long-run assumption; unchanged |
| Cash / debt | $78,213 million / $133,320 million | June 30, 2026 reported components; Lab 06 §1, 10-Q balance sheet and Note 5 |
| Diluted shares for DCF | 10,903 million | Q2 2026 weighted average; Lab 06 §1, 10-Q Note 1 |
| Base DCF | $5.9930/share | Reproduced model output, September 10, 2026 valuation |
| Centered sensitivity range | $4.0382–$9.0873/share | WACC ±1 percentage point and terminal growth 2%–4% |
| Required fixed-grid range | $6.0937–$14.5950/share | WACC 9%–11%, terminal growth 2%–4%; not centered on estimated WACC |

**Explanation to prepare:** increasing WACC lowers the present value of the same forecast cash flows; raising terminal growth increases terminal value. The main uncertainty is the FCFF recovery path applied to a depressed base. Terminal value contributes 74.27% of enterprise value, so assumptions after year five matter substantially. The model is mechanically reproducible but economically fragile. Its required reverse-DCF bracket has no solution for the saved market price; the wider diagnostic is not an adopted forecast. No assumption is changed here to move the valuation toward the market.

**Focused question for peer analysis:** can a positive reported P/E help evaluate Amazon when capital spending depresses FCFF and investment gains affect net income? A peer comparison would add market pricing evidence, but it cannot by itself resolve either accounting issue.

## Define/Discover — what P/E measures

Price per share is the market cost of an equity share at a specified time. Annual diluted EPS allocates annual earnings to the diluted weighted-average share base under the reporting convention. **P/E = price per share / annual diluted EPS** measures the dollars paid for each dollar of annual earnings per share. It is a multiple, not a dollar price, a forecast return, or a guaranteed payback period.

Dividing by EPS removes the arbitrary scale of the share price, letting differently sized companies be compared. A defensible peer P/E multiplied by the target's EPS answers what that target would be worth **if** its earnings deserved that peer's multiple. DCF instead discounts an explicit cash-flow forecast. Neither method automatically validates the other.

Comparisons need compatible dates, fiscal periods, currency, stock-split/share bases, and earnings definitions, plus similar growth, risk, leverage, and business economics. Annual reported, LTM, forecast, adjusted, and continuing-operations earnings cannot be silently mixed. Negative or zero EPS does not support this positive-multiple valuation; very small positive EPS can create a misleadingly large multiple. An unusual gain can make P/E look cheap without improving recurring operations. A lower P/E may reflect lower growth or higher risk, so it is not automatically a better investment. These are the concepts addressed by the [worked case][CASE] and [handout][HAND].

## A. TRAINING / VALIDATION ONLY — Asbury case

### Represent: peer policy and decisions

The case policy requires publicly traded franchised vehicle retailers with new/used sales and meaningful service/parts activity, positive annual earnings, and compatible EPS definitions. Service/parts matters because it ties recurring customer maintenance to the dealership business; a generic retail label does not describe that earnings mix. Geography, financing, acquisition effects, and scale remain explicit qualifications. The policy is stated before the result table; no claim is made that this AI-assisted write-up was produced before exposure to the published checks.

| Company | Decision | Business evidence and interpretation |
|---|---|---|
| Asbury (ABG) | Target; exclude from peer median | Its release describes vehicle retail, parts/service and finance/insurance. Target membership would partly price Asbury using itself. [ABG release][AR], About Asbury and operating tables. |
| AutoNation (AN) | **Use**, with financing caution | New/used vehicles, after-sales, and customer financial services fit the target's core economics. The captive AutoNation Finance business adds lending/credit exposure. Keep that difference visible; it does not erase the core dealership fit. [AN release][NR], Full Year Results, Segment Results, and AutoNation Finance description. |
| Group 1 (GPI) | **Qualify and include** | Vehicle sales and parts/service fit. U.S./U.K. exposure and the 2024 acquisition of 54 Inchcape dealerships create geography and integration differences. Test removal instead of applying an arbitrary haircut or discarding the higher answer. [GPI release][GR], opening business description and U.K. Update. |

These are judgments based on the opened business sources. Both peers remain in the base case. The leave-one-out test measures dependence on each choice; it is not evidence that the less convenient peer should be excluded.

### Inputs and source audit

All six values below are **professor-mandated TRAINING / VALIDATION inputs**, independently checked against the linked primary sources on September 15, 2026. Prices and EPS are USD per ordinary common share on the case's historical, compatible share basis. EPS is **FY ended December 31, 2024, total GAAP diluted EPS**. Prices are the **December 31, 2024 closing prices**, not current quotes.

| Company | Price | Price source and exact locator | Annual EPS | EPS publication date, source and exact locator |
|---|---:|---|---:|---|
| ABG | $243.03 | [2025 proxy][AP], Outstanding Equity Awards, footnote (2), search `243.03` | $21.50 | January 30, 2025 [release][AR], Full Year 2024 Results; consolidated income statement, annual diluted net-income EPS |
| AN | $169.84 | [2025 proxy][NP], Outstanding Equity Awards, footnote (1), printed p. 30 | $16.92 | February 11, 2025 [release][NR], Full Year Results and income statement, annual diluted net-income EPS |
| GPI | $421.48 | [2025 proxy][GP], Termination and Change in Control Tables introduction, printed p. 59 | $36.81 | January 29, 2025 [release][GR], annual Consolidated Statements of Operations, total DILUTED EARNINGS PER SHARE |

The figures are reported historical data, used here as validation inputs. GPI's total $36.81 differs from continuing-operations EPS of $36.72 and adjusted total EPS of $39.29; those alternatives are not substituted. This is a **retrospective** exercise: the full-year earnings were published after the price date. It is not a tradable December 31 information set. Later split-adjusted quotes must not replace these prices without matching EPS adjustments.

### Implement: formulas and reproducible arithmetic

For each admitted peer, calculate `price / EPS`. Take the minimum, median, and maximum of the peer multiples, then multiply by **target EPS**. With two peers the median is their arithmetic midpoint. ABG's own observed P/E is shown only for context. There is no separate share-count conversion because both inputs are already per share, and **no cash/debt bridge** because P/E already values equity earnings.

```text
AN P/E   = 169.84 / 16.92 = 10.037825059... times
GPI P/E  = 421.48 / 36.81 = 11.450149416... times
Median   = (AN P/E + GPI P/E) / 2
ABG value using AN = (169.84 / 16.92) × 21.50 = 215.813238770... dollars/share
ABG midpoint = [(169.84 / 16.92 + 421.48 / 36.81) / 2] × 21.50
```

The AN-implied-price line is a worked hand-calculation guide, not a claim that the student already performed it unaided. The code retains full floating-point precision and independently checks the key result using exact rational arithmetic. Display rounding occurs only at the end.

### Validate: results

| Training output | Calculated result |
|---|---:|
| AN P/E | 10.037825× |
| GPI P/E | 11.450149× |
| ABG observed P/E, excluded from peer set | 11.303721× |
| Median peer P/E | 10.743987× |
| ABG implied low / high | $215.81 / $246.18 |
| ABG at peer median | **$231.00** |
| Remove GPI: AN-only reference | **$215.81**, change **−$15.18** |
| Remove AN: GPI-only reference | **$246.18**, change **+$15.18** |

Every published Lab 07 check is reproduced. The one-file calculator also normalizes ticker case/whitespace, deduplicates peers, excludes the target, labels unusable inputs, and handles zero/one remaining peer. The first occurrence of a duplicate ticker wins and the skipped duplicate is printed; conflicting duplicates should be corrected at the input table. A missing target price prevents its observed P/E, but a valid target EPS still permits peer-implied prices.

### Evolve: prediction, peer change, and interpretation

**Prediction to explain:** GPI has the higher multiple, so removing it should lower the midpoint to AN's implied price. The result confirms a **$15.18 decrease**. Removing AN has the opposite effect. The change is calculated from unrounded estimates: subtracting displayed $231.00 from $215.81 would incorrectly report −$15.19.

With one peer, there is only one independent pricing reference; the calculator does not manufacture a low/high band from the same observation. Removing the sole remaining peer leaves no estimate. The base decision remains to use AN and qualify GPI, because the arithmetic has not changed their business evidence.

### Reflect: what the comparison supports

The observed ABG price, $243.03, lies within $215.81–$246.18 and above the peer midpoint. This establishes only its position relative to two selected earnings multiples. It does not establish fair value, underpricing, or an attractive purchase. Two peers provide no statistical confidence interval; earnings quality, leverage, integration effects, and market-wide overvaluation could affect both endpoints. Before relying on the comparison, verify sustainable earnings and whether differences in financing and geographic exposure justify the multiple gap. This explanation is specific to the case and does not reuse the professor's sample investment conclusion.

## B. AMAZON ANALYSIS ONLY — independently sourced earnings context

This supplement connects the training lesson to the student's company and prepares Thursday's required annual-EPS input. It is **not** a completed Lab 08 peer comparison. Sources were opened on September 15, 2026; the price remains the explicitly dated Lab 06 observation.

| Input or calculation | Value | Units / period | Status and exact source locator |
|---|---:|---|---|
| Annual net income | 77,670 | USD million, FY2025 | Reported; [Amazon 10-K][K], Item 8, Consolidated Statements of Operations, printed p. 37, 2025 column |
| Annual diluted weighted-average shares | 10,827 | Million shares, FY2025 | Reported; [10-K][K], same statement and column, diluted weighted-average shares |
| Annual total GAAP diluted EPS | 7.17 | USD/share, FY2025 | Reported; [10-K][K], same statement, diluted EPS; filed February 6, 2026, accepted February 5 per [SEC index][KI] |
| Prior observed AMZN price | 252.13 | USD/share, September 10, 2026 16:26 EDT after-hours | Saved observation; [Lab 06 source record][PRIOR] §1, quote block on Stock Analysis; not independently recovered as a historical tick in Lab 07 |
| Income / annual diluted shares | 7.173732 | USD/share | Calculated from reported rounded totals; rounds to $7.17 |
| Price / annual reported EPS | **35.164575×** | Annual earnings multiple at saved quote | Calculated: 252.13 / 7.17; not LTM, forecast P/E, or fair value |

The FY2025 denominator is 10,827 million annual diluted shares; 10,903 million from Lab 06 is the Q2 2026 denominator used in that DCF, not an interchangeable EPS input. The reported $7.17 is used directly rather than replacing it with extra decimal places reconstructed from rounded totals.

Amazon's operations combine stores, seller services, advertising, subscriptions and AWS. Its 10-K also reports $15.2 billion of other income, primarily related to Anthropic investment effects (Item 7, pp. 27–28). Positive EPS therefore does not establish recurring operating earnings quality. [Amazon 10-K][K], Item 1 / Note 1 business description and Item 7, Other Income (Expense), Net.

**Amazon-specific judgment:** dealership economics do not adequately represent that business mix, so the Asbury peer policy cannot be transplanted to Amazon. A future peer policy should compare earnings sources, investment intensity, growth and risk; qualify partial business matches; and require compatible reported EPS and same-date prices. There is no invented Amazon peer range here. The observed 35.16× simply identifies what was paid per dollar of reported annual earnings at the saved quote. It neither repairs nor refutes the depressed-FCFF DCF.

The prior **watch/defer** coursework conclusion remains conditional: revisit only after a filing-supported FCFF recovery forecast and evidence of AWS cash conversion. The existing Lab 06 20% value cushion is a decision assumption, not a sourced fact. This lab supplies no basis to raise that forecast or average the Amazon DCF with the unrelated Asbury price range. The saved quote is not represented as today's market price.

## Reproduce and inspect the evidence

Files: [calculator](comps.py), [executed output](lab07_output.txt), and [validation evidence](lab07_validation.txt).

From this `lab07` folder, using the existing working Python 3.13.7 executable:

```powershell
& 'C:\Users\acpie\AppData\Local\Temp\fin439-python-3.13.7\python.exe' comps.py --validate
& 'C:\Users\acpie\AppData\Local\Temp\fin439-python-3.13.7\python.exe' comps.py
& 'C:\Users\acpie\AppData\Local\Temp\fin439-python-3.13.7\python.exe' comps.py --amazon-context
```

On a machine with Python on PATH, the equivalent commands start with `python comps.py`. All editable case inputs are at the top. The default run is clearly labeled training; the Amazon diagnostic requires the separate flag. No package installation or data fetching occurs. Validation ran before the first result run, and all **41 checks passed**. Exact-rational checks, split invariance, invalid inputs, and peer removal test the financial logic as well as the displayed answers. Original Lab 06 tests were also rerun; their evidence is retained in the validation file. Hash checks establish that prior workspace files and the four GitHub Lab 06 files were not modified.

## Requirement review and individual checkout

The instructions and slides were reread after completion. The review covered every explicit build rule and each DRIVER phase, including the discussion prompts. The required written/technical floor is evidenced by the checked Asbury calculation, source-supported peer decisions, and interpreted peer removal. Advanced optional reading adds no deliverable. No private grading key was accessed and no grade is claimed.

| Requirement | Evidence / status |
|---|---|
| Reopen prior DCF and retain assumptions | Unchanged DCF rerun; prior context above and output comparison in validation |
| Define/Discover and specific question | P/E definition, purpose, pitfalls and Amazon question above |
| Represent: explain economic fit, use/qualify/exclude | Case policy and source-supported decisions above |
| Implement: one standard-library file, editable inputs and all edge cases | `comps.py`; 41 checks, no network/package requirement |
| Validate known answers and one worked price | Training table, rational check and calculation guide |
| Evolve: direction, full-precision change, no one-peer range | Both peer removals and interpretation above |
| Reflect: usefulness, qualifications, no proof of fair value | Case reflection and Amazon transfer discussion |
| Own-company preparation | Saved DCF, sourced FY2025 EPS, Lab 08 instructions read |
| Personal before-AI and partner activities | **Student action:** not represented as completed by this AI-assisted package |
| Checkout | GitHub file links; student must complete Brightspace attempt when instructed |

**Personal checkout:** review and explain the calculation and peer choices, follow the instructor's directions for the individual/partner activities, then use **Brightspace → Quizzes → Lab 07** when told. Paste the four file links and complete the attempt. A retrospective AI-assisted note is not evidence of a before-AI step. For Thursday, bring this calculator and the unchanged DCF/source table; the annual-EPS source is above.

## Source links

[L7]: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-04/lab-07-comparable-policy.md
[S7]: https://cinderzhang.github.io/FIN43900-Fall2026/lessons/week-04/slides-session-07.html
[W4]: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-04/README.md
[L8]: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-04/lab-08-deal-triangulation.md
[CASE]: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-04/teach-comps-worked-example.md
[HAND]: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-04/student-handout.md
[PRE]: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-04/student-prework.md
[PRIOR]: https://github.com/acpienkos/Amazon-Report/blob/main/lab06/lab06.md
[AP]: https://www.sec.gov/Archives/edgar/data/1144980/000114498025000092/abg-20250402.htm
[AR]: https://www.sec.gov/Archives/edgar/data/1144980/000114498025000008/a2024q4ex991.htm
[NP]: https://www.sec.gov/Archives/edgar/data/350698/000035069825000068/an-20250311.htm
[NR]: https://www.sec.gov/Archives/edgar/data/350698/000035069825000026/anearningsrelease123124ex9.htm
[GP]: https://www.sec.gov/Archives/edgar/data/1031203/000103120325000018/gpi-20250320.htm
[GR]: https://www.group1corp.com/2025-01-29-Group-1-Automotive-Reports-2024-Fourth-Quarter-Financial-Results-and-Record-Full-Year-Revenues-of-19-9-billion
[K]: https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm
[KI]: https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/0001018724-26-000004-index.htm
