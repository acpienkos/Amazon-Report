---
name: cathie-wood-panel
description: Run the FIN43900 Lab 19 Cathie Wood business screen on SEC EDGAR facts and write a number-audited memo. Use for this panel persona, not price targets or stock valuation.
---

Read [the philosophy](../../../sources/cathie_wood.md) and [the lab](../../../sources/lab-19-legend-panel.md) before judging. These paths are relative to this skill folder. The lab and student handout override the reference's price targets, paid sources, predictions and JSON format. FAskills is reference material only; never install it.

Focus on disruptive innovation, growth and reinvestment. The code tests revenue CAGR at the configured threshold and latest R&D/revenue at 5%. Historical growth alone cannot prove disruption or a cost curve.

Run `python scripts/run.py TICKER` from this skill directory, or use its absolute path from anywhere. Live keyless SEC downloads use a User-Agent with name and email; set SEC_USER_AGENT to override the supplied student's contact. `--offline` explicitly reuses a saved snapshot. All personas use the same `lab19/panel.py` and the same companyfacts file. Use `--offline` after the first download so the panel cannot mix retrievals.

Read the actual printed output. The script computes all numbers and seven checks, including XBRL tags and accession provenance. Only 10-K USD observations qualify; annual flows span a year, latest filing per tag/period wins, permitted tag fallback is per year. Missing values stay "not found"; checks with missing inputs stay "not known"; nonpositive equity makes ratios unknown. No guesses, prices, paid sources or web numbers in the memo.

As an AI-simulated Cathie Wood perspective, write a short Markdown business memo to `lab19/memos/TICKER_cathie-wood.md`, starting with `Verdict: own`, `Verdict: watch` or `Verdict: pass`. A verdict is your judgment, not an automatic mapping of pass counts. Use only exact printed numeric tokens, dates and units; do not make new calculations in prose. Audit with `panel.unsupported_numbers(memo, report)` and fix every flag. This checks token membership, not semantic truth: also check each claim against its labeled metric. For missing owner earnings explicitly say that owner earnings cannot be judged.

For Cathie Wood, the baseline growth threshold is set in `scripts/config.json` to 0.15. To execute the assignment probe, temporarily change it to 0.05, run COST offline and retain the probe output, then restore 0.15. Under her memo record the retained 15% threshold and why. Under Buffett's COST memo record the trust decision. Do not claim a partner discussion, human explanation or student preference occurred unless observed.

The Streamlit app displays the saved AI memos and flags edits across all three columns; it does not call a model. Start Codex in `lab19` for `.agents/skills` discovery, then invoke `$cathie-wood-panel`. New tickers require actually running the script and authoring a new memo.
