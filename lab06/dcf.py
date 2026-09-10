"""FIN 43900 Labs 05/06. Standard library only; sources and assumptions: lab06.md."""

# EDUCATIONAL USE ONLY
# This model was created for Purdue University FIN 43900 coursework.
# It is a simplified valuation exercise and should not be used to make
# investment, trading, or other financial decisions. It is not financial advice.

# EDITABLE SETTINGS. Amounts in USD millions; shares in millions; rates as decimals.
MODEL_CASE = "amazon"  # "training" reproduces the professor's inputs.
OPERATING_CASH_FLOW = 139514.0  # Reported FY2025, 10-K cash-flow statement, p. 36.
INTEREST_PAID = 1458.0  # Reported FY2025 debt cash interest, net of capitalized interest.
TAX_RATE = 0.21  # Estimate of marginal shield; 10-K Note 9 federal statutory rate.
CAPEX = 131819.0  # Reported FY2025 gross cash purchases of property and equipment.
STARTING_FCFF = OPERATING_CASH_FLOW + INTEREST_PAID * (1 - TAX_RATE) - CAPEX
GROWTH_RATES = [-0.50, 0.50, 0.40, 0.25, 0.15]  # FORECAST: pressure, then recovery/fade.
TERMINAL_GROWTH = 0.03  # ESTIMATE: long-run nominal growth, below economy-level trend.
CASH = 78213.0  # Reported 2026-06-30 cash and equivalents, 10-Q balance sheet.
DEBT = 132995.0 + 325.0  # Reported 10-Q Note 5: long-term face incl. current + short-term.
DILUTED_SHARES = 10903.0  # Reported Q2 2026 diluted weighted-average, Note 1 EPS.
REVERSE_TARGET_PRICE = 252.13  # Observed after-hours quote, 2026-09-10 16:26 EDT.
PRICE_OBSERVED_AT = "2026-09-10 16:44:44 EDT (20:44:44 UTC)"
PRICE_QUOTE_AT = "2026-09-10 16:26 EDT; after-hours; Stock Analysis AMZN overview"
RISK_FREE_RATE = 0.0495  # Treasury 2026-09-10 10-year nominal par yield.
BETA = 1.44  # Vendor estimate: Stock Analysis, Stock Price Statistics, Beta (5Y).
EQUITY_RISK_PREMIUM = 0.05  # Professor's stipulated assumption.
DEBT_RATE = 0.05341  # July 7, 2026 SEC pricing term sheet, 2036 notes' issue YTM proxy.
MARKET_COMMON_SHARES = 10783.0  # 2026-06-30 point-in-time common shares; WACC only.
MARKET_DEBT = 123800.0 + 855.0 + 325.0  # Quoted note FV + carrying-value proxies, June 30.
MARKET_EQUITY = REVERSE_TARGET_PRICE * MARKET_COMMON_SHARES  # ESTIMATE at quote date.
COST_OF_EQUITY = RISK_FREE_RATE + BETA * EQUITY_RISK_PREMIUM
AFTER_TAX_COST_OF_DEBT = DEBT_RATE * (1 - TAX_RATE)
WACC = (MARKET_EQUITY * COST_OF_EQUITY + MARKET_DEBT * AFTER_TAX_COST_OF_DEBT) / (MARKET_EQUITY + MARKET_DEBT)
SENSITIVITY_WACCS = [0.09, 0.10, 0.11]
SENSITIVITY_TERMINAL_GROWTHS = [0.02, 0.03, 0.04]
AMAZON_WACC_OFFSETS = [-0.01, 0.0, 0.01]  # Extra grid centered on estimated WACC.
AMAZON_TERMINAL_OFFSETS = [-0.01, 0.0, 0.01]
REVERSE_LOWER_SHIFT = -0.05
REVERSE_UPPER_SHIFT = 0.10
# Explicit supplementary experiment, not a replacement for the required bracket.
SHOW_EXTENDED_REVERSE = True
EXTENDED_REVERSE_LOWER = -0.05
EXTENDED_REVERSE_UPPER = 1.50

