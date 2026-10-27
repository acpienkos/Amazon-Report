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

## Rule 4: actual code and line-by-line explanation

This is preparation for the required no-AI explanation, not evidence that it occurred. The following block is copied from the unchanged `asof.py`:

```python
def latest_vintages(rows):
    """Rule 4: latest publication for each ticker/month; retain original row order."""
    latest = {}
    for row in rows:
        key = (row.ticker, row.month)
        prior = latest.get(key)
        if prior is None or row.published > prior.published:
            latest[key] = row
        elif row.published == prior.published and row.value != prior.value:
            # No intraday time or revision sequence is supplied: do not invent one.
            raise ValueError(f"Conflicting same-date vintages: rows {prior.row}, {row.row}")
    retained_ids = {row.row for row in latest.values()}
    return ([row for row in rows if row.row in retained_ids],
            [row for row in rows if row.row not in retained_ids])
```

1. `def latest_vintages(rows):` defines the revision-selection function; its docstring identifies rule 4 and the output order.
2. `latest = {}` starts a dictionary of selected rows.
3. `for row in rows:` visits every input row. In the as-of path, these rows have already passed rules 1-3.
4. `key = (row.ticker, row.month)` groups versions of one instrument's measured month.
5. `prior = latest.get(key)` fetches the selected candidate, or `None` when the group is new.
6. `if prior is None or row.published > prior.published:` accepts the first candidate or a later publication.
7. `latest[key] = row` stores the entire row, preserving its original ID and value.
8. The `elif` tests whether two candidates have the same publication date but different values. The comment explains that no intraday sequence is provided.
9. `raise ValueError(...)` rejects that ambiguity rather than guessing which version is newer.
10. `retained_ids = {row.row for row in latest.values()}` collects the original IDs of the selected candidates.
11. The first list in `return` keeps rows with those IDs in original input order. The second list returns all other rows as replaced vintages for the funnel.

The date cutoff is enforced in `filter_panel`, before this function is called:

```python
    removed = [] if decision_date is None else [
        row for row in remaining if row.published > decision_date]
    remaining = [row for row in remaining if decision_date is None
                 or row.published <= decision_date]
    funnel.append(("Published after decision date", removed))

    remaining, removed = latest_vintages(remaining)
```

The first comprehension records rows published strictly after the cutoff. The next retains publications on or before it. `None` skips the cutoff only for the naive calculation. The funnel records the cutoff removals, then `latest_vintages(remaining)` selects revisions from the eligible rows. The following funnel entry records its replaced rows.

For AAA February, row 2 ($104, March 10) and row 4 ($103, March 25) both pass March 31. Their dictionary key is identical; March 25 is later, so row 4 replaces row 2. The returned kept list contains row 4, and the replaced list contains row 2. If the input order is reversed, the date comparison still selects row 4. For CCC February, row 10's April 5 publication fails the March cutoff, so row 12 remains eligible. Selecting revisions before the cutoff could wrongly discard that earlier admissible publication.
