# Lab 10 — Pro-Forma: Your Company Through It — Amazon.com, Inc. (AMZN)

Educational Use Disclaimer: This analysis was prepared solely for educational purposes as part of Purdue University FIN 43900 coursework. It is a simplified valuation exercise and should not be relied upon for investment, trading, or other financial decisions. Nothing in this report constitutes financial or investment advice.

**Research question:** “What are five years of your company's statements worth, built from assumptions you can defend?” — [official Lab 10](https://github.com/CinderZhang/FIN43900-Fall2026/blob/6bcbc3c929de59c547b2e421fe0f4ef2dc5d564f/lessons/week-05/lab-10-proforma-your-company.md).

**Status: computational work complete; partner exchange and two manual filing checks confirmed by the student.** The model produces **$32.67 per share**, with **92.11%** of value after 2030. All five annual balance sheets and cash-flow links pass. This is the course's positive-only FCFE exercise, with substantial financing and terminal assumptions; it does not establish Amazon's fair value. The student's standing **watch-defer** judgment is retained. The assumptions below were developed with Codex assistance. The student supplied and confirmed the capital-spending defense recorded below; the other forecast assumptions are not represented as independently authored without AI.

## Official scope and prior-work preservation

I followed the current [Lab 10](https://github.com/CinderZhang/FIN43900-Fall2026/blob/6bcbc3c929de59c547b2e421fe0f4ef2dc5d564f/lessons/week-05/lab-10-proforma-your-company.md), [Week 5 README](https://github.com/CinderZhang/FIN43900-Fall2026/blob/6bcbc3c929de59c547b2e421fe0f4ef2dc5d564f/lessons/week-05/README.md), [handout](https://github.com/CinderZhang/FIN43900-Fall2026/blob/6bcbc3c929de59c547b2e421fe0f4ef2dc5d564f/lessons/week-05/student-handout.md), [prework](https://github.com/CinderZhang/FIN43900-Fall2026/blob/6bcbc3c929de59c547b2e421fe0f4ef2dc5d564f/lessons/week-05/student-prework.md), and complete [Part 1 captions](https://github.com/CinderZhang/FIN43900-Fall2026/blob/6bcbc3c929de59c547b2e421fe0f4ef2dc5d564f/lessons/week-05/pro-forma-abg-tutorial/video-1-captions.vtt), read at course revision `6bcbc3c929de59c547b2e421fe0f4ef2dc5d564f`.

The official assignment adds a filing-versus-provider capital-spending comparison and explicitly says to value only positive flows when FCFE is negative. Those requirements are included. `fact` is retained for definitions and observed share/price inputs, following the transcript standard requested here; it is not a way to label forecast choices as facts. The file is named `amazon_proforma.py` to preserve the ABG engine.

The repository was pulled from `main`; starting commit was `347750c3bc4e8965b40312c5b18c1f49760a63d1`. SHA256 hashes were recorded for all 19 pre-existing tracked files. The unchanged Lab 09 run reproduced **$291.75**, **79.76%** after 2030, and zero balance gaps. The unchanged **lab06/dcf.py** reproduced its complete saved output, including **$5.9930**. The root-level `dcf.py` is an earlier training model, so it was not substituted for Amazon's Lab 06. See [validation evidence](lab10_validation.txt) and the embedded preservation manifest in [validate_lab10.py](validate_lab10.py).

## Three-year filing history

All amounts are **USD millions**, fiscal years ending December 31. Each year is taken from that year's own annual filing. Income and cash-flow comparisons for 2023–24 in the 2025 filing agree; balance-sheet 2023 comparisons in the 2024 filing and 2024 comparisons in the 2025 filing also agree. PP&E depreciation uses the precise consolidated segment-note number, not the rounded billion-dollar note summary. The 81-row [history CSV](amazon_history.csv) gives a source, exact statement/note/page where available, units, period, and arithmetic for every item. [Sources](sources.md) records source-file hashes and the reconciliation method.

| Item ($m) | FY2023 | FY2024 | FY2025 |
| --- | --- | --- | --- |
| Revenue | 574,785 ([2023 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872424000008/amzn-20231231.htm)) | 637,959 ([2024 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872425000004/amzn-20241231.htm)) | 716,924 ([2025 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm)) |
| Cost of sales | 304,739 ([2023 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872424000008/amzn-20231231.htm)) | 326,288 ([2024 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872425000004/amzn-20241231.htm)) | 356,414 ([2025 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm)) |
| Gross profit (calculated) | 270,046 ([2023 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872424000008/amzn-20231231.htm)) | 311,671 ([2024 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872425000004/amzn-20241231.htm)) | 360,510 ([2025 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm)) |
| Sales and marketing | 44,370 ([2023 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872424000008/amzn-20231231.htm)) | 43,907 ([2024 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872425000004/amzn-20241231.htm)) | 47,129 ([2025 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm)) |
| General and administrative | 11,816 ([2023 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872424000008/amzn-20231231.htm)) | 11,359 ([2024 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872425000004/amzn-20241231.htm)) | 11,172 ([2025 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm)) |
| SG&A = previous two rows | 56,186 ([2023 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872424000008/amzn-20231231.htm)) | 55,266 ([2024 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872425000004/amzn-20241231.htm)) | 58,301 ([2025 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm)) |
| Net income | 30,425 ([2023 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872424000008/amzn-20231231.htm)) | 59,248 ([2024 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872425000004/amzn-20241231.htm)) | 77,670 ([2025 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm)) |
| Year-end inventory | 33,318 ([2023 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872424000008/amzn-20231231.htm)) | 34,214 ([2024 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872425000004/amzn-20241231.htm)) | 38,325 ([2025 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm)) |
| Year-end net PP&E | 204,177 ([2023 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872424000008/amzn-20231231.htm)) | 252,665 ([2024 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872425000004/amzn-20241231.htm)) | 357,025 ([2025 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm)) |
| Shareholders' equity | 201,875 ([2023 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872424000008/amzn-20231231.htm)) | 285,970 ([2024 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872425000004/amzn-20241231.htm)) | 411,065 ([2025 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm)) |

Gross profit is revenue less cost of sales. **SG&A means sales and marketing plus general and administrative**, consistently: 44,370 + 11,816 = 56,186; 43,907 + 11,359 = 55,266; 47,129 + 11,172 = 58,301. Fulfillment and technology/infrastructure remain additional operating costs. Amazon does not present a separate gross-profit subtotal; its cost classification is different from a conventional retailer's. Sources: Operations, pp.38/37/37 in the [2023](https://www.sec.gov/Archives/edgar/data/1018724/000101872424000008/amzn-20231231.htm), [2024](https://www.sec.gov/Archives/edgar/data/1018724/000101872425000004/amzn-20241231.htm), and [2025](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm) filings.

### Two manual checks — confirmed by the student

1. **FY2025 gross cash purchases of PP&E: $131,819 million.** Open the [2025 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm), Item 8, Consolidated Statements of Cash Flows, printed p.36, FY2025 column, “Purchases of property and equipment.” It is a cash outflow, shown in parentheses. It is not the $128,320 million net-capex number.
2. **December 31, 2025 net PP&E: $357,025 million.** In the same filing, Item 8, Consolidated Balance Sheets, printed p.39, FY2025 column, “Property and equipment, net.” Note 3, p.54, independently shows 534,098 gross less 177,073 accumulated depreciation = 357,025.

**Student confirmation:** “I personally checked Amazon’s 2025 SEC filing and confirmed that page 36 reports $131.819 billion of property and equipment purchases and page 39 reports $357.025 billion of net property and equipment.” The student explicitly confirmed in the conversation that these manual checks and the partner exchange actually occurred.

## Ratios and organic-growth evidence

| Metric | FY2023 | FY2024 | FY2025 |
| --- | --- | --- | --- |
| Gross margin | 46.98% | 48.85% | 50.29% |
| SG&A / gross profit | 20.81% | 17.73% | 16.17% |
| Inventory days (year-end) | 39.91 | 38.27 | 39.25 |
| PP&E depreciation ($m) | 30,225.00 | 32,067.00 | 41,860.00 |
| D&A / year-end net PP&E | 14.80% | 12.69% | 11.72% |
| Gross cash capex ($m) | 52,729.00 | 82,999.00 | 131,819.00 |
| Sales/incentives ($m) | 4,596.00 | 5,341.00 | 3,499.00 |
| Net cash capex ($m) | 48,133.00 | 77,658.00 | 128,320.00 |
| Provider CapEx field ($m) | 48,133.00 | 77,658.00 | 128,320.00 |
| Effective tax rate | 18.96% | 13.50% | 19.61% |
| Reported sales growth, calculated | 11.83% | 10.99% | 12.38% |
| Disclosed constant-currency growth | 12% | 11% | 12% |
| AWS reported sales growth | 13% | 19% | 20% |
| True organic/same-store growth | NOT DISCLOSED | NOT DISCLOSED | NOT DISCLOSED |

Sources: the corresponding annual filings and exact locators in [amazon_history.csv](amazon_history.csv); provider row from [MarketBeat, Annual Financial Ratios, Capital Expenditures (CapEx)](https://www.marketbeat.com/stocks/NASDAQ/AMZN/financials/), retrieved September 24, 2026. Gross margin = (sales − cost of sales)/sales; inventory days = year-end inventory/cost of sales ×365; depreciation ratio = PP&E D&A/year-end **net** PP&E; tax = provision/pretax income. Year-end ratios are simple course conventions, not average-balance turnover measures.

The provider shows **48,133 / 77,658 / 128,320**, matching gross cash purchases **52,729 / 82,999 / 131,819** less sales/incentives **4,596 / 5,341 / 3,499**. There is no unexplained data conflict: the definitions differ. The forecast uses **net cash capital spending** on the same basis as Amazon's MD&A. Noncash finance leases and changes in unpaid capital equipment are separate PP&E additions. The provider's other classifications are not used as Amazon facts. [Annual cash-flow statements](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm); [Q2 2026 MD&A cash-capex definition](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000026/amzn-20260630.htm).

Organic growth means growth from existing operations excluding acquired/divested businesses; constant-currency growth also removes FX, but is not automatically organic. Searches of all three MD&A sections for organic, comparable, same-store, unit sales, and customer usage found **no true consolidated organic/same-store growth percentage**. This is “NOT DISCLOSED,” not an estimated number or an unresolved reported line. The closest evidence is the constant-currency table and discussion of higher retail unit sales and AWS customer usage; AWS reported growth was 13%, 19%, and 20%. [2023 Item 7](https://www.sec.gov/Archives/edgar/data/1018724/000101872424000008/amzn-20231231.htm); [2024 Item 7](https://www.sec.gov/Archives/edgar/data/1018724/000101872425000004/amzn-20241231.htm); [2025 Item 7](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm). Q2 2026 reports 18% H1 consolidated growth, 17% excluding FX, and 33% H1 AWS growth. These do not establish acquisition-adjusted organic growth. [Q2 Item 2, Net Sales](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000026/amzn-20260630.htm).

The ABG tutorial's 1.8% judgment differs from its 4.7% reported growth because the latter can include acquired operations; Amazon gets its own 16%→8% forecast instead. This comparison is **TRAINING / VALIDATION ONLY**, not an Amazon input. [Part 1 captions](https://github.com/CinderZhang/FIN43900-Fall2026/blob/6bcbc3c929de59c547b2e421fe0f4ef2dc5d564f/lessons/week-05/pro-forma-abg-tutorial/video-1-captions.vtt).

## Labeled assumptions — single input register

The model reads [amazon_assumptions.csv](amazon_assumptions.csv) directly. This table is a readable snapshot of that register. Arrays run 2026–2030; `capex_later` runs 2027–2030. Monetary values are $m; shares are millions; rates are decimals. Historical ratios carried forward become **judgments**, because continuing history is a choice. The three key operating judgments are revenue growth, gross margin, and SG&A/gross profit; **capital spending and access to funding are additional major drivers for Amazon**.

| Assumption | Value | Label | Reason | Exact source or calculation |
| --- | --- | --- | --- | --- |
| opening_revenue | 716924 | history | Audited FY2025 opening balance; reported statement line, not a balancing plug | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Item 8 pp37,39; Consolidated Balance Sheets (revenue: Operations) |
| opening_cash | 86810 | history | Audited FY2025 opening balance; reported statement line, not a balancing plug | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Item 8 pp37,39; Consolidated Balance Sheets (revenue: Operations) |
| opening_securities | 36219 | history | Audited FY2025 opening balance; reported statement line, not a balancing plug | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Item 8 pp37,39; Consolidated Balance Sheets (revenue: Operations) |
| opening_inventory | 38325 | history | Audited FY2025 opening balance; reported statement line, not a balancing plug | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Item 8 pp37,39; Consolidated Balance Sheets (revenue: Operations) |
| opening_receivables | 67729 | history | Audited FY2025 opening balance; reported statement line, not a balancing plug | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Item 8 pp37,39; Consolidated Balance Sheets (revenue: Operations) |
| opening_ppe | 357025 | history | Audited FY2025 opening balance; reported statement line, not a balancing plug | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Item 8 pp37,39; Consolidated Balance Sheets (revenue: Operations) |
| opening_operating_rou | 86054 | history | Audited FY2025 opening balance; reported statement line, not a balancing plug | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Item 8 pp37,39; Consolidated Balance Sheets (revenue: Operations) |
| opening_goodwill | 23273 | history | Audited FY2025 opening balance; reported statement line, not a balancing plug | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Item 8 pp37,39; Consolidated Balance Sheets (revenue: Operations) |
| opening_other_assets | 122607 | history | Audited FY2025 opening balance; reported statement line, not a balancing plug | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Item 8 pp37,39; Consolidated Balance Sheets (revenue: Operations) |
| opening_trade_payables | 94909 | history | Audited FY2025 opening balance; 121909 total AP - 27000 capital AP (Note 3; reported $27.0bn rounded) | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Item 8 pp37,39; 121909 total AP - 27000 capital AP (Note 3; reported $27.0bn rounded) |
| opening_capex_payables | 27000 | history | Audited FY2025 opening balance; Note 3 p54: $27.0bn capital AP, reported rounded | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Item 8 pp37,39; Note 3 p54: $27.0bn capital AP, reported rounded |
| opening_operating_accruals | 57760 | history | Audited FY2025 opening balance; 75520 accrued - 14199 current leases - 2748 current debt - 455 short debt - 358 financing obligations | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Item 8 pp37,39; 75520 accrued - 14199 current leases - 2748 current debt - 455 short debt - 358 financing obligations |
| opening_unearned | 20576 | history | Audited FY2025 opening balance; reported statement line, not a balancing plug | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Item 8 pp37,39; Consolidated Balance Sheets (revenue: Operations) |
| opening_operating_lease | 89252 | history | Audited FY2025 opening balance; Note 4 p55: 89252 present value, current plus long term | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Item 8 pp37,39; Note 4 p55: 89252 present value, current plus long term |
| opening_finance_lease | 12286 | history | Audited FY2025 opening balance; Note 4 p55: 12286 present value, current plus long term | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Item 8 pp37,39; Note 4 p55: 12286 present value, current plus long term |
| opening_financing_obligation | 8158 | history | Audited FY2025 opening balance; Note 7 p59: 358 current + 7800 long-term (latter reported $7.8bn rounded) | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Item 8 pp37,39; Note 7 p59: 358 current + 7800 long-term (latter reported $7.8bn rounded) |
| opening_debt | 68851 | history | Audited FY2025 opening balance; Note 6 pp58-59: 65648 long-term + 2748 current + 455 short-term; carrying values | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Item 8 pp37,39; Note 6 pp58-59: 65648 long-term + 2748 current + 455 short-term; carrying values |
| opening_other_liabilities | 28185 | history | Audited FY2025 opening balance; 35985 other long-term liabilities - 7800 financing obligations | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Item 8 pp37,39; 35985 other long-term liabilities - 7800 financing obligations |
| opening_equity | 411065 | history | Audited FY2025 opening balance; reported statement line, not a balancing plug | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Item 8 pp37,39; Consolidated Balance Sheets (revenue: Operations) |
| opening_revolver | 0 | history | Audited FY2025 opening balance; Note 6 p59: zero draw under $15bn committed revolver | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Item 8 pp37,39; Note 6 p59: zero draw under $15bn committed revolver |
| growth | [0.16, 0.14, 0.12, 0.1, 0.08] | judgment | Moderate the H1 2026 18% reported growth toward 8% as Amazon gets larger; AWS strength supports growth above 2025 early in the forecast, not forever. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000026/amzn-20260630.htm ; Item 2 Net Sales: H1 2026 18%, AWS 33%; 2025 Item 7 12% consolidated |
| gross_margin | [0.51, 0.52, 0.53, 0.535, 0.54] | judgment | Service and AWS mix can lift the 2025 50.29% margin gradually; this is a cost-of-sales margin, not an AWS margin. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; p37: (716924-356414)/716924; Item 7 Net Sales |
| sga_to_gp | [0.16, 0.158, 0.156, 0.154, 0.152] | judgment | Small scale efficiencies from 2025 16.17% of gross profit; retain substantial marketing and corporate costs. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; p37: (47129+11172)/(716924-356414) |
| other_cost_ratio | 0.23205807031149744 | judgment | Hold the 2025 consolidated residual cost ratio; remove PPE D&A and fixed operating lease cost here before adding their explicit schedules, avoiding double counting. No claimed functional allocation. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; pp37,55,71: (fulfillment + technology + other operating - PPE D&A - fixed operating lease cost)/revenue |
| depreciation_rate | 0.15 | judgment | Use 15% of opening net PPE: above FY2025 11.72%, close to annualized H1 2026 D&A/opening PPE of 14.96%, recognizing new infrastructure entering service. This composite rate is not a claimed server useful life. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000026/amzn-20260630.htm ; Note 8 Segment Information: H1 PPE D&A26703; 2*26703/357025 = 14.96%; FY2025 Note 10 p71 |
| capex_2026_guidance | 220000 | guidance | Latest management cash-capex outlook; replaces earlier $200bn. A third-party transcript of management remarks, cross-checked against AP reporting. | https://earningscalls.dev/transcripts/amazon-com-inc_amzn_earnings_call_transcript_2026-07-30 ; July 30 2026 Andy Jassy cash-capex remarks; https://apnews.com/article/b4ce02b4666a35b8975823c5c22072ee |
| capex_later | [230000, 220000, 210000, 200000] | judgment | Keep spending elevated in 2027 then reduce slowly as installed capacity monetizes. This is the main uncertain judgment, not management guidance for 2027-30. | https://earningscalls.dev/transcripts/amazon-com-inc_amzn_earnings_call_transcript_2026-07-30 ; management describes capacity constraints into 2027; latest 10-Q Item 2 cash capex H1 96310 = 98411 - 2101 |
| tax_rate | 0.22 | judgment | Above 2025 19.61% and the unusually low 2024 rate; a normalized provision and cash-tax approximation, not a forecast of tax benefits from investment gains. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; pp37,63-66 Note 9; 19087/97311 |
| inventory_days | 39.24824782415954 | judgment | Hold the latest inventory-days efficiency; no dealer floor-plan funding. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; pp37,39: 38325/356414*365 |
| receivables_ratio | 0.09447165947855003 | judgment | Hold receivables and other current assets at the FY2025 revenue ratio; simplifies restricted cash and prepaid subaccounts. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; pp37,39: 67729/716924 |
| trade_payable_ratio | 0.26628864186030854 | judgment | Hold operating supplier funding relative to cost of sales; remove unpaid capital equipment from trade AP first. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; pp37,39,54: (121909-27000)/356414 |
| accrual_ratio | 0.08056641987156239 | judgment | Hold non-debt, non-lease operating accruals relative to sales after separating financing balances. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; p39 and Notes 4,6,7; 57760/716924 |
| unearned_ratio | 0.02870039223125464 | judgment | Hold current customer prepayments as a share of revenue; this reflects Prime/AWS prepayments without guessing bookings conversion. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; p39 and Note 1 Unearned Revenue |
| capex_payable_ratio | 0.21041147132169577 | judgment | Hold capital suppliers payable relative to NET cash capex. PPE additions include the change; CFO excludes this non-operating payable. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Note 3 p54; p36 net cash capex = 131819-3499 |
| finance_lease_addition | 2911 | judgment | Hold annual new finance-lease equipment near FY2025; Amazon still buys most infrastructure for cash. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Note 1 Supplemental Cash Flow Information: 2911 |
| finance_lease_principal_rate | 0.12567149601172065 | judgment | Use opening current finance-lease principal / total liability as annual paydown rate; a simplified amortization schedule. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Note 4 p55: 1544/12286 |
| finance_lease_rate | 0.034 | history | FY2025 weighted-average finance-lease discount rate; applied to opening forecast liability. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Note 4 p55 |
| operating_lease_rate | 0.037 | history | FY2025 weighted-average operating-lease discount rate used for simplified liability accretion. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Note 4 p55 |
| rou_amortization_rate | 0.12438324772817068 | judgment | Proxy ROU reduction: fixed lease cost less opening liability accretion, divided by opening ROU. Forecast lease cash equals lease expense; not a reported amortization number. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; p39 and Note 4 p55: (14006-89252*3.7%)/86054 |
| rou_growth | 0.05 | judgment | Expand leased capacity more slowly than sales because the forecast cash-capex program supplies most new infrastructure. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; p39 ROU 76141 to 86054; Note 4 p55 |
| financing_rate | 0.029 | history | Reported weighted-average imputed rate for facilities financing obligations; opening balance convention. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Note 7 p59 |
| financing_payments | [577, 582, 592, 601, 612] | history | Existing financing-obligation contractual cash payments including interest; separate principal in model. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Note 7 p59 contractual commitments table FY2026-30 |
| new_financing_obligations | 0 | judgment | No additional build-to-suit financing obligations forecast; new investment is cash-funded or explicitly finance-leased. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Note 7 p59 existing obligations; no forecast commitment invented |
| debt_net_change | [64246, 25000, 0, 0, 0] | judgment | Carry observed H1 2026 net issuance into 2026; issue $25bn additional term debt in 2027 to fund planned infrastructure, then refinance maturities without net growth. This finite funding assumption is below H1 2026 net issuance but requires market access; cash proceeds approximate carrying changes, excluding FX/discount. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000026/amzn-20260630.htm ; p3 six-month proceeds 66998 minus repayments 2752; Note 5 debt; 2027 amount is analyst judgment |
| securities_liquidity_floor | 0 | judgment | Sell liquid marketable securities at book value as needed before drawing the revolver; no sale gains or losses assumed. Do not liquidate private strategic holdings in other assets. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; p39 marketable securities36219; Note 2 Cash, Cash Equivalents, and Marketable Securities |
| debt_rate | 0.045 | judgment | Blended financing rate within the disclosed new/legacy note rates; charge average term debt to include first-year issuance. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000026/amzn-20260630.htm ; Note 5 Debt; FY2025 Note 6 effective rates span roughly 1.1%-5.6% |
| cash_yield | 0.03 | judgment | Modest return on opening cash and marketable securities, below FY2025 interest-income yield; no investment revaluation gains assumed. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; p37 interest income 4381; p39 cash+securities 123029 |
| other_income | 0 | judgment | Do not repeat investment mark-up gains as recurring earnings; FY2025 other income was 15229. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; p37; Note 1 Investments |
| other_balance_growth | 0 | judgment | Hold goodwill, other assets, and residual long-term liabilities constant; content/intangible replacement spending equals amortization embedded in expenses. Excludes new strategic investments and fair-value changes. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; p39; Notes 1,5; latest Q2 investment purchases show this is a material limitation |
| cash_settled_compensation | true | judgment | Treat future employee stock-compensation expense already inside operating costs as cash replacement compensation; no SBC addback or new shares. This prevents free dilution benefits but is not actual Amazon compensation policy. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; p36 SBC19467; Note 8 stock awards |
| distributions | 0 | judgment | Retain cash during infrastructure expansion; no dividends or repurchases forecast. Existing shares remain fixed under the cash-compensation convention. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Note 8 p62 no 2023-25 repurchases; latest Q2 Note 6 no H1 repurchases |
| minimum_cash | 25000 | judgment | Maintain a $25bn unrestricted operating buffer rather than ABG's cash-light dealer assumption; below audited $86.8bn cash but not zero. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; p39 cash 86810; Item 7 liquidity risks; analyst scenario, not company guidance |
| revolver_limit | 15000 | judgment | Use only the disclosed $15bn committed facility; assume renewal after Nov2028, no unlimited lender funding. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Note 6 p59 $15bn facility; renewal remains a forecast judgment |
| revolver_rate | 0.055 | judgment | Round stressed funding cost; charge opening balances, assume draws/repayments at year-end to avoid circularity. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Note 6 benchmark plus 0.45%; 5.5% is a scenario, not observed SOFR |
| cost_of_equity | 0.1 | judgment | Require a round 10% equity return for uncertain cash conversion; test 9%-11%. This is not a claimed CAPM estimate or copied ABG calibration. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Item 1A business/investment risk; analyst required-return judgment |
| terminal_growth | 0.025 | judgment | Use restrained perpetual growth below the equity discount rate; only allow terminal value if sustainable FCFE is positive. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm ; Item 1A risks; long-run scenario, not management guidance |
| shares | 10786.313572 | fact | Latest 10-Q cover common shares outstanding on July22 2026, converted to millions; fixed denominator also used for price-times-shares comparison. | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000026/amzn-20260630.htm ; cover: 10786313572 / 1000000 |
| market_price | 249.38 | fact | Regular-session close, September24 2026 16:00 EDT (UTC-4); retrieved September24 2026 20:47:04 UTC. After-hours quote also visible but not the selected observation. | https://stockanalysis.com/stocks/amzn/ ; quote header |
| first_year | 2026 | fact | Five full annual forecasts begin after latest audited year-end; valuation date convention is December31 2025, not a September2026 stub-period valuation. | Official Lab10 and audited FY2025 opening sheet |
| last_year | 2030 | fact | Five years; year-end discounting. | Official Lab10 |
| days_per_year | 365 | fact | Calendar-day inventory ratio convention. | Definition |
| positive_only | true | fact | Official Lab10 requires value only what is positive when FCFE is negative; cash statements still retain every negative flow. | Official Lab10 lines39-41; explicit course convention, not full signed-FCFE intrinsic value |

### Partner challenge and response — confirmed exchange

**Judgment challenged: capital spending.** My partner asked: “Why are you assuming Amazon’s capital spending will remain so high, and what would make you lower that assumption?”

**My two-sentence response:** “I kept Amazon’s capital spending elevated because its 2025 filing shows $131.819 billion of property and equipment purchases, and management expects continued technology-infrastructure investment to support AWS and AI growth. I would lower the assumption if later filings show that infrastructure spending is declining while Amazon can still maintain AWS growth and operating performance.”

**My challenge to my partner’s revenue-growth judgment:** “Why did you choose your revenue-growth assumption, and what evidence would make you lower it?”

The student supplied this wording and explicitly confirmed that the exchange actually occurred. This records the confirmed exchange; it does not assert attendance, a session token, or any other unconfirmed classroom activity.

## Amazon-specific investment and financing line

**AWS is not modeled separately:** this is one consolidated Amazon forecast and valuation. AWS evidence informs the assumptions, but there is no standalone AWS revenue, margin, capex, or valuation schedule.

Amazon has **no direct equivalent to dealer floor-plan debt**. Its distinctive modeling issue here is **technology infrastructure investment through PP&E, capital-equipment payables, and finance leases**, alongside facility financing obligations. This covers infrastructure and fulfillment; the consolidated filing does not let this model label every dollar “AI.” Net PP&E was $357,025m, including substantial servers/network equipment and construction in progress. Capital equipment acquired but unpaid was $27.0bn. Finance-lease assets are already in PP&E, whereas operating right-of-use assets are separately reported. [2025 Notes 3–4, pp.54–55](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm).

The opening balance sheet is reclassified, not changed: $121,909m AP becomes $94,909m operating AP + $27,000m capital AP. Accrued liabilities are separated into operating accruals, current leases, debt, and facility financing; current and long-term lease portions are combined in their dedicated schedules. The $7.8bn facility-financing long-term amount and $27.0bn capital AP are **reported rounded figures**; residual classifications retain the audited consolidated total. Reclassification uncertainty does not change total opening assets or liabilities. [2025 p.39 and Notes 3,4,6,7](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm).

PP&E ends at opening PP&E + net cash capex + change in capital AP + finance-lease additions + new facility-financing assets − depreciation. Capital AP changes are not also included in operating cash flow. Finance-lease additions increase PP&E and lease debt without cash; lease interest reduces income and principal reduces FCFE. Existing facility-financing payments are split between interest and principal. Operating leases have separate ROU, liability, expense, and cash schedules; interest accretion remains part of operating lease expense, not a second financing-interest charge. [Model implementation](amazon_proforma.py); [2025 Notes 3–4,7](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm).

Amazon embeds depreciation and rent in multiple operating expense functions. To avoid subtracting them twice, the model removes total PP&E D&A and fixed operating lease cost from the **consolidated residual operating-cost baseline** before adding explicit schedules. This is an algebraic consolidated reclassification, not a claim that all historical D&A belongs to fulfillment/technology. At the historical base, gross profit 360,510 − SG&A 58,301 − residual 166,368 − PPE D&A 41,860 − lease cost 14,006 = operating income 79,975. Forecast gross-margin and SG&A rows are simplified presentation drivers; no functional D&A allocation is asserted. [2025 pp.37,55,71](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm).

Other content/intangible amortization is treated as matched by replacement spending within the residual cost: there is no extra D&A addback without corresponding investment. Future stock compensation is treated as **cash replacement compensation**, retaining its expense with no SBC cash-flow addback and no new shares. That is an economic simplifying judgment, not Amazon's reported compensation policy. These choices make the course cash-flow statement different from a full GAAP forecast. [Assumption register](amazon_assumptions.csv); [2025 Notes 1,5,8](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm).

## Calculation order, cash, and financing

The order is income statement → noncash balance-sheet movements and financing schedules → operating/investing/financing cash flows and FCFE → **cash last** → checks → valuation. Ending cash is opening cash plus the three cash-flow subtotals. Equity is opening equity + net income − distributions. Neither is solved from the balance-sheet gap. [Code](amazon_proforma.py).

The initial funding specification failed the cash floor even though it balanced. The final scenario explicitly assumes $25bn net term issuance in 2027, liquidates marketable securities before using the $15bn revolver, and holds a $25bn cash minimum. This is a financing revision, not a higher earnings forecast or a hidden balance-sheet plug. It is supported only as a **conditional scenario** by Amazon's demonstrated H1 2026 net term proceeds of $64,246m; it is not announced 2027 borrowing guidance. Removing that 2027 issuance still causes a refusal in validation. [Q2 cash-flow statement p.3 and debt note](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000026/amzn-20260630.htm); [validation](lab10_validation.txt).

In the final base run, **no revolver draw is needed**: scheduled term financing and sales of liquid securities maintain the cash floor. A separate passing test reduces the 2027 term issuance to $15bn and verifies actual revolver drawing and later repayment; removing that issuance entirely exhausts funding and refuses valuation. The $15bn facility requires a renewal assumption beyond its November 2028 term. Interest uses average term debt and opening lease/revolver balances; revolver transactions are assumed at year-end. [2025 Note 6](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm); [model output](lab10_output.txt); [liquidity tests](lab10_validation.txt).

## Five-year statements

All amounts below are USD millions, rounded to one decimal only for display. Expense, capex, and principal rows are positive magnitudes; cash-flow subtotals carry their actual signs. Working-capital change is positive for investment and negative for a source of cash. Forecasts are **conditional scenarios**, not management forecasts.

### Income Statement

| USD millions | 2026 | 2027 | 2028 | 2029 | 2030 |
| --- | --- | --- | --- | --- | --- |
| revenue | 831,631.8 | 948,060.3 | 1,061,827.5 | 1,168,010.3 | 1,261,451.1 |
| cost of sales | 407,499.6 | 455,068.9 | 499,058.9 | 543,124.8 | 580,267.5 |
| gross profit | 424,132.2 | 492,991.4 | 562,768.6 | 624,885.5 | 681,183.6 |
| sga | 67,861.2 | 77,892.6 | 87,791.9 | 96,232.4 | 103,539.9 |
| other operating cost | 192,986.9 | 220,005.0 | 246,405.6 | 271,046.2 | 292,729.9 |
| depreciation | 53,553.8 | 81,850.9 | 104,825.5 | 122,222.7 | 135,510.4 |
| operating lease expense | 14,006.0 | 14,700.4 | 15,429.5 | 16,195.0 | 16,998.9 |
| operating income | 95,724.5 | 98,542.4 | 108,316.0 | 119,189.1 | 132,404.5 |
| interest income | 3,690.9 | 3,067.2 | 1,797.1 | 927.9 | 1,106.6 |
| debt interest | 4,543.8 | 6,551.9 | 7,114.4 | 7,114.4 | 7,114.4 |
| finance lease interest | 417.7 | 464.2 | 504.8 | 540.4 | 571.4 |
| financing interest | 236.6 | 226.7 | 216.4 | 205.5 | 194.0 |
| revolver interest | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| interest expense | 5,198.1 | 7,242.8 | 7,835.6 | 7,860.2 | 7,879.8 |
| other income | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| pretax income | 94,217.2 | 94,366.8 | 102,277.5 | 112,256.8 | 125,631.3 |
| income tax | 20,727.8 | 20,760.7 | 22,501.0 | 24,696.5 | 27,638.9 |
| net income | 73,489.4 | 73,606.1 | 79,776.4 | 87,560.3 | 97,992.4 |

### Balance Sheet

| USD millions | 2026 | 2027 | 2028 | 2029 | 2030 |
| --- | --- | --- | --- | --- | --- |
| cash | 66,022.2 | 25,000.0 | 25,000.0 | 30,957.1 | 69,208.9 |
| securities | 36,219.0 | 34,901.8 | 5,929.2 | 5,929.2 | 5,929.2 |
| inventory | 43,818.2 | 48,933.3 | 53,663.5 | 58,401.9 | 62,395.8 |
| receivables | 78,565.6 | 89,564.8 | 100,312.6 | 110,343.9 | 119,171.4 |
| ppe | 545,672.8 | 698,837.0 | 814,818.3 | 903,402.5 | 968,699.0 |
| operating rou | 90,356.7 | 94,874.5 | 99,618.3 | 104,599.2 | 109,829.1 |
| goodwill | 23,273.0 | 23,273.0 | 23,273.0 | 23,273.0 | 23,273.0 |
| other assets | 122,607.0 | 122,607.0 | 122,607.0 | 122,607.0 | 122,607.0 |
| total assets | 1,006,534.5 | 1,137,991.4 | 1,245,221.9 | 1,359,513.6 | 1,481,113.4 |
| trade payables | 108,512.5 | 121,179.7 | 132,893.7 | 144,628.0 | 154,518.6 |
| capex payables | 46,290.5 | 48,394.6 | 46,290.5 | 44,186.4 | 42,082.3 |
| operating accruals | 67,001.6 | 76,381.8 | 85,547.6 | 94,102.4 | 101,630.6 |
| unearned | 23,868.2 | 27,209.7 | 30,474.9 | 33,522.4 | 36,204.1 |
| operating lease | 93,554.7 | 98,072.5 | 102,816.3 | 107,797.2 | 113,027.1 |
| finance lease | 13,653.0 | 14,848.2 | 15,893.2 | 16,806.9 | 17,605.7 |
| financing obligation | 7,817.6 | 7,462.3 | 7,086.7 | 6,691.2 | 6,273.3 |
| debt | 133,097.0 | 158,097.0 | 158,097.0 | 158,097.0 | 158,097.0 |
| revolver | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| other liabilities | 28,185.0 | 28,185.0 | 28,185.0 | 28,185.0 | 28,185.0 |
| total liabilities | 521,980.1 | 579,830.9 | 607,284.9 | 634,016.4 | 657,623.8 |
| equity | 484,554.4 | 558,160.5 | 637,936.9 | 725,497.2 | 823,489.6 |
| liabilities equity | 1,006,534.5 | 1,137,991.4 | 1,245,221.9 | 1,359,513.6 | 1,481,113.4 |

### Cash Flow / Equity Cash Flow

| USD millions | 2026 | 2027 | 2028 | 2029 | 2030 |
| --- | --- | --- | --- | --- | --- |
| net income | 73,489.4 | 73,606.1 | 79,776.4 | 87,560.3 | 97,992.4 |
| depreciation | 53,553.8 | 81,850.9 | 104,825.5 | 122,222.7 | 135,510.4 |
| change operating wc | -9,807.4 | -9,274.6 | -8,667.0 | -8,566.8 | -7,279.2 |
| operating cash flow | 136,850.6 | 164,731.7 | 193,269.0 | 218,349.9 | 240,782.0 |
| capex | 220,000.0 | 230,000.0 | 220,000.0 | 210,000.0 | 200,000.0 |
| change other net assets | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| securities sale | 0.0 | 1,317.2 | 28,972.6 | 0.0 | 0.0 |
| investing cash flow | -220,000.0 | -228,682.8 | -191,027.4 | -210,000.0 | -200,000.0 |
| debt net change | 64,246.0 | 25,000.0 | 0.0 | 0.0 | 0.0 |
| finance lease principal | 1,544.0 | 1,715.8 | 1,866.0 | 1,997.3 | 2,112.1 |
| financing principal | 340.4 | 355.3 | 375.6 | 395.5 | 418.0 |
| fcfe before revolver | -20,787.8 | -42,339.4 | -28,972.6 | 5,957.1 | 38,251.9 |
| revolver draw | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| revolver repayment | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| fcfe | -20,787.8 | -42,339.4 | -28,972.6 | 5,957.1 | 38,251.9 |
| distributions | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| financing cash flow | 62,361.6 | 22,928.9 | -2,241.6 | -2,392.8 | -2,530.1 |
| opening cash | 86,810.0 | 66,022.2 | 25,000.0 | 25,000.0 | 30,957.1 |
| net cash change | -20,787.8 | -41,022.2 | -0.0 | 5,957.1 | 38,251.9 |
| cash | 66,022.2 | 25,000.0 | 25,000.0 | 30,957.1 | 69,208.9 |

### Noncash Investment And Lease Schedule

| USD millions | 2026 | 2027 | 2028 | 2029 | 2030 |
| --- | --- | --- | --- | --- | --- |
| change capex payables | 19,290.5 | 2,104.1 | -2,104.1 | -2,104.1 | -2,104.1 |
| finance lease addition | 2,911.0 | 2,911.0 | 2,911.0 | 2,911.0 | 2,911.0 |
| financing addition | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| ppe additions | 242,201.5 | 235,015.1 | 220,806.9 | 210,806.9 | 200,806.9 |
| operating lease addition | 15,006.4 | 15,756.7 | 16,544.5 | 17,371.8 | 18,240.3 |
| rou amortization | 10,703.7 | 11,238.9 | 11,800.8 | 12,390.8 | 13,010.4 |
| operating lease accretion | 3,302.3 | 3,461.5 | 3,628.7 | 3,804.2 | 3,988.5 |
| operating lease cash | 14,006.0 | 14,700.4 | 15,429.5 | 16,195.0 | 16,998.9 |


## Checks and deliberate break test

The tolerance is **$0.000001 million ($1)**. All gap rows must be zero within tolerance, liquidity headroom must be nonnegative, assets/financing balances must be nonnegative, and each opening balance must equal the preceding close. `value_equity()` calls `assert_balanced()` first. All figures below are recomputed checks, not hard-coded zeros. [Executed output](lab10_output.txt).

| Check ($m) | 2026 | 2027 | 2028 | 2029 | 2030 |
| --- | --- | --- | --- | --- | --- |
| balance gap | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| cash gap | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| fcfe gap | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| securities gap | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| ppe gap | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| capital ap gap | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| debt gap | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| finance lease gap | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| financing gap | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| rou gap | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| operating lease gap | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| equity gap | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| revolver gap | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| cash headroom | 41,022.2 | 0.0 | 0.0 | 5,957.1 | 44,208.9 |
| revolver headroom | 15,000.0 | 15,000.0 | 15,000.0 | 15,000.0 | 15,000.0 |

The deliberate run `python -B lab10/amazon_proforma.py --break-cash` temporarily replaces FY2026 computed cash **66,022.2** with opening cash **86,810.0** in memory. It must exit 1 with **FY2026 balance_gap = 20787.8 million; valuation refused**. The gap is 86,810.0 − 66,022.2 = 20787.8; it differs from ABG's −61.4 because these are Amazon cash flows. No valuation is printed. A fresh normal run restores the computed cash, exits 0, and reproduces the original output; the Python file hash remains unchanged. [Saved refusal and restoration evidence](lab10_validation.txt).

The independent script rebuilds every financial output using 40-digit Decimal arithmetic, verifies historical fixtures and ratio calculations, checks all roll-forwards, mutates each important balance to verify refusal, tests exhausted funding, and tests a negative sustainable terminal flow. It also verifies share-count arithmetic, discount/margin sensitivities, output reproducibility, the required disclosure, and all 19 original hashes. The validation log reports the executed test count. Default validation certifies computation, **not personal checkout completion**; `--submission-ready` also checks that the required partner/manual sections are no longer pending; the personal completion evidence is the student’s explicit confirmation, not the software itself. [Validation script](validate_lab10.py).

## One course valuation and dated market comparison

Negative FCFE remains in **2026, 2027, and 2028**; it is not silently removed from the cash roll-forward. FCFE available from operations and financing excludes selling the existing marketable-securities reserve, which funds retained liquidity rather than a shareholder distribution here. The official course instruction says to value only positive flows, so explicit PV uses `max(FCFE, 0)`. **This omits $75,656.81m of discounted negative flows and is not a complete signed-flow intrinsic valuation.** No opening excess-cash/private-investment value is added separately. [Official rule](https://github.com/CinderZhang/FIN43900-Fall2026/blob/6bcbc3c929de59c547b2e421fe0f4ef2dc5d564f/lessons/week-05/lab-10-proforma-your-company.md); [output](lab10_output.txt).

- Explicit positive FCFE PV = Σ max(FCFE_t, 0)/(1.10)^t = **$27,820.16m**.
- Terminal-eligible proxy = FY2030 FCFE before temporary revolver movements and new term borrowing = **$38,251.88m**. Recurring lease/facility principal is retained as a cost.
- Terminal value = 38,251.88 × 1.025 / (0.10 − 0.025) = **$522,775.72m** at year-end 2030; PV = **$324,602.59m**.
- Equity value = explicit PV + terminal PV = **$352,422.75m**; divide by **10,786.313572m** common shares = **$32.67 per share**.
- Terminal share = **92.11%**. A negative sustainable FCFE cannot support a meaningful positive going-concern perpetuity under this formula; the code refuses it instead of printing a misleading terminal number.

The model says **$32.67 per share**, while the market says **$249.38 as of September 24, 2026, 16:00 EDT**, using the same disclosed share-count basis. [Stock Analysis quote](https://stockanalysis.com/stocks/amzn/), regular-session close, retrieved **2026-09-24 20:47:04 UTC / 16:47:04 EDT**. The page also showed $248.97 after-hours at 16:41 EDT; the selected observation is the regular-session close, not that after-hours trade.

The denominator is the latest 10-Q cover's **10,786,313,572 common shares outstanding July 22, 2026**, converted to millions; both model value and price-times-shares use it. Market-equity comparison is $249.38 × 10,786.313572m = **$2,689,890.88m**. This is a fixed-share economic scenario, not the FY2025 weighted-average diluted EPS denominator. It does not predict future share issuance. [10-Q cover](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000026/amzn-20260630.htm).

The forecast starts at December 31, 2025 and discounts five full years, using information available September 24, 2026. **It is not a September 24 stub-period valuation**; the model-versus-market gap therefore also contains a timing mismatch. The difference is a question about cash conversion, investment intensity, funding, and terminal assumptions—not an investment recommendation.

| Required equity return | Sensitivity value/share |
| --- | --- |
| 9% | $39.04 |
| 10% | $32.67 |
| 11% | $27.85 |

These are sensitivities around one base case, not additional selected base valuations. The validation also tests +0.5 percentage point gross margins and a 10% increase in post-2026 capex. The latter exhausts the stated liquidity policy and is reported as a refusal rather than a forced price. [Validation results](lab10_validation.txt).

## Interpretation, uncertainty, and continuing decision

The central uncertainty is **when AWS/AI infrastructure spending becomes cash available to shareholders**. The scenario assumes capex reaches $230bn in 2027 and declines to $200bn by 2030 even as revenue grows. Keeping capex high longer, losing refinancing access, weaker margins, or shorter equipment lives could change the result substantially. The 15% depreciation rate uses recent H1 expense evidence but is not a vintage-level asset schedule. [Assumptions](amazon_assumptions.csv); [Q2 segment D&A and MD&A](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000026/amzn-20260630.htm).

The latest reported guidance is approximately $220bn cash capex for 2026, replacing the older $200bn figure. It comes from management's July 30 remarks as reproduced in the [earnings-call transcript](https://earningscalls.dev/transcripts/amazon-com-inc_amzn_earnings_call_transcript_2026-07-30), cross-checked with [AP](https://apnews.com/article/b4ce02b4666a35b8975823c5c22072ee). Annual filings remain the primary history source; a transcript host is identified honestly as a secondary carrier of management guidance.

Other important limits are the consolidated retail/cloud mix, aggregate D&A reclassification, constant residual assets, tax provision treated as cash tax, and cash replacement of stock compensation. Large strategic investments and fair-value gains after the audited opening date are **not** modeled. For example, the latest filing reports H1 acquisition/investment cash outflows of about $39.8bn; leaving those out can materially overstate available liquidity, and additional financing would be needed if repeated on top of this scenario. This makes the model a deliberately limited operating/infrastructure scenario, not a complete prediction of FY2026 financial statements. [Q2 cash-flow statement and MD&A](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000026/amzn-20260630.htm).

Over 92.1% of course value depends on the positive 2030 proxy continuing. Positive FCFE is necessary for the formula, but does not prove a sustainable steady state: the model does not separately rebuild 2031 replacement capex, competitive returns, or asset vintages. The course positive-only convention also removes the economic charge for negative early flows from valuation. These limits are reasons to question the result rather than call the market wrong.

The student's existing **watch-defer** conclusion remains: wait for stronger evidence that operating cash generation can cover infrastructure spending and financing costs. A concrete metric to monitor is **trailing-twelve-month operating cash flow minus net cash PP&E purchases and finance-lease/facility principal payments**, alongside the amount funded by new debt. Sustained improvement without greater funding dependence would support revisiting the judgment. This is a coursework decision call, not financial advice. The large difference from Lab 06's preserved **$5.9930** reflects a five-year FCFE model, separate financing, different capex/margin paths, and the positive-only rule; Lab 06 has not been changed to match it. [Lab 06](../lab06/lab06.md); [Lab 08](../lab08/lab08.md); [model](amazon_proforma.py).

For the live reflection, the capex taper is the judgment most worth defending and challenging: the spending must ultimately earn cash returns, but the timetable is uncertain. The history figure worth discussing is gross PP&E purchases of $131.819bn in 2025 versus $82.999bn in 2024, a sharp increase. These are preparation notes for the live reflection; only the separate partner exchange recorded above has been confirmed. [2025 cash-flow statement p.36](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm).

## Public merit-criteria review and checkout status

| Criterion | Evidence | Status |
| --- | --- | --- |
| History and sources | Three own-year 10-Ks; every grid item sourced; overlap reconciled; provider definition checked | Complete; **both student manual checks confirmed** |
| Assumptions and labels | One 62-row CSV register, table snapshot, labels, reasons, sources, independent formula tests | Complete labeled set; AI assistance disclosed; student’s capital-spending defense recorded |
| Statements and checks | Five statements, all balances/roll-forwards/floors, refusal and restored run, valuation guard | Computational checks pass; see executed log |
| Personalization | Infrastructure PP&E, capital AP, two lease types, financing obligations, explicit financing and dilution conventions | Complete with disclosed simplifications |
| Partner review | Exact challenge, two-sentence answer, and student's specific challenge required | Complete; actual exchange explicitly confirmed by student |

All five public merit criteria have corresponding evidence in this package, including the student-confirmed manual checks and partner exchange. This is a completeness review, not a claim of an instructor-awarded 25/25 score. Final validation reruns the model, submission-readiness checks, and preservation hashes before committing only `lab10/`. Retain the Lab 09 chat and complete any live explanation/reflection or Brightspace submission the instructor requires; no token or attendance is asserted.

## AI-use disclosure

I used **Codex** to help **research and organize Amazon's SEC filing data**, **adapt and debug the Python three-statement model**, **create independent validation tests**, and **draft this report**. Codex also ran the scripts and checked the output and preservation hashes. The forecast assumptions were developed with AI assistance; my previously stated watch-defer judgment is preserved. I supplied the capital-spending response above and confirmed that I completed the partner exchange and personally checked the two specified filing figures. This disclosure does not claim that I independently completed the AI-assisted research, coding, tests, or drafting, or that I confirmed a separate comprehensive review of every model input. The judgment labels, financial judgments I adopt, and final submission are my responsibility.
