# Code walkthrough preparation

This AI-authored guide supports preparation. Complete the professor's six-minute line-by-line explanation **with no AI**, then answer the partner's question and swap roles.

1. Start at `DATA` and `DECISION_DATE`: locate row IDs, event months, publication dates and prices.
2. Read `parse_rows`: identify how dates and values become comparable without losing row numbers.
3. Trace `filter_panel` in order: missing ticker, duplicate identity, inclusive date cutoff, then `latest_vintages`. Find where each removed row enters the funnel.
4. Focus on every line of `latest_vintages`: explain the dictionary key, prior candidate, date comparison, replacement, conflict branch, retained IDs and two returned lists. Trace rows 2 and 4 yourself, then rows 10 and 12 after the March cutoff. Explain why the cutoff must precede revision selection.
5. Trace `calculate_signals`: locate the latest month, preceding available month, missing/zero checks and percentage expression. Explain why sorting publication dates alone does not identify the latest measured month.
6. Find the naive call with a `None` cutoff. Identify which rules still run and which rule is skipped.
7. Find `main` and its main guard. Explain why imports in tests do not print results and how the command-line date override leaves the source default unchanged.

During preparation, choose the line you understand least and ask AI for one quiz question about it. **Answer before requesting an explanation.** No quiz answer or personal reflection is supplied here.

During the actual explanation, have the partner ask a question, answer from the code, and swap. If a line remains unclear, bring that specific line back to AI afterward as instructed. Use the actual partner file for swap-and-break; restore its March 31 input after the April 15 run.
