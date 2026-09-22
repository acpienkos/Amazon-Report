"""Lab 09: ABG TRAINING / VALIDATION ONLY, not Amazon analysis.
Educational use only; simplified coursework, not investment advice.
Standard library only. Sources, labels, and judgments are documented in lab09.md.
"""

import argparse
import math

# ONE INPUT REGISTER: (value, label, reason/source).
# All monetary inputs are USD millions; shares are millions; rates are decimals.
# Source: official Lab 09 assumption table/opening sheet and complete Part 1 captions.
INPUTS = {
    'revenue': (17999.0, 'history', 'FY2025 revenue supplied in Lab 09.'),
    'gross_profit_2025': (3071.7, 'history', 'FY2025 numerator used by the inventory-days formula.'),
    'depreciation_2025': (82.4, 'history', 'FY2025 depreciation used in the historical PP&E ratio.'),
    'inventory': (2135.8, 'history', 'FY2025 opening inventory.'),
    'ppe': (3070.4, 'history', 'FY2025 opening net PP&E.'),
    'other_assets': (6371.6, 'history', 'Official lab opening other assets; no cash plug.'),
    'cash': (40.4, 'history', 'FY2025 opening cash.'),
    'floor_plan': (2027.0, 'history', 'FY2025 inventory financing.'),
    'debt': (3572.0, 'history', 'FY2025 opening term debt.'),
    'other_liabilities': (2127.5, 'history', 'FY2025 opening other liabilities.'),
    'equity': (3891.7, 'history', 'FY2025 opening equity.'),
    'revolver': (0.0, 'fact', 'No opening revolver in the supplied case.'),
    'growth': (0.018, 'judgment', 'Modest organic growth above 1.2% same-store history; exclude bought growth.'),
    'gross_margin': (0.1705, 'judgment', 'Hold near FY2025 after the vehicle-shortage premium normalized.'),
    'sga_ratios': ((0.665, 0.655, 0.645, 0.645, 0.645), 'judgment', 'Integration costs rise first, then recover near recent normal; not the 2023 low.'),
    'impairment': (120.0, 'judgment', 'Recurring franchise write-downs; below the three-year average, not zero.'),
    'capex': (250.0, 'guidance', '2026 management guidance as identified in the tutorial.'),
    'tax_rate': (0.255, 'judgment', 'Between the three-year effective rate and FY2025 rate.'),
    'other_wc_ratio': (0.008, 'judgment', 'Small incremental non-inventory working-capital need as sales grow.'),
    'min_cash': (25.0, 'history', 'Course cash floor reflects the dealer cash-light funding pattern.'),
    'revolver_limit': (850.0, 'judgment', 'Finite liquidity backstop; do not allow unlimited funding to hide failure.'),
    'revolver_rate': (0.06, 'judgment', 'Assumed cost for the liquidity backstop; charge opening borrowings.'),
    'repayment': (150.0, 'judgment', 'Steady annual deleveraging in the five explicit years; not forever.'),
    'buyback': (150.0, 'judgment', 'Moderate distribution within recent repurchase experience; below FCFE.'),
    'floor_plan_rate': (0.0467, 'history', 'Tutorial FY2025 floor-plan interest/opening balance convention.'),
    'debt_rate': (0.0544, 'history', 'Tutorial FY2025 term interest/opening balance convention.'),
    'cost_of_equity': (0.10, 'judgment', 'Round base-case required equity return; not an independently estimated beta result.'),
    'terminal_growth': (0.025, 'judgment', 'Modest perpetual growth strictly below the required equity return.'),
    'shares': (17.951349, 'fact', 'June 30, 2026 10-Q share count supplied by the official lab.'),
    'other_liability_growth': (0.0, 'judgment', 'Hold other liabilities flat, as required by the simplified case.'),
    'first_year': (2026, 'fact', 'Official forecast starts in FY2026.'),
    'last_year': (2030, 'fact', 'Official forecast ends in FY2030; annual end-period discounting.'),
    'days_per_year': (365, 'fact', 'Course inventory-days convention.'),
}