import argparse
import math


TRAINING = dict(starting_fcff=100.0, growth_rates=[0.08, 0.06, 0.05, 0.04, 0.03],
                wacc=0.10, terminal_growth=0.03, cash=50.0, debt=300.0, shares=50.0)


def amazon_inputs():
    return dict(starting_fcff=STARTING_FCFF, growth_rates=list(GROWTH_RATES), wacc=WACC,
                terminal_growth=TERMINAL_GROWTH, cash=CASH, debt=DEBT, shares=DILUTED_SHARES)


def calculate_dcf(inputs=None):
    """Lab 05 calculation, generalized so grid/solver never mutate the base inputs."""
    p = inputs if inputs is not None else (TRAINING if MODEL_CASE == "training" else amazon_inputs())
    rates = p["growth_rates"]
    values = [p[k] for k in ("starting_fcff", "wacc", "terminal_growth", "cash", "debt", "shares")] + list(rates)
    if not all(math.isfinite(v) for v in values):
        raise ValueError("All inputs must be finite numbers.")
    if p["terminal_growth"] >= p["wacc"]:
        raise ValueError("Terminal growth must be less than WACC.")
    if p["wacc"] <= -1 or p["terminal_growth"] <= -1:
        raise ValueError("WACC and terminal growth must exceed -100%.")
    if len(rates) != 5 or any(g <= -1 for g in rates):
        raise ValueError("Enter five growth rates, each above -100%.")
    if p["shares"] <= 0:
        raise ValueError("Diluted shares must be positive.")
    if p["starting_fcff"] <= 0:
        raise ValueError("Nonpositive starting FCFF requires an explicit recovery path; do not grow a loss.")

    fcff = p["starting_fcff"]
    forecast = []
    for growth in rates:
        fcff = fcff * (1 + growth)
        forecast.append(fcff)
    pv_explicit = sum(cash_flow / (1 + p["wacc"]) ** year
                      for year, cash_flow in enumerate(forecast, start=1))
    terminal_value = forecast[-1] * (1 + p["terminal_growth"]) / (p["wacc"] - p["terminal_growth"])
    pv_terminal = terminal_value / (1 + p["wacc"]) ** 5
    enterprise_value = pv_explicit + pv_terminal
    equity_value = enterprise_value + p["cash"] - p["debt"]
    value_per_share = equity_value / p["shares"]
    terminal_share = pv_terminal / enterprise_value
    return [(f"FCFF Year {year}", value) for year, value in enumerate(forecast, 1)] + [
        ("PV of explicit FCFF", pv_explicit), ("Terminal value at Year 5", terminal_value),
        ("PV of terminal value", pv_terminal), ("Enterprise value", enterprise_value),
        ("Equity value", equity_value), ("Value per diluted share", value_per_share),
        ("PV of terminal value / enterprise value", terminal_share),
    ]


def share_value(p):
    return calculate_dcf(p)[10][1]


def sensitivity_grid(p, waccs, terminal_rates):
    return [[None if g >= w else share_value(dict(p, wacc=w, terminal_growth=g))
             for g in terminal_rates] for w in waccs]


def reverse_dcf(p, target, lower=REVERSE_LOWER_SHIFT, upper=REVERSE_UPPER_SHIFT):
    """Bisection for one uniform additive shift; None means unbracketed."""
    if not all(math.isfinite(v) for v in (target, lower, upper)) or lower >= upper:
        raise ValueError("Target/bounds must be finite and lower must be below upper.")
    if any(g + min(lower, upper) <= -1 for g in p["growth_rates"]):
        raise ValueError("Rejected bracket: an annual growth rate reaches -100% or below.")
    def price(shift):
        return share_value(dict(p, growth_rates=[g + shift for g in p["growth_rates"]]))
    low_price, high_price = price(lower), price(upper)
    tolerance = 1e-8
    if abs(low_price - target) <= tolerance:
        return lower
    if abs(high_price - target) <= tolerance:
        return upper
    if not low_price < target < high_price:
        return None
    for _ in range(200):
        middle = (lower + upper) / 2
        middle_price = price(middle)
        if abs(middle_price - target) <= tolerance:
            return middle
        if middle_price < target:
            lower = middle
        else:
            upper = middle
    raise ValueError("Bisection did not converge to the requested price tolerance.")


