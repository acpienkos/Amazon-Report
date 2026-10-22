# Individual checkout checklist

## Computational package

Implementation, tests and execution evidence are in this folder. See README and validation.txt for verified results. GitHub publication is reported in the delivery message; this checklist does not itself certify a push.

## Student and partner activities - pending

- [ ] Bring the Course/Work Folder, Lab 15 chat and partner; complete the assigned ALFRED prework reading. Paste the lab's D question into the Lab 15 chat.
- [ ] Give the five-minute no-screen explanation of month measured versus publication date to the partner, then swap.
- [ ] Read, run and personally review `asof.py`; choose the least-understood line and ask AI to quiz you. Answer before receiving its explanation.
- [ ] Explain the revision-handling block line by line for six minutes with no AI; answer the partner's question from the code, then swap roles.
- [ ] Run the partner's actual `asof.py` and verify the known answers. In their file change the decision date to `2026-04-15`, verify as-of equals naive for each ticker, then undo. The local automated sensitivity test does not fulfill this.
- [ ] Independently explain look-ahead bias, event time, publication time and revisions; explain to the partner why AAA's +5.83% was not knowable on March 31.
- [ ] Discuss both reflection questions with the partner: which rule removed the row that mattered most, and what a backtest using the naive column would claim.
- [ ] Verify Brightspace's deadline and submission fields; submit individually with the GitHub file links below. No submission or attendance completion is claimed.

## GitHub links for Brightspace

Primary Markdown and Python files:

- [README.md](https://github.com/acpienkos/Amazon-Report/blob/main/lab16/README.md)
- [asof.py](https://github.com/acpienkos/Amazon-Report/blob/main/lab16/asof.py)

Supporting evidence and preparation:

- [test_asof.py](https://github.com/acpienkos/Amazon-Report/blob/main/lab16/test_asof.py)
- [validation.txt](https://github.com/acpienkos/Amazon-Report/blob/main/lab16/validation.txt)
- [WALKTHROUGH.md](https://github.com/acpienkos/Amazon-Report/blob/main/lab16/WALKTHROUGH.md)
- [SUBMISSION_CHECKLIST.md](https://github.com/acpienkos/Amazon-Report/blob/main/lab16/SUBMISSION_CHECKLIST.md)

Thursday preview: prepare to apply this filter to your own monthly ALFRED series; that later work is outside this training-table implementation.