VALUES = {name: item[0] for name, item in INPUTS.items()}
# Derived assumptions retain exact arithmetic; never replace with rounded percentages.
INPUTS.update({
    'capex_after_2026': (VALUES['capex'], 'judgment', 'Hold the 2026 investment level through 2030; a simplifying choice challenged by the higher H1 pace.'),
    'depreciation_ratio': (VALUES['depreciation_2025']/VALUES['ppe'], 'history', '82.4 / 3070.4, exact historical ratio.'),
    'inventory_days': (VALUES['inventory']/(VALUES['revenue']-VALUES['gross_profit_2025'])*VALUES['days_per_year'], 'history', '2135.8 / (17999.0 - 3071.7) * 365, exact.'),
    'floor_plan_ratio': (VALUES['floor_plan']/VALUES['inventory'], 'history', '2027.0 / 2135.8, exact.'),
})
VALUES = {name: item[0] for name, item in INPUTS.items()}
TOLERANCE = 1e-7  # Numerical checking tolerance, USD million; not a financial assumption.
OPENING_KEYS = ('revenue', 'inventory', 'ppe', 'other_assets', 'cash', 'floor_plan',
                'debt', 'other_liabilities', 'equity', 'revolver')


def project(values=None):
    a = dict(VALUES if values is None else values)
    years = range(a['first_year'], a['last_year'] + 1)
    if len(a['sga_ratios']) != len(years):
        raise ValueError('One SG&A assumption is required per forecast year.')
    prior = {key: a[key] for key in OPENING_KEYS}
    rows = []
    for index, year in enumerate(years):
        r = {'year': year, 'opening': dict(prior)}
        # 1. Income statement; financing interest uses OPENING balances.
        r['revenue'] = prior['revenue'] * (1 + a['growth'])
        r['gross_profit'] = r['revenue'] * a['gross_margin']
        r['cost_of_sales'] = r['revenue'] - r['gross_profit']
        r['sga'] = r['gross_profit'] * a['sga_ratios'][index]
        r['depreciation'] = prior['ppe'] * a['depreciation_ratio']
        r['impairment'] = a['impairment']
        r['operating_income'] = r['gross_profit'] - r['sga'] - r['depreciation'] - r['impairment']
        r['floor_interest'] = prior['floor_plan'] * a['floor_plan_rate']
        r['debt_interest'] = prior['debt'] * a['debt_rate']
        r['revolver_interest'] = prior['revolver'] * a['revolver_rate']
        r['interest'] = r['floor_interest'] + r['debt_interest'] + r['revolver_interest']
        r['pretax'] = r['operating_income'] - r['interest']
        r['tax'] = max(0, r['pretax']) * a['tax_rate']
        r['net_income'] = r['pretax'] - r['tax']
        # 2. Balance-sheet movements EXCEPT cash.
        r['inventory'] = r['cost_of_sales'] * a['inventory_days'] / a['days_per_year']
        r['floor_plan'] = r['inventory'] * a['floor_plan_ratio']
        r['capex'] = a['capex'] if year == a['first_year'] else a['capex_after_2026']
        r['ppe'] = prior['ppe'] + r['capex'] - r['depreciation']
        r['change_other_wc'] = a['other_wc_ratio'] * (r['revenue'] - prior['revenue'])
        r['other_assets'] = prior['other_assets'] + r['change_other_wc'] - r['impairment']
        r['repayment'] = a['repayment']
        r['debt'] = prior['debt'] - r['repayment']
        if r['debt'] < 0:
            raise ValueError(f'FY{year}E: repayment exceeds opening term debt.')
        r['other_liabilities'] = prior['other_liabilities'] * (1 + a['other_liability_growth'])
        r['buyback'] = a['buyback']
        r['equity'] = prior['equity'] + r['net_income'] - r['buyback']
        # 3. Cash flows; floor plan funds inventory, not an extra valuation bridge.
        r['change_inventory'] = r['inventory'] - prior['inventory']
        r['change_floor_plan'] = r['floor_plan'] - prior['floor_plan']
        r['operating_cash_flow'] = (r['net_income'] + r['depreciation'] + r['impairment']
                                   - r['change_inventory'] - r['change_other_wc'] + r['change_floor_plan'])
        r['fcfe'] = r['operating_cash_flow'] - r['capex'] - r['repayment']
        r['cash_before_revolver'] = prior['cash'] + r['fcfe'] - r['buyback']
        needed = max(0, a['min_cash'] - r['cash_before_revolver'])
        r['revolver_draw'] = min(needed, max(0, a['revolver_limit'] - prior['revolver']))
        r['revolver_repayment'] = min(prior['revolver'], max(0, r['cash_before_revolver'] - a['min_cash']))
        r['revolver'] = prior['revolver'] + r['revolver_draw'] - r['revolver_repayment']
        r['net_cash_change'] = r['fcfe'] - r['buyback'] + r['revolver_draw'] - r['revolver_repayment']
        r['cf_ending_cash'] = prior['cash'] + r['net_cash_change']
        # 4. Cash LAST: linked to cash flow, never liabilities + equity - other assets.
        r['cash'] = r['cf_ending_cash']
        rows.append(r)
        prior = {key: r[key] for key in OPENING_KEYS}
    return rows


