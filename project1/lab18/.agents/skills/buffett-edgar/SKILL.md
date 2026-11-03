---
name: buffett-edgar
description: Analyze a ticker with the FIN43900 Lab 18 Buffett business screen using keyless SEC companyfacts, deterministic checks, and a number-audited business memo. Use for this screen, not stock valuation or price forecasts.
---

Run the bundled `scripts/companyfacts.py TICKER` with Python. Supply a real name and email via `SEC_USER_AGENT` or `--user-agent`; ask for missing contact information. No paid data or API key. Live downloads are default; `--offline` explicitly uses the saved snapshot.

Use only 10-K facts and the last five annual-flow fiscal end dates. Annual flows must cover a year (350–380 elapsed days permits 52/53-week calendars). Select latest filing for a period within each permitted tag; use fallback only when the preferred tag has no eligible observation for that period. Do not use filing fiscal-year labels for comparative facts. Preserve missing inputs and their resulting unknown checks. The bundled script is the calculation authority, including the lab's simplified owner earnings; do not substitute maintenance-capex estimates from the reference philosophy.

Read the script's printed output before writing a short Buffett-style business memo. Save it under `memos/TICKER.md` relative to the lab root. Choose own, watch, or pass as a judgment, never as a deterministic check result. Discuss earning power and limits of evidence; do not invent moat/management facts, price claims, forecasts, or new calculations. Every numeric token must use an exact printed financial value or fiscal end date, preserving units. Audit with `unsupported_numbers`; revise until none remain. For missing owner earnings explicitly state that owner earnings cannot be judged. Add one line immediately below the memo explaining trust in the COST judgment and its limitations.

Launch Codex from the `lab18` directory to discover this repository-scoped skill under `.agents/skills`. Run the app with `python -m streamlit run app.py` from that directory. The app reviews saved AI-authored memos; it does not pretend to call an AI or generate new judgments for arbitrary tickers.

References: [official lab](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/lab-18-legend-investor-as-skill.md), [Buffett philosophy](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/warren_buffett.md), [SEC API](https://www.sec.gov/search-filings/edgar-application-programming-interfaces). Lab rules override the philosophy page's pricing and estimation requests.
