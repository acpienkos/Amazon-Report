"""Independent Lab10 arithmetic, Decimal reference, refusal, and preservation tests.
Educational coursework only. Codex assisted with these tests. Standard library only.
Run: python -B lab10/validate_lab10.py [--submission-ready]
Default tests computation; --submission-ready also refuses missing personal work.
"""
import argparse
import copy
import csv
from decimal import Decimal as D, getcontext
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import amazon_proforma as m
getcontext().prec = 40
COUNT = 0
STARTING_COMMIT = '347750c3bc4e8965b40312c5b18c1f49760a63d1'
# SHA256 snapshot of ALL 19 pre-existing tracked files, taken before Lab10 edits.
PRESERVED = {'Amazon_2026-09-03_report.md': 'e450f1e144703d7c5026f139de9b254ce1105ad1c953ee0077e3f56d32a57d8b', 'dcf.py': '1ee0fcb5b1b6205b8edbe561ea49a1e25c03f69d2cde9b3b56ac885a9dffe858', 'lab06/dcf.py': 'a4a7cccba3184c2f9e66851c192a4d34dcc06e381b901b7f6d259bb5326400ff', 'lab06/dcf_output_lab06.txt': '450007043c613ab892d6f55d15911d1c569336002e2ded09e307b1bd8e2d4067', 'lab06/lab06.md': '7d7fa927acc23b7ed15532a22c47355b648f8ec0e0a043d86b03be803811ce9f', 'lab06/lab06_validation.txt': 'ac0fef9355ee68323ee33a8d13c02411adaa1d9a11fa5adb50cb210439dfaeb0', 'lab07/comps.py': '0eec20d0d3a7bb57a0c817c4ad9c94fe44782574b6a40c5ca7c44c37dcc9d81b', 'lab07/lab07.md': 'bf10705108157ee663c2c0e91a07d7e8c6ad2fe9da6e3b12265bdab9a461f4ee', 'lab07/lab07_output.txt': '84ecfca6472739257ab821482920d9b13a40f742ec870a00792e9d22328b2091', 'lab07/lab07_validation.txt': '597961cc02fc1bb9ddec838e22070b0d6f5fafa4d499b3f7ccdc161cf497158a', 'lab08/comps_lab08.py': 'f62a96cfb383e1f7ff4726fcbaf3dfb44c89042256885aa38c3b650af0f3d1a9', 'lab08/lab08.md': '59401d981e4be08b54f78516bb768bdce1e37496205242190e02af17470ac548', 'lab08/lab08_output.txt': '04deb5952aa2aaf3bc38c0400f742d22aea004a0dcac1368c9be4feafbeb0362', 'lab08/lab08_validation.txt': 'c6bde178a6b8dd27b89edfa0750b697a98dda22be6e2ce09f79179c8d2fd1e48', 'lab09/lab09.md': '6d5abcefceb9520b494eba94acb31162e5facc9b5bcb07b4c16bbb8b1b1ab26d', 'lab09/lab09_output.txt': '186e3a11a059699f7508213034b263d0674142dbeb31cd3d912234075a742d10', 'lab09/lab09_validation.txt': '606fba741c210449f9a99c3f802d91f98d15b4b7bf67450c43bee277e6a1f009', 'lab09/proforma.py': 'c2fe8509fc880684941b09f4ac5ea5cb3897d5d720d4bd498028fedade03d4c9', 'lab09/validate_lab09.py': '140a4b674e8ac0f834500579115abf01c4e74731dffb382697e81cd6bf292cea'}


def check(name,condition):
    global COUNT
    COUNT += 1
    if not condition:
        raise AssertionError(name)


def near(name,actual,expected,tolerance=1e-6):
    check(name, abs(D(str(actual))-D(str(expected))) <= D(str(tolerance)))


def refused(name,fn,contains):
    try:
        fn()
    except ValueError as e:
        check(name,contains in str(e))
        print('EXPECTED REFUSAL:',e)
    else:
        check(name,False)


