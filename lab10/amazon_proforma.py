"""Amazon FIN439 Lab10. Educational use only; not investment advice.
Adapted from the preserved Lab09 calculation order, tables, and refusal gate.
All financial assumptions live in amazon_assumptions.csv; no third-party packages.
Codex-assisted model; proposed judgments require the student's review.
"""
import argparse
import csv
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
with (HERE / 'amazon_assumptions.csv').open(encoding='utf-8', newline='') as f:
    REGISTER = list(csv.DictReader(f))
VALUES = {r['Assumption']: json.loads(r['Value']) for r in REGISTER}
TOLERANCE = 1e-6  # USD million: $1; numerical tolerance, not an economic input.
ASSETS = ('cash','securities','inventory','receivables','ppe','operating_rou','goodwill','other_assets')
LIABILITIES = ('trade_payables','capex_payables','operating_accruals','unearned','operating_lease',
               'finance_lease','financing_obligation','debt','revolver','other_liabilities')
OPENING_KEYS = ASSETS + LIABILITIES + ('equity','revenue')


def opening(a):
    return {key:a['opening_'+key] for key in OPENING_KEYS}


def project(values=None):
    a = dict(VALUES if values is None else values)
    if not a['cash_settled_compensation']:
        raise ValueError('Changing cash compensation requires an explicit dilution model; valuation refused')
    p = opening(a)
    rows = []
    for i,y in enumerate(range(a['first_year'], a['last_year']+1)):
        r = {'year':y, 'opening':dict(p)}
        # 1. Income statement: explicit depreciation and lease expense schedules.
        r['revenue'] = p['revenue']*(1+a['growth'][i])
        r['gross_profit'] = r['revenue']*a['gross_margin'][i]
        r['cost_of_sales'] = r['revenue']-r['gross_profit']
        r['sga'] = r['gross_profit']*a['sga_to_gp'][i]
        r['other_operating_cost'] = r['revenue']*a['other_cost_ratio']
        r['depreciation'] = p['ppe']*a['depreciation_rate']
        r['rou_amortization'] = p['operating_rou']*a['rou_amortization_rate']
        r['operating_lease_accretion'] = p['operating_lease']*a['operating_lease_rate']
        r['operating_lease_expense'] = r['rou_amortization']+r['operating_lease_accretion']
        r['operating_lease_cash'] = r['operating_lease_expense']
        r['operating_income'] = (r['gross_profit']-r['sga']-r['other_operating_cost']
                                 -r['depreciation']-r['operating_lease_expense'])
        r['debt_net_change'] = a['debt_net_change'][i]
        r['debt_interest'] = (p['debt']+r['debt_net_change']/2)*a['debt_rate']
        r['finance_lease_interest'] = p['finance_lease']*a['finance_lease_rate']
        r['financing_interest'] = p['financing_obligation']*a['financing_rate']
        r['revolver_interest'] = p['revolver']*a['revolver_rate']
        r['interest_expense'] = sum(r[k] for k in ('debt_interest','finance_lease_interest','financing_interest','revolver_interest'))
        r['interest_income'] = (p['cash']+p['securities'])*a['cash_yield']
        r['other_income'] = a['other_income']
        r['pretax_income'] = r['operating_income']+r['interest_income']+r['other_income']-r['interest_expense']
        r['income_tax'] = max(0,r['pretax_income'])*a['tax_rate']
        r['net_income'] = r['pretax_income']-r['income_tax']
        # 2. All noncash balance-sheet movements and financing schedules.
        r['inventory'] = r['cost_of_sales']*a['inventory_days']/a['days_per_year']
        r['receivables'] = r['revenue']*a['receivables_ratio']
        r['trade_payables'] = r['cost_of_sales']*a['trade_payable_ratio']
        r['operating_accruals'] = r['revenue']*a['accrual_ratio']
        r['unearned'] = r['revenue']*a['unearned_ratio']
        r['capex'] = a['capex_2026_guidance'] if i==0 else a['capex_later'][i-1]
        r['capex_payables'] = r['capex']*a['capex_payable_ratio']
        r['change_capex_payables'] = r['capex_payables']-p['capex_payables']
        r['finance_lease_addition'] = a['finance_lease_addition']
        r['finance_lease_principal'] = min(p['finance_lease'],p['finance_lease']*a['finance_lease_principal_rate'])
        r['finance_lease'] = p['finance_lease']+r['finance_lease_addition']-r['finance_lease_principal']
        r['financing_addition'] = a['new_financing_obligations']
        r['financing_principal'] = min(p['financing_obligation'],max(0,a['financing_payments'][i]-r['financing_interest']))
        r['financing_obligation'] = p['financing_obligation']+r['financing_addition']-r['financing_principal']
        r['ppe_additions'] = r['capex']+r['change_capex_payables']+r['finance_lease_addition']+r['financing_addition']
        r['ppe'] = p['ppe']+r['ppe_additions']-r['depreciation']
        r['operating_lease_addition'] = r['rou_amortization']+p['operating_rou']*a['rou_growth']
        r['operating_rou'] = p['operating_rou']+r['operating_lease_addition']-r['rou_amortization']
        r['operating_lease'] = p['operating_lease']+r['operating_lease_addition']+r['operating_lease_accretion']-r['operating_lease_cash']
        r['debt'] = p['debt']+r['debt_net_change']
        r['securities'] = p['securities']
        for k in ('goodwill','other_assets','other_liabilities'):
            r[k] = p[k]*(1+a['other_balance_growth'])
        r['distributions'] = a['distributions']
        r['equity'] = p['equity']+r['net_income']-r['distributions']
        # 3. Cash flows. Capital AP is excluded from OPERATING working capital.
        r['change_operating_wc'] = (r['inventory']-p['inventory']+r['receivables']-p['receivables']
                                   -(r['trade_payables']-p['trade_payables'])
                                   -(r['operating_accruals']-p['operating_accruals'])
                                   -(r['unearned']-p['unearned']))
        r['change_other_net_assets'] = (r['goodwill']-p['goodwill']+r['other_assets']-p['other_assets']
                                       -(r['other_liabilities']-p['other_liabilities']))
        # Equal operating lease expense/cash cancels ROU and liability noncash moves.
        # SBC is cash-replacement compensation inside expenses: no fictitious addback.
        r['operating_cash_flow'] = r['net_income']+r['depreciation']-r['change_operating_wc']
        r['investing_cash_flow'] = -r['capex']-r['change_other_net_assets']
        r['fcfe_before_revolver'] = (r['operating_cash_flow']+r['investing_cash_flow']+r['debt_net_change']
                                     -r['finance_lease_principal']-r['financing_principal'])
        cash_before_securities = p['cash']+r['fcfe_before_revolver']-r['distributions']
        r['securities_sale'] = min(max(0,p['securities']-a['securities_liquidity_floor']),
                                    max(0,a['minimum_cash']-cash_before_securities))
        r['securities'] = p['securities']-r['securities_sale']
        r['investing_cash_flow'] += r['securities_sale']
        r['cash_before_revolver'] = cash_before_securities+r['securities_sale']
        need = max(0,a['minimum_cash']-r['cash_before_revolver'])
        r['revolver_draw'] = min(need,max(0,a['revolver_limit']-p['revolver']))
        r['revolver_repayment'] = min(p['revolver'],max(0,r['cash_before_revolver']-a['minimum_cash']))
        r['revolver'] = p['revolver']+r['revolver_draw']-r['revolver_repayment']
        r['financing_cash_flow'] = (r['debt_net_change']-r['finance_lease_principal']-r['financing_principal']
                                    +r['revolver_draw']-r['revolver_repayment']-r['distributions'])
        # FCFE excludes liquidation of an existing securities reserve: not recurring
        # operations and not a new shareholder distribution in this retained-cash model.
        r['fcfe'] = r['fcfe_before_revolver']+r['revolver_draw']-r['revolver_repayment']
        r['net_cash_change'] = r['operating_cash_flow']+r['investing_cash_flow']+r['financing_cash_flow']
        # 4. Cash LAST, from cash flows; never assets-minus-liabilities balancing.
        r['cash'] = p['cash']+r['net_cash_change']
        rows.append(r)
        p = {key:r[key] for key in OPENING_KEYS}
    return rows


