"""Independent Lab 11 computational checks; --submission-ready also checks personal status.
No changed financial case or Lab 10 validator is executed by --base-only.
"""
import argparse
import hashlib
import json
import math
import subprocess
import sys
import copy
from datetime import datetime
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0,str(Path(__file__).resolve().parent))
import amazon_sensitivity as s

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
COUNT=0


def check(label, condition):
    global COUNT
    COUNT += 1
    if not condition:
        raise AssertionError(label)


def near(label,actual,expected,tol=1e-6):
    check(label,math.isfinite(actual) and math.isfinite(expected) and abs(actual-expected)<=tol)


def base_tests():
    manifest=json.loads((HERE/'preservation_manifest.json').read_text(encoding='utf-8'))
    git=[r'C:\Program Files\Git\cmd\git.exe','-c','safe.directory='+ROOT.as_posix()]
    tracked=subprocess.check_output(git+['ls-tree','-r','--name-only',manifest['starting_commit']],cwd=ROOT,text=True).splitlines()
    check('manifest covers every original tracked file',set(tracked)==set(manifest['sha256']))
    for p,h in manifest['sha256'].items():
        check('preserved '+p,hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h)
    print(f'PASS: all {len(tracked)} original tracked files preserved from {manifest["starting_commit"]}.')
    snapshot=json.loads((HERE/'base_snapshot.json').read_text(encoding='utf-8'))
    a=s.fresh_base()
    check('base assumptions match captured original',a==snapshot['assumptions'])
    x=s.fresh_base();y=s.fresh_base()
    check('fresh independent dictionaries',x is not y)
    for k in a:
        if isinstance(a[k],list): check('fresh nested list '+k,x[k] is not y[k])
    # Identity checks only: no altered assumptions are projected before the lock.
    initial=s.evaluate();restored=s.evaluate()
    check('captured rows reproduced',initial['rows']==snapshot['rows'])
    check('captured valuation reproduced',initial['valuation']==snapshot['valuation'])
    check('exact restored base',initial==restored)
    check('global input unchanged',s.m.VALUES==a)
    rows=initial['rows'];v=initial['valuation']
    assets=('cash','securities','inventory','receivables','ppe','operating_rou','goodwill','other_assets')
    liabilities=('trade_payables','capex_payables','operating_accruals','unearned','operating_lease',
                 'finance_lease','financing_obligation','debt','revolver','other_liabilities')
    for i,r in enumerate(rows):
        p=r['opening'];year=r['year']
        near(f'{year} independent balance',sum(r[k] for k in assets),sum(r[k] for k in liabilities)+r['equity'])
        near(f'{year} cash',r['cash'],p['cash']+r['operating_cash_flow']+r['investing_cash_flow']+r['financing_cash_flow'])
        near(f'{year} income',r['operating_income'],r['revenue']-r['cost_of_sales']-r['sga']-r['other_operating_cost']-r['depreciation']-r['operating_lease_expense'])
        near(f'{year} gross margin link',r['gross_profit'],r['revenue']*a['gross_margin'][i])
        near(f'{year} capex link',r['capex'],a['capex_2026_guidance'] if i==0 else a['capex_later'][i-1])
        near(f'{year} capital AP',r['capex_payables'],r['capex']*a['capex_payable_ratio'])
        near(f'{year} depreciation',r['depreciation'],p['ppe']*a['depreciation_rate'])
        near(f'{year} PPE',r['ppe'],p['ppe']+r['capex']+r['capex_payables']-p['capex_payables']+r['finance_lease_addition']+r['financing_addition']-r['depreciation'])
        near(f'{year} equity',r['equity'],p['equity']+r['net_income']-r['distributions'])
        # Reconstruct signed FCFE without calling production checks().
        nwc=lambda q:q['inventory']+q['receivables']-q['trade_payables']-q['operating_accruals']-q['unearned']
        cf=(r['net_income']+r['depreciation']-(nwc(r)-nwc(p))-r['capex']-r['change_other_net_assets']
            +r['debt_net_change']-r['finance_lease_principal']-r['financing_principal']
            +r['revolver_draw']-r['revolver_repayment'])
        near(f'{year} signed FCFE',r['fcfe'],cf)
        check(f'{year} cash floor',r['cash']>=a['minimum_cash']-1e-6)
        check(f'{year} finite revolver',0<=r['revolver']<=a['revolver_limit'])
        for name,gap in initial['checks'][i].items():
            check(f'{year} check {name}',math.isfinite(gap) and (gap>=-1e-6 if name.endswith('headroom') else abs(gap)<=1e-6))
    check('negative FCFE years retained',[r['year'] for r in rows if r['fcfe']<0]==[2026,2027,2028])
    check('positive FCFE years retained',[r['year'] for r in rows if r['fcfe']>0]==[2029,2030])
    check('positive only retained',a['positive_only'] is True)
    near('fixed shares in millions',a['shares'],10786.313572)
    k=a['cost_of_equity'];g=a['terminal_growth']
    explicit=sum(max(0,r['fcfe'])/(1+k)**(i+1) for i,r in enumerate(rows))
    terminal=(rows[-1]['fcfe_before_revolver']-rows[-1]['debt_net_change'])*(1+g)/(k-g)/(1+k)**5
    near('independent valuation',v['per_share'],(explicit+terminal)/a['shares'])
    near('independent terminal share',v['terminal_share'],terminal/(explicit+terminal))
    check('rounded value',f'{v["per_share"]:.2f}'=='32.67')
    check('rounded terminal share',f'{v["terminal_share"]:.2%}'=='92.11%')
    command=[sys.executable,'-B',str(ROOT/'lab10/amazon_proforma.py')]
    run=subprocess.run(command,capture_output=True,text=True,check=True,cwd=ROOT)
    check('exact Lab10 saved stdout',run.stdout==(ROOT/'lab10/lab10_output.txt').read_text(encoding='utf-8'))
    check('exact Lab11 base stdout',run.stdout==(HERE/'base_output.txt').read_text(encoding='utf-8'))
    new=subprocess.run([sys.executable,'-B',str(HERE/'amazon_sensitivity.py')],capture_output=True,text=True,check=True,cwd=ROOT)
    check('base command succeeds','Accounting/liquidity: True Valuation: True' in new.stdout)
    config=json.loads((HERE/'approved_ranges.json').read_text(encoding='utf-8'))
    if config['status']!='LOCKED':
        try:s.load_approved_plan()
        except ValueError as e:check('guard refuses before execution','STOP:' in str(e))
        else:check('missing prediction must refuse',False)
        check('no changed result artifact',(HERE/'sensitivity_results.json').exists() is False)
    print('PASS: independent base accounting, liquidity, FCFE and valuation arithmetic; exact saved-output reproduction.')
    print('PASS: fresh-copy identities and initial/restored base equality; base tests execute only base cases.')
    print(f'PASS: {COUNT} base-preparation checks. This is NOT full sensitivity or submission validation.')