def history_tests():
    with (HERE/'amazon_history.csv').open(encoding='utf-8',newline='') as f: raw=list(csv.DictReader(f))
    h={}
    for r in raw:
        check('source and locator '+r['metric'],bool(r['source'] and r['locator']))
        check('history label '+r['metric'],r['label'] in ('history','fact'))
        h[int(r['year']),r['metric']]=r['value'] if r['value']=='NOT DISCLOSED' else D(r['value'])
    # Independently transcribed official filing fixture, never professor/ABG values.
    fixtures={2023:[574785,304739,44370,11816,30425,33318,204177,201875,30225,52729,4596,37557,7120,513983,12,13],2024:[637959,326288,43907,11359,59248,34214,252665,285970,32067,82999,5341,68614,9265,574785,11,19],2025:[716924,356414,47129,11172,77670,38325,357025,411065,41860,131819,3499,97311,19087,637959,12,20]}
    names=['revenue','cost_of_sales','sales_marketing','general_administrative','net_income','inventory','ppe','equity','ppe_depreciation','gross_cash_capex','capex_proceeds_incentives','pretax_income','income_tax','prior_revenue','constant_currency_growth','aws_reported_growth']
    for y,nums in fixtures.items():
        for k,n in zip(names,nums): near(f'{y} SEC {k}',h[y,k],n)
        z=lambda k:h[y,k]
        gp=z('revenue')-z('cost_of_sales'); sg=z('sales_marketing')+z('general_administrative')
        expected=dict(gross_profit=gp,sga=sg,gross_margin=gp/z('revenue'),sga_gross_profit=sg/gp,
                      inventory_days=z('inventory')/z('cost_of_sales')*365,
                      depreciation_ppe=z('ppe_depreciation')/z('ppe'),
                      effective_tax_rate=z('income_tax')/z('pretax_income'),
                      reported_growth=z('revenue')/z('prior_revenue')-1,
                      net_cash_capex=z('gross_cash_capex')-z('capex_proceeds_incentives'),
                      provider_capex=z('gross_cash_capex')-z('capex_proceeds_incentives'))
        for k,n in expected.items(): near(f'{y} arithmetic {k}',z(k),n)
        check('organic not invented',z('organic_growth')=='NOT DISCLOSED')
    print('PASS: all 81 history rows, 48 source fixtures, all derived ratios and provider reconciliation.')


