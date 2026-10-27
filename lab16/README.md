# Lab 16 - Provenance Gate

Purdue FIN 43900, Fall 2026 - Professor Cinder Zhang

## Objective and source

On the day we would have traded, what did the data actually say, and how much arrived later? We distinguish the month measured from the publication date when investors could know the value.

The [official assignment](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-10/lab-16-provenance-gate.md), checked October 27, supplies the fictional card-spend table and provenance known answers. The requested fixed-income extension interprets the same numbers as prices of funds of one-year zero-coupon bonds paying 100 at maturity. That interpretation is an added exercise assumption; the official table originally calls these values indices. The 12 exact inputs and default March 31 decision date are editable at the top of `asof.py`.

AI disclosure: OpenAI Codex extended the existing implementation, ran validation and drafted documentation. Student review and independent/partner activities remain outstanding. Lab 14 conventions were inspected; no Lab 15 folder was present. Existing supporting files are preserved.

## Files and commands

| File | Purpose |
|---|---|
| `asof.py` | Reusable filters, signals, comparison and separate yield checks |
| `test_asof.py` | 13 standard-library known-answer and boundary tests |
| `validation.txt` | Actual March 31 output and test results |
| `april15_validation.txt` | Actual April 15 output and test results |
| `WALKTHROUGH.md` | Code explanation preparation |
| `SUBMISSION_CHECKLIST.md` | Pending student tasks and submission links |

Python 3.10+; standard library only. From the repository root:

```text
python -B lab16/asof.py
python -B lab16/asof.py --decision-date 2026-04-15
python -B -m unittest discover -s lab16 -p test_asof.py -v
```

The logs use the existing `project1/.runtime/python.exe` (Python 3.13.7), since Python is not on this machine's PATH. No installation or network is needed. `-B` prevents bytecode caches; importing the module does not print the report.

## Four rules and March 31 funnel

1. Quarantine missing or whitespace-only tickers.
2. Remove exact duplicates using ticker, measured month, publication date and price. Retain the first occurrence; row ID is excluded from duplicate identity.
3. Remove publications strictly after the decision date. Publications on the cutoff are admissible.
4. For each ticker/month, retain the latest publication that survived the cutoff. Record replaced vintages.

| Step | Original rows affected | Count | Remaining |
|---|---|---:|---:|
| Missing ticker | 11 | 1 | 11 |
| Exact duplicate | 7 | 1 | 10 |
| Published after cutoff | 3, 8, 10 | 3 | 7 |
| Older vintage replaced | 2 | 1 | 6 |

Original row numbers remain attached throughout processing. The complete panel is printed in input order:

| Row | Ticker | Measured month | Published | Price |
|---:|---|---|---|---:|
| 1 | AAA | 2026-01 | 2026-02-10 | 101.0 |
| 4 | AAA | 2026-02 | 2026-03-25 | 103.0 |
| 5 | BBB | 2026-01 | 2026-02-10 | 98.0 |
| 6 | BBB | 2026-02 | 2026-03-10 | 97.0 |
| 9 | CCC | 2026-01 | 2026-02-10 | 110.0 |
| 12 | CCC | 2026-02 | 2026-03-10 | 111.0 |

## Signals and look-ahead bias

Signal = `(latest price / previous price - 1) * 100`. The latest measured month is compared with the preceding available measured month. All training pairs are consecutive months; a gap in other inputs would represent a multi-month change. Decimal arithmetic preserves precision until display. Missing preceding observations and zero denominators produce an unavailable result.

| Ticker | March 31 as-of | Naive, cutoff ignored |
|---|---|---|
| AAA | +1.98% (February) | +5.83% (March) |
| BBB | -1.02% (February) | -5.15% (March) |
| CCC | +0.91% (February) | +1.82% (February, revised) |

The naive panel still removes missing tickers and exact duplicates, but selects the latest publications without a decision-date cutoff. Both columns are computed dynamically.

