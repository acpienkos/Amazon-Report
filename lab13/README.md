# Lab 13 — Portfolio Mandate Defense

Run from the repository root using Python 3; standard library only:

```text
python -B lab13/mandate.py
python -B lab13/validate_lab13.py
```

`lab13.md` contains the completed written submission and AI disclosure. `mandate.py` checks the fictional course case; `validate_lab13.py` independently verifies the supplied answers, the required negative-weight probe, issuer aggregation, exact boundaries, computed thresholds, and invalid inputs.

Execution evidence: `mandate_output.txt`, `probe_output.txt`, and `lab13_validation.txt`. All seven tests passed with Python 3.13.7. A passes, B fails three rules, C fails one, and D passes. The probe fails only long-only. Candidate A's original weights remain unchanged. The undefined loss rule requires CIO clarification.

Previous labs are preserved. Student-provided responses are retained; classification before code implementation, attendance, assigned reading completion, and personal code execution are not claimed. Brightspace requirements were verified by the student as a GitHub link and AI disclosure. Submission to Brightspace is the student's final step.
