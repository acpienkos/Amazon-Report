"""Lab 11 sensitivity. Default is base-only; changed runs require a saved human record.

Imports the unchanged Lab 10 engine. No model runs occur on import.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
spec = importlib.util.spec_from_file_location('lab10_engine', ROOT/'lab10/amazon_proforma.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
# An immutable serialized source prevents shared nested-list mutations.
BASE_JSON = json.dumps(m.VALUES, sort_keys=True)
OUTPUTS = ('operating_income', 'fcfe', 'per_share')
TOLERANCE = 1e-6  # USD million for statements; USD/share for share value.


def fresh_base():
    return json.loads(BASE_JSON)


def verify_preservation():
    manifest = json.loads((HERE/'preservation_manifest.json').read_text(encoding='utf-8'))
    for path, expected in manifest['sha256'].items():
        if hashlib.sha256((ROOT/path).read_bytes()).hexdigest() != expected:
            raise ValueError('Prior file changed: '+path)
    return manifest


def load_approved_plan():
    p = json.loads((HERE/'approved_ranges.json').read_text(encoding='utf-8'))
    if p['status'] != 'LOCKED' or not p.get('partner_pre_run_confirmed'):
        raise ValueError('STOP: genuine locked prediction and pre-run partner review required.')
    record = (HERE/'locked_prediction.md').read_bytes()
    record = record.split(b'\n## Post-run reconciliation',1)[0]
    if not p.get('exact_user_response') or hashlib.sha256(record).hexdigest() != p.get('locked_record_sha256'):
        raise ValueError('STOP: missing or mismatched locked record.')
    when = datetime.fromisoformat(p['recorded_at_utc'])
    if when.tzinfo is None or when > datetime.now(timezone.utc):
        raise ValueError('STOP: invalid actual record timestamp.')
    if len(p['drivers']) != 2 or len({d['key'] for d in p['drivers']}) != 2:
        raise ValueError('Exactly two different drivers required.')
    allowed = {'gross_margin','capex_later','growth','sga_to_gp','other_cost_ratio',
               'inventory_days','depreciation_rate','receivables_ratio','trade_payable_ratio'}
    for d in p['drivers']:
        if d['key'] not in allowed or not d.get('reason') or not d.get('units'):
            raise ValueError('Driver, units, and range evidence must be explicit.')
        base = fresh_base()[d['key']]
        expected_years = list(range(2027 if d['key']=='capex_later' else 2026,2031))
        if d['years'] != expected_years:
            raise ValueError('Affected years do not match the actual model indexing.')
        n = len(base) if isinstance(base,list) else 1
        if d['base'] != base or len(d['years']) != (n if isinstance(base,list) else 5):
            raise ValueError('Base or affected years mismatch.')
        lo, hi = d['lower'], d['higher']
        if lo is None or hi is None:
            raise ValueError('No endpoint may be inferred by the program.')
        b = base if isinstance(base,list) else [base]
        lo = lo if isinstance(lo,list) else [lo]
        hi = hi if isinstance(hi,list) else [hi]
        if len(lo)!=n or len(hi)!=n or not all(math.isfinite(x) for x in lo+hi):
            raise ValueError('Invalid endpoint path.')
        if not all(l<=x<=h for l,x,h in zip(lo,b,hi)) or lo==b or hi==b:
            raise ValueError('Require distinct lower/base/higher paths in input order.')
    return p


def evaluate(key=None, path=None, *, authorization=None):
    a = fresh_base()
    if key is not None:
        approved = load_approved_plan()
        if authorization != approved or not any(d['key']==key and path in
                (d['lower'],d['base'],d['higher']) for d in approved['drivers']):
            raise ValueError('Changed run is outside the locked plan.')
        a[key] = copy.deepcopy(path)
    before = copy.deepcopy(a)
    rows = m.project(a)
    if before != a or json.dumps(m.VALUES,sort_keys=True) != BASE_JSON:
        raise ValueError('Input mutation detected.')
    result = dict(inputs=before, rows=rows, checks=[m.checks(r,a) for r in rows],
                  accounting_valid=False, valuation_valid=False, error=None,
                  outputs=dict(operating_income=rows[-1]['operating_income'],
                               fcfe=rows[-1]['fcfe'],per_share=None))
    try:
        m.assert_balanced(rows,a)
        result['accounting_valid'] = True
        result['valuation'] = m.value_equity(rows,a)
        result['valuation_valid'] = True
        result['outputs']['per_share'] = result['valuation']['per_share']
    except ValueError as e:
        result['error'] = str(e)
    return result


def changed_analysis():
    plan = load_approved_plan()  # Gate BEFORE any changed execution.
    verify_preservation()
    started = datetime.now(timezone.utc).isoformat()
    initial = evaluate()
    cases = []
    for driver in plan['drivers']:
        for level in ('lower','base','higher'):
            case = evaluate(driver['key'],driver[level],authorization=plan)
            case.update(driver=driver['key'], level=level, units=driver['units'],years=driver['years'])
            b = driver['base'] if isinstance(driver['base'],list) else [driver['base']]
            p = driver[level] if isinstance(driver[level],list) else [driver[level]]
            case['input_delta'] = [x-y for x,y in zip(p,b)]
            case['input_delta_unit'] = driver['units']
            if driver['units']=='decimal ratio':
                case['percentage_point_delta'] = [100*(x-y) for x,y in zip(p,b)]
                case['relative_percent_delta'] = [100*(x/y-1) if y else None for x,y in zip(p,b)]
            case['delta'] = {k:(case['outputs'][k]-initial['outputs'][k]
                               if case['outputs'][k] is not None else None)
                             for k in OUTPUTS}
            cases.append(case)
    spans = {}
    for driver in plan['drivers']:
        group = [c for c in cases if c['driver']==driver['key']]
        spans[driver['key']] = {}
        for k in OUTPUTS:
            valid = [c['outputs'][k] for c in group if c['accounting_valid'] and c['outputs'][k] is not None]
            spans[driver['key']][k] = dict(span=max(valid)-min(valid) if valid else None,
                                         valid_count=len(valid),ranking_eligible=len(valid)==3)
    restored = evaluate()
    if initial != restored:
        raise ValueError('Restored base differs from initial base.')
    verify_preservation()
    return dict(started_at_utc=started,executed_at_utc=datetime.now(timezone.utc).isoformat(),plan=plan,
                initial=initial,cases=cases,spans=spans,restored=restored,
                restored_exact_match=True,tolerance=TOLERANCE)


def render_output(data):
    import contextlib
    import io
    out=io.StringIO()
    with contextlib.redirect_stdout(out):
        print('AMAZON (AMZN) LAB 11 | FCFE | all statement amounts USD million')
        print('Prediction locked UTC:',data['plan']['recorded_at_utc'])
        print('Execution started UTC:',data['started_at_utc'])
        print('Invalid-case amounts/deltas are diagnostic only and excluded from spans/ranking.')
        for label,case in [('INITIAL BASE',data['initial'])]+[(c['driver']+' / '+c['level'],c) for c in data['cases']]+[('RESTORED BASE',data['restored'])]:
            print('\nCASE:',label)
            if 'driver' in case:
                print('ACTUAL INPUT:',case['inputs'][case['driver']],case['units'],'YEARS:',case['years'])
                print('INPUT DELTA:',case['input_delta'],case['input_delta_unit'])
                if 'percentage_point_delta' in case:
                    print('PERCENTAGE-POINT DELTA:',case['percentage_point_delta'])
                    print('RELATIVE PERCENT DELTA:',case['relative_percent_delta'])
                print('SIGNED OUTPUT DELTAS:',json.dumps(case['delta']))
            print('ACCOUNTING/LIQUIDITY:', 'PASS' if case['accounting_valid'] else 'INVALID')
            print('VALUATION:', 'VALID (course convention)' if case['valuation_valid'] else 'UNAVAILABLE')
            if case['error']: print('REFUSAL:',case['error'])
            print('OUTPUTS:',json.dumps(case['outputs']))
            m.show(case['rows'],case['inputs'])
        print('\nSPANS:',json.dumps(data['spans']))
        print('RESTORED BASE: exact input and output match; tolerance',TOLERANCE)
    return out.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-approved',action='store_true')
    args = parser.parse_args()
    verify_preservation()
    if args.run_approved:
        data = changed_analysis()
        (HERE/'sensitivity_results.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
        print(render_output(data),end='')
    else:
        base = evaluate()
        print('BASE ONLY - this command executes no changed assumptions.')
        m.show(base['rows'],base['inputs'])
        print('BASE OUTPUTS:',json.dumps(base['outputs']))
        print('Accounting/liquidity:',base['accounting_valid'],'Valuation:',base['valuation_valid'])
        print('Value after 2030:',format(base['valuation']['terminal_share'],'.2%'))
        if not base['accounting_valid'] or not base['valuation_valid']:
            raise ValueError(base['error'])
    return 0


if __name__=='__main__':
    try:
        raise SystemExit(main())
    except (ValueError,KeyError) as e:
        print('REFUSED:',e)
        raise SystemExit(1)