def checks(r, values=None):
    a = VALUES if values is None else values
    p = r['opening']
    return {
        'balance_gap':sum(r[k] for k in ASSETS)-sum(r[k] for k in LIABILITIES)-r['equity'],
        'cash_gap':r['cash']-p['cash']-r['operating_cash_flow']-r['investing_cash_flow']-r['financing_cash_flow'],
        'fcfe_gap':r['fcfe']-(r['net_cash_change']+r['distributions']-r['securities_sale']),
        'securities_gap':r['securities']-p['securities']+r['securities_sale'],
        'ppe_gap':r['ppe']-p['ppe']-r['capex']-r['change_capex_payables']-r['finance_lease_addition']-r['financing_addition']+r['depreciation'],
        'capital_ap_gap':r['change_capex_payables']-(r['capex_payables']-p['capex_payables']),
        'debt_gap':r['debt']-p['debt']-r['debt_net_change'],
        'finance_lease_gap':r['finance_lease']-p['finance_lease']-r['finance_lease_addition']+r['finance_lease_principal'],
        'financing_gap':r['financing_obligation']-p['financing_obligation']-r['financing_addition']+r['financing_principal'],
        'rou_gap':r['operating_rou']-p['operating_rou']-r['operating_lease_addition']+r['rou_amortization'],
        'operating_lease_gap':r['operating_lease']-p['operating_lease']-r['operating_lease_addition']-r['operating_lease_accretion']+r['operating_lease_cash'],
        'equity_gap':r['equity']-p['equity']-r['net_income']+r['distributions'],
        'revolver_gap':r['revolver']-p['revolver']-r['revolver_draw']+r['revolver_repayment'],
        'cash_headroom':r['cash']-a['minimum_cash'],
        'revolver_headroom':a['revolver_limit']-r['revolver'],
    }