def print_grid(p, waccs, terminal_rates, title):
    grid = sensitivity_grid(p, waccs, terminal_rates)
    print(f"\n{title} (USD per diluted share)")
    print("WACC / g | " + " | ".join(f"{g:.2%}" for g in terminal_rates))
    for w, row in zip(waccs, grid):
        print(f"{w:.6%} | " + " | ".join("INVALID" if v is None else f"{v:.2f}" for v in row))
    valid = [v for row in grid for v in row if v is not None]
    if valid:
        print(f"Grid range: {min(valid):.4f} to {max(valid):.4f}")


def print_reverse(p, target, lower, upper, title):
    print(f"\n{title}")
    print(f"Target share price: {target:.4f}")
    print(f"Search shift bounds: {lower * 100:+.2f} to {upper * 100:+.2f} percentage points")
    endpoint_prices = [share_value(dict(p, growth_rates=[g + s for g in p['growth_rates']]))
                       for s in (lower, upper)] if all(g + lower > -1 for g in p['growth_rates']) else []
    shift = reverse_dcf(p, target, lower, upper)
    if endpoint_prices:
        print(f"Endpoint prices (not solutions): {endpoint_prices[0]:.4f}, {endpoint_prices[1]:.4f}")
    if shift is None:
        print("no solution in bracket")
        print("Solved shift: unavailable; shifted growth rates: unavailable in this bracket")
    else:
        shifted = [g + shift for g in p["growth_rates"]]
        print(f"Solved growth-rate shift: {shift * 100:+.6f} percentage points")
        print("Shifted growth rates: " + ", ".join(f"{g:.6%}" for g in shifted))
        print(f"Repriced share value: {share_value(dict(p, growth_rates=shifted)):.8f}")
    print(f"Held fixed: starting FCFF={p['starting_fcff']:.4f} USD m; WACC={p['wacc']:.8%}; "
          f"terminal growth={p['terminal_growth']:.2%}; cash={p['cash']:.4f} USD m; "
          f"debt={p['debt']:.4f} USD m; diluted shares={p['shares']:.4f} m; "
          "five end-of-year cash flows; terminal discount=5 years.")
    print("Only the uniform explicit-growth shift changes; WACC weights are not recalculated.")
    return shift


def report(p, training=False, lab05_only=False):
    for label, value in calculate_dcf(p):
        print(f"{label}: {value:.4f}")
    if lab05_only:
        return
    print("\nCASE: " + ("TRAINING (not Amazon)" if training else "AMAZON - sourced inputs and forecasts; see lab06.md"))
    print("Monetary totals: USD millions; share value: USD; last standard line: ratio.")
    print_grid(p, SENSITIVITY_WACCS, SENSITIVITY_TERMINAL_GROWTHS, "Required 9%/10%/11% WACC grid")
    if not training:
        print_grid(p, [p['wacc'] + d for d in AMAZON_WACC_OFFSETS],
                   [p['terminal_growth'] + d for d in AMAZON_TERMINAL_OFFSETS],
                   "Amazon grid centered on estimated base WACC and terminal growth")
        print(f"Market price quote: {PRICE_QUOTE_AT}; observed {PRICE_OBSERVED_AT}")
    target = 30.0 if training else REVERSE_TARGET_PRICE
    shift = print_reverse(p, target, REVERSE_LOWER_SHIFT, REVERSE_UPPER_SHIFT, "Required reverse DCF")
    if not training and shift is None and SHOW_EXTENDED_REVERSE:
        print_reverse(p, target, EXTENDED_REVERSE_LOWER, EXTENDED_REVERSE_UPPER,
                      "SUPPLEMENT: explicitly wider bracket; not a solution in the required bracket")
    if not training:
        ratio = share_value(p) / target
        print(f"\nValue / observed market price: {ratio:.6f}x")
        print(f"Reasonableness band: {0.5 * target:.4f} to {2 * target:.4f}")
        print("Band result: " + ("INSIDE" if 0.5 <= ratio <= 2 else "OUTSIDE"))
        print("Reverse DCF describes conditional assumptions consistent with price, not proof of mispricing.")