def decimal_reference():
    """Separate 40-digit calculation from CSV; no production formulas/checks called.
    Reconstruct every forecast financial line and compare to float implementation.
    """
    with (HERE/'amazon_assumptions.csv').open(encoding='utf-8',newline='') as f: register=list(csv.DictReader(f))
    a={r['Assumption']:json.loads(r['Value'],parse_float=D,parse_int=D) for r in register}
    for r in register:
        check('label '+r['Assumption'],r['Label'] in ('history','guidance','judgment','fact'))
        check('reason/source '+r['Assumption'],len(r['Reason'])>15 and bool(r['Exact source or calculation']))
    near('share conversion',a['shares'],D(10786313572)/1000000)
    near('opening current reclassification',a['opening_operating_accruals'],75520-14199-2748-455-358)
    near('opening term and short debt',a['opening_debt'],65648+2748+455)
    near('opening financing',a['opening_financing_obligation'],358+7800)
    near('opening other liabilities',a['opening_other_liabilities'],35985-7800)
    near('opening trade AP',a['opening_trade_payables'],121909-27000)
    near('opening assets',sum(a['opening_'+k] for k in m.ASSETS),818042)
    near('opening liabilities',sum(a['opening_'+k] for k in m.LIABILITIES),818042-411065)
    source_opening={'revenue':716924,'cash':86810,'securities':36219,'inventory':38325,'receivables':67729,'ppe':357025,'operating_rou':86054,'goodwill':23273,'other_assets':122607,'trade_payables':94909,'capex_payables':27000,'operating_accruals':57760,'unearned':20576,'operating_lease':89252,'finance_lease':12286,'financing_obligation':8158,'debt':68851,'other_liabilities':28185,'equity':411065,'revolver':0}
    for key,amount in source_opening.items():near('SEC opening fixture '+key,a['opening_'+key],amount)
    # All calculated history-linked forecast inputs must remain tied to sources.
    formulas={'other_cost_ratio':D(109074+108521+4639-41860-14006)/716924,
      'inventory_days':D(38325)/356414*365,
      'receivables_ratio':D(67729)/716924,'trade_payable_ratio':D(94909)/356414,
      'accrual_ratio':D(57760)/716924,'unearned_ratio':D(20576)/716924,
      'capex_payable_ratio':D(27000)/128320,'finance_lease_principal_rate':D(1544)/12286,
      'rou_amortization_rate':(D(14006)-D(89252)*D('.037'))/86054}
    for k,n in formulas.items(): near('assumption formula '+k,a[k],n,1e-12)
    p={k:a['opening_'+k] for k in m.OPENING_KEYS}; results=[]
    for i,y in enumerate(range(2026,2031)):
        z={}
        z['revenue']=p['revenue']*(1+a['growth'][i]); z['gross_profit']=z['revenue']*a['gross_margin'][i]
        z['cost_of_sales']=z['revenue']-z['gross_profit']; z['sga']=z['gross_profit']*a['sga_to_gp'][i]
        z['other_operating_cost']=z['revenue']*a['other_cost_ratio']; z['depreciation']=p['ppe']*a['depreciation_rate']
        z['rou_amortization']=p['operating_rou']*a['rou_amortization_rate']
        z['operating_lease_accretion']=p['operating_lease']*a['operating_lease_rate']
        z['operating_lease_expense']=z['rou_amortization']+z['operating_lease_accretion']
        z['operating_lease_cash']=z['operating_lease_expense']
        z['operating_income']=z['revenue']-sum(z[k] for k in ('cost_of_sales','sga','other_operating_cost','depreciation','operating_lease_expense'))
        z['debt_net_change']=a['debt_net_change'][i]; z['debt']=p['debt']+z['debt_net_change']
        z['debt_interest']=(p['debt']+z['debt'])/2*a['debt_rate']
        z['finance_lease_interest']=p['finance_lease']*a['finance_lease_rate']
        z['financing_interest']=p['financing_obligation']*a['financing_rate']
        z['revolver_interest']=p['revolver']*a['revolver_rate']
        z['interest_expense']=z['debt_interest']+z['finance_lease_interest']+z['financing_interest']+z['revolver_interest']
        z['interest_income']=(p['cash']+p['securities'])*a['cash_yield']; z['other_income']=a['other_income']
        z['pretax_income']=z['operating_income']+z['interest_income']+z['other_income']-z['interest_expense']
        z['income_tax']=max(D(0),z['pretax_income'])*a['tax_rate'];z['net_income']=z['pretax_income']-z['income_tax']
        z['inventory']=z['cost_of_sales']/a['days_per_year']*a['inventory_days']; z['receivables']=z['revenue']*a['receivables_ratio']
        z['trade_payables']=z['cost_of_sales']*a['trade_payable_ratio']; z['operating_accruals']=z['revenue']*a['accrual_ratio']
        z['unearned']=z['revenue']*a['unearned_ratio']; z['capex']=a['capex_2026_guidance'] if i==0 else a['capex_later'][i-1]
        z['capex_payables']=z['capex']*a['capex_payable_ratio']; z['change_capex_payables']=z['capex_payables']-p['capex_payables']
        z['finance_lease_addition']=a['finance_lease_addition'];z['finance_lease_principal']=min(p['finance_lease'],p['finance_lease']*a['finance_lease_principal_rate'])
        z['finance_lease']=p['finance_lease']+z['finance_lease_addition']-z['finance_lease_principal']
        z['financing_addition']=a['new_financing_obligations'];z['financing_principal']=min(p['financing_obligation'],max(D(0),a['financing_payments'][i]-z['financing_interest']))
        z['financing_obligation']=p['financing_obligation']+z['financing_addition']-z['financing_principal']
        z['ppe_additions']=z['capex']+z['change_capex_payables']+z['finance_lease_addition']+z['financing_addition']
        z['ppe']=p['ppe']+z['ppe_additions']-z['depreciation']
        z['operating_lease_addition']=z['rou_amortization']+p['operating_rou']*a['rou_growth']
        z['operating_rou']=p['operating_rou']+z['operating_lease_addition']-z['rou_amortization']
        z['operating_lease']=p['operating_lease']+z['operating_lease_addition']+z['operating_lease_accretion']-z['operating_lease_cash']
        for k in ('goodwill','other_assets','other_liabilities'):z[k]=p[k]*(1+a['other_balance_growth'])
        z['distributions']=a['distributions'];z['equity']=p['equity']+z['net_income']-z['distributions']
        def nwc(q):return q['inventory']+q['receivables']-q['trade_payables']-q['operating_accruals']-q['unearned']
        z['change_operating_wc']=nwc(z)-nwc(p)
        z['change_other_net_assets']=(z['goodwill']+z['other_assets']-z['other_liabilities'])-(p['goodwill']+p['other_assets']-p['other_liabilities'])
        z['operating_cash_flow']=z['net_income']+z['depreciation']-z['change_operating_wc']
        z['fcfe_before_revolver']=z['operating_cash_flow']-z['capex']-z['change_other_net_assets']+z['debt_net_change']-z['finance_lease_principal']-z['financing_principal']
        basecash=p['cash']+z['fcfe_before_revolver']-z['distributions']
        z['securities_sale']=min(max(D(0),p['securities']-a['securities_liquidity_floor']),max(D(0),a['minimum_cash']-basecash))
        z['securities']=p['securities']-z['securities_sale'];z['cash_before_revolver']=basecash+z['securities_sale']
        z['revolver_draw']=min(max(D(0),a['minimum_cash']-z['cash_before_revolver']),max(D(0),a['revolver_limit']-p['revolver']))
        z['revolver_repayment']=min(p['revolver'],max(D(0),z['cash_before_revolver']-a['minimum_cash']))
        z['revolver']=p['revolver']+z['revolver_draw']-z['revolver_repayment']
        z['fcfe']=z['fcfe_before_revolver']+z['revolver_draw']-z['revolver_repayment']
        z['investing_cash_flow']=-z['capex']-z['change_other_net_assets']+z['securities_sale']
        z['financing_cash_flow']=z['debt_net_change']-z['finance_lease_principal']-z['financing_principal']+z['revolver_draw']-z['revolver_repayment']-z['distributions']
        z['net_cash_change']=z['operating_cash_flow']+z['investing_cash_flow']+z['financing_cash_flow']
        z['cash']=p['cash']+z['fcfe']+z['securities_sale']-z['distributions']
        # Independent balance and cash reconstruction, not production checks().
        near(f'{y} decimal balance',sum(z[k] for k in m.ASSETS),sum(z[k] for k in m.LIABILITIES)+z['equity'])
        near(f'{y} independent cash',z['cash'],p['cash']+z['net_cash_change'])
        check(f'{y} cash floor',z['cash']>=a['minimum_cash']-D('0.000001'))
        check(f'{y} revolver bound',0<=z['revolver']<=a['revolver_limit'])
        results.append(z);p=z
    return results,a