def assert_balanced(rows, values=None):
    """Gate valuation on independently recomputed links and funding limits."""
    a = VALUES if values is None else values
    if [r['year'] for r in rows] != list(range(a['first_year'],a['last_year']+1)):
        raise ValueError('Missing or duplicate forecast year; valuation refused')
    p = opening(a)
    if abs(sum(p[k] for k in ASSETS)-sum(p[k] for k in LIABILITIES)-p['equity'])>TOLERANCE:
        raise ValueError('FY2025 opening balance gap; valuation refused')
    for r in rows:
        for k in OPENING_KEYS:
            gap = r['opening'][k]-p[k]
            if not math.isfinite(gap) or abs(gap)>TOLERANCE:
                raise ValueError(f"FY{r['year']} opening {k} gap {gap:.1f}; valuation refused")
        for name,gap in checks(r,a).items():
            bad = gap < -TOLERANCE if name.endswith('headroom') else abs(gap)>TOLERANCE
            if not math.isfinite(gap) or bad:
                raise ValueError(f"FY{r['year']} {name} = {gap:.1f} million; valuation refused")
        for k in ASSETS+LIABILITIES:
            if not math.isfinite(r[k]) or r[k]<-TOLERANCE:
                raise ValueError(f"FY{r['year']} invalid {k} = {r[k]}; valuation refused")
        p = r


def value_equity(rows, values=None):
    a = VALUES if values is None else values
    assert_balanced(rows,a)
    k,g = a['cost_of_equity'],a['terminal_growth']
    if not (math.isfinite(k) and math.isfinite(g) and k>g>-1):
        raise ValueError('Require finite equity return > terminal growth > -100%; valuation refused')
    if not math.isfinite(a['shares']) or a['shares']<=0:
        raise ValueError('Invalid share count; valuation refused')
    # Remove temporary revolver movements from sustainable CF; retain recurring
    # lease principal. Term debt is refinanced, so no perpetually shrinking debt.
    sustainable = rows[-1]['fcfe_before_revolver']-rows[-1]['debt_net_change']
    if not math.isfinite(sustainable) or sustainable<=0:
        raise ValueError(f"FY{rows[-1]['year']} negative or zero sustainable FCFE {sustainable:.1f}; terminal value refused")
    selected = [max(0,r['fcfe']) if a['positive_only'] else r['fcfe'] for r in rows]
    pv_explicit = sum(cf/(1+k)**t for t,cf in enumerate(selected,1))
    excluded_negative_pv = -sum(min(0,r['fcfe'])/(1+k)**t for t,r in enumerate(rows,1))
    terminal_cf = sustainable*(1+g)
    terminal_value = terminal_cf/(k-g)
    pv_terminal = terminal_value/(1+k)**len(rows)
    equity_value = pv_explicit+pv_terminal
    return dict(pv_explicit=pv_explicit,excluded_negative_pv=excluded_negative_pv,
                sustainable_fcfe=sustainable,terminal_cf=terminal_cf,terminal_value=terminal_value,
                pv_terminal=pv_terminal,equity_value=equity_value,per_share=equity_value/a['shares'],
                terminal_share=pv_terminal/equity_value,market_equity=a['market_price']*a['shares'])


