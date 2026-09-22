"""Independent Lab 09 checks; standard library only. Educational use, not advice.
Run: python -B lab09/validate_lab09.py from the repository root.
Published checkpoints are test expectations, never inputs to the forecast engine.
"""

import copy
from decimal import Decimal as D, getcontext
import hashlib
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import proforma as model

getcontext().prec = 40
COUNT = 0


def check(condition, message):
    global COUNT
    if not condition:
        raise AssertionError(message)
    COUNT += 1
    print('PASS | ' + message)


def close(actual, expected, message, tolerance=1e-7):
    check(abs(actual - float(expected)) <= tolerance, message)


def decimal_reference():
    """Separate high-precision reconstruction from literal official inputs.
    Does not use model.project, model.VALUES, checks, or valuation formulas.
    Cash is independently reconciled via changes in balance-sheet accounts.
    """
    p = dict(revenue=D('17999'), inventory=D('2135.8'), ppe=D('3070.4'),
             other_assets=D('6371.6'), cash=D('40.4'), floor_plan=D('2027'),
             debt=D('3572'), other_liabilities=D('2127.5'), equity=D('3891.7'))
    rows = []
    for year, sga in zip(range(2026,2031),map(D,('0.665','0.655','0.645','0.645','0.645'))):
        r = {}
        r['revenue'] = p['revenue']*D('1.018')
        r['gross_profit'] = r['revenue']*D('0.1705')
        r['depreciation'] = p['ppe']*D('82.4')/D('3070.4')
        r['operating_income'] = r['gross_profit']*(1-sga)-r['depreciation']-D('120')
        r['interest'] = p['floor_plan']*D('0.0467')+p['debt']*D('0.0544')
        pretax = r['operating_income']-r['interest']
        r['net_income'] = pretax-max(D(0),pretax)*D('0.255')
        r['inventory'] = (r['revenue']-r['gross_profit'])*D('2135.8')/D('14927.3')
        r['floor_plan'] = r['inventory']*D('2027')/D('2135.8')
        r['ppe'] = p['ppe']+D('250')-r['depreciation']
        r['other_assets'] = p['other_assets']+(r['revenue']-p['revenue'])*D('0.008')-D('120')
        r['debt'] = p['debt']-D('150')
        r['other_liabilities'] = p['other_liabilities']
        r['equity'] = p['equity']+r['net_income']-D('150')
        # Assets/investment and funding movements provide an independent cash bridge.
        r['fcfe'] = (r['net_income']-(r['ppe']-p['ppe'])-(r['other_assets']-p['other_assets'])
                     -(r['inventory']-p['inventory'])+(r['floor_plan']-p['floor_plan'])+(r['debt']-p['debt']))
        r['cash'] = p['cash']+r['fcfe']-D('150')
        rows.append(r)
        p = r
    pv = sum(r['fcfe']/D('1.1')**i for i,r in enumerate(rows,1))
    tv = (rows[-1]['fcfe']+D('150'))*D('1.025')/D('0.075')
    terminal_pv = tv/D('1.1')**5
    return rows, dict(pv_years=pv,terminal_value=tv,pv_terminal=terminal_pv,
                     equity_value=pv+terminal_pv,terminal_share=terminal_pv/(pv+terminal_pv),
                     per_share=(pv+terminal_pv)/D('17.951349'))