def check(condition, message):
    if not condition:
        raise AssertionError(message)
    print("PASS | " + message)


def validate_training():
    expected = [108.0, 114.48, 120.204, 125.0122, 128.7625, 448.4408,
                1894.6486, 1176.4277, 1624.8685, 1374.8685, 27.4974, 0.7240]
    lines = calculate_dcf(TRAINING)
    check(len(lines) == 12, "Lab 05: exactly twelve standard outputs")
    for (label, value), answer in zip(lines, expected):
        check(f"{value:.4f}" == f"{answer:.4f}", f"Lab 05: {label} = {value:.4f}; expected {answer:.4f}")
    check(abs(share_value(dict(TRAINING, wacc=.11)) - 23.41) < .01, "Lab 05: 11% WACC gives approximately $23.41")
    grid = sensitivity_grid(TRAINING, [.09, .10, .11], [.02, .03, .04])
    expected_grid = [[28.60, 32.94, 39.02], [24.36, 27.50, 31.69], [21.06, 23.41, 26.44]]
    for i, row in enumerate(grid):
        for j, value in enumerate(row):
            check(f"{value:.2f}" == f"{expected_grid[i][j]:.2f}",
                  f"Training grid WACC={[9,10,11][i]}%, g={[2,3,4][j]}% = {value:.2f}")
    validate_grid(TRAINING, [.09, .10, .11], [.02, .03, .04], "Training")
    shift = reverse_dcf(TRAINING, 30.0)
    check(shift is not None and abs(shift * 100 - 1.78) < .01, f"Training reverse shift = {shift * 100:+.6f} pp (about +1.78)")
    check(abs(share_value(dict(TRAINING, growth_rates=[g + shift for g in TRAINING['growth_rates']])) - 30) < 1e-7,
          "Training reverse DCF reprices to $30 within 0.0000001")
    check(reverse_dcf(TRAINING, 1000000) is None, "Unreachable target returns no solution, not a boundary")
    for w in (.03, .02):
        try:
            calculate_dcf(dict(TRAINING, wacc=w))
        except ValueError:
            print("PASS | Base calculation rejects terminal growth >= WACC")
        else:
            raise AssertionError("Missing terminal-growth guard")
    check(sensitivity_grid(TRAINING, [.03], [.03, .04]) == [[None, None]], "Invalid grid cells print INVALID")
    for lower in (-1.03, -1.04):
        try:
            reverse_dcf(TRAINING, 30, lower, .10)
        except ValueError:
            print("PASS | Reverse bracket rejects growth at or below -100%")
        else:
            raise AssertionError("Missing reverse-growth guard")
    lower_price = share_value(dict(TRAINING, growth_rates=[g - .05 for g in TRAINING['growth_rates']]))
    check(reverse_dcf(TRAINING, lower_price) == -.05, "An endpoint is accepted only when it actually matches the target")
    check(TRAINING['wacc'] == .10, "Training WACC remains 10%; test calculations do not mutate inputs")
    print("ALL TRAINING VALIDATIONS PASSED")