def checks(row, values=None):
    a = VALUES if values is None else values
    p = row['opening']
    assets = sum(row[k] for k in ('cash', 'inventory', 'ppe', 'other_assets'))
    liabilities = sum(row[k] for k in ('floor_plan', 'debt', 'revolver', 'other_liabilities'))
    return {
        'balance_gap': assets - liabilities - row['equity'],
        'cash_flow_gap': row['cash'] - (p['cash'] + row['net_cash_change']),
        'ppe_gap': row['ppe'] - (p['ppe'] + row['capex'] - row['depreciation']),
        'debt_gap': row['debt'] - (p['debt'] - row['repayment']),
        'cash_headroom': row['cash'] - a['min_cash'],
    }


def assert_balanced(rows, values=None):
    """Recompute checks from statement lines, not cached totals; fail before valuation."""
    a = VALUES if values is None else values
    if [r['year'] for r in rows] != list(range(a['first_year'], a['last_year'] + 1)):
        raise ValueError('Forecast must contain every required year in order.')
    for row in rows:
        c = checks(row, a)
        for name, gap in c.items():
            bad = not math.isfinite(gap) or (gap < -TOLERANCE if name == 'cash_headroom' else abs(gap) > TOLERANCE)
            if bad:
                raise ValueError(f"FY{row['year']}E {name} = {gap:.1f} million; valuation refused")
        if not 0 <= row['revolver'] <= a['revolver_limit']:
            raise ValueError(f"FY{row['year']}E revolver outside limit; valuation refused")


def value_equity(rows, values=None):
    a = VALUES if values is None else values
    assert_balanced(rows, a)  # Mandatory first gate before any valuation arithmetic.
    k, g = a['cost_of_equity'], a['terminal_growth']
    if not (math.isfinite(k) and math.isfinite(g) and k > g > -1 and k > -1):
        raise ValueError('Require finite cost of equity > terminal growth > -100%.')
    if not math.isfinite(a['shares']) or a['shares'] <= 0:
        raise ValueError('Shares must be positive and finite.')
    pv_years = sum(r['fcfe'] / (1 + k)**t for t, r in enumerate(rows, 1))
    terminal_cf = (rows[-1]['fcfe'] + rows[-1]['repayment']) * (1 + g)
    terminal_value = terminal_cf / (k - g)
    pv_terminal = terminal_value / (1 + k)**len(rows)
    equity_value = pv_years + pv_terminal
    return dict(pv_years=pv_years, terminal_cf=terminal_cf, terminal_value=terminal_value,
                pv_terminal=pv_terminal, equity_value=equity_value,
                terminal_share=pv_terminal/equity_value, per_share=equity_value/a['shares'])


