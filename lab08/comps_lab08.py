"""FIN 43900 Lab 08: Amazon reported annual P/E comparison.

Educational use only: simplified coursework, not financial or investment advice.
Sources and qualifications: lab08.md. Standard library; no network or packages.
Core calculation follows the student's Lab 07 logic; prior files stay unchanged.
"""

import argparse
import math
from datetime import date
from fractions import Fraction
from statistics import median

# AMAZON ANALYSIS ONLY. USD/common share, reported total GAAP diluted annual EPS.
VALUATION_DATE = "2026-09-10"
TARGET = dict(ticker="AMZN", price=251.89, eps=7.17, decision="target",
              price_date=VALUATION_DATE, year_end="2025-12-31", published="2026-02-05")
PEERS = [
    dict(ticker="WMT", price=105.73, eps=2.73, decision="qualify",
         price_date=VALUATION_DATE, year_end="2026-01-31", published="2026-02-19"),
    dict(ticker="MSFT", price=492.44, eps=17.95, decision="qualify",
         price_date=VALUATION_DATE, year_end="2026-06-30", published="2026-07-29"),
]
CURRENT_PRICE = 247.81
CURRENT_QUOTE_TIME = "2026-09-16 19:59 EDT (UTC-04:00), after-hours; Stock Analysis"
DCF_BASE = 5.9930
DCF_CENTERED_RANGE = (4.0382, 9.0873)
DCF_FIXED_GRID_RANGE = (6.0937, 14.5950)

# TRAINING / VALIDATION ONLY: never inputs to the Amazon run.
TRAINING_TARGET = dict(ticker="ABG", price=243.03, eps=21.50)
TRAINING_PEERS = [dict(ticker="AN", price=169.84, eps=16.92),
                  dict(ticker="GPI", price=421.48, eps=36.81)]


def positive(value):
    return (isinstance(value, (int, float)) and not isinstance(value, bool)
            and math.isfinite(value) and value > 0)


def ticker(row):
    return str(row.get("ticker", "")).strip().upper()


def pe(row):
    if not positive(row.get("price")) or not positive(row.get("eps")):
        return None
    value = row["price"] / row["eps"]
    return value if math.isfinite(value) else None


def analyze(target, peers):
    """Lab 07 min/median/max policy, with explicit admission decisions."""
    seen, accepted, notes = set(), [], []
    for row in peers:
        name = ticker(row)
        if not name:
            notes.append("Missing ticker: excluded")
        elif name == ticker(target):
            notes.append(f"{name}: target excluded from peers")
        elif name in seen:
            notes.append(f"{name}: duplicate excluded; first occurrence retained")
        else:
            seen.add(name)
            if row.get("decision", "use") not in ("use", "qualify"):
                notes.append(f"{name}: excluded by documented decision")
            elif pe(row) is None:
                notes.append(f"{name}: P/E not meaningful; missing/nonpositive/nonfinite input")
            else:
                accepted.append((name, pe(row)))
    multiples = [v for _, v in accepted]
    middle = median(multiples) if multiples else None
    eps = target.get("eps")
    estimate = middle * eps if middle is not None and positive(eps) else None
    bounds = ((min(multiples) * eps, max(multiples) * eps)
              if len(multiples) >= 2 and positive(eps) else None)
    removals = []
    for name, _ in accepted:
        remaining = [v for other, v in accepted if other != name]
        value = median(remaining) * eps if remaining and positive(eps) else None
        removals.append((name, len(remaining), value,
                         value - estimate if value is not None else None))
    return dict(peers=accepted, notes=notes, median=middle, estimate=estimate,
                range=bounds, removals=removals)


def check_dates(target, peers):
    comparison = date.fromisoformat(VALUATION_DATE)
    for row in [target] + list(peers):
        if date.fromisoformat(row["price_date"]) != comparison:
            raise ValueError(f"{ticker(row)}: price date mismatch")
        end = date.fromisoformat(row["year_end"])
        published = date.fromisoformat(row["published"])
        if not end <= published <= comparison:
            raise ValueError(f"{ticker(row)}: annual earnings unavailable by valuation date")