def validate_grid(p, waccs, terminal_rates, name):
    grid = sensitivity_grid(p, waccs, terminal_rates)
    check(all(row[j] < row[j + 1] for row in grid for j in range(len(row) - 1)), name + ": value rises with terminal growth")
    check(all(grid[i][j] > grid[i + 1][j] for i in range(len(grid) - 1) for j in range(len(grid[0]))), name + ": value falls with WACC")
    if math.isclose(waccs[1], p['wacc']) and math.isclose(terminal_rates[1], p['terminal_growth']):
        check(math.isclose(grid[1][1], share_value(p)), name + ": center equals base-case value")
    flat = [v for row in grid for v in row]
    check(min(flat) == grid[-1][0] and max(flat) == grid[0][-1], name + ": minimum/maximum occur at expected corners")


def validate_amazon():
    p = amazon_inputs()
    check(MODEL_CASE == 'amazon', "Final default case is Amazon; no training placeholders")
    check(math.isclose(STARTING_FCFF, 8846.82), "Amazon FCFF = 139514 + 1458*(1-0.21) - 131819 = 8846.82 USD m")
    check(0 < TERMINAL_GROWTH < WACC, "Amazon WACC exceeds terminal growth")
    values = [v for _, v in calculate_dcf(p)]
    check(all(math.isfinite(v) for v in values), "All twelve Amazon outputs are finite")
    check(math.isclose(values[6] / (1 + WACC) ** 5, values[7]), "Terminal value discounted exactly five years")
    check(math.isclose(values[8] + CASH - DEBT, values[9]), "Enterprise-to-equity bridge reconciles")
    check(math.isclose(values[9] / DILUTED_SHARES, values[10]), "Equity / EPS-note diluted shares equals value per share")
    validate_grid(p, SENSITIVITY_WACCS, SENSITIVITY_TERMINAL_GROWTHS, "Amazon required grid")
    validate_grid(p, [WACC+d for d in AMAZON_WACC_OFFSETS], [TERMINAL_GROWTH+d for d in AMAZON_TERMINAL_OFFSETS], "Amazon centered grid")
    low = share_value(dict(p, growth_rates=[g+REVERSE_LOWER_SHIFT for g in GROWTH_RATES]))
    high = share_value(dict(p, growth_rates=[g+REVERSE_UPPER_SHIFT for g in GROWTH_RATES]))
    shift = reverse_dcf(p, REVERSE_TARGET_PRICE)
    if shift is None:
        check(not low <= REVERSE_TARGET_PRICE <= high,
              f"Amazon no solution in required bracket: target {REVERSE_TARGET_PRICE:.4f} outside [{low:.4f}, {high:.4f}]")
    else:
        check(abs(share_value(dict(p, growth_rates=[g+shift for g in GROWTH_RATES]))-REVERSE_TARGET_PRICE)<1e-7, "Amazon reverse solution reprices to target")
    if SHOW_EXTENDED_REVERSE and shift is None:
        wide = reverse_dcf(p, REVERSE_TARGET_PRICE, EXTENDED_REVERSE_LOWER, EXTENDED_REVERSE_UPPER)
        check(wide is not None, "Supplementary wider bracket actually contains the target")
        check(abs(share_value(dict(p, growth_rates=[g+wide for g in GROWTH_RATES]))-REVERSE_TARGET_PRICE)<1e-7,
              f"Supplementary shift {wide*100:+.6f} pp reprices to target; not within required bracket")
    check(amazon_inputs() == p, "Sensitivity and reverse DCF leave Amazon base inputs unchanged")
    print("ALL AMAZON COMPUTATIONAL CHECKS PASSED")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--training', action='store_true', help='Print all three blocks for the training case')
    parser.add_argument('--lab05', action='store_true', help='Print only the original twelve training lines')
    parser.add_argument('--validate-training', action='store_true', help='Run training checks before any company run')
    parser.add_argument('--validate', action='store_true', help='Run training checks followed by Amazon checks')
    args = parser.parse_args()
    try:
        if args.validate_training or args.validate:
            validate_training()
            if args.validate:
                validate_amazon()
        else:
            training = args.training or args.lab05 or MODEL_CASE == 'training'
            report(TRAINING if training else amazon_inputs(), training, args.lab05)
    except (ValueError, AssertionError) as error:
        raise SystemExit(f"Error: {error}")
