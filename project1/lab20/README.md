# Project 2 · Home Down-Payment Portfolio

OpenAI Codex assisted with implementation, stress testing, repository checks, and drafting. Andrew Pienkos owns the final analysis and decision upon review.

Education, not investment advice.

**Committee decision for the October 20, 2026 research snapshot:** Reject live allocation (0% through this process). Reconsider a 0–5% VT pilot only after the purchase date and loss tolerance are confirmed, fund exposures and five-day cash availability are verified, and an independent holdout supports the 4% net objective under realistic costs and the nearer-purchase glide path.

## Run

From a clone of this repository, change into `project1/lab20`. Use a standard Python 3.13 environment. Install once with `python -m pip install -r requirements.txt`. Then run:

```sh
python -m streamlit run app.py
```

The landing page displays the decision and mandate verdicts. Increase incremental annual cost to 50 bp to see the qualifying mix fail. Use the 36-month switch to see how window choice changes the result. Default settings reproduce the frozen output. No keys or live data fetches are needed at runtime.

`python engine.py` prints the frozen analysis and five stress scenarios. `python verify.py` checks the published output, arithmetic, timing, and app interaction.

## Evidence

- [Visible executed output](docs/visible-output.json) and [committee memo](docs/decision-memo.md)
- [Validation, stress comparison, and AI disclosure](docs/validation-and-ai-use.md)
- [Data card and sources](docs/data-card.md)
- [Lab 20 readiness record](docs/lab20-readiness.md) and [Project 2 manifest](docs/manifest.md)
- [Calculation engine](engine.py) reuses the Lab 14 [portfolio arithmetic](portfolio.py)

The mandate comes from [Lab 13](../../lab13/lab13.md#my-project-2-mandate--ai-assistance-permitted). The proposed BIL/IEF/LQD/VT universe and monthly Yahoo snapshots come from [Lab 14](../../lab14/README.md). The date-level BAA vintage comes from [Lab 17](../../lab17/DATA_CARD.md). The research uses historical sample averages and covariance with no holdout performance claim. Allocation controls model portfolio weights and costs. Live settlement, stressed liquidity, and fund-level restrictions require separate verification.
