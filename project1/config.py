"""Dated inputs. All amounts USD millions, shares millions; rates decimal annual."""
AS_OF='2026-09-10'
PRICE=251.89
PRICE_SOURCE='https://chartexchange.com/symbol/nasdaq-amzn/historical/'
SEC='https://www.sec.gov/Archives/edgar/data/1018724/000101872426000026/amzn-20260630.htm'
K='https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm'
WACC_INPUTS=dict(risk_free=.0495,beta=1.44,equity_risk_premium=.05,debt_cost=.05341,
                 marginal_tax=.22,market_debt=124980+25000+13451+9315,market_equity=PRICE*10783)
# Market debt: Lab06 fair-value proxy plus Q2 finance leases and facility financing.
# Beta is a preserved vendor estimate; method/as-of cannot be independently reconstructed.
BRIDGE=dict(cash=78213,operating_cash=25000,securities=44775,debt=133320,
            finance_leases=13451,facility_financing=9315,operating_leases=96320,
            nonoperating_assets=0,other_claims=0,common_shares=10786.313572,
            incremental_dilutive_awards=134)
BRIDGE['known_debt_issuance']=25000
BRIDGE['known_subsequent_investment_cash']=21300
BRIDGE['debt']+=25000
# Denominator adds Q2 treasury-stock-method incremental awards to July22 common count.
# This is a disclosed proxy, not an exact point-in-time fully diluted share count.
TERMINAL_G=.025
# SEC Q2 cash-flow statement and Note2 subsequent-event disclosure. Known cash
# investments, not newly assumed growth spending. Future undisclosed purchases =0.
NONOPERATING_INVESTMENTS=[39767+21300,0,0,0,0]
NORMALIZATION_FTC=2500 # FY2025 Note1 named FTC settlement, removed from recurring forecast residual cost only
STRATEGIC_ASSETS=dict(private_equity=122300,anthropic_notes=97900,
                      equity_method=395,warrants=4300,subsequent_openai=21300)
AWS_2025=128725
ADVERTISING_2025=68635
AWS_GROWTH=[.33,.28,.23,.20,.16]
AD_GROWTH=[.26,.22,.18,.15,.12]
SCENARIOS={
 'base':dict(reason='Preserved Lab10 consolidated growth/margin/capex paths; provisional analyst judgments.'),
 'low':dict(margin_pp=-.01,capex_scale=1.10,aws_growth_pp=-.10,reason='Combined adverse legacy margin/capex endpoints plus slower AWS; illustrative joint stress, not a probability forecast.'),
 'high':dict(margin_pp=.01,capex_scale=.90,reason='Legacy favorable margin/capex endpoints; fixed growth under lower investment is an unproven joint assumption.'),
 'aws_slowdown':dict(aws_growth_pp=-.10,reason='Illustrative 10 percentage-point annual AWS growth reduction; other business revenue paths fixed, capex unchanged. Severity is judgment.'),
 'infrastructure_stress':dict(capex_scale=1.10,reason='Legacy +10% FY2027-2030 capex test; FY2026 $220bn unchanged.'),
 'margin_downside':dict(margin_pp=-.01,reason='Legacy one-percentage-point gross-margin reduction across forecast.'),
 'funding_stress':dict(no_2027_issuance=True,reason='Remove assumed $25bn FY2027 new term funding; do not add replacement funding.'),
}
PEERS=[
 dict(ticker='WMT',decision='qualify',price=105.73,price_date=AS_OF,eps=2.73,
      shares=7972.402501,share_date='2026-03-11',revenue=713163,ebit=29825,da=14203,
      cash=10727,securities=0,debt=6596+3542+34624,finance_leases=856+5905,
      minority=293+6270,restricted_securities=0,period_end='2026-01-31',published='2026-03-13',
      source='https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm',
      qualification='Retail/membership reference; no AWS. March outstanding shares proxy; older balance sheet. NCI at book proxy.'),
 dict(ticker='MSFT',decision='qualify',price=492.44,price_date=AS_OF,eps=17.95,
      shares=7427,share_date='2026-06-30',revenue=331839,ebit=155237,da=34300+4700,
      cash=20935,securities=55908,debt=9227+31067,finance_leases=66594,
      minority=0,restricted_securities=3800,period_end='2026-06-30',published='2026-07-29',
      source='https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm',
      qualification='Cloud/software reference; no retail. D&A sums rounded Note8 depreciation and Note10 intangible amortization, not CFO D&A-and-other. Restricted short-term investments not subtracted.'),
]
