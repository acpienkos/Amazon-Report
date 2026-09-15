"""FIN 43900 Lab 07: required training case and separate Amazon context.

Educational use only: simplified coursework, not financial or investment advice.
Sources, dates, definitions, and limitations are documented in lab07.md.
Standard library only; no network requests or package installation.
"""

# EDITABLE INPUTS: USD per ordinary share; annual total GAAP diluted EPS.
# TRAINING / VALIDATION ONLY: frozen 2024 prices and subsequently released EPS.
TARGET = {"ticker": "ABG", "price": 243.03, "eps": 21.50}
PEERS = [
    {"ticker": "AN", "price": 169.84, "eps": 16.92},
    {"ticker": "GPI", "price": 421.48, "eps": 36.81},
]

# AMAZON ONLY: supplemental earnings diagnostic, NOT a peer-implied valuation.
AMAZON_PRICE = 252.13  # Saved Lab 06 quote: 2026-09-10 16:26 EDT, after-hours.
AMAZON_EPS = 7.17  # FY2025 reported diluted EPS; 10-K, p. 37.
AMAZON_NET_INCOME = 77670.0  # USD million, FY2025; same statement.
AMAZON_ANNUAL_DILUTED_SHARES = 10827.0  # Million, FY2025 weighted average.

import argparse
import math
from fractions import Fraction
from statistics import median


def positive(value):
    return (isinstance(value, (int, float)) and not isinstance(value, bool)
            and math.isfinite(value) and value > 0)


def ticker(row):
    return str(row.get("ticker", "")).strip().upper()


def pe(row):
    price, eps = row.get("price"), row.get("eps")
    if not positive(price) or not positive(eps):
        return None
    result = price / eps
    return result if math.isfinite(result) else None


def analyze(target, peers):
    """First occurrence of a normalized ticker wins; all exclusions are visible."""
    seen, accepted, notes = set(), [], []
    for row in peers:
        name = ticker(row)
        if not name:
            notes.append("Missing ticker: excluded; identity cannot be deduplicated")
        elif name == ticker(target):
            notes.append(f"{name}: target excluded from peers")
        elif name in seen:
            notes.append(f"{name}: duplicate excluded (first occurrence retained)")
        else:
            seen.add(name)
            multiple = pe(row)
            if multiple is None:
                notes.append(f"{name}: P/E not meaningful; missing/nonpositive/nonfinite price or EPS")
            else:
                accepted.append((name, multiple))
    multiples = [value for _, value in accepted]
    middle = median(multiples) if multiples else None
    # The target price is needed for its observed P/E, not for an EPS-based implied value.
    eps = target.get("eps")
    estimate = middle * eps if middle is not None and positive(eps) else None
    bounds = (min(multiples) * eps, max(multiples) * eps) if len(multiples) >= 2 and positive(eps) else None
    removals = []
    for name, _ in accepted:
        remaining = [value for other, value in accepted if other != name]
        value = median(remaining) * eps if remaining and positive(eps) else None
        removals.append((name, len(remaining), value, value - estimate if value is not None else None))
    return {"peers": accepted, "notes": notes, "median": middle,
            "estimate": estimate, "range": bounds, "removals": removals}


def report(target, peers):
    result = analyze(target, peers)
    print("A. TRAINING / VALIDATION ONLY - required Asbury case, NOT AMAZON")
    print("Prices: 2024-12-31 close; earnings: FY2024 total GAAP diluted EPS.")
    print("Retrospective: annual earnings were published in 2025; not a point-in-time backtest.")
    print("Inputs and prices are USD/share; multiples are x. No cash/debt bridge.")
    observed = pe(target)
    print(f"Target {ticker(target)} observed P/E: " + (f"{observed:.6f}x" if observed is not None else "not meaningful"))
    for note in result["notes"]:
        print(note)
    for name, multiple in result["peers"]:
        print(f"{name} P/E: {multiple:.6f}x")
    if not result["peers"]:
        print("No usable peers; no estimate or range.")
        return
    print(f"Peer median P/E: {result['median']:.6f}x")
    if result["estimate"] is None:
        print("Target implied prices not meaningful: missing/nonpositive/nonfinite target EPS.")
    elif result["range"] is None:
        print(f"Single-peer reference estimate: ${result['estimate']:.2f}; no range")
    else:
        low, high = result["range"]
        print(f"Implied range: ${low:.2f} to ${high:.2f}")
        print(f"Median-implied price: ${result['estimate']:.2f}")
    for name, count, value, delta in result["removals"]:
        if value is None:
            print(f"Remove {name}: no estimate (no usable peers or target EPS not meaningful)")
        else:
            label = "reference estimate; no range" if count == 1 else "median-implied price"
            print(f"Remove {name}: {label} ${value:.2f}; change ${delta:+.2f}")
    print("Changes use unrounded estimates, not differences of displayed cents.")


def amazon_context():
    print("B. AMAZON ANALYSIS ONLY - supplemental earnings diagnostic, no peer valuation")
    print("Saved quote: $252.13, 2026-09-10 16:26 EDT after-hours; not a refreshed quote.")
    print(f"FY2025 reported total GAAP diluted EPS: ${AMAZON_EPS:.2f}")
    print(f"Net income / annual diluted shares: {AMAZON_NET_INCOME / AMAZON_ANNUAL_DILUTED_SHARES:.6f}")
    print(f"Observed price / FY2025 reported EPS: {AMAZON_PRICE / AMAZON_EPS:.6f}x")
    print("Annual EPS, not LTM or forecast EPS. Investment gains affect earnings quality.")
    print("No dealership multiple, cash/debt adjustment, or peer-implied Amazon range used.")