Observation month is event time: the period described. Publication time tells us when the value became available. A revision changes an earlier month's value at a later publication date. Look-ahead bias means a historical decision uses information that arrived afterward.

AAA's naive signal is `(109 / 103 - 1) * 100 = +5.83%`. The March value of 109 was published April 10, so a March 31 investor could not know it. The admissible signal was `(103 / 101 - 1) * 100 = +1.98%`. Row 4 replaces row 2 because its March 25 revision was already available and newer than March 10. Keeping 104 would incorrectly give +2.97%. CCC's revised 112 arrived April 5, so March 31 must use 111.

A naive backtest would show stronger positive AAA/CCC signals and a more negative BBB signal using future information. That could change rankings and trades and make results misleading. These signal differences alone do not establish any strategy's realized profit.

## Fixed-income sanity checks: separate extension

Yield = `(100 / price - 1) * 100` for a one-year zero-coupon instrument paying 100.

| Row | Price | Yield | Concern |
|---:|---:|---:|---|
| 1 | 101.0 | -0.99% | Negative yield |
| 4 | 103.0 | -2.91% | Negative yield |
| 5 | 98.0 | +2.04% | None |
| 6 | 97.0 | +3.09% | None |
| 9 | 110.0 | -9.09% | Negative yield; CCC priced above BBB and AAA |
| 12 | 111.0 | -9.91% | Negative yield; CCC priced above BBB and AAA |

Negative yields can occur in real markets. In this fictional bond extension they are planted economic warnings. At equal maturities, the exercise assumes safer-to-riskier credit order AAA, BBB, CCC: riskier credit should have higher yield and lower price. CCC instead costs more than both safer instruments in the same measured month. The code reports this separately.

Proposed fifth rule: quarantine a positive price above the maturity payment of 100, equivalently a negative yield, for economic review. This flags rows **1, 4, 9 and 12** on March 31. It is proposed only and never changes the required six-row panel or signals. Provenance establishes what was knowable; economic checks assess plausibility. Nonpositive prices cannot produce a meaningful yield and the yield function rejects them.

## Rule 4 line by line: preparation

The `latest_vintages(rows)` function receives rows admitted by the earlier rules.

| Code | Explanation |
|---|---|
| `latest = {}` | Start a dictionary of selected observations. |
| `for row in rows:` | Examine each admissible row. |
| `key = (row.ticker, row.month)` | Group versions of the same measured period and instrument. |
| `prior = latest.get(key)` | Fetch the current candidate, or `None`. |
| `if prior is None or row.published > prior.published:` | Accept the first candidate or a newer publication. |
| `latest[key] = row` | Save the entire candidate, including its original row number. |
| `elif row.published == prior.published and row.value != prior.value:` | Detect conflicting values without a supplied intraday ordering. |
| `raise ValueError(...)` | Refuse to guess between those conflicting candidates. |
| `retained_ids = {row.row for row in latest.values()}` | Collect selected original IDs. |
| First returned list comprehension | Keep selected rows in original input order. |
| Second returned list comprehension | Return all replaced rows for the funnel. |

The cutoff must come first. Otherwise CCC's April revision could displace its admissible March publication before filtering. Exact duplicates have already been removed. Equal-date conflicting candidates cause an explicit error rather than an invented sequence.

## April 15 counterfactual and automated validation

The CLI override leaves the default March 31 date unchanged. By April 15 all publications are available. Missing ticker row 11 and duplicate row 7 still leave first; the cutoff removes none, then rule 4 replaces rows 2 and 12. The final eight rows are **1, 3, 4, 5, 6, 8, 9, 10**.

| Ticker | April 15 as-of | Naive | Equal? |
|---|---|---|---|
| AAA | +5.83% (March) | +5.83% (March) | Yes |
| BBB | -5.15% (March) | -5.15% (March) | Yes |
| CCC | +1.82% (February) | +1.82% (February) | Yes |

