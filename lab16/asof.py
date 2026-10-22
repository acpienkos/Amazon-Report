"""FIN 43900 Lab 16: auditable point-in-time filtering (standard library only)."""

# Editable assignment inputs: (original row, ticker, month measured, published, index).
DECISION_DATE = "2026-03-31"
DATA = [
    (1, "AAA", "2026-01", "2026-02-10", 101.0),
    (2, "AAA", "2026-02", "2026-03-10", 104.0),
    (3, "AAA", "2026-03", "2026-04-10", 109.0),
    (4, "AAA", "2026-02", "2026-03-25", 103.0),
    (5, "BBB", "2026-01", "2026-02-10", 98.0),
    (6, "BBB", "2026-02", "2026-03-10", 97.0),
    (7, "BBB", "2026-02", "2026-03-10", 97.0),
    (8, "BBB", "2026-03", "2026-04-10", 92.0),
    (9, "CCC", "2026-01", "2026-02-10", 110.0),
    (10, "CCC", "2026-02", "2026-04-05", 112.0),
    (11, "", "2026-02", "2026-03-10", 99.0),
    (12, "CCC", "2026-02", "2026-03-10", 111.0),
]

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
import argparse


@dataclass(frozen=True)
class Observation:
    row: int
    ticker: str
    month: date
    published: date
    value: Decimal


@dataclass(frozen=True)
class Signal:
    ticker: str
    month: date
    previous_month: date
    percent: Decimal


def parse_rows(data):
    """Convert editable inputs, retaining provenance; reject ambiguous identifiers."""
    rows = []
    seen_ids = set()
    for number, ticker, month, published, value in data:
        if number in seen_ids:
            raise ValueError(f"Repeated original row number: {number}")
        seen_ids.add(number)
        index = Decimal(str(value))
        if not index.is_finite():
            raise ValueError(f"Nonfinite index in row {number}")
        rows.append(Observation(number, ticker, date.fromisoformat(month + "-01"),
                                date.fromisoformat(published), index))
    return rows


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


def filter_panel(rows, decision_date):
    """Apply all four rules in order; None skips only the cutoff for naive use."""
    remaining = list(rows)
    funnel = []

    removed = [row for row in remaining if not row.ticker.strip()]
    remaining = [row for row in remaining if row.ticker.strip()]
    funnel.append(("Missing ticker", removed))

    unique, removed, seen = [], [], set()
    for row in remaining:
        # Original row ID is provenance, not part of the observation identity.
        identity = (row.ticker, row.month, row.published, row.value)
        if identity in seen:
            removed.append(row)
        else:
            seen.add(identity)
            unique.append(row)
    remaining = unique
    funnel.append(("Exact duplicate", removed))

    removed = [] if decision_date is None else [
        row for row in remaining if row.published > decision_date]
    remaining = [row for row in remaining if decision_date is None
                 or row.published <= decision_date]
    funnel.append(("Published after decision date", removed))

    remaining, removed = latest_vintages(remaining)
    funnel.append(("Superseded vintage", removed))
    return remaining, funnel


def calculate_signals(panel):
    """Use the immediately preceding calendar month, never bridge a missing month."""
    by_ticker = {}
    for row in panel:
        monthly = by_ticker.setdefault(row.ticker, {})
        if row.month in monthly:
            raise ValueError("Signal input must have one vintage per ticker/month")
        monthly[row.month] = row
    signals, unavailable = {}, {}
    for ticker, monthly in sorted(by_ticker.items()):
        latest_month = max(monthly)
        previous = (date(latest_month.year - 1, 12, 1) if latest_month.month == 1
                    else date(latest_month.year, latest_month.month - 1, 1))
        if previous not in monthly:
            unavailable[ticker] = "previous calendar month unavailable"
        elif monthly[previous].value == 0:
            unavailable[ticker] = "previous index is zero"
        else:
            percent = (monthly[latest_month].value / monthly[previous].value - 1) * 100
            signals[ticker] = Signal(ticker, latest_month, previous, percent)
    return signals, unavailable


def print_signals(label, panel):
    print(label)
    signals, unavailable = calculate_signals(panel)
    for ticker, signal in signals.items():
        print(f"  {ticker}: {signal.percent:+.2f}% ({signal.month:%Y-%m}, "
              f"{signal.month:%B}); previous {signal.previous_month:%Y-%m}")
    for ticker, reason in unavailable.items():
        print(f"  {ticker}: unavailable ({reason})")
    if not panel:
        print("  No observations available")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--decision-date", default=DECISION_DATE,
                        help="ISO date; overrides the editable default for a local test")
    args = parser.parse_args(argv)
    cutoff = date.fromisoformat(args.decision_date)
    rows = parse_rows(DATA)
    panel, funnel = filter_panel(rows, cutoff)
    print(f"Decision date: {cutoff}; input observations: {len(rows)}")
    count = len(rows)
    for label, removed in funnel:
        count -= len(removed)
        numbers = ", ".join(str(row.row) for row in removed) or "none"
        print(f"{label}: removed {len(removed)} (rows {numbers}); remaining {count}")
    print("As-of panel (original input order):")
    print("Row  Ticker  Month    Published   Index")
    for row in panel:
        print(f"{row.row:>3}  {row.ticker:<6}  {row.month:%Y-%m}  "
              f"{row.published}  {row.value:.1f}")
    print_signals("As-of signals:", panel)
    naive_panel, _ = filter_panel(rows, None)
    print_signals("Naive signals (latest vintage, publication cutoff ignored):", naive_panel)


if __name__ == "__main__":
    main()
