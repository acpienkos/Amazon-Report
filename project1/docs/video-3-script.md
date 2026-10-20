# Video 3 | Investment committee defense through the live application

Hard maximum 5:00. Target 4:45; roughly 460 spoken words plus live navigation. Keep the application visible for most of the recording.

These are AI-assisted preparation scripts, not actual transcripts. Review every statement and use your own delivery. Record personally with clear audio and a small webcam view unless an approved accommodation provides an equivalent. The times below are rehearsal targets, not recorded timestamps. Keep the hard limit; rehearse navigation and shorten pauses. Do not rerun student_exercise.py or edit any student-only evidence.

## Before recording | start the live product

From the repository root:

```powershell
project1/.runtime/python.exe -m streamlit run project1/app.py --server.address 127.0.0.1 --server.port 8501 --browser.gatherUsageStats false
```

Open http://127.0.0.1:8501. Leave the server terminal running. Stop it with Ctrl+C after recording. Prepare the sidebar pages Decision, Financial statements, Scenarios & funding, FCFF & capital, Sensitivity & reverse DCF, Comparable companies, and Sources & validation. Open project1/docs/decision-memo.pdf as a backup, not a substitute for the live demonstration. Select base explicitly when tracing statements or funding.

## 0:00-0:40 | decision and committee ask

Screen: Decision page, committee action and dated market close.

Speaking script:

My recommendation is do not initiate Amazon at the September 10, 2026 comparison price of two hundred fifty-one dollars and eighty-nine cents. The fund has no current position. I am asking the committee to authorize no purchase under the current evidence. This is a decision about whether we have a defensible investment case, not a claim that Amazon will default or that a short position is justified. Here the application displays the dated comparison, the decision and the conditions for reopening it.

## 0:40-1:25 | valuation and uncertainty

Screen: core subtotal, WACC, then strategic carrying-reference table.

Speaking script:

The operating core subtotal is thirty-nine dollars and five cents, using eleven-point-six-seven-percent WACC and two-point-five-percent terminal growth. Strategic assets are excluded from that subtotal. Adding reported carrying references gives fifty-seven dollars and six cents to sixty-one dollars and fifty-nine cents under two explicit haircut conventions. These are not fair-value bounds. Tax basis, liquidity restrictions, commitments and commercial relationships remain unresolved. I will not convert an incomplete core estimate into a precise claim about total-company downside.

## 1:25-2:15 | live funding and statement trace

Screen: Financial statements, base cash-flow statement; then Scenarios & funding, base and high.

Speaking script:

The forecast includes known investment cash uses and July financing. Follow the cash-flow statement into the funding page: the base breaches its required cash floor in 2028 and 2029 even though its cash stays positive. Only high passes funding among low, base and high; one funded case is not a defensible investment range. Negative cash in stress paths is a modeled funding shortfall, not a viable negative asset balance. My independent increase in the receivables-and-other-current-assets ratio made liquidity worse and lowered value, reinforcing the unchanged do-not-initiate action.

## 2:15-3:05 | cash economics, bridge and terminal risk

Screen: FCFF & capital tabs, annual signed FCFF, terminal dependence and enterprise-to-equity bridge.

Speaking script:

The application retains negative operating cash flows. Borrowing and strategic investment purchases do not enter operating FCFF. Lease investment, principal and operating rent are reconciled under explicit conventions, and cash and debt are bridged to equity without double counting. Terminal present value exceeds enterprise value because explicit-period present value is negative. Terminal depreciation now follows the opening-asset rule, but required investment still normalizes down from 2030. That favorable transition remains a major assumption requiring evidence.

## 3:05-3:50 | sensitivity and comparable references

Screen: Sensitivity & reverse DCF grid, then Comparable companies.

Speaking script:

This grid changes WACC and growth, including growth-linked reinvestment. Its cells remain diagnostics for a funding-infeasible base. The reverse solver shows conditional operating expectations, not proof that those expectations are plausible. Walmart and Microsoft are qualified retail and cloud references with different fiscal periods and business mixes. P/E values equity directly; enterprise multiples require the bridge. I do not average incompatible references to manufacture a price target.

## 3:50-4:45 | evidence, reversal triggers and close

Screen: Sources & validation, then return to Decision and reversal triggers.

Speaking script:

Sources, assumptions, model checks and AI-use disclosure are available in the package. The independent changed-input record is compiled separately; technical tests cannot certify AI-off conduct. Important limits remain in seasonality, exact-date balances, dilution, taxes and strategic-asset appraisal. Reopen this proposal only when documented funding covers commitments, operating returns support reinvestment, the dated equity bridge is defensible and a supported margin of safety exists against a newly dated price. My committee ask remains no new position while those evidence gaps are investigated.

## Personally complete

Rehearse this as a live product demonstration under 5:00 with webcam and clear audio. Be prepared to explain funding versus positive cash, terminal dependence over 100%, and why carrying references are not fair-value bounds. Record the actual video, correct project1/docs/transcript-video-3.txt, and supply its real URL, title, duration, evidence timestamps and access check.
