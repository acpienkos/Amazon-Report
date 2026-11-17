"""Reproduce the Project 2 committee research snapshot."""
import csv
import json
import math
from dataclasses import dataclass, replace
from datetime import date
from pathlib import Path
from statistics import correlation, mean, stdev

import portfolio

DATA = Path(__file__).resolve().parent / "data"
TICKERS = ("BIL", "IEF", "LQD", "VT")
DECISION_DATE = date(2026, 10, 20)
VINTAGE = date(2026, 9, 30)


@dataclass(frozen=True)
class Inputs:
    months: int = 59
    cost_bps: int = 20
    equity_shock_pp: float = 0
    reserve_pct: int = 20
    years_remaining: int = 5


def price_returns(months):
    with (DATA / "prices.csv").open(newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != ["date", *TICKERS]:
            raise ValueError("Unexpected price columns")
        prices = list(reader)
    indexes = []
    columns = [[] for _ in TICKERS]
    for row in prices:
        day = date.fromisoformat(row["date"])
        if day.day != 1 or (day.year, day.month) >= (DECISION_DATE.year, DECISION_DATE.month):
            raise ValueError("Use completed months only")
        indexes.append(day.year * 12 + day.month)
        for ticker, column in zip(TICKERS, columns):
            price = float(row[ticker])
            if not math.isfinite(price) or price <= 0:
                raise ValueError(f"Invalid {ticker} adjusted close")
            column.append(price)
    if len(indexes) <= months or any(b - a != 1 for a, b in zip(indexes, indexes[1:])):
        raise ValueError("Incomplete or non-contiguous price history")
    return [[b / a - 1 for a, b in zip(column, column[1:])][-months:] for column in columns]


def credit_snapshot(vintage=VINTAGE, decision=DECISION_DATE):
    if not 0 < (decision - vintage).days <= 30:
        raise ValueError("BAA vintage unavailable or stale")
    field = f"BAA_{vintage:%Y%m%d}"
    with (DATA / f"BAA_{vintage}.csv").open(newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != ["observation_date", field]:
            raise ValueError("BAA vintage header mismatch")
        values = []
        for row in reader:
            day = date.fromisoformat(row["observation_date"])
            if day.day != 1 or (day.year, day.month) >= (vintage.year, vintage.month):
                raise ValueError("BAA snapshot contains an incomplete observation month")
            if row[field] not in {"", "."}:
                value = float(row[field])
                if not math.isfinite(value) or value < 0:
                    raise ValueError("Invalid BAA yield")
                values.append((day, value))
    if not values or (decision - max(values)[0]).days > 90:
        raise ValueError("BAA observation missing or stale")
    measured, yield_pct = max(values)
    return {"vintage": str(vintage), "month": str(measured), "yield_pct": yield_pct}


def grid():
    for bills in range(21):
        for treasury in range(21 - bills):
            for credit in range(21 - bills - treasury):
                equity = 20 - bills - treasury - credit
                yield tuple(value / 20 for value in (bills, treasury, credit, equity))


def evaluate(inputs=Inputs()):
    if (not 2 <= inputs.months <= 59 or not 0 <= inputs.cost_bps <= 500
            or not -20 <= inputs.equity_shock_pp <= 20 or not 20 <= inputs.reserve_pct <= 100
            or not 0 <= inputs.years_remaining <= 5):
        raise ValueError("Scenario outside supported values")
    returns = price_returns(inputs.months)
    signal = credit_snapshot()
    volatility_cap = .04 if signal["yield_pct"] >= 6 else .05
    equity_cap = inputs.years_remaining * .05
    estimates = [12 * mean(column) for column in returns]
    estimates[-1] += inputs.equity_shock_pp / 100
    vols = [math.sqrt(12) * stdev(column) for column in returns]
    cov = portfolio.covariance_matrix(
        vols, [[correlation(left, right) for right in returns] for left in returns],
    )

    def measure(weights):
        net = portfolio.expected_return(weights, estimates) - inputs.cost_bps / 10_000
        vol = portfolio.portfolio_volatility(weights, cov)
        rules = (
            ("4% net objective", net >= .04),
            ("BIL reserve", weights[0] >= inputs.reserve_pct / 100),
            ("corporate issuer bound", weights[2] + weights[3] <= .10 + 1e-12),
            ("equity glide-path cap", weights[3] <= equity_cap + 1e-12),
            ("volatility cap", vol <= volatility_cap),
        )
        return {
            "weights": weights, "net_pct": 100 * net, "vol_pct": 100 * vol,
            "failures": [name for name, passed in rules if not passed],
        }

    equal = measure((.25,) * 4)
    inverse = measure(portfolio.inverse_volatility_weights(vols))
    benchmark = measure((1., 0., 0., 0.))
    feasible = []
    policy_only = []
    for weights in grid():
        row = measure(weights)
        if not row["failures"]:
            feasible.append(row)
        if row["failures"] in ([], ["4% net objective"]):
            policy_only.append(row)
    candidate = min(feasible, key=lambda row: (row["vol_pct"], -row["net_pct"]), default=None)
    return {
        "decision_date": str(DECISION_DATE), "ticker_order": TICKERS, "inputs": vars(inputs),
        "signal": signal, "volatility_cap_pct": 100 * volatility_cap,
        "equity_cap_pct": 100 * equity_cap, "gross_estimates_pct": [100 * n for n in estimates],
        "rows": {"Equal weight": equal, "Inverse volatility": inverse,
                 "BIL benchmark": benchmark, "Lowest-risk qualifying mix": candidate},
        "best_net_under_modeled_risk_limits": max(policy_only, key=lambda row: row["net_pct"], default=None),
        "feasible_count": len(feasible),
        "action": "Reject live allocation",
    }


def research():
    base = Inputs()
    stresses = {
        "equity estimate −1 pp": replace(base, equity_shock_pp=-1),
        "last 36 months": replace(base, months=36),
        "annual drag 50 bp": replace(base, cost_bps=50),
        "reserve 40%": replace(base, reserve_pct=40),
        "one year to purchase": replace(base, years_remaining=1),
    }
    return {"base": evaluate(base), "AI-assisted stress runs": {
        name: evaluate(inputs) for name, inputs in stresses.items()
    }}


if __name__ == "__main__":
    print(json.dumps(research(), indent=2, ensure_ascii=True))
