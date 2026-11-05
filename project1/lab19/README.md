# Lab 19 — Legend Panel

Three discoverable, executable skills share a deterministic SEC 10-K pipeline: `buffett-panel`, `cathie-wood-panel` and `burry-panel`. The official investor additions are **Cathie Wood and Burry**, as stated in the November 1 rewrite of [Lab 19](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/lab-19-legend-panel.md). The prior Lab 18 preview mentioning Graham is superseded. Earlier labs are unchanged.

## Run

From `project1/lab19`, use Python 3.13 (the existing local runtime is `../.runtime/python.exe`):

```powershell
python -m pip install -r requirements.txt
python panel.py COST --offline
python panel.py NVDA --offline
python .agents/skills/cathie-wood-panel/scripts/run.py COST --offline
python run_demo.py
python verify.py
python -m streamlit run app.py
```

Without `--offline`, `panel.py TICKER` and all skill wrappers download live keyless SEC facts. The supplied SEC User-Agent identifies Andrew Pienkos and his Purdue email; other users must set `SEC_USER_AGENT` to their own name/email. Network failures are surfaced, not silently replaced with snapshots. App defaults explicitly to saved snapshots; turn off its offline checkbox for a live fetch. The live app caches downloads for an hour. New tickers require running the code and authoring their memos; there is no paid API or hidden model call in the app.

Start Codex **in this lab19 directory**, then invoke `$buffett-panel`, `$cathie-wood-panel` or `$burry-panel` on the requested ticker. Each skill has frontmatter, a bundled executable wrapper, configuration and UI metadata. Skill scripts work from any working directory. The actual Codex `skills/list` API discovered all three as enabled repository skills, with zero errors; see `evidence/codex_discovery.json`. `discover_skills.py` reproduces that check if the Codex CLI is installed; it starts no model turn and uses an isolated temporary Codex home. The app-server stderr is not treated as financial evidence.

## Calculation and memo contract

The self-contained EDGAR extractor is copied from Lab 18 and extended with the handout's R&D primary and fallback tags. `engine.py` imports that implementation; `panel.py` performs the new calculations and shared rendering. Only USD 10-K facts qualify. Flows cover 350–380 elapsed days for calendar and 52/53-week fiscal years. Fiscal ends come from annual flow observations, not the filing `fy` label; latest filing wins within a permitted tag/period, with tag priority and per-year fallback. Equity/liabilities are year-end instants. Each selected metric retains tag, filing date and accession. This follows the course's current-restated-data convention, not a point-in-time backtest.

ROE uses year-end equity; owner earnings are OCF minus the lab's permitted capital spending. Revenue CAGR is `(last / first) ** (1/4) - 1`, requiring five consecutive valid annual observations. R&D/revenue uses the same year. Nonpositive equity makes ROE and liabilities/equity unknown. Missing financial values print `not found`; checks with missing inputs print `not known`. R&D/revenue prints `not found` when an input is absent. All threshold decisions use unrounded values. Display: USD millions, one decimal for ROE, two decimals for R&D intensity, CAGR and liabilities/equity.

The three personas read identical printed output, then Codex authors separate `.md` judgments; **verdicts are not computed from pass counts**. `run_demo.py` executes all nine company/skill combinations and audits nine saved memos. It does not generate AI prose. The numeric auditor checks exact token membership in the printed financial cells, dates, computed CAGR and printed thresholds; it does not let accession digits whitelist claims. Numeric membership cannot prove a claim's meaning, correct metric, units or context; those require review. The app makes that limitation visible and tests injection in every investor column.

## Results and evidence

- [Panel results](RESULTS.md): COST and NVDA check tables, verdicts and memo links; JPM demonstrates preserved gaps.
- [Interpretation and human activities](ANSWERS.md): fund-selection evidence and assumption, bull/bear drafts, conditional decision, code explanation preparation and manual checkout boundary.
- [Official requirements checklist](CHECKLIST.md): every required artifact/activity and five merit anchors.
- `evidence/tests.txt` and `verification.json`: actual test counts, validator results and hashes; not handwritten success evidence.
- `evidence/*_printed.txt` / `*_report.json`: actual code output; `*_execution.txt`: each skill execution.
- `evidence/threshold_probe.txt`: actual 5% skill-config probe, restored to retained 15% afterward.
- `sources/*.provenance.json`: SEC URL, retrieval timestamp, User-Agent and SHA-256. COST/NVDA downloaded for this lab; JPM legitimately reuses the November 3 Lab 18 snapshot with its original provenance.
- `sources/reference_provenance.json`: downloaded full official lab, handout, prework, slides, optional challenge, investor philosophy pages and relevant technical references. `read_reference_text.py` extracts technical reference HTML without extra dependencies.

The official COST answer is read from the frozen assignment Markdown by tests, never inserted into the computation. The original 35 financial cells, ten new ratio/gap cells, growth and seven checks match. NVIDIA is the largest company in the saved VT holdings page; **VT remains an explicitly stated working assumption from the proposed Project 2 universe until Andrew confirms it**.

The lab's `.gitattributes` preserves exact artifact bytes so Git newline conversion cannot invalidate the recorded SHA-256 values. Upstream HTML whitespace is retained as retrieved and excluded from whitespace-style checks.

## Sources and attribution

The [official lab](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/lab-19-legend-panel.md) and [student handout](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/student-handout.md) define calculation and output requirements. [FAskills](https://github.com/CinderZhang/FAskills) is read as philosophy only; its installation, paid data, forecasts, target prices and rigid JSON output are overridden by the course. [SEC API](https://www.sec.gov/search-filings/edgar-application-programming-interfaces), [Codex skills](https://developers.openai.com/codex/skills) and [Streamlit](https://docs.streamlit.io/) are the technical references. `tools/quick_validate.py` is the unmodified bundled OpenAI Codex skill-creator validator, copied for reproducible local validation; it needs PyYAML. It validates packaging, not investment quality. No subagents or paid model calls were used.

Codex read instructions/references, implemented the skills, calculations and app, downloaded public sources, wrote the simulated investor memos and written drafts, ran the tests and prepared checkout text. No partner discussion, no-AI student explanation, private quiz access or actual student decision is claimed. The final delivery text includes the local commit hash; publishing and Brightspace submission remain separate from local validation.

Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.