def run_tests(submission_ready=False):
    history_tests()
    reference,a=decimal_reference()
    rows=m.project();v=m.value_equity(rows)
    for i,r in enumerate(rows):
        check('all formulas covered',set(r)-{'year','opening'}==set(reference[i]))
        for k,n in reference[i].items():near(f"{r['year']} {k}",r[k],n)
    print('PASS: every forecast financial line independently rebuilt using 40-digit Decimal arithmetic.')
    # Independently recompute annual PVs and terminal; source of terminal is not
    # a temporary securities sale, a revolver draw, or a repeated term borrowing.
    k,g=a['cost_of_equity'],a['terminal_growth']
    cf=reference[-1]['fcfe_before_revolver']-reference[-1]['debt_net_change']
    expected_pv=sum(max(D(0),r['fcfe'])/(1+k)**t for t,r in enumerate(reference,1))
    expected_tv=cf*(1+g)/(k-g)/(1+k)**5
    near('explicit PV',v['pv_explicit'],expected_pv)
    near('terminal PV',v['pv_terminal'],expected_tv)
    near('equity value',v['equity_value'],expected_pv+expected_tv)
    near('per share',v['per_share'],(expected_pv+expected_tv)/a['shares'])
    near('terminal share',v['terminal_share'],expected_tv/(expected_pv+expected_tv))
    near('market shares',v['market_equity']/m.VALUES['market_price'],a['shares'])
    near('negative flow disclosure',v['excluded_negative_pv'],-sum(min(D(0),r['fcfe'])/(1+k)**t for t,r in enumerate(reference,1)))
    check('base negative years preserved',[r['year'] for r in rows if r['fcfe']<-m.TOLERANCE]==[2026,2027,2028])
    for field in ('cash','ppe','debt','finance_lease','financing_obligation','operating_rou','operating_lease','equity','revolver','capex_payables','securities'):
        bad=copy.deepcopy(rows);bad[2][field]+=1
        refused('mutated '+field,lambda:m.value_equity(bad),'FY2028')
    lowfund=copy.deepcopy(m.VALUES);lowfund['debt_net_change'][1]=0
    refused('funding dependence',lambda:m.value_equity(m.project(lowfund),lowfund),'cash_headroom')
    finitefund=copy.deepcopy(m.VALUES);finitefund['debt_net_change'][1]=15000
    funding_rows=m.project(finitefund);m.assert_balanced(funding_rows,finitefund)
    check('finite revolver draws',any(r['revolver_draw']>0 for r in funding_rows))
    check('finite revolver repays',any(r['revolver_repayment']>0 for r in funding_rows))
    for r in funding_rows:
        check('draw scenario floor',r['cash']>=finitefund['minimum_cash']-m.TOLERANCE)
        check('draw scenario cap',0<=r['revolver']<=finitefund['revolver_limit'])
    print('PASS: finite liquidity scenario ($15bn 2027 term issuance) draws and repays revolver while preserving the cash floor.')
    stressed=copy.deepcopy(m.VALUES);stressed['capex_later']=[n*1.1 for n in stressed['capex_later']]
    refused('higher capex funding limit',lambda:m.value_equity(m.project(stressed),stressed),'cash_headroom')
    # Very high last-year capex funded with explicit extra debt: statements pass,
    # but negative SUSTAINABLE FCFE must not create a terminal value.
    negative=copy.deepcopy(m.VALUES);negative['capex_later'][-1]+=300000;negative['debt_net_change'][-1]+=300000
    refused('negative terminal eligibility',lambda:m.value_equity(m.project(negative),negative),'terminal value refused')
    invalid=copy.deepcopy(m.VALUES);invalid['terminal_growth']=invalid['cost_of_equity']
    refused('discount spread',lambda:m.value_equity(rows,invalid),'equity return')
    invalid=copy.deepcopy(m.VALUES);invalid['shares']=0
    refused('share positivity',lambda:m.value_equity(rows,invalid),'share count')
    invalid=copy.deepcopy(m.VALUES);invalid['cash_settled_compensation']=False
    refused('dilution policy guard',lambda:m.project(invalid),'dilution model')
    # Required genuine directional tests. Higher discount rate lowers value.
    for rate in (.09,.11):
        b=copy.deepcopy(m.VALUES);b['cost_of_equity']=rate;sv=m.value_equity(rows,b)
        check('discount direction',sv['per_share']>v['per_share'] if rate<.10 else sv['per_share']<v['per_share'])
        print(f"SENSITIVITY cost of equity {rate:.0%}: ${sv['per_share']:.2f}/share")
    b=copy.deepcopy(m.VALUES);b['gross_margin']=[x+.005 for x in b['gross_margin']]
    high=m.value_equity(m.project(b),b)
    check('higher margin direction',high['per_share']>v['per_share'])
    print(f"SENSITIVITY +0.5 percentage point gross margin in all years: ${high['per_share']:.2f}/share")
    script=HERE/'amazon_proforma.py'; digest=hashlib.sha256(script.read_bytes()).hexdigest()
    normal=subprocess.run([sys.executable,'-B',str(script)],capture_output=True,text=True,check=True)
    broken=subprocess.run([sys.executable,'-B',str(script),'--break-cash'],capture_output=True,text=True)
    check('break process exit',broken.returncode==1)
    expected_gap=m.VALUES['opening_cash']-rows[0]['cash']
    check('break specific gap',f'FY2026 balance_gap = {expected_gap:.1f}' in broken.stdout)
    check('no valuation after break','Value per share:' not in broken.stdout)
    print('DELIBERATE BREAK COMMAND: python -B lab10/amazon_proforma.py --break-cash')
    print('Exit code:',broken.returncode)
    print(broken.stdout.splitlines()[-1])
    print(f"Explanation: substituted opening cash {m.VALUES['opening_cash']:,.1f} minus computed cash {rows[0]['cash']:,.1f} = {expected_gap:,.1f} million.")
    restored=subprocess.run([sys.executable,'-B',str(script)],capture_output=True,text=True,check=True)
    check('restored output identical',restored.stdout==normal.stdout)
    check('source unchanged by break',digest==hashlib.sha256(script.read_bytes()).hexdigest())
    saved=(HERE/'lab10_output.txt').read_text(encoding='utf-8')
    check('saved executed output exact',saved.replace('\r\n','\n')==normal.stdout.replace('\r\n','\n'))
    print('RESTORED: normal run exit0, all checks pass, same source hash and output.')
    root=HERE.parent
    check('19-file snapshot present',len(PRESERVED)==19)
    for file,sha in PRESERVED.items():
        check('preserved '+file,hashlib.sha256((root/file).read_bytes()).hexdigest()==sha)
    git=shutil.which('git') or r'C:\Program Files\Git\cmd\git.exe'
    tracked=subprocess.run([git,'-c','safe.directory='+root.as_posix(),'ls-tree','-r','--name-only',STARTING_COMMIT],cwd=root,capture_output=True,text=True,check=True).stdout.splitlines()
    check('snapshot covers every original tracked file',set(tracked)==set(PRESERVED))
    print('PASS: all 19 pre-existing tracked files unchanged from',STARTING_COMMIT)
    prior=subprocess.run([sys.executable,'-B',str(root/'lab09/proforma.py')],capture_output=True,text=True,check=True)
    check('ABG291.75','$291.75' in prior.stdout);check('ABG79.76','79.76%' in prior.stdout)
    check('ABG no failed balances','FAIL' not in prior.stdout)
    prior6=subprocess.run([sys.executable,'-B',str(root/'lab06/dcf.py')],capture_output=True,text=True,check=True)
    check('Amazon Lab06 saved output',prior6.stdout.replace('\r\n','\n')==(root/'lab06/dcf_output_lab06.txt').read_text(encoding='utf-8').replace('\r\n','\n'))
    print('PASS: unchanged ABG $291.75 / 79.76%; unchanged Amazon Lab06 $5.9930 and exact saved output.')
    report=(HERE/'lab10.md').read_text(encoding='utf-8')
    check('visible AI disclosure','## AI-use disclosure' in report and 'Codex' in report)
    for word in ('SEC','debug','validation','draft'):check('disclosure scope '+word,word in report.split('## AI-use disclosure')[1])
    for expected in ('lab10.md','amazon_history.csv','amazon_assumptions.csv','amazon_proforma.py','lab10_output.txt','validate_lab10.py','sources.md'):
        check('required file '+expected,(HERE/expected).is_file())
    if submission_ready:
        check('partner and manual work complete','PENDING PARTNER INPUT' not in report and 'PENDING MANUAL CONFIRMATION' not in report)
    else:
        print('PERSONAL REQUIREMENTS: report status governs; default run does not certify manual checks or partner work.')
    print(f'PASS: {COUNT} required computational, source-arithmetic, refusal, artifact, and preservation checks.')
    print(f"BASE: equity ${v['equity_value']:,.2f} million; ${v['per_share']:.2f}/share; terminal {v['terminal_share']:.2%}.")


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--submission-ready',action='store_true')
    args=parser.parse_args()
    try:run_tests(args.submission_ready)
    except (AssertionError,ValueError,subprocess.CalledProcessError) as e:
        print('VALIDATION FAILED:',e);raise SystemExit(1)
