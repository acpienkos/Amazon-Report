# Validation and AI use

Snapshot October 20, 2026. Source dates, use limits, and archive gates are in the [data card](data-card.md). The app uses the same engine as the [frozen output](visible-output.json). Setups and open items are in the [readiness record](lab20-readiness.md).

## Baseline and mandate check

The engine evaluates all 1,771 long-only, fully invested four-fund allocations on a five-percentage-point grid. It uses the Lab 14 weighted return, inverse volatility, covariance, and portfolio volatility functions. Annualized monthly arithmetic returns are estimates. Subtract 20 basis points of assumed incremental annual costs at the base. Adjusted closes already reflect historical fund-level expenses through fund performance. No taxes, market impact, or client-specific transaction costs are modeled explicitly.

Equal weight and inverse volatility fail the modeled mandate. The BIL-only benchmark fails the 4% net objective. The sole modeled pass at default inputs is 90% BIL and 10% VT with 4.20% estimated net return and 1.66% annualized volatility. Its 90% BIL clears the reserve gate, and 10% VT meets the conservative corporate issuer bound and the five-year equity cap. The proposed 4% annualized volatility cap applies when the known BAA observation reaches 6%. Five-day liquidity and fund-exposure checks are open, so modeled eligibility does not authorize a live allocation.

## AI-assisted sensitivity runs

| Scenario | Feasible mixes | Minimum-risk passing mix | Highest net within modeled risk limits |
|---|---:|---|---:|
| Base, 59 months, 20 bp | 1 | 90% BIL / 10% VT | 4.20% |
| VT annual estimate down 1 percentage point | 1 | 90% BIL / 10% VT | 4.10% |
| Last 36 monthly returns | 41 | 100% BIL | 5.75% |
| 50 bp annual drag | 0 | None | 3.90% |
| 40% BIL reserve floor | 1 | 90% BIL / 10% VT | 4.20% |
| One year until purchase | 0 | None | 3.83% |

The 36-month row's highest net estimate is for a different mix from the minimum-risk passing mix. The latter estimates 4.17% net. The 40% reserve stress leaves the result unchanged because the base passes with 90% BIL. At 50 bp the net estimate loses 30 bp while asset weights, means and covariance inputs stay fixed. At one year, the modeled equity cap drops to 5%, so the 90/10 portfolio is ineligible. The live decision remains reject throughout while the operational checks are open. The tested cost cutoff for modeled feasibility is 39 bp passes / 40 bp fails at integer precision.

## Locked Changed-Input Record

**Unresolved.** No verified student-authored, AI-off prediction commit or subsequent AI-off execution is available. The authored stress table above is an engineering diagnostic with Codex assistance. The student record requires a single independently chosen load-bearing input, old/new values with units, expected direction and decision impact, timestamp, pushed prediction commit, then preserved before/after output and reconciliation. The completed record belongs here, with the immutable commit link.

## AI disclosure

On November 17, 2026, OpenAI Codex assisted with course and repository review, design, implementation, automated tests, and documentation. The model version was not exposed in the work environment for this record. Codex proposed a 90/10 candidate based on the engine output. Validation recomputes its net estimate directly as 90% of the BIL estimate plus 10% of the VT estimate minus annual drag and probes the modeled 39/40 bp boundary. The result is accepted for a frozen scenario and qualified for deployment because the estimate is in-sample and operational mandate gates are open. Student review and ownership evidence remain pending.