def print_result(target, peers):
    result = analyze(target, peers)
    observed = pe(target)
    print(f"{ticker(target)} observed annual P/E: " +
          (f"{observed:.6f}x" if observed is not None else "not meaningful"))
    for note in result["notes"]:
        print(note)
    for name, multiple in result["peers"]:
        print(f"{name} P/E: {multiple:.6f}x")
    if result["median"] is None:
        print("No usable peers; no estimate or range.")
        return result
    print(f"Peer median P/E: {result['median']:.6f}x")
    if result["estimate"] is None:
        print("Target EPS not meaningful; no implied price.")
    elif result["range"] is None:
        print(f"Single-peer reference: ${result['estimate']:.2f}; no range")
    else:
        print(f"Implied low/high: ${result['range'][0]:.2f} / ${result['range'][1]:.2f}")
        print(f"Median-implied price: ${result['estimate']:.2f}")
    for name, count, value, delta in result["removals"]:
        if value is None:
            print(f"Remove {name}: no estimate")
        else:
            label = "reference; no range" if count == 1 else "median estimate"
            print(f"Remove {name}: {label} ${value:.2f}; change ${delta:+.2f} "
                  f"({delta / result['estimate'] * 100:+.2f}%)")
    return result


def report():
    check_dates(TARGET, PEERS)
    print("AMAZON ANALYSIS ONLY - independent AMZN/WMT/MSFT inputs")
    print("Educational use only; not investment advice.")
    print(f"Valuation date: {VALUATION_DATE}; all prices regular-session close, USD/share.")
    print("Policy: qualified peers; min/median/max; no weighting, trimming, or cash/debt bridge.")
    for row in [TARGET] + PEERS:
        print(f"{row['ticker']}: price={row['price']:.2f}; EPS={row['eps']:.2f}; "
              f"year-end={row['year_end']}; published={row['published']}; {row['decision']}")
    result = print_result(TARGET, PEERS)
    if result["estimate"] is not None and positive(TARGET.get("price")):
        values = ([result["range"][0], result["estimate"], result["range"][1]]
                  if result["range"] else [result["estimate"]])
        for label, value in zip(("low", "median", "high") if result["range"] else ("reference",), values):
            print(f"{label}: unrounded={value:.10f}; vs dated market="
                  f"{(value / TARGET['price'] - 1) * 100:+.2f}%; "
                  f"vs newer quote={(value / CURRENT_PRICE - 1) * 100:+.2f}%")
    print(f"Newer AMZN context only: ${CURRENT_PRICE:.2f}; {CURRENT_QUOTE_TIME}")
    print("Newer quote does not update the historical peer valuation.")
    print(f"Saved September 10 DCF base: ${DCF_BASE:.4f}")
    print(f"Saved centered DCF sensitivity: ${DCF_CENTERED_RANGE[0]:.4f}-${DCF_CENTERED_RANGE[1]:.4f}")
    print(f"Saved required fixed-grid DCF: ${DCF_FIXED_GRID_RANGE[0]:.4f}-${DCF_FIXED_GRID_RANGE[1]:.4f}")
    print("No averaging of methods. Watch/defer; conditional peer references are not intrinsic value.")