def validate():
    checks = 0

    def check(condition, message):
        nonlocal checks
        if not condition:
            raise AssertionError(message)
        checks += 1
        print("PASS | " + message)

    print("A. TRAINING / VALIDATION ONLY - frozen professor inputs")
    r = analyze(TARGET, PEERS)
    a = Fraction(16984, 1692)
    g = Fraction(42148, 3681)
    eps = Fraction(2150, 100)
    exact_mid = (a + g) / 2 * eps
    check(f"{pe(PEERS[0]):.6f}" == "10.037825", "AN P/E = 10.037825x")
    check(f"{pe(PEERS[1]):.6f}" == "11.450149", "GPI P/E = 11.450149x")
    check(f"{pe(TARGET):.6f}" == "11.303721", "ABG observed P/E = 11.303721x")
    check(f"{r['median']:.6f}" == "10.743987", "Median P/E = 10.743987x")
    check(tuple(f"{v:.2f}" for v in r['range']) == ("215.81", "246.18"), "Implied range = $215.81-$246.18")
    check(f"{r['estimate']:.2f}" == "231.00", "Median-implied price = $231.00")
    check(math.isclose(r['estimate'], float(exact_mid), abs_tol=1e-12), "Independent rational arithmetic matches full-precision midpoint")
    removed_gpi = r['removals'][1]
    check(f"{removed_gpi[2]:.2f}" == "215.81" and f"{removed_gpi[3]:.2f}" == "-15.18", "Remove GPI: $215.81 and change -$15.18")
    check(math.isclose(removed_gpi[3], float(a * eps - exact_mid), abs_tol=1e-12), "Leave-one-out delta uses unrounded values")
    check(f"{r['removals'][0][2]:.2f}" == "246.18" and f"{r['removals'][0][3]:.2f}" == "15.18", "Remove AN: $246.18 and change +$15.18")
    check(analyze(TARGET, PEERS[:1])['range'] is None, "One peer gives reference, no range")
    check(analyze(TARGET, PEERS[:1])['removals'][0][2] is None, "Removing sole peer gives no estimate")
    check(analyze(TARGET, [])['estimate'] is None, "No peers gives no estimate")
    messy = PEERS + [dict(PEERS[0], ticker=' an '), TARGET]
    clean = analyze(TARGET, messy)
    check(clean['peers'] == r['peers'] and len(clean['notes']) == 2, "Duplicate ticker and target excluded visibly")
    for bad in (None, 0, -1, float('nan'), float('inf'), 'missing'):
        for field in ('price', 'eps'):
            invalid_peer = analyze(TARGET, [dict(PEERS[0], **{field: bad})])
            check(not invalid_peer['peers'] and 'not meaningful' in invalid_peer['notes'][0], f"Invalid peer {field}={bad}: not meaningful")
        invalid_target = dict(TARGET, eps=bad)
        check(analyze(invalid_target, PEERS)['estimate'] is None, f"Invalid target EPS={bad}: implied prices not meaningful")
    no_price = dict(TARGET, price=None)
    check(pe(no_price) is None and analyze(no_price, PEERS)['estimate'] == r['estimate'], "Missing target price affects observed P/E, not EPS-based implied price")
    check(analyze(TARGET, [{"price": 10, "eps": 2}])['estimate'] is None, "Missing peer identity excluded")
    check(analyze(TARGET, PEERS[::-1])['estimate'] == r['estimate'], "Peer order does not change median")
    check(analyze(TARGET, [dict(p, price=p['price']/2, eps=p['eps']/2) for p in PEERS])['estimate'] == r['estimate'], "Consistent peer split adjustment preserves multiple")
    scaled = analyze(dict(TARGET, price=TARGET['price']/2, eps=TARGET['eps']/2), PEERS)
    check(scaled['estimate'] == r['estimate']/2, "Target split halves per-share implied value")
    # Synthetic test only: checks the odd-count median, not a company observation.
    odd = analyze(TARGET, PEERS + [{'ticker': 'SYNTHETIC', 'price': 100, 'eps': 1}])
    check(odd['median'] == pe(PEERS[1]), "Synthetic validation: three-peer median is middle observation")
    print("ALL TRAINING AND EDGE-CASE CHECKS PASSED")
    print("B. AMAZON ONLY - separate input and unit checks")
    check(f"{AMAZON_NET_INCOME/AMAZON_ANNUAL_DILUTED_SHARES:.2f}" == '7.17', "FY2025 net income / FY2025 diluted shares rounds to reported EPS")
    check(math.isclose(AMAZON_PRICE / AMAZON_EPS, float(Fraction(25213, 717)), abs_tol=1e-12), "Amazon annual P/E independently reconciles")
    check(AMAZON_ANNUAL_DILUTED_SHARES != 10903, "Annual EPS uses annual shares, not Lab 06 quarterly share count")
    print(f"ALL {checks} CHECKS PASSED")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--validate', action='store_true')
    group.add_argument('--amazon-context', action='store_true')
    args = parser.parse_args()
    if args.validate:
        validate()
    elif args.amazon_context:
        amazon_context()
    else:
        report(TARGET, PEERS)
