# Lab 19 — panel interpretation and checkout notes

**Question:** When three investors' skills read the same 10-K facts, where do they agree, where do they split — and would you trust the panel?

Codex prepared these written answers from the executed panel. They are drafts for Andrew to review; they do not document a partner conversation or a no-AI explanation.

## Company selection and evidence

The existing [Lab 14 proposed universe](../../lab14/README.md) lists BIL, IEF, LQD and VT. No confirmed Project 2 fund selection was found. For this autonomous run, **VT is the working assumption**, rather than an asserted personal selection. The [Schwab VT holdings page](https://www.schwab.wallst.com/Prospect/Research/etfs/portfolio.asp?symbol=vt), saved in `sources/VT-schwab-holdings.html`, lists NVIDIA (NVDA) first at **4.54%**, ahead of Apple at 4.11%, with portfolio details dated **September 30, 2026**. These are disclosed holdings, not live positions. Alphabet's two listed classes sum to less than NVIDIA's weight. Vanguard's public product page was retrieved but its HTML did not expose the individual holdings; the unusable Vanguard API URL initially returned 404. The successful public holdings-page fallback is documented, not presented as issuer-confirmed data.

NVDA files a 10-K; no next-largest substitution was needed. The actual SEC snapshot, retrieval time, SHA-256, tags, fiscal end dates and accession numbers are preserved. NVIDIA's printed fiscal ends are 2022-01-30 through 2026-01-25; these are its fiscal dates, not calendar years. Confirm VT as a Project 2 fund before representing the run as your actual fund selection; otherwise run the relevant company's panel using the same skills.

## Known answer and probe

COST reproduces all seven official checks: Buffett pass/pass/pass; Cathie Wood fail/not known; Burry pass/pass. CAGR is 7.51%; liabilities/equity is 2.11, 1.75, 1.96, 1.64 and 1.49; all R&D/revenue observations stay not found. The 35 original Lab 18 financial cells also match the official table.

`run_demo.py` temporarily changed Wood's actual skill `scripts/config.json` from 0.15 to 0.05 and executed the bundled skill on COST. Growth became pass; R&D stayed not known. The retained configuration is 0.15. Her memo records the reason: keep a consistent innovation-growth hurdle rather than tune it to rescue a company. `evidence/threshold_probe.txt` and `COST_probe_report.json` contain the actual run. Thresholds change classifications without changing the underlying business; lowering a hurdle is not new evidence.

## NVIDIA: agreement and disagreement

Buffett passes all three historical checks and returns **watch** pending business-durability work. Wood passes both checks and returns **own**, a conditional business-screen candidate based on 68.30% revenue CAGR and 8.57% latest R&D/revenue, with no price judgment. Burry passes latest leverage (0.31) but fails cash backing earnings and returns **watch**: latest OCF is 102,718 versus net income of 120,067, both USD millions. His cash test also fails on earlier observations. These are model-authored judgments after reading code output, not deterministic verdict mappings or statements by the real investors.

The panel shares facts but assigns different importance to earning power, growth/reinvestment and cash conversion. Agreement on a dataset is not independence of evidence; the perspectives can share the same extraction errors and omit the same risks. The simplified accounting checks do not establish a moat, technological disruption, fraud, hidden liabilities or future returns.

## Bull and bear — two sentences each

**Bull draft:** NVIDIA passes Buffett's profitability and owner-earnings checks, and its 68.30% revenue CAGR and 8.57% latest R&D/revenue pass Wood's growth and reinvestment screens. Latest liabilities/equity of 0.31 also passes Burry's leverage check, supporting further business research.

**Bear draft:** Burry's cash-conversion check fails, with latest operating cash flow of 102,718 below net income of 120,067 USD millions. The other passes do not explain that gap or establish durable future earning power, so I would investigate the filings before relying on the favorable business screen.

These are prepared arguments, **not a claim that a partner delivered either case**. Andrew still needs to perform the partner attack and swap if not already done.

## Decision — one line

**Only with a condition: I would use this panel to shortlist Project 2 research candidates only after verifying the fund holding and SEC inputs, and I would investigate NVIDIA's cash-versus-earnings gap and business durability before acting on its favorable screens.**

This is a suggested decision for Andrew's review; it does not replace his independent choice.

## Explain the code — preparation for the required no-AI activity

Open `panel.py:cathie_checks`. It reads only the latest row's R&D/revenue, or uses `None` if no row exists. `result` maps a missing value to `not known`; otherwise the predicate decides pass/fail. The growth predicate compares unrounded CAGR with the configured threshold; the R&D predicate compares unrounded latest intensity with 0.05. `analyze` computes CAGR only for five consecutive annual observations with valid positive revenue; the formula uses the first and last revenue over four intervals. The test suite verifies exact boundaries and missing-input behavior.

The lab requires Andrew and a partner to explain this function line by line **without AI**, ask what happens with missing input, and swap. Reading this preparation is not evidence that the activity occurred.

## Opening discussion and reflection preparation

From Wood's philosophy, a sell-off could prompt revisiting or adding to an innovation thesis if the long-term evidence remains strong. From Burry's philosophy, falling prices alone would not settle the question; cash quality, balance-sheet exposure and an explicit bear case deserve investigation. These are interpretations of the reference pages, not verified actions or recommendations by either investor. The lab's linked Yahoo market story was inaccessible through the web tool; no market-move figures from it are used in the calculations or memos.

A panel of AI personas applies different decision instructions to a shared evidence set. Code fixes selection, calculations and pass/fail/unknown checks; the AI supplies the business judgment. Only names/descriptions need to be visible for initial skill routing; the selected skill's full instructions and supporting files are loaded when relevant. Missing tags stay missing because an estimate would replace reproducible evidence with an assumption. On NVIDIA the panel agrees on profitability, growth, reinvestment and leverage but splits on cash conversion and how much confidence to place in the business.

## Brightspace boundary and human work

The public assignment and slides direct **Brightspace → Quizzes → Lab 19** and request **GitHub links of files (md, py and/or others as needed)**. The public rubric has five criteria worth five points each: known answer, numbers in code, honest gaps, company run and the decision. The weekly page says instructor grading/verification files are private. No private Brightspace questions, attempt, submission receipt or timing were accessed.

Still personal: confirm the fund assumption, review/adopt or revise the decision and memos, complete the partner discussions/swap and no-AI explanation, publish the committed files if needed, then enter the actual quiz and submit before the stated deadline. The 30-minute quiz-opening instruction is a classroom timing action and cannot be truthfully reconstructed after the fact. The open-ended challenge is explicitly after class and optional; its push instruction belongs to that challenge, not the required Lab 19 workflow.
