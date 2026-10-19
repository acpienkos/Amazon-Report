# Video 2 | Code and validation

AI-assisted speaking draft, NOT an actual transcript. 293 approximate spoken words; about 3.2 minutes at 125 wpm including transitions; hard limit 5:00. Review and use your own words. Do not claim checks not personally performed.

[Display README, then model.py and statements.py.]

The application uses a separate Edition B workspace; historical labs and original evidence are unchanged. The adapted statement engine starts with reported FY 2025 balances and forecasts 2026 through 2030. Cash follows operating, investing and financing cash flows; it is not a balance-sheet plug.

[Display financial statements and nonoperating investment row.]

The review added 39.767 billion of first-half investment uses,21.3 billion of subsequent OpenAI funding and 25 billion of July notes. The asset purchases reduce cash and increase other assets; borrowing enters financing. Neither becomes operating FCFF. The corrected base fails the funding floor in 2028 and 2029, even though accounting identities reconcile.

[Display FCFF reconciliation and terminal schedule.]

FCFF uses EBIT, an explicitly qualified 22% unlevered tax proxy, eligible depreciation, capital investment and working capital. Negative cash flows remain signed. New finance-lease assets count as investment; principal is financing. Operating leases remain rent, so their liability is not deducted again. Capital AP provides investment working-capital funding.

The terminal correction applies 15% to opening net PP&E, rather than growing last year's D&A with sales. Rental expense also follows opening assets and liabilities. Terminal investment still normalizes downward: that is an important assumption requiring evidence, not an established fact.

[Display tests and actual log.]

The latest suite has 59 passing model tests. It includes the original known answer and statement regression, cash-flow identities, negative FCFF, WACC/bridge/share checks, peers, scenario isolation, reverse repricing and deliberate accounting failures. New targeted tests cover the omitted investments, July debt, terminal policy and strategic-asset double counting. Seven dashboard pages and the technical cold run also execute.

[Display student worksheet and limitations.]

Those results do not certify my independent source checking or the AI-off exercise. The model remains approximate on seasonality, exact-date balances, diluted shares, taxes and segment profitability. The code makes these limits and funding failures visible rather than producing a false precise fair value.