def main():
    root = Path(__file__).resolve().parent.parent
    existing = [p for p in root.rglob('*') if p.is_file() and '.git' not in p.parts
                and 'lab09' not in p.relative_to(root).parts and '__pycache__' not in p.parts]
    before = {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in existing}
    print('LAB 09 VALIDATION | ABG TRAINING / VALIDATION ONLY | Educational use only')
    print('Independent decimal reconstruction and published checkpoint checks')
    rows = model.project()
    reference, valuation_ref = decimal_reference()
    checkpoints = {
        'revenue': ('18323.0','19678.3'), 'operating_income': ('844.2','971.4'),
        'net_income': ('413.6','527.5'), 'fcfe': ('211.4','342.3'), 'cash': ('101.8','719.8'),
    }
    for key, expected in checkpoints.items():
        for index, target in zip((0,-1),expected):
            check(f"{rows[index][key]:.1f}"==target, f"FY{rows[index]['year']}E {key} = {target}, published checkpoint")
    for key, target in {'gross_profit':'3124.1','sga':'2077.5','depreciation':'82.4','impairment':'120.0','interest':'289.0'}.items():
        check(f"{rows[0][key]:.1f}"==target, f'FY2026 handout {key} = {target}')
    check(f"{rows[0]['change_inventory']+rows[0]['change_other_wc']:.1f}"=='41.5','FY2026 handout working-capital investment = 41.5')
    check(f"{rows[0]['change_floor_plan']:.1f}"=='36.9','FY2026 handout floor-plan funding increase = 36.9')
    for r, ref in zip(rows,reference):
        year = r['year']
        for key, expected in ref.items():
            close(r[key],expected,f'FY{year}E {key}: independent Decimal reference')
        assets = r['cash']+r['inventory']+r['ppe']+r['other_assets']
        claims = r['floor_plan']+r['debt']+r['revolver']+r['other_liabilities']+r['equity']
        close(assets,claims,f'FY{year}E independently summed balance gap = 0.0')
        check(r['cash'] >= 25,f'FY{year}E cash >= 25.0')
        close(r['cash'],r['opening']['cash']+r['net_cash_change'],f'FY{year}E balance-sheet cash = cash-flow closing cash')
        close(r['ppe'],r['opening']['ppe']+r['capex']-r['depreciation'],f'FY{year}E PP&E roll-forward')
        close(r['debt'],r['opening']['debt']-r['repayment'],f'FY{year}E term-debt roll-forward')
        close(r['revolver'],0,f'FY{year}E base requires no revolver')
    v = model.value_equity(rows)
    for key, expected in valuation_ref.items():
        close(v[key],expected,f'{key}: independent Decimal valuation')
    check(f"{v['equity_value']:.1f}"=='5237.3','Equity value rounds to 5237.3 million')
    check(f"{100*v['terminal_share']:.1f}"=='79.8','Terminal share rounds to 79.8%')
    check(f"{v['per_share']:.2f}"=='291.75','Value per share = 291.75')
    check(f"{v['pv_years']:.1f}"=='1059.9' and f"{v['pv_terminal']:.1f}"=='4177.5','Handout explicit/terminal PV checkpoints = 1059.9 / 4177.5')

    print('\nDELIBERATE CASH-LINK BREAK')
    broken = copy.deepcopy(rows)
    broken[0]['cash'] = 40.4
    gap = (broken[0]['cash']+broken[0]['inventory']+broken[0]['ppe']+broken[0]['other_assets']
           -broken[0]['floor_plan']-broken[0]['debt']-broken[0]['revolver']-broken[0]['other_liabilities']-broken[0]['equity'])
    check(f'{gap:.1f}'=='-61.4','Independent deliberate FY2026 gap = -61.4')
    close(gap,-rows[0]['net_cash_change'],'Broken gap = negative of FY2026 cash increase')
    try:
        model.value_equity(broken)
    except ValueError as error:
        check('FY2026E' in str(error) and '-61.4' in str(error),'Valuation call refuses and names FY2026E and -61.4')
        print('Observed exception:',error)
    else:
        raise AssertionError('Broken balance sheet was valued')

    script = Path(__file__).with_name('proforma.py')
    script_hash = hashlib.sha256(script.read_bytes()).hexdigest()
    command = [sys.executable,'-B',str(script)]
    broken_run = subprocess.run(command+['--break-cash'],capture_output=True,text=True)
    check(broken_run.returncode==1,'Actual broken CLI exits 1')
    check('FY2026E balance_gap = -61.4' in broken_run.stdout,'Actual CLI reports required year and gap')
    check('Value per share:' not in broken_run.stdout and '\nVALUATION (' not in broken_run.stdout,'Actual broken CLI never prints valuation')
    print('COMMAND: python -B lab09/proforma.py --break-cash')
    print(broken_run.stdout[broken_run.stdout.index('CHECK BLOCK'):].strip())
    restored = subprocess.run(command,capture_output=True,text=True)
    check(restored.returncode==0 and 'Value per share: $291.75' in restored.stdout,'Undo run-time override: corrected CLI passes and prints $291.75 again')
    check(script_hash==hashlib.sha256(script.read_bytes()).hexdigest(),'Break test leaves original source unchanged')
    print('COMMAND: python -B lab09/proforma.py (override removed)')
    print(restored.stdout[restored.stdout.index('CHECK BLOCK'):].strip())

    # Independent liquidity failure: preserve balance while making cash insufficient.
    low_cash = copy.deepcopy(rows)
    shortfall = low_cash[2]['cash']-24
    low_cash[2]['cash'] -= shortfall
    low_cash[2]['other_assets'] += shortfall
    low_cash[2]['net_cash_change'] -= shortfall
    try:
        model.value_equity(low_cash)
    except ValueError as error:
        check('FY2028E cash_headroom = -1.0' in str(error),'Cash floor independently blocks a balanced but illiquid sheet')
    else:
        raise AssertionError('Minimum cash failure not rejected')
    for key in ('ppe','debt','cash'):
        altered = copy.deepcopy(rows)
        altered[3][key] += 1
        altered[3]['equity'] += 1  # Preserve balance so linkage check must detect it.
        try:
            model.value_equity(altered)
        except ValueError as error:
            check('FY2029E' in str(error),'Roll-forward check rejects isolated '+key+' error')
        else:
            raise AssertionError(key+' linkage error not rejected')
    for g in (0.10,0.11):
        bad_assumptions = dict(model.VALUES,terminal_growth=g)
        try:
            model.value_equity(rows,bad_assumptions)
        except ValueError:
            check(True,f'Terminal growth {g:.0%} >= cost of equity rejected')
        else:
            raise AssertionError('Invalid perpetual growth accepted')
    # Synthetic financing tests, not alternative ABG valuations.
    stressed_a = dict(model.VALUES,buyback=250.0)
    stressed = model.project(stressed_a)
    model.assert_balanced(stressed,stressed_a)
    check(stressed[0]['revolver_draw']>0,'Revolver draws only to fund cash floor')
    close(stressed[0]['cash'],25,'Draw restores cash exactly to floor')
    check(any(r['revolver_repayment']>0 for r in stressed[1:]),'Later excess cash repays revolver first')
    close(stressed[1]['revolver_interest'],stressed[0]['revolver']*.06,'Revolver interest uses opening drawn balance')
    no_floor_a = dict(model.VALUES,floor_plan_ratio=0.0)
    no_floor = model.project(no_floor_a)
    close(no_floor[0]['revolver'],850,'Removing floor plan exhausts revolver limit')
    close(no_floor[0]['change_floor_plan'],-2027,'Removing floor plan repays opening inventory loans')
    close(model.checks(no_floor[0],no_floor_a)['balance_gap'],0,'No-floor-plan diagnostic still balances')
    try:
        model.value_equity(no_floor,no_floor_a)
    except ValueError as error:
        check('cash_headroom' in str(error),'Missing floor-plan funding is rejected for insufficient cash')
        print(f"Floor-plan omission diagnostic FY2026 cash: {no_floor[0]['cash']:.1f} million; {error}")
    else:
        raise AssertionError('No-floor-plan liquidity failure accepted')
    check(all(label in ('history','guidance','judgment','fact') and reason.strip() for _,label,reason in model.INPUTS.values()),'Every input has a valid label and explanation')

    print('\nUNCHANGED PRIOR DCF EVIDENCE')
    root_run = subprocess.run([sys.executable,'-B',str(root/'dcf.py')],capture_output=True,text=True,check=True)
    check('Value per diluted share: 27.4974' in root_run.stdout,'Root dcf.py reproduces existing training value; not misidentified as Amazon')
    print('COMMAND: python -B dcf.py\n'+root_run.stdout.strip())
    amazon_run = subprocess.run([sys.executable,'-B',str(root/'lab06/dcf.py')],capture_output=True,text=True,check=True)
    saved = (root/'lab06/dcf_output_lab06.txt').read_text(encoding='utf-8-sig')
    check(amazon_run.stdout.strip()==saved.strip(),'Unchanged lab06/dcf.py exactly reproduces saved Week 3 output (newline-normalized)')
    print('COMMAND: python -B lab06/dcf.py\n'+amazon_run.stdout.strip())
    after = {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in existing}
    check(before==after,'All pre-existing repository files unchanged during validation')
    print('\nPRESERVATION SHA-256')
    for name,digest in before.items():
        print(name+': '+digest)
    print(f'\nALL {COUNT} CHECKS PASSED')


if __name__ == '__main__':
    main()  # An assertion, failed subprocess, or unhandled error exits nonzero.
