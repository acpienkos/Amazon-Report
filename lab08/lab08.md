# Lab 08 — Deal Evidence and Valuation Triangulation: Amazon (AMZN)

Educational Use Disclaimer: This analysis was prepared solely for educational purposes as part of Purdue University FIN 43900 coursework. It is a simplified valuation exercise and should not be relied upon for investment, trading, or other financial decisions. Nothing in this report constitutes financial or investment advice.

**Valuation date: September 10, 2026. Prepared September 16, 2026 (EDT). Conditional decision: watch/defer.**

The two qualified peers imply **$196.70–$277.69 per Amazon share**, with a **$237.19 median-based midpoint**. That midpoint is 5.83% below Amazon's same-date closing price of $251.89. This is a conditional reported-earnings comparison, not a defensible claim of intrinsic fair value. Removing either peer moves the midpoint 17.07%, and neither company reproduces Amazon's consolidated economics.

## 1. Assignment, authorship, and question

The current [Lab 08][L8] requires two sourced candidate decisions, a reported annual P/E comparison or supported limitation, arithmetic and peer-removal checks, comparison with the saved DCF, evaluated AI criticism, and a conditional call. [Session 08][S8], the [weekly README][W4], [handout][HAND], [worked case][CASE], and prework were reviewed. The public merit rubric is embedded in Lab 08; there is no additional public Lab 08 starter, dataset, or grading key. The acquisition packet and advanced methods are optional, outside this lab. The verified course revision is `6b259a25e194b1d56e08dbf2502373ba334b22a0`. Brightspace remains authoritative for private instructions, deadlines, and the actual checkout; it was not accessed.

**AI-use disclosure:** the initial policy and personal criticism judgment quoted below were supplied by the student as their own words. Codex researched the sources, operationalized the policy, drafted the remaining explanations and code, and executed checks. Those assisted portions are not represented as unaided student work. Only this resumed Codex conversation was used; no second independent AI consultation or classroom partner exchange is claimed. Personal checkout actions are listed in §9.

**Research question:** can two large infrastructure-backed ecosystems provide useful reported P/E references for Amazon despite its mixed earnings sources, and what does that add to the September 10 DCF?

Amazon earns revenue from product sales, third-party seller services, advertising, subscriptions, and AWS. FY2025 revenue was $716.924 billion. AWS contributed $128.725 billion of revenue and $45.606 billion of $79.975 billion consolidated operating income: its profit importance exceeds its revenue weight. Annual reported EPS is positive. [Amazon 10-K][AK], Item 1; Item 8, statement of operations; Note 10, segment information. The research needs were compatible prices, annual EPS available by the comparison date, business evidence, and investment-related earnings effects.

## 2. Initial policy and implementation rules — before valuation

**Student's initial policy, preserved verbatim:**

> A company is economically comparable to Amazon when it matches its massive revenue scale, integrated ecosystem, and dual economic moats of customer loyalty and infrastructure control.
>
> For example, I would not consider Boeing comparable to Amazon. It does not really bring in money in the same way, it has very different customers, completely different products, and a completely different business model.

**AI-assisted operational interpretation, stated before calculating:** investigate exactly two publicly listed operating companies with substantial revenue scale, connected services that encourage repeat usage, and control of infrastructure supporting an Amazon-relevant activity. Infrastructure may be physical distribution or cloud computing; loyalty may be membership-based or reinforced by integrated software. These are economic hypotheses, not proof that a moat is permanent. Do not invent a revenue threshold to admit preferred names.

An exact consolidated match would be too restrictive for Amazon. Therefore, **qualify** a partial match and disclose the omitted economics; do not call it an unqualified substitute. This makes explicit how the initial policy is applied rather than silently weakening it after seeing multiples. Reject a candidate whose revenues come from unrelated economics, whose infrastructure does not support a comparable activity, or whose price/EPS/share basis cannot be verified. Missing or nonpositive annual EPS cannot enter a positive P/E calculation. These rules precede interpretation of the output.