def refused(label,fn,expected):
    try: fn()
    except ValueError as e:
        check(label,expected in str(e))
        print('EXPECTED REFUSAL:',label,':',str(e))
    else: check(label+' must refuse',False)


def full_tests():
    from independent_reference import rebuild, ASSETS, LIABILITIES
    plan=s.load_approved_plan()
    data=json.loads((HERE/'sensitivity_results.json').read_text(encoding='utf-8'))
    check('locked plan exact',data['plan']==plan)
    check('timestamp ordering',datetime.fromisoformat(plan['recorded_at_utc'])<datetime.fromisoformat(data['started_at_utc'])<=datetime.fromisoformat(data['executed_at_utc']))
    check('verbatim response in locked file',plan['exact_user_response'] in (HERE/'locked_prediction.md').read_text(encoding='utf-8'))
    base=data['initial'];cases=data['cases'];allcases=[base]+cases+[data['restored']]
    check('six cases exact',[(c['driver'],c['level']) for c in cases]==[(d['key'],l) for d in plan['drivers'] for l in ('lower','base','higher')])
    for case in allcases:
        a=case['inputs'];rows=case['rows'];reference,decimal_a=rebuild(a)
        for i,(r,z) in enumerate(zip(rows,reference)):
            check('all reference fields covered',set(r)-{'year','opening'}==set(z))
            for field,number in z.items():near(f'{i} independent {field}',r[field],float(number))
            near('independent accounting balance',sum(float(z[k]) for k in ASSETS),sum(float(z[k]) for k in LIABILITIES)+float(z['equity']))
            near('FCFE output sign preserved',r['fcfe'],float(z['fcfe']))
        invalid=any(float(z['cash'])<a['minimum_cash']-1e-6 or float(z['revolver'])>a['revolver_limit']+1e-6 or any(float(z[k]) < -1e-6 for k in ASSETS+LIABILITIES) for z in reference)
        check('independent liquidity classification',case['accounting_valid']==(not invalid))
        if invalid:
            check('invalid explicitly flagged',bool(case['error']) and not case['valuation_valid'])
            check('invalid value unavailable',case['outputs']['per_share'] is None and 'valuation' not in case)
        else:
            s.m.assert_balanced(rows,a)
            for checks in case['checks']:
                for key,gap in checks.items():check('all usable checks pass',gap>=-1e-6 if key.endswith('headroom') else abs(gap)<=1e-6)
            k=decimal_a['cost_of_equity'];g=decimal_a['terminal_growth']
            from decimal import Decimal as D
            pv=sum(max(D(0),z['fcfe'])/(1+k)**t for t,z in enumerate(reference,1))
            terminal=(reference[-1]['fcfe_before_revolver']-reference[-1]['debt_net_change'])*(1+g)/(k-g)/(1+k)**5
            near('independent per-share valuation',case['outputs']['per_share'],float((pv+terminal)/decimal_a['shares']))
        near('final income output',case['outputs']['operating_income'],rows[-1]['operating_income'])
        near('final FCFE output',case['outputs']['fcfe'],rows[-1]['fcfe'])
        if 'driver' not in case:continue
        d=next(d for d in plan['drivers'] if d['key']==case['driver'])
        changed={k for k in a if a[k]!=base['inputs'][k]}
        check('only chosen input changed',changed==({d['key']} if case['level']!='base' else set()))
        for k in a:
            if k!=d['key']:check('other assumption at base '+k,a[k]==base['inputs'][k])
        check('actual approved path',a[d['key']]==d[case['level']])
        check('actual affected years',case['years']==d['years'])
        for j,(old,new) in enumerate(zip(d['base'],d[case['level']])):
            near('input difference',case['input_delta'][j],new-old)
            if d['key']=='gross_margin':
                near('percentage points',case['percentage_point_delta'][j],(new-old)*100)
                near('relative percentage',case['relative_percent_delta'][j],(new/old-1)*100)
                if case['level']!='base':check('pp distinct from relative percent',abs(case['percentage_point_delta'][j]-case['relative_percent_delta'][j])>.1)
            else:
                check('USD million maintained',case['units']=='USD million')
                near('10 percent capex endpoint',new/old,{'lower':.9,'base':1,'higher':1.1}[case['level']])
        for k in s.OUTPUTS:
            if case['outputs'][k] is None:check('unavailable delta',case['delta'][k] is None)
            else:near('signed delta '+k,case['delta'][k],case['outputs'][k]-base['outputs'][k])
        if case['level']!='base':
            fields=('gross_profit','sga','inventory','trade_payables','net_income','equity','cash') if d['key']=='gross_margin' else ('capex','capex_payables','ppe','depreciation','net_income','equity','cash')
            for f in fields:check('linked line recalculated '+f,abs(rows[-1][f]-base['rows'][-1][f])>1e-6)
        if d['key']=='capex_later':check('2026 entirely unchanged',rows[0]==base['rows'][0])
    for d in plan['drivers']:
        group=[c for c in cases if c['driver']==d['key']]
        for k in s.OUTPUTS:
            valid=[c['outputs'][k] for c in group if c['accounting_valid'] and c['outputs'][k] is not None]
            span=data['spans'][d['key']][k]
            near('valid max-minus-min span',span['span'],max(valid)-min(valid))
            check('valid count',span['valid_count']==len(valid))
            check('incomplete set not ranked',span['ranking_eligible']==(len(valid)==3))
    # Instrument actual runner: hold references to every input to prove no sharing.
    seen=[];original=s.m.project
    def observe(a):
        seen.append(a)
        return original(a)
    s.m.project=observe
    try:rerun=s.changed_analysis()
    finally:s.m.project=original
    check('eight complete reruns',len(seen)==8)
    for i,a in enumerate(seen):
        for b in seen[i+1:]:
            check('separate run dictionaries',a is not b)
            for k in a:
                if isinstance(a[k],list):check('separate run nested lists '+k,a[k] is not b[k])
    for k in ('initial','cases','spans','restored'):check('saved numerical results reproducible '+k,rerun[k]==data[k])
    check('exact final restored base',data['initial']==data['restored'])
    # Mutation/refusal tests are diagnostics, not extra sensitivity endpoints.
    bad=copy.deepcopy(base['rows']);bad[2]['cash']+=1
    refused('broken balance',lambda:s.m.value_equity(bad,base['inputs']),'balance_gap')
    badcase=next(c for c in cases if not c['accounting_valid'])
    refused('approved high capex funding refusal',lambda:s.m.value_equity(badcase['rows'],badcase['inputs']),'cash_headroom')
    # Preserve balances/FCFE checks but make the sustainable terminal proxy negative.
    terminal=copy.deepcopy(base['rows']);terminal[-1]['fcfe_before_revolver']=-1
    refused('nonpositive sustainable terminal gate',lambda:s.m.value_equity(terminal,base['inputs']),'terminal value refused')
    rate=copy.deepcopy(base['inputs']);rate['terminal_growth']=rate['cost_of_equity']
    refused('invalid discount spread',lambda:s.m.value_equity(base['rows'],rate),'equity return')
    check('immutable baseline survives',s.fresh_base()==base['inputs']==s.m.VALUES)
    check('executed text exact',s.render_output(data)==(HERE/'lab11_output.txt').read_text(encoding='utf-8'))
    report=(HERE/'lab11.md').read_text(encoding='utf-8')
    table_rows=[line.split('|')[1:-1] for line in report.splitlines()
                if line.startswith('| lower ') or line.startswith('| base ') or line.startswith('| higher ')]
    check('exactly six displayed result rows',len(table_rows)==6)
    for c,cells in zip(cases,table_rows):
        check('case order in report',cells[0].strip().startswith(c['level']))
        for cell,(kind,key) in zip(cells[1:7],[(kind,key) for key in s.OUTPUTS for kind in ('outputs','delta')]):
            expected=c[kind][key]
            if expected is None:check('table unavailable',cell.strip()=='Unavailable')
            else:near('report table numeric cell',float(cell.replace(',','')),expected,.005001)
        check('report case validity',('PASS:' in cells[-1])==c['accounting_valid'])
    for c in cases:
        for k in s.OUTPUTS:
            for val in (c['outputs'][k],c['delta'][k]):
                if val is not None:check('report includes output/delta',f'{val:,.2f}' in report)
    for driver in data['spans'].values():
        for span in driver.values():check('report span',f'{span["span"]:,.2f}' in report)
    for text in ('over these ranges','Actual partner evidence','AI-use disclosure','watch-defer','diagnostic','positive-only'):
        check('report disclosure '+text,text in report)
    s.verify_preservation()
    print('PASS: every forecast line independently rebuilt with 40-digit Decimal for all eight runs.')
    print('PASS: actual fresh-copy isolation, approved paths/units, linked recalculation, signed differences and valid spans.')
    print('PASS: expected funding/valuation refusals, restored base, saved output/report and 27 prior file hashes.')
    print(f'PASS: {COUNT} computational validation checks. Personal completion is not certified.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-only',action='store_true')
    parser.add_argument('--submission-ready',action='store_true')
    args=parser.parse_args()
    try:
        base_tests()
        if not args.base_only:full_tests()
        if args.submission_ready:
            report=(HERE/'lab11.md').read_text(encoding='utf-8')
            check('personal completion','PENDING PARTNER INPUT' not in report and 'PENDING STUDENT REVIEW' not in report)
            for evidence in ('Why did your higher-capex case produce no valuation','Specific check of the partner',
                             'Base: 1%, 2%, 1%','Lower: 0%, 1%, 0%','Higher: 2%, 3%, 2%',
                             'percentage-point changes rather than percentage changes','My final conclusion is watch-defer'):
                check('student-confirmed evidence '+evidence,evidence in report)
            print(f'PASS: submission-readiness evidence documented; {COUNT} total checks. Human activity is supported by student confirmation, not software observation.')
    except (AssertionError,ValueError,subprocess.CalledProcessError) as e:
        print('VALIDATION REFUSED/FAILED:',e)
        raise SystemExit(1)
