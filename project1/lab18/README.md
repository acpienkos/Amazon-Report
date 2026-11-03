# FIN43900 Lab 18 — Buffett business screen

Self-contained lab; earlier labs are unchanged. AI judgment: **COST — watch**. The saved memo uses only script-printed financial values and includes the required trust decision beneath it.

## Run

From `project1/lab18` with Python 3.13:

```powershell
python -m pip install -r requirements.txt
python .agents/skills/buffett-edgar/scripts/companyfacts.py COST
python .agents/skills/buffett-edgar/scripts/companyfacts.py JPM
python -m streamlit run app.py
python verify.py
```

The live script uses keyless SEC requests with `Andrew Pienkos apienkos@purdue.edu` in the User-Agent. Other users should set `SEC_USER_AGENT` to their own name and email. Use `--offline` for the committed SEC snapshots. The app initially uses those snapshots; uncheck its offline box for a live fetch. Network errors are shown, never replaced with fabricated data.

Start Codex **inside lab18** to discover `.agents/skills/buffett-edgar/SKILL.md`, then request `$buffett-edgar` for a ticker. The bundled script computes; Codex writes the judgment to `memos/TICKER.md`. The Streamlit app displays saved AI memos and supports pasted/edited memos and downloads; it does not make paid model calls. New tickers need a live SEC download and an AI-authored memo.

## Rules and evidence

Only 10-K USD companyfacts are eligible. Fiscal end dates come from annual flows, not comparative facts' filing `fy` labels. Annual periods cover 350–380 elapsed days to include calendar and 52/53-week fiscal years. Within each tag and period, latest filing date wins; accession breaks ties. Tag fallback is per metric/year in lab order. Equity is a year-end instant; ROE uses year-end equity. Owner earnings are operating cash flow minus the permitted capital-spending concept, with no estimation or zero filling. Nonpositive equity makes ratios unknown; missing inputs make checks unknown. Checks use unrounded values; the printed table uses USD millions and one-decimal percentage ROE.

Executed verification is in [tests.txt](evidence/tests.txt) and [verification.json](evidence/verification.json): all five COST rows (all seven official columns) are compared directly with the downloaded official lab Markdown, rather than hardcoding table values into the implementation. Tests also exercise JPM missing spending/owner earnings, both unknown checks, annual versus quarterly flows, latest filing, tag fallback, invalid equity, missing years, memo auditing, and the Streamlit chart/table/checks with the `40.0%` insertion probe. The UI test uses Streamlit AppTest; no manual browser visual inspection is claimed.

Live runs of the bundled script produce [COST output](evidence/COST_printed.txt), [JPM output](evidence/JPM_printed.txt), and structured reports. Raw SEC snapshots are in `sources/`; each ticker's `.provenance.json` records its URL, actual UTC retrieval time, User-Agent and SHA-256. `verification.json` hashes the exact tested sources. COST passes all three checks. JPM capital spending and owner earnings remain `not found`; its owner-earnings checks are `not known`.

The numeric auditor flags each occurrence absent from printed financial cells or fiscal end dates, preserving signs, percent units and formatting. Source accession numbers do not whitelist memo claims. Numeric membership cannot establish that an allowed number is attached to the correct claim; the app states this limitation. The simplified historical screen cannot establish moat durability, management quality or future results.

## Sources

- [Official Lab 18](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/lab-18-legend-investor-as-skill.md)
- [Buffett FAskills page](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/warren_buffett.md): read as philosophy only; FAskills was not installed and none of its paid sources were used. The lab overrides its estimation and price-analysis instructions.
- [SEC API documentation](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)
- [Codex skills and discovery locations](https://developers.openai.com/codex/skills)
- [Streamlit documentation](https://docs.streamlit.io/)

Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.