**Calculation policy fixed before the run:** apply the unchanged Lab 07 formulas to admitted peers only. Use the minimum, median, and maximum P/E; with two peers the median is their arithmetic midpoint. No group weights, segment weights, discretionary haircut, outlier trimming, adjusted EPS, or price-target fitting. Preserve precision until display. One remaining peer provides one reference, not a range; no remaining peer means no estimate. Exclude AMZN from its own peer median. P/E already values equity, so do not subtract net debt.

## 3. Exactly two researched candidate decisions

| Candidate | Decision and evidence opened | Why it fits the policy | Material qualification / rejection boundary |
|---|---|---|---|
| **Walmart (WMT)** | **Qualify and include.** [FY2026 10-K][WK], Item 1, General Development, Walmart U.S., Sam's Club U.S., and Distribution; [annual release][WR], Full Year Highlights. | $713.163 billion annual revenue; stores, e-commerce, fulfillment, marketplace, advertising, and Walmart+/Sam's membership support scale, repeated customer interaction, and distribution control. | Physical-store/grocery exposure and no AWS-equivalent operating segment make it a retail-side reference. Exclude it as a stand-alone proxy for Amazon's cloud economics; retain it as a qualified consolidated reference. |
| **Microsoft (MSFT)** | **Qualify and include.** [July 29 annual release][MR], Business Highlights and Fiscal Year 2026 Results; [earnings call][MC], Nadella's infrastructure/platform discussion. | $331.839 billion annual revenue; Azure, integrated enterprise applications, and subscriptions link infrastructure to recurring customer relationships. The call describes datacenter expansion and integration across the software stack. | Less than half Amazon's revenue, enterprise/software-heavy economics, and no comparable mass retail/fulfillment business. Retention through switching costs differs from retail loyalty. It is a cloud/ecosystem reference, not a proxy for all Amazon earnings. |

These are the only two candidates fully investigated and valued. Both stay in the base case regardless of which yields the more attractive answer. Their equal influence is the course's two-peer median convention, **not** an estimate of Amazon's segment mix or a sum-of-the-parts valuation.

**Scope screen, not additional researched candidates:** Boeing is excluded under the student's stated reasoning. Alphabet is a plausible cloud/advertising alternative, but choosing it alongside Microsoft would leave no retail-side reference in this two-candidate exercise. Costco could test membership retail but would not add cloud coverage; Meta, Apple, and pure logistics businesses would emphasize narrower advertising, device, or shipping economics. These are scope judgments, not source-audited exclusion findings or claims that those companies could never be peers. No financial inputs or multiples for them enter the analysis.

## 4. Source audit and compatible inputs

All prices and EPS are **USD per U.S. common share**, on compatible contemporary split bases. Prices are the **September 10, 2026 regular-session close** (4:00 p.m. EDT, UTC−04:00), not dividend-adjusted total-return prices. Annual EPS means total reported GAAP diluted EPS, not quarterly, LTM, forecast, basic, or adjusted EPS. The figures below are reported observations; multiples and implied prices are calculated.

| Company | Closing price | Price source and exact locator | Annual diluted EPS | Fiscal period | Publication and exact earnings locator |
|---|---:|---|---:|---|---|
| Amazon / AMZN | $251.89 | [ChartExchange AMZN][AP], Historical Prices, `2026-09-10`, **Close** column | $7.17 | Jan. 1–Dec. 31, 2025 | Feb. 5, 2026 [annual release][AR], Full Year 2025; [10-K][AK], Item 8, Consolidated Statements of Operations, p. 37, 2025 diluted EPS row. [SEC index][AI]: accepted Feb. 5, filed Feb. 6. |
| Walmart / WMT | $105.73 | [ChartExchange WMT][WP], same date and column; cross-check [Investing.com][WX], historical `Price` column | $2.73 | Feb. 1, 2025–Jan. 31, 2026 | Feb. 19, 2026 [release][WR], Consolidated Statements of Income, **fiscal year** diluted net income per common share attributable to Walmart; [10-K][WK], Note 2, p. 63. |
| Microsoft / MSFT | $492.44 | [ChartExchange MSFT][MP], same date and column; cross-check [Investing.com][MX], historical `Price` column | $17.95 | July 1, 2025–June 30, 2026 | July 29, 2026 [release][MR], Fiscal Year 2026 Results and Income Statements, **year ended June 30, 2026**, diluted EPS row. |