STATEMENTS = {
 'INCOME STATEMENT':('revenue','cost_of_sales','gross_profit','sga','other_operating_cost','depreciation',
  'operating_lease_expense','operating_income','interest_income','debt_interest','finance_lease_interest',
  'financing_interest','revolver_interest','interest_expense','other_income','pretax_income','income_tax','net_income'),
 'BALANCE SHEET':ASSETS+('total_assets',)+LIABILITIES+('total_liabilities','equity','liabilities_equity'),
 'CASH FLOW / EQUITY CASH FLOW':('net_income','depreciation','change_operating_wc','operating_cash_flow',
  'capex','change_other_net_assets','securities_sale','investing_cash_flow','debt_net_change','finance_lease_principal',
  'financing_principal','fcfe_before_revolver','revolver_draw','revolver_repayment','fcfe','distributions',
  'financing_cash_flow','opening_cash','net_cash_change','cash'),
 'NONCASH INVESTMENT AND LEASE SCHEDULE':('change_capex_payables','finance_lease_addition','financing_addition',
  'ppe_additions','operating_lease_addition','rou_amortization','operating_lease_accretion','operating_lease_cash'),
}


def number(r,k):
    if k=='total_assets': return sum(r[z] for z in ASSETS)
    if k=='total_liabilities': return sum(r[z] for z in LIABILITIES)
    if k=='liabilities_equity': return number(r,'total_liabilities')+r['equity']
    if k=='opening_cash': return r['opening']['cash']
    return r[k]


def show(rows,a):
    for title,keys in STATEMENTS.items():
        print('\n'+title+' (USD million; expense/investment/principal rows positive unless cash-flow subtotal)')
        print(f"{'Line':<29}"+''.join(f"{r['year']:>14}" for r in rows))
        for k in keys:
            print(f"{k:<29}"+''.join(f'{number(r,k):14,.1f}' for r in rows))
    print('\nCHECK BLOCK: USD million; tolerance 0.000001 ($1); headroom must be nonnegative')
    print(f"{'Check':<29}"+''.join(f"{r['year']:>14}" for r in rows))
    for k in checks(rows[0],a):
        print(f'{k:<29}'+''.join(f'{0.0 if abs(checks(r,a)[k])<=TOLERANCE else checks(r,a)[k]:14,.1f}' for r in rows))
    for r in rows:
        status = 'negative FCFE' if r['fcfe'] < -TOLERANCE else ('zero FCFE' if abs(r['fcfe'])<=TOLERANCE else 'positive FCFE')
        print(f"FY{r['year']}: {status} {0.0 if abs(r['fcfe'])<=TOLERANCE else r['fcfe']:,.1f}; revolver draw {r['revolver_draw']:,.1f}, repayment {r['revolver_repayment']:,.1f}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--break-cash',action='store_true',help='Replace FY2026 ending cash with opening cash; expected refusal/exit1.')
    args = parser.parse_args()
    a = VALUES
    print('AMAZON.COM, INC. (AMZN) | FIN439 Lab10 | Educational use only')
    print('Financial inputs: amazon_assumptions.csv (single input register).')
    print('Forecast 2026-2030 from audited December31 2025; full-year discounting, not September2026 stub valuation.')
    print('Course positive-only convention; negative flows remain in statements and liquidity checks.')
    rows = project(a)
    if args.break_cash:
        rows[0]['cash'] = a['opening_cash']
        print('DELIBERATE BREAK: FY2026 computed ending cash replaced with FY2025 opening cash.')
    show(rows,a)
    try:
        v = value_equity(rows,a)
    except ValueError as e:
        print('ERROR:',e)
        return 1
    print('\nALL REQUIRED STATEMENT CHECKS PASS; valuation permitted.')
    for k in ('pv_explicit','excluded_negative_pv','sustainable_fcfe','terminal_cf','terminal_value','pv_terminal','equity_value'):
        print(f"{k}: {v[k]:,.2f} USD million")
    print(f"Value after 2030: {v['terminal_share']:.2%}")
    print(f"Fixed common shares: {a['shares']:,.6f} million")
    print(f"Value per share: ${v['per_share']:.2f}")
    print(f"The model says ${v['per_share']:.2f} per share, while the market says ${a['market_price']:.2f} as of September 24, 2026, 16:00 EDT, using the same disclosed share-count basis.")
    print(f"Market price times the same shares: {v['market_equity']:,.2f} USD million")
    return 0


if __name__=='__main__':
    raise SystemExit(main())
