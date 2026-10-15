# Lab 13 — Portfolio Mandate Defense

**Status: written sections complete; computational validation passed. Brightspace requirements verified by the student: GitHub link and AI disclosure.**
This is the fictional Meridian Foundation common case, not my Amazon valuation or the separate open-ended challenge. No market data or investment forecast is introduced.

## Sources and scope

Read at official course commit `1b6c33a1d3c46ceb8657e85cdb4571c13e9cfcb6` on October 15, 2026:

- [Exact Lab 13 checkout](https://github.com/CinderZhang/FIN43900-Fall2026/blob/1b6c33a1d3c46ceb8657e85cdb4571c13e9cfcb6/lessons/week-08/lab-13-portfolio-mandate.md).
- [Week 8 README](https://github.com/CinderZhang/FIN43900-Fall2026/blob/1b6c33a1d3c46ceb8657e85cdb4571c13e9cfcb6/lessons/week-08/README.md), student handout, prework, common-case pointer and open challenge in that directory.
- [Course README](https://github.com/CinderZhang/FIN43900-Fall2026/blob/1b6c33a1d3c46ceb8657e85cdb4571c13e9cfcb6/README.md): Brightspace governs dates, grading and submission conflicts.

The prework assigns the Introduction (p.1) and Section 3 (pp.8–15) of [CFA Institute's institutional IPS paper](https://rpc.cfainstitute.org/sites/default/files/-/media/documents/article/position-paper/investment-policy-statement-institutional-investors.pdf). Student reading completion is not claimed. No separate Lab 13 starter Python file appears in the Week 8 file listing; the worksheet supplies the implementation prompt.

## D — Define

Which of these portfolios does the Meridian Foundation's mandate permit — and what must the CIO answer before anyone optimizes?

The checker evaluates five allocation rules from supplied fictional facts. It cannot certify future performance, suitability, turnover, annual rebalancing, or the absence of borrowing or derivatives beyond the supplied holdings and weight representation.

## R — Represent: student-only sorting

The student reports independently completing these classifications and explanations. They were supplied and inserted after the checker was built; no claim is made that classification preceded implementation. The student's wording is preserved below, with the duplicate pasted table included only once.

| Statement | Classification | Reasoning |
|---|---|---|
| S1 | Preference | The seven-year horizon establishes how long the money will be invested, while annual rebalancing describes how the portfolio should be managed. Neither specifies a return target or an explicit prohibition. |
| S2 | Objective | The CIO explicitly states the desired investment outcome: earning 4% above inflation annually, after costs, over rolling five-year periods. This is a measurable performance goal. |
| S3 | Hard constraint | The foundation must distribute $750,000 every quarter and maintain enough liquid assets to cover 12 months of payouts ($3 million). The portfolio must accommodate these requirements. |
| S4 | Preference | The 60/40 allocation is a benchmark used to evaluate performance, not necessarily a requirement to invest exactly 60% in equities and 40% in bonds. |
| S5 | Hard constraint | The CIO explicitly prohibits borrowing, short selling, and derivatives. These are binding restrictions on investment strategies. |
| S6 | Hard constraint | The 8% maximum exposure to any single issuer is a specific, measurable concentration limit that cannot be exceeded. |
| S7 | Hard constraint | Portfolio turnover cannot exceed 25% annually unless the committee approves. The approval exception does not eliminate the restriction. |
| S8 | Hard constraint | At least 90% of the portfolio must be redeemable within five business days. This establishes a measurable liquidity requirement. |
| S9 | Unverifiable promise | The CIO demands that the portfolio never lose more than 10% in a calendar year. Market losses cannot be guaranteed against, and the statement provides no measurement method or procedure for breaches. |
| S10 | Missing | Although the CIO identifies several areas without preferences, they never specify what the investment pilot should optimize. That critical information is missing. |

## I — Implement

[mandate.py](mandate.py) contains editable holdings, candidates and thresholds and uses only the standard library. Run `python -B lab13/mandate.py` from the project root. Weights are percent; reserve and payout are USD millions; redemption times are business days. Issuer exemptions and reserve eligibility follow the supplied table exactly. Acme stock and bonds aggregate. Calendar-year loss always prints `requires CIO clarification`.

**Learning quiz**

Selected line: 54 — companies[issuer] += weight

Question: For line 54, what does this line do when the checker encounters Acme Corp bonds and then Acme Corp stock in candidate B?

My answer (written before receiving the explanation): Line 54 combines the weights of investments from the same issuer to check whether their total exposure exceeds the 8% issuer limit.

The student answered before receiving the explanation. The answer above is preserved in the student's wording.

## V — Validate

The payout reserve is 4 x $0.75m = $3m; $3m / $100m = 3.0%. The supplied validation table is the independent oracle, not a result hard-coded in the checker.

| Candidate | Total | Lowest | Reserve | Liquid within 5 days | Largest company | Failures |
|---|---:|---:|---:|---:|---:|---:|
| A | 100.0 | 0.0 | 14.0 | 100.0 | 0.0 | 0 |
| B | 100.0 | 0.0 | 1.0 | 85.0 | 9.0 | 3 |
| C | 100.0 | 0.0 | 2.0 | 100.0 | 8.0 | 1 |

See [executed output](mandate_output.txt), [probe output](probe_output.txt), and [test log](lab13_validation.txt). Run instructions are in [README](README.md). The required probe copies A, changes Cash to -2 and global equity to 64, and checks total 100, lowest -2, reserve 10, liquid 100 and company 0. Only long-only fails. The saved A remains restored at Cash 2 and global equity 60.

These tests do not claim that S9 is enforceable or that A is suitable.

Executed October 15, 2026 with Python 3.13.7: all seven tests passed, both program exits were zero, and the probe produced only the expected long-only failure. All 46 previously tracked files matched the local SHA-256 preservation manifest during final validation; previous labs were preserved. The test suite includes exact boundary tests for reserve, liquidity and issuer concentration, rejection just above the company cap, and a changed payout to prove the reserve threshold is computed.

## E — Evolve: AI proposal and independent judgment

AI-proposed D: 100% Cash and 0% in every other permitted holding. It passes the five implemented checks. AI's proposed objection refers to S2: allocation feasibility alone gives no evidence of achieving CPI + 4% net over rolling five-year periods. No cash return or future inflation assumption is supplied, so this is not proof that D will miss the target. Do not optimize.

**AI closed — my own two-sentence judgment, naming the deciding statement:**

The objection to Candidate D holds because, although a 100% cash portfolio satisfies all checkable constraints, it does not meaningfully pursue the foundation’s investment objective. S2 establishes a target return of CPI + 4% annually, net of costs, which an all-cash portfolio is unlikely to achieve over time.

**Skeptical-colleague argument:**

A skeptical colleague could argue that Candidate D prioritizes satisfying constraints over achieving the foundation’s actual purpose. Under S2, the CIO wants returns exceeding inflation by 4% annually, and holding 100% cash would likely sacrifice the growth needed to meet that objective.

## One question for the CIO — AI closed

Question for the CIO:
Should we prioritize achieving the CPI + 4% return objective or minimizing the risk of losses when optimizing the portfolio?

How the answer changes investment decisions:
If the CIO prioritizes returns, I would allocate more toward equities and other growth investments. If minimizing losses is more important, I would favor safer investments like Treasury securities and investment-grade bonds, even if that means potentially falling short of the return target.

## R — Reflect and explain the IPS

1. What is an Investment Policy Statement (IPS)?
An IPS is a document that outlines an investor's financial goals, risk tolerance, and rules for managing their portfolio. It serves as a guide for making investment decisions and making sure those decisions align with the client's needs.

2. How do investment objectives and constraints work together within an IPS?
Objectives explain what the investor wants to achieve, while constraints establish the limits the portfolio manager must work within. Both are important because a portfolio needs to pursue its return goals without violating restrictions related to risk, liquidity, or investment strategies.

3. How do the CIO's statements S1–S10 map onto the different components of an IPS?
S2 establishes the return objective, while S1 identifies the investment horizon and rebalancing approach. S3 and S8 address liquidity requirements, S5–S7 establish investment restrictions, and S4 provides a benchmark for evaluating performance. S9 raises concerns about risk tolerance because it promises a maximum loss without explaining how that limit would be measured or enforced. Finally, S10 identifies missing information about what the portfolio should prioritize when making investment decisions.

Reflection 1: Why can a portfolio pass every checkable rule and still be wrong for the client?
A portfolio can pass every checkable rule because those tests only determine whether it follows certain restrictions, not whether it actually accomplishes the client's goals. For example, Candidate D holds 100% cash and passes all the tests, but it is unlikely to achieve the foundation's objective of earning CPI + 4% annually. This shows that meeting the constraints doesn't automatically mean a portfolio is a good investment strategy.

Reflection 2: Which S1–S10 classification were you least confident about, and why?
I was least confident about S1 because it combines two different ideas: a seven-year investment horizon and annual rebalancing. The investment horizon helps establish how long the foundation plans to invest, while annual rebalancing sounds more like a portfolio management rule. I initially classified it as a preference, but I could also see why annual rebalancing might be considered a hard constraint if the CIO expects it to be followed strictly.

## My Project 2 mandate — AI assistance permitted

**Client and Purpose:**  
My client is a 25-year-old professional who has saved $50,000 and wants to invest the money toward purchasing a first home within five years. The goal is to grow the savings while preserving enough capital for the down payment.

**Investment Objective:**  
Earn an average annual return of approximately 4–5%, net of fees, over the five-year investment horizon while limiting the risk of significant losses as the home purchase approaches.

**Hard Constraints:**
1. The portfolio must maintain at least 20% in cash, Treasury bills, or other highly liquid, low-risk investments.
2. No individual corporate issuer may represent more than 10% of the portfolio.
3. No borrowing, short selling, or derivatives are permitted.
4. At least 90% of the portfolio must be accessible within five business days.
5. The portfolio must gradually reduce equity exposure as the anticipated home purchase date approaches.

**One Question for the Client:**  
If the portfolio experiences a market decline shortly before your planned home purchase, would you be willing to delay buying the home, or must the down payment be available on the original timeline?

**Why This Matters:**  
If the purchase date is flexible, the portfolio could accept somewhat more investment risk in pursuit of higher returns. If the date is fixed, I would emphasize capital preservation and allocate more heavily toward Treasury securities and cash equivalents.

## Evidence and disclosure

I used ChatGPT and OpenAI Codex to assist with implementing, testing, and validating the Python portfolio mandate checker, organizing my Lab 13 submission, and explaining investment policy statement concepts. I independently completed the S1–S10 classifications and reasoning, Candidate D evaluation, CIO question, and personal reflections. AI also assisted with drafting my Project 2 mandate. I reviewed the results and retained responsibility for the final submission.

The classifications were supplied and inserted after the checker was built; classification before implementation is not claimed. Attendance, completion of the assigned IPS reading, and personal code execution are not claimed. The checker and tests were executed by the AI assistant. The student confirmed that Brightspace requires a GitHub link and AI disclosure. Brightspace submission itself is not claimed.
