"""Interactive view of the frozen portfolio study."""
import streamlit as st

from engine import Inputs, TICKERS, evaluate

st.set_page_config(page_title="Home Down-Payment Portfolio", layout="wide")
st.title("Home Down-Payment Portfolio")
st.caption("OpenAI Codex assisted with implementation, testing and drafting. Andrew Pienkos owns the final analysis and decision after review.")
st.caption("Education, not investment advice.")

years = st.sidebar.slider("Years until purchase", 0, 5, 5)
reserve = st.sidebar.slider("Minimum BIL reserve (%)", 20, 100, 20, step=5)
cost = st.sidebar.number_input("Incremental annual cost (basis points)", 0, 500, 20, step=5)
shock = st.sidebar.number_input("VT annual estimate adjustment (percentage points)", -20., 20., 0., step=.5)
short_window = st.sidebar.checkbox("Use last 36 monthly returns")

try:
    result = evaluate(Inputs(36 if short_window else 59, cost, shock, reserve, years))
except (OSError, ValueError) as error:
    st.error(f"Stop: input checks failed. {error}")
    st.stop()

st.warning("Reject live allocation. The portfolio-level trading, liquidity and fund-exposure checks remain open.")
st.caption(f"Research snapshot {result['decision_date']} · {result['inputs']['months']} monthly returns")
signal = result["signal"]
st.write(f"BAA {signal['yield_pct']:.2f}% for {signal['month'][:7]} "
         f"(ALFRED vintage {signal['vintage']}). Volatility ceiling {result['volatility_cap_pct']:.0f}%.")
st.write(f"Equity ceiling {result['equity_cap_pct']:.0f}%. "
         f"{result['feasible_count']} mixes pass all modeled gates.")
rows = []
for name, row in result["rows"].items():
    if row is None:
        rows.append({"Portfolio": name, "Modeled verdict": "FAIL: no feasible mix"})
        continue
    rows.append({
        "Portfolio": name,
        **{ticker: f"{weight:.0%}" for ticker, weight in zip(TICKERS, row["weights"])},
        "Net estimate": f"{row['net_pct']:.2f}%",
        "Volatility": f"{row['vol_pct']:.2f}%",
        "Modeled verdict": "FAIL: " + ", ".join(row["failures"]) if row["failures"] else "PASS",
    })
st.table(rows)
best = result["best_net_under_modeled_risk_limits"]
if best:
    st.write(f"Highest modeled net estimate under the risk limits: {best['net_pct']:.2f}%.")
st.caption("Net estimates are annualized historical monthly means less the scenario cost. "
           "Modeled passes remain conditional on live implementation checks.")
