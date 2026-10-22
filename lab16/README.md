# Lab 16 - Provenance Gate

## Objective and source

Build a point-in-time panel: use only observations published by the trading decision date, including only revisions already available then. The month measured describes economic activity; the publication date determines when its value becomes knowable.

Implemented from the complete [Professor Zhang assignment](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-10/lab-16-provenance-gate.md), read October 22, 2026. The 12 fictional card-spend observations are copied into the editable inputs at the top of `asof.py`. They are training data, not real retailer data.

## Run

Python 3.10+; standard library only. From the repository root:

```text
python -B lab16/asof.py
python -B -m unittest discover -s lab16 -p test_asof.py -v
python -B lab16/asof.py --decision-date 2026-04-15
```

Alternatively, from `lab16/`, run `python asof.py`. The evidence uses the existing `project1/.runtime/python.exe` (Python 3.13.7), because `python` is not on this machine's PATH. `-B` prevents bytecode caches. No installation or network is required to run the program or tests.

## Rules and verified results

Rules run in this order. Original row numbers survive parsing and are excluded from duplicate identity.

| Rule | Removed original rows | Count | Remaining |
|---|---|---:|---:|
| Quarantine missing/blank ticker | 11 | 1 | 11 |
| Remove exact duplicate ticker, month, publication and index | 7 | 1 | 10 |
| Remove publication strictly after March 31, 2026 | 3, 8, 10 | 3 | 7 |
| Keep latest available publication for each ticker/month | 2 | 1 | 6 |

Complete surviving panel, in original input order:

| Row | Ticker | Month measured | Published on | Index |
|---:|---|---|---|---:|
| 1 | AAA | 2026-01 | 2026-02-10 | 101.0 |
| 4 | AAA | 2026-02 | 2026-03-25 | 103.0 |
| 5 | BBB | 2026-01 | 2026-02-10 | 98.0 |
| 6 | BBB | 2026-02 | 2026-03-10 | 97.0 |
| 9 | CCC | 2026-01 | 2026-02-10 | 110.0 |
| 12 | CCC | 2026-02 | 2026-03-10 | 111.0 |

Signal = `(latest month index / previous calendar month index - 1) * 100`. Decimal arithmetic retains precision until the two-decimal display. Missing prior months and zero denominators produce an explicit unavailable result. Same-day conflicting values raise an error because the table supplies no intraday ordering.

| Ticker | As-of March 31 | Naive latest vintage |
|---|---|---|
| AAA | +1.98% (February) | +5.83% (March) |
| BBB | -1.02% (February) | -5.15% (March) |
| CCC | +0.91% (February) | +1.82% (February, revised) |

The naive panel applies missing-ticker and duplicate cleanup and selects latest publications without the decision-date cutoff. March values for AAA and BBB were published April 10; CCC's February revision was published April 5. Using those values on March 31 imports future knowledge into a backtest (look-ahead bias). AAA's March 25 revision was already available, so February must use 103 rather than 104. Revisions can change historical values even when the measured month stays the same. This is AI-authored study context; the student's independent explanation remains required.

## Validation and independent local sensitivity test

`validation.txt` records actual commands, interpreter version, program output, test output and exit codes. The initial run found two incorrect test expectations (omitted April row 6 and duplicate row-ID invariance under reordered inputs). Those assertions and the April panel documentation were corrected; the implementation needed no change. All 11 unittest methods pass on the final run, covering the ordered funnel, complete retained observations, all six full-precision and rounded signals, revision selection independent of input order, inclusive publication cutoff, duplicate identity, April sensitivity, empty inputs, missing prior months, zero denominators, year boundaries and ambiguous/invalid inputs.

The independent local April 15 run retains rows **1, 3, 4, 5, 6, 8, 9, 10**. Its as-of signals equal the naive signals for every ticker: AAA +5.83% (March), BBB -5.15% (March), CCC +1.82% (February). This uses a command-line override, leaving the editable default at **2026-03-31**. A subsequent default run and the tests verify that setting. This local test does **not** complete the required exercise on the partner's actual file.

## Remaining requirements and AI assistance

See [SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md) for pending personal/partner activities and individual submission links, and [WALKTHROUGH.md](WALKTHROUGH.md) for preparation prompts. No partner interaction, student quiz answer, independent explanation, reflection, attendance or Brightspace submission is claimed.

OpenAI Codex read the assignment and existing repository conventions, wrote the implementation, tests and documentation, executed validation, and prepared the GitHub delivery. The student must review the code and personally complete the assigned learning and partner work.