def table(title, rows, lines):
    print('\n' + title)
    print(f"{'USD millions':<32}" + ''.join(f"{str(r['year'])+'E':>13}" for r in rows))
    for label, getter in lines:
        values = [getter(r) for r in rows]
        print(f'{label:<32}' + ''.join(f'{0.0 if abs(v) <= TOLERANCE else v:13,.1f}' for v in values))


def display(rows):
    labels = {'sga': 'SG&A', 'ppe': 'PP&E', 'fcfe': 'FCFE', 'cf_ending_cash': 'Ending cash from cash flow'}
    fields = lambda names: [(labels.get(name, name.replace('_',' ').capitalize()), lambda r, k=name: r[k]) for name in names]
    table('INCOME STATEMENT', rows, fields(('revenue','cost_of_sales','gross_profit','sga','depreciation','impairment','operating_income','floor_interest','debt_interest','revolver_interest','interest','pretax','tax','net_income')))
    table('BALANCE SHEET', rows, fields(('cash','inventory','ppe','other_assets')) + [
        ('Total assets', lambda r: sum(r[k] for k in ('cash','inventory','ppe','other_assets')))] +
        fields(('floor_plan','debt','revolver','other_liabilities')) + [
        ('Total liabilities',lambda r: sum(r[k] for k in ('floor_plan','debt','revolver','other_liabilities')))] + fields(('equity',)) + [
        ('Liabilities plus equity',lambda r: sum(r[k] for k in ('floor_plan','debt','revolver','other_liabilities','equity')))])
    table('CASH FLOW TO EQUITY / CASH ROLL-FORWARD', rows, fields(('net_income','depreciation','impairment')) + [
        ('Inventory investment',lambda r: -r['change_inventory']),('Other WC investment',lambda r: -r['change_other_wc']),
        ('Floor-plan funding change',lambda r: r['change_floor_plan'])] + fields(('operating_cash_flow',)) + [
        ('Capital spending',lambda r: -r['capex']),('Term debt repayment',lambda r: -r['repayment'])] + fields(('fcfe',)) + [
        ('Share buyback',lambda r: -r['buyback']),('Revolver draw',lambda r: r['revolver_draw']),
        ('Revolver repayment',lambda r: -r['revolver_repayment']),('Opening cash',lambda r:r['opening']['cash'])] + fields(('net_cash_change','cf_ending_cash')))
    print('\nCHECK BLOCK (USD millions; zero gaps, nonnegative cash headroom required)')
    print('Year       Balance gap   Cash-flow gap    PP&E gap    Debt gap   Cash headroom   Status')
    for r in rows:
        c = checks(r)
        good = all(math.isfinite(v) and (v >= -TOLERANCE if k == 'cash_headroom' else abs(v) <= TOLERANCE) for k,v in c.items())
        shown = [0.0 if abs(v) <= TOLERANCE else v for v in c.values()]
        print(f"FY{r['year']}E" + ''.join(f'{v:14.1f}' for v in shown) + ('   PASS' if good else '   FAIL'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--break-cash', action='store_true', help='Deliberate temporary FY2026 cash-link error; expected exit 1.')
    args = parser.parse_args()
    print('ABG TRAINING / VALIDATION ONLY | Educational use; not investment advice.')
    print('INPUT REGISTER: value | label | reason/source')
    for key, (value, label, reason) in INPUTS.items():
        print(f'{key}: {value} | {label} | {reason}')
    rows = project()
    if args.break_cash:
        rows[0]['cash'] = VALUES['cash']
        print('\nDELIBERATE BREAK: FY2026 balance-sheet cash replaced by opening cash.')
    display(rows)
    try:
        v = value_equity(rows)
    except ValueError as error:
        print(f'ERROR: {error}')
        return 1
    print('\nVALUATION (USD millions except per share; annual end-period discounting)')
    for key in ('pv_years','terminal_cf','terminal_value','pv_terminal','equity_value'):
        print(f"{key}: {v[key]:,.2f}")
    print(f"Share of value after 2030: {v['terminal_share']*100:.2f}%")
    print(f"Value per share: ${v['per_share']:.2f}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
