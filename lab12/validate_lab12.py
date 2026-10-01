"""Validate the written review against preserved evidence; never alter prior files.

Run: python -B lab12/validate_lab12.py [--published] [--write-log]
Published mode requires live HTTP checks. Report hash binds the reviewed prose;
numeric-token provenance is a coverage guard, not a semantic truth detector.
Context-specific assertions and independent calculation checks supply substance.
"""
import argparse
import copy
import csv
import hashlib
import importlib.util
import json
import math
import re
import subprocess
import sys
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from urllib.parse import urljoin

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
GIT = [r'C:\Program Files\Git\cmd\git.exe', '-c', 'safe.directory='+ROOT.as_posix()]
BASE = 'https://github.com/acpienkos/Amazon-Report/blob/main/lab12/'
LINES = []
COUNT = 0


def check(label, ok):
    global COUNT
    if not ok:
        raise AssertionError(label)
    COUNT += 1
    LINES.append('PASS | '+label)


def near(label, actual, expected, tol=1e-6):
    check(label, math.isfinite(float(actual)) and abs(float(actual)-float(expected)) <= tol)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return (ROOT/path).read_text(encoding='utf-8')


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT/path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def visible(text):
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    return re.sub(r'`[^`]*`', '', text)


def numbers(text):
    return set(re.findall(r'\d[\d,]*(?:\.\d+)?', visible(text)))


def canonical(number):
    return str(Decimal(number.replace(',', '')).normalize())


def github_links(report):
    urls = set()
    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', report):
        url = urljoin(BASE, target)
        if url.startswith('https://github.com/'):
            urls.add(url)
    for name in ('lab12.md', 'validate_lab12.py', 'lab12_validation.txt', 'audit_manifest.json'):
        urls.add(BASE+name)
    return sorted(urls)


