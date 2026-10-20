"""Lab 13 Meridian mandate checker. Inputs are fictional course case facts.

Weights are percentages, money is USD millions, liquidity is business days.
This checks five allocation rules; it does not establish client suitability.
"""

from collections import defaultdict
from math import isclose, isfinite

# Editable inputs, transcribed from the official Lab 13 holdings table.
HOLDINGS = {
    "Cash": {"issuer": "none", "days": 0, "reserve_eligible": True},
    "Treasury bills": {"issuer": "U.S. Treasury", "days": 1, "reserve_eligible": True},
    "Treasury 10-year note": {"issuer": "U.S. Treasury", "days": 1, "reserve_eligible": True},
    "Global equity index fund": {"issuer": "diversified fund", "days": 2, "reserve_eligible": False},
    "Investment-grade bond fund": {"issuer": "diversified fund", "days": 3, "reserve_eligible": False},
    "Private real estate fund": {"issuer": "diversified fund", "days": 90, "reserve_eligible": False},
    "Acme Corp bonds": {"issuer": "Acme Corp", "days": 4, "reserve_eligible": False},
    "Acme Corp stock": {"issuer": "Acme Corp", "days": 1, "reserve_eligible": False},
}
CANDIDATES = {
    "A": dict(zip(HOLDINGS, [2, 2, 10, 60, 26, 0, 0, 0])),
    "B": dict(zip(HOLDINGS, [1, 0, 0, 55, 20, 15, 5, 4])),
    "C": dict(zip(HOLDINGS, [1, 1, 0, 70, 20, 0, 0, 8])),
    # AI-proposed attack: all cash. Student must independently judge it.
    "D": dict(zip(HOLDINGS, [100, 0, 0, 0, 0, 0, 0, 0])),
}
CANDIDATES["E"] = {holding: (40 if holding == "Investment-grade bond fund" else 60 if holding == "Global equity index fund" else 0) for holding in HOLDINGS}

RESERVE_SIZE = 100
QUARTERLY_DISTRIBUTION = 0.75
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW = 5
MINIMUM_LIQUID_SHARE = 90
ISSUER_LIMIT = 8
EXEMPT_ISSUERS = {"none", "U.S. Treasury", "diversified fund"}
TOLERANCE = 1e-9  # percentage points; rounding is for display only


def reserve_minimum():
    if not isfinite(RESERVE_SIZE) or RESERVE_SIZE <= 0:
        raise ValueError("Reserve size must be finite and positive")
    return QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION / RESERVE_SIZE * 100


def evaluate(weights):
    """Return measured percentages and pass flags, computed at full precision."""
    if set(weights) != set(HOLDINGS):
        raise ValueError("Candidate must contain exactly the holdings table keys")
    if any(not isfinite(w) for w in weights.values()):
        raise ValueError("Weights must be finite")
    companies = defaultdict(float)
    for holding, weight in weights.items():
        issuer = HOLDINGS[holding]["issuer"]
        if issuer not in EXEMPT_ISSUERS:
            companies[issuer] += weight
    total = sum(weights.values())
    lowest = min(weights.values())
    reserve = sum(w for h, w in weights.items() if HOLDINGS[h]["reserve_eligible"])
    liquid = sum(w for h, w in weights.items() if HOLDINGS[h]["days"] <= LIQUIDITY_WINDOW)
    largest = max(companies.values(), default=0.0)
    return {
        "Weights sum to 100": (total, isclose(total, 100, abs_tol=TOLERANCE, rel_tol=0)),
        "Long-only (lowest weight)": (lowest, lowest >= 0),
        f"Reserve >= {reserve_minimum():.1f}%": (reserve, reserve + TOLERANCE >= reserve_minimum()),
        f"Redeemable in {LIQUIDITY_WINDOW} days >= {MINIMUM_LIQUID_SHARE:g}%": (liquid, liquid + TOLERANCE >= MINIMUM_LIQUID_SHARE),
        f"Largest single company <= {ISSUER_LIMIT:g}%": (largest, largest <= ISSUER_LIMIT + TOLERANCE),
    }


def main():
    print(f"Reserve minimum: {reserve_minimum():.1f}%")
    for name, weights in CANDIDATES.items():
        print(f"\nCandidate {name}")
        checks = evaluate(weights)
        for rule, (value, passed) in checks.items():
            print(f"  {rule}: {value:.1f} {'pass' if passed else 'FAIL'}")
        print("  Calendar-year loss: requires CIO clarification")
        failures = sum(not passed for _, passed in checks.values())
        print("  " + (f"fails {failures} rule(s)" if failures else "passes every checkable rule"))


if __name__ == "__main__":
    main()