All 13 tests pass. Coverage includes the ordered funnel, six-row panel, full-precision and rounded signals, revisions, inclusive cutoff, duplicate identity, April panel and equivalence, yields, separation of economic warnings, empty inputs, missing/zero denominators, year boundaries and conflicting/invalid inputs. A changed NEW ticker with different dates, prices and row numbers checks dynamic filtering and signals. Production calculation functions contain no known-answer tables or row-ID exceptions; expected results are confined to tests and documentation. Both logs record actual program/test output and exit codes.

## Partner Discussion and Reflection

Written reflection and discussion preparation, based on the supplied conceptual review. This section does not certify a completed partner conversation, no-AI explanation or partner file swap.

The observation month tells me what period a value measures, while the publication date tells me when investors could use it. AAA's February price of $104, for example, was published March 10. A historical decision needs the publication date so that a value describing an earlier month does not enter the backtest before it was available.

The four rules establish what investors could have known: first quarantine missing tickers, then remove exact duplicates, exclude publications after the decision date, and finally keep the latest eligible publication for each ticker and month. I would emphasize the last rule because an available value may already have been revised. AAA row 2 reports February at $104 on March 10; row 4 revises it to $103 on March 25. Both were available by March 31, but row 4 is newer and must replace row 2. Using the original release would give an inaccurate historical signal even though it passes the publication cutoff.

Look-ahead bias occurs when future information influences a historical investment decision. AAA's March 31 as-of signal is +1.98%, using February, while the naive signal is +5.83%, using March. The March observation was published April 10, so using it on March 31 would give the backtest information no investor had then. The distortion can work in either direction: BBB's naive signal is -5.15%, compared with its admissible -1.02%. Future information can raise or lower signals and distort reported returns in either direction, depending on the strategy; it does not necessarily improve performance.

The local April 15 test helps confirm the timing logic. AAA moves from +1.98% on March 31 to +5.83%, BBB from -1.02% to -5.15%, and CCC from +0.91% to +1.82%. All April 15 as-of signals equal the naive signals because every relevant publication was available by then. This is program validation, not evidence that I completed the exercise on my partner's file.

For the fixed-income extension, I interpret the fictional instruments as one-year zero-coupon bond funds paying $100 at maturity. Using `Yield = (100 / Price - 1) * 100`, February AAA at $103 yields -2.91%, and CCC at $111 yields -9.91%. Both prices exceed the maturity payoff. CCC also costs more than AAA and BBB despite being the riskiest credit in this exercise. These are economic warnings under the stated assumptions; negative yields are possible in real markets. The four provenance rules do not catch them because those rules check identifiers, duplicates, publication timing and revisions, rather than economic plausibility.

My proposed fifth rule would quarantine zero-coupon prices above the $100 maturity payoff for review. Applied to the March 31 panel, it flags exactly rows 1, 4, 9 and 12. A separate credit-risk ordering check would flag CCC's higher price than AAA and BBB at equal maturities. These checks remain separate proposals and do not change the original four-rule filter or its six-row panel.

My takeaway is that a historical strategy must use the information available at the decision date, including only revisions already published. Passing the provenance gate does not guarantee that a value makes economic sense. Reliable backtesting needs both point-in-time accuracy and economic sanity checks.

Partner question for preparation: Why group by ticker and measured month rather than publication date? Suggested answer: Those fields identify versions of the same observation; comparing publication dates within the group selects the latest admissible version. Actual partner question and observations remain **unanswered; student to supply**.

The AI quiz, no-AI code explanation, partner question and role swap, actual partner-file changed-date exercise, and partner discussion remain to be completed or confirmed personally. Review this AI-assisted written reflection and complete any required personal reflection. Finish assigned reading and individual checkout, confirm Brightspace fields/deadline, and submit individually. No attendance or submission is claimed.