def validate(published=False):
    report = read('lab12/lab12.md')
    manifest = json.loads(read('lab12/audit_manifest.json'))
    check('reviewed report text unchanged since contextual evidence audit', digest(HERE/'lab12.md') == manifest['reviewed_report_sha256'])
    original = subprocess.check_output(GIT+['ls-tree','-r','--name-only',manifest['starting_commit']], cwd=ROOT, text=True).splitlines()
    check('starting inventory contains all 40 prior tracked files', set(original)==set(manifest['sha256']) and len(original)==40)
    old = json.loads(read('lab11/preservation_manifest.json'))['sha256']
    check('27-file pre-Lab11 inventory explicitly included', len(old)==27 and set(old)<=set(original))
    for name, expected in manifest['sha256'].items():
        check('prior bytes unchanged: '+name, digest(ROOT/name)==expected)
    check('all 27 earlier hashes match their original preservation manifest', all(manifest['sha256'][p]==h for p,h in old.items()))
    changed = subprocess.check_output(GIT+['diff','--name-only',manifest['starting_commit']], cwd=ROOT, text=True).splitlines()
    check('all tracked additions/changes confined to lab12', all(p.startswith('lab12/') for p in changed))

    stops = ['Target selection','Company and evidence','My pro-forma','Valuation','Sensitivity and drivers','Interpretation']
    for i, name in enumerate(stops,1):
        section = re.search(rf'## Stop {i} — {re.escape(name)}\n(.*?)(?=\n## |\Z)',report,re.S)
        check('presentation stop: '+name, section is not None and len(section[1].split())>=65 and '[' in section[1])
    review = report.split('## Reciprocal written review')[1]
    for name in ('Selection and evidence','Model and valuation','Sensitivity and interpretation'):
        section = review.split('### '+name)[1].split('\n### ')[0]
        check('specific Partner question and sourced answer: '+name, '**Partner:**' in section and '?' in section and '**My evidence-based answer:**' in section)
    phrases = {
        'actual calculation check and bounded conclusion':['Evidence check performed for this review','Result: supported','reruns the unchanged model in memory'],
        'explanation back':['Partner — conclusion','Partner — main driver','Partner — largest limitation','My response'],
        'strength and actionable improvement':['Partner — evidence-backed strength','Partner — actionable improvement','funding and reinvestment reconciliation'],
        'reciprocal questioning and review':['My question back to Partner','My reviewer response to Partner','no independent Partner-company model'],
        'keep revise investigate and conclusion effect':['**Keep:**','**Revise:**','**Investigate:**','Effect on conclusion and priority','neither changes'],
        'reconsideration and unresolved evidence':['Question that caused reconsideration','specific unresolved gap','not a new valuation model claimed as completed'],
        'valuation basis':['December 31, 2025','USD','10,786.313572 million common shares','July 22, 2026','not a diluted weighted-average'],
        'ranges and qualified ranking':['±1 percentage point','±10% relative','Over these tested ranges','failed capex endpoint prevents a full-range ranking'],
        'impact versus uncertainty':['**Impact**','**uncertainty**','endpoints carry no probabilities'],
        'invalid case has no valuation':['higher capex has no valuation','diagnostics','excluded from valid ranges and rankings'],
        'no fabricated classroom or human exchange':['not a transcript of new spoken answers','No second-company presentation, human classmate exchange, attendance','does not contain a separate original selection diary'],
        'honest disclosure':['Codex served as my permitted learning partner','organizing, checking, validating, and documenting','I remain responsible for reviewing the work, understanding the analysis, the final conclusion, and any errors.'],
        'critical conventions':['positive-only','negative flows','no solution in bracket','Held fixed','Averaging the methods would conceal'],
    }
    for label, terms in phrases.items():
        check(label, all(t in report for t in terms))
    check('Partner is the sole partner speaker label', not re.search(r'\*\*(?:AI|Codex|Classmate)\s*:',report))
    check('contextual attribution audit recorded with honest scope', manifest['contextual_review']['status']=='reviewed' and 'not software proof' in manifest['contextual_review']['limitation'])

    # Every visible numeric token needs an existing-file locator or inventory/structure derivation.
    check('numeric coverage ledger covers every visible number', set(manifest['numeric_evidence'])==numbers(report))
    for token, evidence in manifest['numeric_evidence'].items():
        if 'file' in evidence:
            source_line = read(evidence['file']).splitlines()[evidence['line']-1]
            factor=Decimal(str(evidence.get('scale',1)))
            check('numeric provenance '+token+' in '+evidence['file'], source_line==evidence['source_line'] and Decimal(token.replace(',','')) in {Decimal(n.replace(',',''))*factor for n in numbers(source_line)})
        else:
            expected = {'starting_file_count':len(original),'lab11_file_count':sum(p.startswith('lab11/') for p in original),'prior_file_count':len(old)}
            check('structural/inventory number '+token, token in ('1','2','3','4','5','6','12','03','04') or Decimal(token)==expected[evidence['derivation']])

    m = module('lab12_existing_engine','lab10/amazon_proforma.py')
    ref = module('lab12_existing_reference','lab11/independent_reference.py')
    saved = json.loads(read('lab11/sensitivity_results.json'))
    a = copy.deepcopy(m.VALUES)
    check('base assumptions equal saved independent inputs',a==saved['initial']['inputs'])
    base_rows = m.project(a)
    check('entire base statements reproduce saved evidence',base_rows==saved['initial']['rows'])
    base_val = m.value_equity(base_rows,a)
    check('entire base valuation reproduces saved evidence',base_val==saved['initial']['valuation'])
    vfmt = {'operating_income':'132,404.53','fcfe':'38,251.88'}
    for field, shown in vfmt.items():
        check('base report '+field, f'{base_rows[-1][field]:,.2f}'==shown and shown in report)
    for key, shown in {'per_share':'32.67','pv_explicit':'27,820.16','terminal_value':'522,775.72','pv_terminal':'324,602.59','equity_value':'352,422.75','excluded_negative_pv':'75,656.81'}.items():
        check('base valuation report '+key,f'{base_val[key]:,.2f}'==shown and shown in report)
    check('terminal percentage exact to displayed precision',f'{base_val["terminal_share"]:.2%}'=='92.11%' and '92.11%' in report)
    check('saved market price and share basis',a['market_price']==249.38 and a['shares']==10786.313572 and a['cost_of_equity']==.10 and a['terminal_growth']==.025)
    check('signed FCFE display',all(f'{r["fcfe"]:,.2f}'.replace('-', '−') in report for r in base_rows))

    cases = {(c['driver'],c['level']):c for c in saved['cases']}
    for (driver,level), case in cases.items():
        values = copy.deepcopy(a); values[driver]=case['inputs'][driver]
        check('only approved input differs '+driver+'/'+level, values==case['inputs'])
        rows = m.project(values)
        check('complete case rerun '+driver+'/'+level, rows==case['rows'])
        independent,_ = ref.rebuild(values)
        for i, r in enumerate(independent):
            for key, value in r.items():
                near(f'independent {driver}/{level} FY{rows[i]["year"]} {key}',rows[i][key],value)
        if case['valuation_valid']:
            check('valid valuation rerun '+driver+'/'+level,m.value_equity(rows,values)==case['valuation'])
        else:
            try:
                m.value_equity(rows,values)
                refused = False
            except ValueError as e:
                refused = 'cash_headroom' in str(e)
            check('higher capex refuses valuation on funding failure',refused and case['outputs']['per_share'] is None and 'valuation' not in case)
    for d in saved['plan']['drivers']:
        for level, sign in [('lower',-1),('higher',1)]:
            expected=[x+sign*.01 for x in d['base']] if d['key']=='gross_margin' else [x*(1+sign*.1) for x in d['base']]
            check('correct approved range '+d['key']+'/'+level,all(abs(x-y)<1e-8 for x,y in zip(expected,d[level])))
        for case in [c for c in saved['cases'] if c['driver']==d['key']]:
            check('separate FY2026 capex unchanged '+d['key']+'/'+case['level'],case['inputs']['capex_2026_guidance']==220000)
    for driver in saved['spans']:
        for key, entry in saved['spans'][driver].items():
            usable=[c['outputs'][key] for c in saved['cases'] if c['driver']==driver and c['valuation_valid']]
            near('valid-subset span '+driver+'/'+key, entry['span'],max(usable)-min(usable))
            check('span displayed '+driver+'/'+key, f'{entry["span"]:,.2f}' in report)
            check('full-range eligibility '+driver+'/'+key,entry['ranking_eligible']==(driver=='gross_margin'))
    table = [line for line in report.splitlines() if re.match(r'\| (Base|Lower gross margin|Higher gross margin|Lower capex|Higher capex) \|',line)]
    ordered=[saved['initial'],cases['gross_margin','lower'],cases['gross_margin','higher'],cases['capex_later','lower'],cases['capex_later','higher']]
    check('exact sensitivity table row count',len(table)==len(ordered))
    for line,case in zip(table,ordered):
        cells=[s.strip() for s in line.split('|')[1:-1]]
        for i,key in enumerate(('operating_income','fcfe','per_share'),1):
            value=case['outputs'][key]
            check('contextual table '+cells[0]+'/'+key,cells[i]==('Unavailable' if value is None else f'{value:,.2f}'))
    invalid=cases['capex_later','higher']
    near('invalid FY2028 cash',invalid['rows'][2]['cash'],1309.67,.005)
    near('invalid cash headroom',invalid['checks'][2]['cash_headroom'],-23690.33,.005)
    check('invalid funding exhausted',invalid['rows'][2]['securities']==0 and invalid['rows'][2]['revolver']==15000)

    # Independent input -> statement -> CFO -> FCFE -> value check, no new financial assumptions.
    b=base_rows[-1]; lower=cases['capex_later','lower']; r=lower['rows'][-1]
    near('trace capex saving',b['capex']-r['capex'],20000)
    delta=lambda key:r[key]-b[key]
    near('trace opening PP&E to depreciation',delta('depreciation'),(r['opening']['ppe']-b['opening']['ppe'])*a['depreciation_rate'])
    near('trace depreciation to operating income',delta('operating_income'),-delta('depreciation'))
    near('trace CFO',delta('operating_cash_flow'),delta('net_income')+delta('depreciation')-delta('change_operating_wc'))
    near('trace working capital unchanged',delta('change_operating_wc'),0)
    near('trace CFO plus capex saving to FCFE',delta('fcfe'),delta('operating_cash_flow')+20000)
    for key,expected in {'operating_income':8913.71,'depreciation':-8913.71,'net_income':8477.53,'operating_cash_flow':-436.19,'fcfe':19563.81}.items():
        near('trace displayed delta '+key,delta(key),expected,.005)
    check('trace growth held fixed',all(x['revenue']==y['revenue'] for x,y in zip(lower['rows'],base_rows)))
    for label, rows, val in [('base',base_rows,base_val),('lower capex',lower['rows'],lower['valuation'])]:
        k,g=a['cost_of_equity'],a['terminal_growth']
        explicit=sum(max(x['fcfe'],0)/(1+k)**t for t,x in enumerate(rows,1))
        terminal=(rows[-1]['fcfe_before_revolver']-rows[-1]['debt_net_change'])*(1+g)/(k-g)/(1+k)**len(rows)
        near('independent PV to share value '+label,(explicit+terminal)/a['shares'],val['per_share'])
    near('trace price delta',lower['valuation']['per_share']-base_val['per_share'],17.82,.005)
    LINES.append('TRACE | Supported: capex saving 20,000.00; CFO delta -436.19; FCFE delta +19,563.81 USD million; value delta +17.82 USD/share. Full precision used.')

    dcf=module('lab12_prior_dcf','lab06/dcf.py'); p=dcf.amazon_inputs()
    results=dict(dcf.calculate_dcf(p))
    check('prior DCF base and bridge',f'{results["Value per diluted share"]:.4f}'=='5.9930' and abs(results['Equity value']-(results['Enterprise value']+p['cash']-p['debt']))<1e-6)
    check('required reverse bracket has no solution',dcf.reverse_dcf(p,252.13,-.05,.1) is None)
    shift=dcf.reverse_dcf(p,252.13,-.05,1.5)
    check('supplementary reverse shift',f'{shift*100:.6f}'=='96.978684')
    near('reverse target reprices',dcf.share_value(dict(p,growth_rates=[x+shift for x in p['growth_rates']])),252.13,1e-7)
    check('reverse held-fixed input labels',all(t in report for t in ('starting FCFF','WACC','terminal growth','cash, debt, shares','WACC weights were not recalculated')))
    peers=[105.73/2.73,492.44/17.95]; implied=sorted(x*7.17 for x in peers); midpoint=sum(implied)/2
    check('peer min median max from saved inputs',[f'{x:.2f}' for x in [implied[0],midpoint,implied[1]]]==['196.70','237.19','277.69'])
    check('peer removal sensitivity',f'{(midpoint-implied[0])/midpoint*100:.2f}'=='17.07')
    history=list(csv.DictReader(read('lab10/amazon_history.csv').splitlines()))
    h={(int(r['year']),r['metric']):float(r['value']) for r in history if r['value'] not in ('NOT DISCLOSED','')}
    for year in (2023,2024,2025):
        margin=(h[year,'revenue']-h[year,'cost_of_sales'])/h[year,'revenue']*100
        check('historical margin calculation '+str(year),f'{margin:.2f}%' in report)
        near('historical net capex definition '+str(year),h[year,'net_cash_capex'],h[year,'gross_cash_capex']-h[year,'capex_proceeds_incentives'])
    for label,key in [('Revenue','revenue'),('Gross cash PP&E purchases','gross_cash_capex'),('PP&E proceeds/incentives','capex_proceeds_incentives'),('Net cash capex','net_cash_capex')]:
        line=next(s for s in report.splitlines() if s.startswith('| '+label+' |'))
        cells=[s.strip() for s in line.split('|')[2:-1]]
        check('historical table by year '+key,cells==[f'{h[y,key]:,.0f}' for y in (2023,2024,2025)])
    for label,key in [('Sales growth, judgment','growth'),('Gross margin, judgment','gross_margin'),('SG&A / gross profit, judgment','sga_to_gp')]:
        line=next(s for s in report.splitlines() if s.startswith('| '+label+' |'))
        cells=[s.strip() for s in line.split('|')[2:-1]]
        check('forecast table assumption path '+key,all(abs(float(s.rstrip('%'))/100-x)<1e-10 for s,x in zip(cells,a[key])) and len(cells)==5)

    urls=github_links(report)
    for url in urls:
        if '/Amazon-Report/blob/main/' in url:
            path=url.split('/Amazon-Report/blob/main/')[1]
            check('GitHub target exists locally '+path,(ROOT/path).is_file() or path=='lab12/lab12_validation.txt')
    if published:
        published_results=[]
        for url in urls:
            quoted=url.replace("'", "''")
            command="$ErrorActionPreference='Stop'; $r=Invoke-WebRequest -UseBasicParsing -TimeoutSec 45 -Uri '"+quoted+"'; @{status=[int]$r.StatusCode; length=$r.RawContentLength; final_url=$r.BaseResponse.ResponseUri.AbsoluteUri} | ConvertTo-Json -Compress"
            result=subprocess.run(['powershell.exe','-NoProfile','-Command',command],capture_output=True,text=True,check=True)
            response=json.loads(result.stdout)
            status=response['status']; final=response['final_url']
            check('published HTTP '+str(status)+' '+url,status==200 and response['length']>100 and final.startswith('https://github.com/'))
            published_results.append({'url':url,'status':status,'final_url':final,'checked_at_utc':datetime.now(timezone.utc).isoformat()})
        head=subprocess.check_output(GIT+['rev-parse','HEAD'],cwd=ROOT,text=True).strip()
        (HERE/'publication_checks.json').write_text(json.dumps({'checked_after_publication':True,'published_commit_checked':head,'links':published_results},indent=2)+'\n',encoding='utf-8')
    else:
        LINES.append('PUBLICATION | Live GitHub checks not run in local mode; use --published after push.')
    for path, expected in manifest['sha256'].items():
        check('post-execution preservation '+path,digest(ROOT/path)==expected)
    LINES.append('SCOPE | Automated coverage and arithmetic, plus bound contextual review; not proof of external-source truth, forecast accuracy, human conduct, or grading.')
    LINES.append(f'ALL {COUNT} CHECKS PASSED'+(' | publication verified' if published else ' | local validation'))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--published',action='store_true')
    parser.add_argument('--write-log',action='store_true')
    args=parser.parse_args()
    LINES.append('FIN439 LAB12 VALIDATION | '+datetime.now(timezone.utc).isoformat())
    try:
        validate(args.published)
    except Exception as exc:
        LINES.append('FAIL | '+type(exc).__name__+': '+str(exc))
        print('\n'.join(LINES[-8:]))
        raise SystemExit(1)
    if args.write_log:
        (HERE/'lab12_validation.txt').write_text('\n'.join(LINES)+'\n',encoding='utf-8')
    print('\n'.join(LINES[-5:]))
