"""Meridian training values: annual decimal returns/volatilities, fractional weights."""
import math
import sys

ASSETS = ("Treasury bills", "Treasury 10-year note", "Investment-grade bond fund", "Global equity index fund")
RETURNS = (0.035, 0.043, 0.050, 0.080)
VOLATILITIES = (0.005, 0.070, 0.060, 0.160)
CORRELATIONS = ((1., .10, .05, 0.), (.10, 1., .80, -.10), (.05, .80, 1., .25), (0., -.10, .25, 1.))
OBJECTIVE = .065  # CPI estimate .025 plus .04; not a forecast or guarantee
RESERVE_INDICES = (0, 1)
BENCHMARK = (0., 0., .4, .6)


def validate_correlations(matrix, n):
    if len(matrix) != n or any(len(row) != n for row in matrix):
        raise ValueError("Correlation matrix dimensions must match asset count")
    for i in range(n):
        for j in range(n):
            if not math.isfinite(matrix[i][j]) or not -1 <= matrix[i][j] <= 1:
                raise ValueError(f"Correlation [{i},{j}] must be finite and within [-1, 1]")
            if not math.isclose(matrix[i][j], matrix[j][i], abs_tol=1e-12, rel_tol=0):
                raise ValueError(f"Correlation matrix must be symmetric at [{i},{j}]")
        if not math.isclose(matrix[i][i], 1., abs_tol=1e-12, rel_tol=0):
            raise ValueError("Correlation diagonal must equal 1")


def validate_vector(values, n, label):
    if len(values) != n or any(not math.isfinite(v) for v in values):
        raise ValueError(f"{label} must have {n} finite entries")


def validate_weights(weights, n):
    validate_vector(weights, n, "Weights")
    if any(w < 0 or w > 1 for w in weights) or not math.isclose(sum(weights), 1., abs_tol=1e-10, rel_tol=0):
        raise ValueError("Long-only weights must lie in [0, 1] and sum to 1")


def covariance_matrix(volatilities, correlations):
    n = len(volatilities)
    validate_vector(volatilities, n, "Volatilities")
    if not n or any(v <= 0 for v in volatilities):
        raise ValueError("Volatilities must be positive")
    validate_correlations(correlations, n)
    return [[correlations[i][j] * volatilities[i] * volatilities[j] for j in range(n)] for i in range(n)]


def expected_return(weights, returns):
    validate_weights(weights, len(returns))
    validate_vector(returns, len(weights), "Returns")
    return sum(w * r for w, r in zip(weights, returns))


def portfolio_variance(weights, covariance):
    n = len(weights)
    validate_weights(weights, n)
    if len(covariance) != n or any(len(row) != n for row in covariance):
        raise ValueError("Covariance dimensions must match weights")
    for row in covariance:
        validate_vector(row, n, "Covariance row")
    variance = sum(weights[i] * weights[j] * covariance[i][j] for i in range(n) for j in range(n))
    if variance < -1e-12:
        raise ValueError("Negative portfolio variance: check covariance assumptions")
    return max(0., variance)


def portfolio_volatility(weights, covariance):
    return math.sqrt(portfolio_variance(weights, covariance))


def reserve_allocation(weights, indices=RESERVE_INDICES):
    validate_weights(weights, len(weights))
    if len(set(indices)) != len(indices) or any(i < 0 or i >= len(weights) for i in indices):
        raise ValueError("Reserve indices must be distinct valid asset indices")
    return sum(weights[i] for i in indices)


def meets_objective(portfolio_return, objective=OBJECTIVE):
    if not math.isfinite(portfolio_return) or not math.isfinite(objective):
        raise ValueError("Return and objective must be finite")
    return portfolio_return >= objective


def inverse_volatility_weights(volatilities):
    validate_vector(volatilities, len(volatilities), "Volatilities")
    if not volatilities or any(v <= 0 for v in volatilities):
        raise ValueError("Inverse volatility requires positive volatilities")
    inverse = [1 / v for v in volatilities]
    weights = tuple(x / sum(inverse) for x in inverse)
    validate_weights(weights, len(volatilities))
    return weights


def baselines():
    validate_vector(RETURNS, len(ASSETS), "Returns")
    validate_vector(VOLATILITIES, len(ASSETS), "Volatilities")
    return {"Benchmark": BENCHMARK, "Equal weight": (1 / len(ASSETS),) * len(ASSETS), "Inverse volatility": inverse_volatility_weights(VOLATILITIES)}


def comparison_rows():
    cov = covariance_matrix(VOLATILITIES, CORRELATIONS)
    rows = []
    for name, weights in baselines().items():
        ret = expected_return(weights, RETURNS)
        rows.append(f"| {name} | {' / '.join(f'{w * 100:.1f}' for w in weights)} | {ret * 100:.2f}% | {portfolio_volatility(weights, cov) * 100:.2f}% | {reserve_allocation(weights) * 100:.1f}% | {'Yes' if meets_objective(ret) else 'No'} |")
    return rows


def main():
    print("Meridian: course-authored annual training inputs; objective 6.50%")
    print("Weights order: " + " / ".join(ASSETS))
    print("| Portfolio | Weights (%) | Return | Volatility | Reserve | Meets objective? |")
    print("|---|---|---:|---:|---:|---|")
    print("\n".join(comparison_rows()))


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        print(f"Input error: {error}", file=sys.stderr)
        sys.exit(1)
