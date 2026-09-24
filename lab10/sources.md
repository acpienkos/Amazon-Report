# Lab 10 source and reproducibility register

All filing data were retrieved directly from SEC EDGAR on September24 2026. Dollar amounts are USD millions unless explicitly shown as a reported rounded billion-dollar number. Forecasts are judgments, not reported facts. [History CSV](amazon_history.csv) is the row-level source ledger; [assumption CSV](amazon_assumptions.csv) is the sole financial input register.

## Official materials

Course revision: `6bcbc3c929de59c547b2e421fe0f4ef2dc5d564f`.

- [lab-10-proforma-your-company.md](https://github.com/CinderZhang/FIN43900-Fall2026/blob/6bcbc3c929de59c547b2e421fe0f4ef2dc5d564f/lessons/week-05/lab-10-proforma-your-company.md)
- [README.md](https://github.com/CinderZhang/FIN43900-Fall2026/blob/6bcbc3c929de59c547b2e421fe0f4ef2dc5d564f/lessons/week-05/README.md)
- [student-handout.md](https://github.com/CinderZhang/FIN43900-Fall2026/blob/6bcbc3c929de59c547b2e421fe0f4ef2dc5d564f/lessons/week-05/student-handout.md)
- [student-prework.md](https://github.com/CinderZhang/FIN43900-Fall2026/blob/6bcbc3c929de59c547b2e421fe0f4ef2dc5d564f/lessons/week-05/student-prework.md)
- [pro-forma-abg-tutorial/video-1-captions.vtt](https://github.com/CinderZhang/FIN43900-Fall2026/blob/6bcbc3c929de59c547b2e421fe0f4ef2dc5d564f/lessons/week-05/pro-forma-abg-tutorial/video-1-captions.vtt)

The complete Part1 captions were read, not only a summary. The lab explicitly requires provider-capex comparison, hand checks, a real partner exchange, positive-only treatment of negative FCFE, and individual GitHub checkout. No ABG company values are inputs to Amazon.

## SEC annual filings and locators

| Period | Direct SEC filing | Statements and notes |
| --- | --- | --- |
| 2023 | https://www.sec.gov/Archives/edgar/data/1018724/000101872424000008/amzn-20231231.htm | Item8 Operations p38; Cash Flows p37; Balance Sheets p40; Note10 consolidated PPE D&A p70; Item7 MD&A Net Sales |
| 2024 | https://www.sec.gov/Archives/edgar/data/1018724/000101872425000004/amzn-20241231.htm | Item8 Operations p37; Cash Flows p36; Balance Sheets p39; Note10 consolidated PPE D&A p69; Item7 MD&A Net Sales |
| 2025 | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm | Item8 Operations p37; Cash Flows p36; Balance Sheets p39; Note10 consolidated PPE D&A p71; Item7 MD&A Net Sales |

These are the three latest annual periods available at the analysis date, FY2023/FY2024/FY2025; the current interim filing is [June30 2026 10-Q](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000026/amzn-20260630.htm). Use fiscal period, not accession year, to identify history. Exact accessions appear in each URL. Annual report signatures are February1 2024, February6 2025, February5 2026; electronic filing dates may be the following day. The report does not confuse signature date with fiscal year.

History arithmetic uses Operations for revenue/COS/SG&A/NI/pretax/tax; Balance Sheets for inventory/PPE/equity; Cash Flows for gross PPE purchases and proceeds/incentives; Note10 for precise PPE D&A. Cash-flow D&A of 65,756 in 2025 includes content, operating leases, and other items and is **not** the 41,860 PPE depreciation used in the PPE roll-forward. Note3's $41.9bn agrees after rounding.

FY2025 opening assets 818,042 and equity411,065 are unaltered. Source details for liability splits: Note3 p54 (capital AP27000), Note4 p55 (operating lease89252, finance lease12286; current portions12655 and1544), Note6 pp58–59 (long-term65648,current2748,short455), Note7 p59 (facility financing358+7800, cash commitments577/582/592/601/612). The rounded figures are labeled as reported rounding; no estimated hidden precision is claimed.

## Comparative reconciliation

The 2023 own-year values were checked against the 2024 and 2025 comparative Operations/Cash Flows and Note10 D&A columns. The 2024 own-year values were checked against the 2025 comparative columns. 2023 inventory33318, PPE204177, equity201875 agree in the 2024 opening comparative balance sheet; 2024 inventory34214, PPE252665, equity285970 agree in the 2025 opening comparative balance sheet. No restatement differences were found in this history set. Every published historical checkpoint is independently transcribed in the validation fixture; derived ratios are recomputed there. This automated review does not replace the student's two manual checks.

## Current inputs and secondary cross-checks

- [Q2 2026 10-Q](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000026/amzn-20260630.htm), cover: 10,786,313,572 common shares July22; p3 cash flows: H1 term issuance66998 and repayment2752, gross PPE98411 and sales/incentives2101; Item2 sales: H1 revenue382125 and 18% growth; Note8 segment D&A26703; Note5 financing. Annualized D&A/openingPPE = 2×26703/357025 =14.96%, supporting the 15% forecast judgment.
- [July30 earnings-call transcript](https://earningscalls.dev/transcripts/amazon-com-inc_amzn_earnings_call_transcript_2026-07-30), Andy Jassy discussion of investment cycles and increased **$220bn cash capex**; secondary transcript carrier, not SEC filing. Cross-check: [AP report](https://apnews.com/article/b4ce02b4666a35b8975823c5c22072ee). Forecast later-year taper is NOT guidance.
- [MarketBeat annual financials](https://www.marketbeat.com/stocks/NASDAQ/AMZN/financials/), Annual Financial Ratios, Capital Expenditures (CapEx), FY2023 48133, FY2024 77658, FY2025 128320. These match net cash capex. Other provider fields are not accepted without source reconciliation.
- [Stock Analysis AMZN quote](https://stockanalysis.com/stocks/amzn/): selected $249.38 regular-session close September24 2026 16:00 EDT. Retrieved2026-09-24 20:47:04 UTC. Page also showed after-hours248.97 at16:41EDT. The selected price is fixed in the assumption register so rerunning code does not silently update the comparison.
- Prior [Lab06](../lab06/lab06.md), [Lab08](../lab08/lab08.md), [Lab09 model](../lab09/proforma.py). No edits to these sources.

## Download fingerprints and audit baseline

Raw SEC HTML was downloaded outside the repository for reading. SHA256 fingerprints below identify the exact retrieved documents; the linked filings remain the reproducible primary sources.

| Document | SHA256 |
| --- | --- |
| 2023 | 67711a7f373498a72f846308bdf539cfa93bbbb31892ac50424228a6e4eb3f3f |
| 2024 | 307d4b056a55e010f76b30f07925a985a08198ce0c86adc0380eaf48ed89f65e |
| 2025 | 89825b2a6a4410d91fdc925e6c1c84e1a06052d1df9ef68d0eaf4d2dcc5f9614 |
| q2 | 4e62f248ae8be4916fe5b835be2ee9545d0d8dfdcccbd0fae05e1b3859b46e39 |

Starting personal-repository commit: `347750c3bc4e8965b40312c5b18c1f49760a63d1`. The validation script embeds the 19 starting tracked-file SHA256 hashes and verifies its inventory against `git ls-tree` at that commit. It checks bytes, not just filenames or Git status. Prior model runs were executed before Lab10 creation and are rerun in final validation.

## Reproduce

From repository root, Python standard library only:

```text
python -B lab09/proforma.py
python -B lab06/dcf.py
python -B lab10/amazon_proforma.py
python -B lab10/amazon_proforma.py --break-cash
python -B lab10/validate_lab10.py
python -B lab10/validate_lab10.py --submission-ready
```

The break run must exit1; the correct run and default computational validator must exit0. Submission-ready validation must exit0 now that the student has explicitly confirmed the manual filing checks and supplied the authentic partner exchange. Those confirmations are documented in lab10.md. Saved stdout is UTF-8. Financial inputs have no network dependency; source data and market observation are frozen and dated. Git is used only for original-inventory verification.