def validate():
    count = 0

    def check(condition, message):
        nonlocal count
        if not condition:
            raise AssertionError(message)
        count += 1
        print("PASS | " + message)

    print("TRAINING / VALIDATION ONLY - professor Asbury regression FIRST")
    r = analyze(TRAINING_TARGET, TRAINING_PEERS)
    check(f"{r['peers'][0][1]:.6f}" == "10.037825", "AN P/E published answer")
    check(f"{r['peers'][1][1]:.6f}" == "11.450149", "GPI P/E published answer")
    check(f"{r['median']:.6f}" == "10.743987", "Training median published answer")
    check(tuple(f"{v:.2f}" for v in r['range']) == ("215.81", "246.18"), "Training range published answer")
    check(f"{r['estimate']:.2f}" == "231.00", "Training midpoint published answer")
    check(f"{r['removals'][1][2]:.2f}" == "215.81" and
          f"{r['removals'][1][3]:.2f}" == "-15.18", "Remove GPI and unrounded delta published answer")
    check(math.isclose(r['estimate'], float((Fraction(16984,1692)+Fraction(42148,3681))/2*Fraction(215,10)), abs_tol=1e-12), "Exact rational training cross-check")
    print("AMAZON ONLY - independent rational, date, and policy checks")
    check_dates(TARGET, PEERS)
    check(True, "All price dates match; all annual EPS published by comparison date")
    a = analyze(TARGET, PEERS)
    exact = [Fraction(10573,273), Fraction(49244,1795)]
    exact_values = sorted(v * Fraction(717,100) for v in exact)
    exact_mid = sum(exact_values) / 2
    check(all(math.isclose(v, float(e), abs_tol=1e-12) for (_,v),e in zip(a['peers'],exact)), "Both peer P/Es match exact rational division")
    check(all(math.isclose(v,float(e),abs_tol=1e-12) for v,e in zip(a['range'],exact_values)), "Amazon endpoints independently reconciled")
    check(math.isclose(a['estimate'],float(exact_mid),abs_tol=1e-12), "Amazon midpoint independently reconciled")
    for removal, value in zip(a['removals'], exact_values):
        check(math.isclose(removal[2],float(value),abs_tol=1e-12) and
              math.isclose(removal[3],float(value-exact_mid),abs_tol=1e-12), f"Remove {removal[0]}: exact reference and full-precision delta")
    check(analyze(TARGET, PEERS[:1])['range'] is None, "One peer is a reference, not a range")
    check(analyze(TARGET, PEERS[:1])['removals'][0][2] is None, "Removing sole peer leaves no estimate")
    check(analyze(TARGET, [])['estimate'] is None, "No peers leaves no estimate")
    check(analyze(TARGET, PEERS+[dict(PEERS[0],ticker=' wmt '),TARGET])['peers'] == a['peers'], "Deduplicate normalized names and exclude target")
    check(analyze(TARGET,[dict(PEERS[0],decision='exclude')])['estimate'] is None, "Excluded candidate cannot enter calculation")
    for bad in (None, 0, -1, float('nan'), float('inf'), 'missing', True):
        check(pe(dict(PEERS[0],price=bad)) is None and pe(dict(PEERS[0],eps=bad)) is None
              and analyze(dict(TARGET,eps=bad),PEERS)['estimate'] is None, f"Invalid input {bad!r} does not generate a valuation")
    check(analyze(dict(TARGET,price=None),PEERS)['estimate'] == a['estimate'], "Missing target price does not erase valid EPS-based value")
    check(analyze(TARGET,PEERS[::-1])['estimate'] == a['estimate'], "Peer order does not affect median")
    check(analyze(TARGET,[dict(p,price=p['price']/2,eps=p['eps']/2) for p in PEERS])['estimate'] == a['estimate'], "Matched peer split adjustment preserves valuation")
    for changed in (dict(PEERS[0],price_date='2026-09-11'),dict(PEERS[0],published='2026-09-11')):
        try:
            check_dates(TARGET,[changed])
        except ValueError:
            check(True, "Date mismatch or look-ahead rejected")
        else:
            check(False, "Invalid date accepted")
    check(f"{77670/10827:.2f}" == '7.17', "Annual Amazon income/share denominator rounds to reported EPS")
    check(set(t for t,_ in a['peers']) == {'WMT','MSFT'} and ticker(TARGET)=='AMZN', "No professor company or value enters Amazon peer case")
    print(f"ALL {count} CHECKS PASSED")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--validate', action='store_true')
    mode.add_argument('--training', action='store_true')
    args = parser.parse_args()
    if args.validate:
        validate()
    elif args.training:
        print("TRAINING / VALIDATION ONLY - Asbury; retrospective frozen 2024 case")
        print_result(TRAINING_TARGET, TRAINING_PEERS)
    else:
        report()
