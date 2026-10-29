Andrew Pienkos — FIN 43900 Lab 17: Point-in-Time Audit

My [Lab 17 package](https://github.com/acpienkos/Amazon-Report/tree/main/lab17) includes a Streamlit app for BAA, FEDFUNDS, DGS10 and MORTGAGE30US, additional FRED IDs, current charts and historical ALFRED comparisons with separate late and revised counts. All four October 5, 2026 known-answer checks match. The PAYEMS probe reproduces December 2024 at 159,536 thousand historically versus 158,316 currently, with 381 overlapping observations revised.

The provisional BAA data card finds August 6.32% available September 30, September 6.47% present October 1, and no changed values in 1,292 overlapping observations. My provisional decision is quarantine pending confirmation of the prework series and release/trading-time policy. The proposed rule uses the previous calendar day's ALFRED vintage for each trade date, never today's finalized values.

The package contains 17 passing deterministic tests, live integration evidence and Streamlit app-harness checks. Codex assisted with implementation, research, testing and writing. The three personal FRED checks, no-AI explanation, actual partner challenge/response and individual quiz checkout remain pending until I complete them; no partner work is claimed here.

Deliverables:

- [asof_app.py](https://github.com/acpienkos/Amazon-Report/blob/main/lab17/asof_app.py)
- [README.md](https://github.com/acpienkos/Amazon-Report/blob/main/lab17/README.md)
- [DATA_CARD.md](https://github.com/acpienkos/Amazon-Report/blob/main/lab17/DATA_CARD.md)
- [ANSWERS.md](https://github.com/acpienkos/Amazon-Report/blob/main/lab17/ANSWERS.md)
- [test_asof_app.py](https://github.com/acpienkos/Amazon-Report/blob/main/lab17/test_asof_app.py)
- [validation.txt](https://github.com/acpienkos/Amazon-Report/blob/main/lab17/validation.txt)
- [requirements.txt](https://github.com/acpienkos/Amazon-Report/blob/main/lab17/requirements.txt)
- [SUBMISSION_CHECKLIST.md](https://github.com/acpienkos/Amazon-Report/blob/main/lab17/SUBMISSION_CHECKLIST.md)
- [verify_live.py](https://github.com/acpienkos/Amazon-Report/blob/main/lab17/verify_live.py)
- [verify_app.py](https://github.com/acpienkos/Amazon-Report/blob/main/lab17/verify_app.py)

Partner confirmation paragraph — **use only after completing the work, fill all brackets and update pending statements above**:

On [date], I explained the historical-vintage function to [partner] without AI and answered [actual code question]. My partner challenged [actual data-card field/question]; I responded: “[actual two-sentence answer supported by specific app/FRED evidence].” We completed the required role swaps and discussion, and I recorded the evidence in DATA_CARD.md.
