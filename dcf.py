"""FIN 43900 Lab 05: training FCFF DCF (not an Amazon valuation)."""

# Editable inputs: dollars and diluted shares are in millions.
STARTING_FCFF = 100.0
GROWTH_RATES = [0.08, 0.06, 0.05, 0.04, 0.03]
WACC = 0.10
TERMINAL_GROWTH = 0.03
CASH = 50.0
DEBT = 300.0
DILUTED_SHARES = 50.0


def calculate_dcf():
    if TERMINAL_GROWTH >= WACC:
        raise ValueError("Terminal growth must be less than WACC.")
    if len(GROWTH_RATES) != 5:
        raise ValueError("Enter exactly five yearly growth rates.")
    if DILUTED_SHARES <= 0:
        raise ValueError("Diluted shares must be positive.")

    fcff = STARTING_FCFF
    forecast = []
    for growth in GROWTH_RATES:
        fcff = fcff * (1 + growth)
        forecast.append(fcff)

    pv_explicit = sum(
        cash_flow / (1 + WACC) ** year
        for year, cash_flow in enumerate(forecast, start=1)
    )
    terminal_value = forecast[-1] * (1 + TERMINAL_GROWTH) / (WACC - TERMINAL_GROWTH)
    pv_terminal = terminal_value / (1 + WACC) ** 5
    enterprise_value = pv_explicit + pv_terminal
    equity_value = enterprise_value + CASH - DEBT
    value_per_share = equity_value / DILUTED_SHARES
    terminal_share = pv_terminal / enterprise_value

    return [(f"FCFF Year {year}", value) for year, value in enumerate(forecast, 1)] + [
        ("PV of explicit FCFF", pv_explicit),
        ("Terminal value at Year 5", terminal_value),
        ("PV of terminal value", pv_terminal),
        ("Enterprise value", enterprise_value),
        ("Equity value", equity_value),
        ("Value per diluted share", value_per_share),
        ("PV of terminal value / enterprise value", terminal_share),
    ]


if __name__ == "__main__":
    try:
        for label, value in calculate_dcf():
            print(f"{label}: {value:.4f}")
    except ValueError as error:
        raise SystemExit(f"Error: {error}")