Sources were opened September 16, 2026 EDT. Nasdaq historical data was tried first but did not expose the required dated rows in the available page response, so named market-data sources were used. Microsoft's SEC 10-K full text did not load reliably; its primary-source annual release and call supply the evidence actually used. This does not claim the inaccessible filing was successfully audited.

**Period limitation:** these are each company's latest annual reported earnings public by September 10. Fiscal labels differ and Microsoft includes six months of 2026 while Amazon ends in December 2025. The information cutoff and accounting definition match; the underlying earnings windows do not. No annualization or invented calendar-year adjustment hides that difference. Walmart's already-restated annual EPS is paired with a contemporary share price; no additional historical split factor is applied.

**Earnings quality:** Amazon reports $15.229 billion other income, net, with material Anthropic investment effects (10-K Item 7, pp. 27–28; Notes 1–2). Its $77.670 billion net income divided by 10.827 billion annual diluted shares rounds to $7.17; the quarterly DCF share denominator is not substituted. Microsoft reports an annual $0.67 EPS benefit from OpenAI investments and $17.28 non-GAAP EPS. Walmart's annual reconciliation removes $0.20/share of investment gains among other adjustments and shows $2.64 adjusted EPS. [AK], [MR] Non-GAAP Definition, [WR] Non-GAAP Measures/EPS reconciliation. **Those adjusted figures are disclosure only, not valuation inputs.** A common GAAP label does not make the earnings equally recurring. No flat tax-rate adjustment to Amazon's gains is invented.

**Newer market observation, separate from the historical valuation:** [Stock Analysis AMZN overview][CURRENT] displayed **$247.81, September 16, 2026, 7:59 p.m. EDT**, after-hours; its regular close was $245.96 at 4:00 p.m. EDT. Retrieved approximately 9:07 p.m. EDT (September 17, 01:07 UTC). This is the latest displayed observation obtained, not a continuously live quote. It does not change the September 10 peer inputs. Lab 06's saved $252.13 at 4:26 p.m. EDT on September 10 is preserved in that lab; using $251.89 here aligns regular-session closes across all three companies.

## 5. Implementation, arithmetic, and peer-removal check

Formula: `peer P/E = peer price / peer annual EPS`; `AMZN implied price = peer P/E × AMZN annual EPS`. Compare with market using `(implied price / observed AMZN price − 1) × 100`.

**Worked arithmetic check:** Walmart `105.73 / 2.73 = 38.7289377289×`; multiplying back gives `38.7289377289 × 2.73 ≈ 105.73`. Applying that multiple to Amazon gives `38.7289377289 × 7.17 = 277.6864835165`. This is a reproducible hand-calculation guide and is independently checked with exact rational arithmetic in Python; it is not a claim of an unaided student hand calculation.

| Calculated output | Result |
|---|---:|
| Walmart annual P/E | 38.728938× |
| Microsoft annual P/E | 27.433983× |
| Peer median = (38.7289377289 + 27.4339832869) / 2 | 33.081461× |
| Amazon observed price / annual EPS = 251.89 / 7.17 | 35.131102× |
| Low: (492.44 / 17.95) × 7.17 | **$196.70/share** |
| High: (105.73 / 2.73) × 7.17 | **$277.69/share** |
| Midpoint: median peer P/E × 7.17 | **$237.19/share** |
| Low / midpoint / high versus September 10 market | **−21.91% / −5.83% / +10.24%** |
| Same historical implied values versus newer $247.81 observation | −20.62% / −4.28% / +12.06% |

**Direction to predict before a classroom rerun:** Walmart has the higher price/EPS ratio, so removing Walmart must lower the midpoint; removing Microsoft must raise it. This is an AI-assisted explanation, not a retrospective claim that the student recorded a prediction before the first run.

| Removal | Remaining reference | Dollar change from full midpoint | Percent change | What is lost |
|---|---:|---:|---:|---|
| Remove Walmart | Microsoft-only **$196.70** | **−$40.49** | **−17.07%** | Retail/distribution and membership reference |
| Remove Microsoft | Walmart-only **$277.69** | **+$40.49** | **+17.07%** | Cloud/software infrastructure reference |

Changes use unrounded values: the first is `196.7016601671 − 237.1940718418 = −40.4924116747`. Both remaining outputs are single references with **no range**. The $80.98 spread and symmetric 17.07% changes show material dependence on both observations; a two-observation median offers no protection from one weak peer choice. There is no evidence-based reason here to remove the inconvenient result. Keep both qualified decisions and withhold confidence in a precise fair-value point estimate.

## 6. Compare with the unchanged September 10 DCF

| Method | Amazon result and date | Main assumption or limitation |
|---|---|---|
| Week 3 DCF | Sept. 10, 2026: **$5.9930/share** base; centered sensitivity **$4.0382–$9.0873**. Required fixed WACC grid separately: **$6.0937–$14.5950**. | Starting FCFF $8,846.82 million; growth −50%, +50%, +40%, +25%, +15%; WACC 11.80145113%; terminal growth 3%. The centered and fixed grids answer different questions. |
| Peer annual reported P/E | Sept. 10, 2026 closes: **$196.70–$277.69**; midpoint **$237.19**. | Two qualified consolidated partial matches, different annual periods, and non-operating investment effects. |

Source: unchanged [Lab 06 report][DCF] and saved output; `dcf.py` rerun reproduces the saved output. Its simplified FCFF is `139,514 + 1,458 × (1 − 0.21) − 131,819 = 8,846.82` USD million. Large gross cash capex depresses this base, and the forecast never returns to the earlier cash-flow scale. The DCF is therefore a scenario result, not proof Amazon is worth approximately $6.

P/E prices accounting earnings, whereas the DCF discounts a particular forecast after investment spending. Capital spending reduces current FCFF immediately but generally enters earnings over time through depreciation; investment gains can raise EPS without cash from customer operations. Peer prices also embed growth expectations not imposed on the saved DCF. Their disagreement identifies weak assumptions in both methods. It is not resolved by changing Lab 06 or averaging the two results. Both outputs concern Amazon equity per share; neither P/E endpoint needs an enterprise-to-equity bridge. The different September 10 price timestamps are disclosed above and are far too small to explain the gap.

## 7. AI criticism and personal judgment

**AI criticism presented in the resumed chat:** the weakest link is treating Walmart's retail earnings and Microsoft's software/cloud earnings as substitutes for Amazon's consolidated earnings. Reproducible arithmetic alone cannot turn those partial matches into fair value. Additional checks identify differing fiscal windows and the historical-versus-newer quote distinction; these must stay explicit.

**Student's evaluation — ACCEPT, preserved verbatim:**

> I accept the criticism. I think Walmart is comparable to Amazon in some important ways because it operates at a massive revenue scale, serves a huge number of customers, and has a major retail and delivery business. However, Walmart does not capture major parts of Amazon's economics, especially AWS/cloud infrastructure and its broader technology and digital-services ecosystem. Because of that, I do not think the P/E comparison by itself is strong enough to establish Amazon's fair value, so I would retain my watch/defer conclusion pending stronger evidence of cash conversion.

**Source check supporting that judgment:** Walmart's Item 1 establishes the retail ecosystem and distribution fit; Amazon's segment note separately identifies AWS; Microsoft's annual release identifies its different software/cloud business mix. These sources support a qualified comparison and the accepted limitation. They do not establish that all three consolidated earnings streams deserve the same multiple. This source check was AI-assisted; the student supplied the quoted judgment directly.

**Skeptical question to defend:** what evidence would show that Amazon's infrastructure investment is producing sustainable cash for shareholders, rather than merely increasing reported earnings or revenue?

**Answer / conditional conclusion:** retain **watch/defer**. Defend $196.70–$277.69 only as the outcome of this disclosed two-peer reported-EPS policy, and withhold an intrinsic fair-value range. A price inside that band does not establish an attractive purchase. Reconsider when filings support sustained cash conversion and a credible forecast that still supports the price under less favorable growth/discount assumptions. One concrete metric to monitor is **trailing-twelve-month operating cash flow less gross cash purchases of property and equipment**. Sustained positive improvement over at least two successive reports, alongside evidence that it is not simply a working-capital timing benefit or deferred investment, would justify revisiting the forecast; it would not automatically trigger initiation. That two-report criterion is an analytical monitoring rule, not management guidance. Retain the same definition over time and distinguish it from company-reported net-capex FCF and the course's interest-adjusted FCFF.

## 8. Reproduction and validation

Files: [calculator](comps_lab08.py), [executed results](lab08_output.txt), [validation evidence](lab08_validation.txt). The calculator is a standalone standard-library Lab 08 implementation of Lab 07's logic; it does not import or modify prior submissions, fetch data, or install packages.

From the local `lab08` folder:

```powershell
& 'C:\Users\acpie\AppData\Local\Temp\fin439-python-3.13.7\python.exe' comps_lab08.py --validate
& 'C:\Users\acpie\AppData\Local\Temp\fin439-python-3.13.7\python.exe' comps_lab08.py
& 'C:\Users\acpie\AppData\Local\Temp\fin439-python-3.13.7\python.exe' comps_lab08.py --training
```

With Python on PATH, use `python comps_lab08.py` and the same flags. Training regression executes first inside validation. All **32 Lab 08 checks passed**: published case answers, exact rational Amazon arithmetic, peer removal, positive/missing inputs, duplicate/target exclusions, admission decisions, split consistency, and date/look-ahead rejection. The original Lab 07's **41 checks** also passed. The unchanged DCF was rerun and compared with its saved output. Preservation hashes and Git scope checks protect prior files.

**TRAINING / VALIDATION ONLY:** Asbury using AutoNation and Group 1 reproduces **$215.81–$246.18**, midpoint **$231.00**, and removing Group 1 yields **$215.81**, a **−$15.18** unrounded change. There are no new Lab 08 training values. These company inputs never enter Amazon's calculation; the Amazon run uses only independently researched AMZN, WMT, and MSFT data. No synthetic test value is presented as company evidence.

## 9. Rubric review and individual checkout

Lab 08, its embedded five-criterion merit rubric, and Session 08 were reread after drafting. Each written/technical criterion has evidence below. This is a completeness review, not a promised score or certification of classroom actions.

| Criterion / requirement | Evidence and status |
|---|---|
| Problem/decision | AMZN, Sept. 10 information cutoff, verbatim initial policy, and operational interpretation before calculation (§§1–2). |
| Data/evidence | Exactly two qualified candidate decisions; opened primary business/earnings sources, dated market rows, publication dates, currency/share definitions, and fiscal/earnings limitations (§§3–4). |
| Validation | Worked division, exact-rational checks, both changed-peer results and causal interpretation, single/no-peer handling (§5; validation file). |
| Financial judgment | Saved DCF ranges compared without modification or averaging; limited defensible peer band, watch/defer, monitoring evidence (§§6–7). |
| Explanation/transfer | Student's accepted criticism preserved and checked against sources; earnings/cash-flow mechanism and skeptical-question answer (§§6–7). |
| Training separation and educational disclaimer | Required disclaimer directly below title; script comment; isolated training flag and regression tests (§8). |
| Reproducibility and preservation | Four submission files; executed outputs; 32 new and 41 prior checks; DCF reproduction; prior-file hashes. |
| Personal process and checkout | Initial unaided policy and personal judgment supplied. Remaining personal actions below are **not certified completed**. |

**Still personal:** open and review the cited evidence and assisted decisions; perform/defend the hand division and removal prediction; explain P/E to the class partner and answer their actual skeptical question. The answer in §7 prepares that conversation, but does not invent one. Lab 08 also asks that the policy be sent independently to both AI partners; only Codex was used here, so complete the second consultation if the instructor requires that process step. The course says any AI partner is acceptable and no grade depends on an extension/account; no installation is needed for this package. A before-AI action cannot be reconstructed after the fact, so follow instructor guidance for any outstanding process requirement.

**Brightspace → Quizzes → Lab 08:** start when instructed, paste the GitHub links below, answer the actual checkout prompts, and finish the attempt. This repository upload is not a Brightspace submission. Bring the sources and unresolved cash-conversion question into Week 5 prework.

### Ready-to-copy submission

Lab 08 — Deal Evidence and Valuation Triangulation — Amazon (AMZN)

My September 10, 2026 reported annual P/E comparison uses exactly two qualified peers, Walmart and Microsoft. The implied range is $196.70–$277.69/share, with a $237.19 midpoint, versus AMZN's $251.89 same-date close. Removing either peer changes the midpoint by $40.49 (17.07%). I retain watch/defer: the comparison does not establish fair value, and I want stronger evidence of cash conversion. The report preserves my initial policy and personal evaluation of AI criticism, compares the unchanged Lab 06 DCF, and documents sources, qualifications, educational use, and AI assistance. Code was executed; 32 Lab 08 validation checks passed. Professor inputs are labeled TRAINING / VALIDATION ONLY.

- Report: https://github.com/acpienkos/Amazon-Report/blob/main/lab08/lab08.md
- Python: https://github.com/acpienkos/Amazon-Report/blob/main/lab08/comps_lab08.py
- Executed output: https://github.com/acpienkos/Amazon-Report/blob/main/lab08/lab08_output.txt
- Validation: https://github.com/acpienkos/Amazon-Report/blob/main/lab08/lab08_validation.txt

## Source links

[L8]: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-04/lab-08-deal-triangulation.md
[S8]: https://cinderzhang.github.io/FIN43900-Fall2026/lessons/week-04/slides-session-08.html
[W4]: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-04/README.md
[HAND]: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-04/student-handout.md
[CASE]: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-04/teach-comps-worked-example.md
[AK]: https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm
[AI]: https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/0001018724-26-000004-index.htm
[AR]: https://ir.aboutamazon.com/news-release/news-release-details/2026/Amazon-com-Announces-Fourth-Quarter-Results/default.aspx
[WK]: https://stock.walmart.com/sec-filings/all-sec-filings/content/0000104169-26-000055/wmt-20260131.htm
[WR]: https://stock.walmart.com/sec-filings/all-sec-filings/content/0000104169-26-000032/earningsreleasefy26q4.htm
[MR]: https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast
[MC]: https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q4
[AP]: https://chartexchange.com/symbol/nasdaq-amzn/historical/
[WP]: https://chartexchange.com/symbol/nasdaq-wmt/historical/
[MP]: https://chartexchange.com/symbol/nasdaq-msft/historical/
[WX]: https://www.investing.com/equities/wal-mart-stores-historical-data
[MX]: https://www.investing.com/equities/microsoft-corp-historical-data
[CURRENT]: https://stockanalysis.com/stocks/amzn/
[DCF]: https://github.com/acpienkos/Amazon-Report/blob/main/lab06/lab06.md
