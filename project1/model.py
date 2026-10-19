"""Integrated signed-FCFF valuation over the unchanged Lab10 statement engine.

Accounting policy: operating leases remain operating. Finance leases/facility
financing are debt-like; new noncash assets are investment, principal is financing.
Capital AP is investment working capital, not a separate debt deduction.
"""
import sys
sys.dont_write_bytecode=True
import copy,csv,importlib.util,json,math
from pathlib import Path
from datetime import date
from statistics import median
import config as c
import statements
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
spec=importlib.util.spec_from_file_location('legacy_amazon',ROOT/'lab10/amazon_proforma.py')
legacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(legacy)

def fresh(): return copy.deepcopy(legacy.VALUES)

def operating_nwc(r):
    return r['inventory']+r['receivables']-r['trade_payables']-r['operating_accruals']-r['unearned']

def forecast(case='base',override=None):
    a=fresh();s=c.SCENARIOS[case]
    a['nonoperating_investments']=list(c.NONOPERATING_INVESTMENTS)
    a['other_cost_ratio']-=c.NORMALIZATION_FTC/a['opening_revenue']
    a['debt_net_change'][0]+=25000 # reported July notes, distinct from assumed FY2027 issuance
    for key in ['gross_margin']:
        a[key]=[v+s.get('margin_pp',0) for v in a[key]]
    a['capex_later']=[v*s.get('capex_scale',1) for v in a['capex_later']]
    if s.get('no_2027_issuance'): a['debt_net_change'][1]=0
    # Scenario changes AWS only; non-AWS sales are residual of legacy base total.
    base_total=a['opening_revenue'];aws=c.AWS_2025;ads=c.ADVERTISING_2025
    shifted_aws=c.AWS_2025;last_total=a['opening_revenue'];business=[]
    for i,g in enumerate(fresh()['growth']):
        base_total*=1+g;aws*=1+c.AWS_GROWTH[i];ads*=1+c.AD_GROWTH[i]
        shifted_aws*=1+c.AWS_GROWTH[i]+s.get('aws_growth_pp',0)
        total=base_total-aws+shifted_aws
        a['growth'][i]=total/last_total-1;last_total=total
        business.append(dict(aws_revenue=shifted_aws,advertising_revenue=ads,
                             retail_and_other_revenue=total-shifted_aws-ads))
    if override:
        for k,v in override.items(): a[k]=copy.deepcopy(v)
    rows=statements.project(a)
    for i,r in enumerate(rows):
        r.update(business[i]);r['operating_nwc']=operating_nwc(r)
        r['operating_cash_taxes']=max(0,r['operating_income'])*a['tax_rate']
        r['nopat']=r['operating_income']-r['operating_cash_taxes']
        r['eligible_da']=r['depreciation']
        r['operating_residual_investment']=r['change_other_net_assets']-r['nonoperating_investment_purchase']
        r['economic_asset_additions']=r['ppe_additions']+r['operating_residual_investment']
        r['investment_working_capital_credit']=r['change_capex_payables']
        r['operating_investment']=r['economic_asset_additions']-r['investment_working_capital_credit']
        r['fcff']=r['nopat']+r['eligible_da']-r['operating_investment']-r['change_operating_wc']
        # Cash-tax provision is a proxy, not a historical paid-tax forecast.
        r['unlevering_tax_adjustment']=r['income_tax']-r['operating_cash_taxes']
        r['fcff_from_cfo']=(r['operating_cash_flow']+r['interest_expense']-r['interest_income']-r['other_income']
            +r['unlevering_tax_adjustment']-r['operating_investment'])
        r['fcff_gap']=r['fcff']-r['fcff_from_cfo']
    return a,rows

def diagnose(rows,a):
    accounting=[];funding=[]
    for r in rows:
        expected_additions=r['capex']+r['change_capex_payables']+r['finance_lease_addition']+r['financing_addition']
        if abs(r['ppe_additions']-expected_additions)>1e-6:
            accounting.append(f"{r['year']} PP&E additions omit or duplicate financed investment")
        expected_investment=expected_additions+r['change_other_net_assets']-r.get('nonoperating_investment_purchase',0)-r['change_capex_payables']
        if abs(r['operating_investment']-expected_investment)>1e-6:
            accounting.append(f"{r['year']} operating investment mismatch")
        for k,v in legacy.checks(r,a).items():
            if not math.isfinite(v): accounting.append(f"{r['year']} nonfinite {k}")
            elif k.endswith('headroom'):
                if v < -1e-6: funding.append(f"{r['year']} {k}: {v:.2f} USDm")
            elif abs(v)>1e-6: accounting.append(f"{r['year']} {k}: {v:.6f}")
        if abs(r['fcff_gap'])>1e-6:accounting.append(f"{r['year']} FCFF route mismatch")
        if abs(r['change_operating_wc']-(operating_nwc(r)-operating_nwc(r['opening'])))>1e-6:
            accounting.append(f"{r['year']} operating WC continuity")
    # Legacy gate independently checks opening links, years, balances and asset signs.
    try: legacy.assert_balanced(rows,a)
    except ValueError as e:
        if not funding: accounting.append(str(e))
    return dict(accounting_valid=not accounting,funding_feasible=not funding,
                accounting_errors=accounting,funding_errors=funding)

def wacc(inputs=None):
    p=dict(c.WACC_INPUTS if inputs is None else inputs)
    if not all(math.isfinite(x) for x in p.values()) or p['market_debt']<0 or p['market_equity']<=0:
        raise ValueError('Invalid WACC components')
    ke=p['risk_free']+p['beta']*p['equity_risk_premium']
    dw=p['market_debt']/(p['market_debt']+p['market_equity'])
    return dict(**p,cost_of_equity=ke,after_tax_debt_cost=p['debt_cost']*(1-p['marginal_tax']),
                debt_weight=dw,equity_weight=1-dw,wacc=(1-dw)*ke+dw*p['debt_cost']*(1-p['marginal_tax']))

def terminal(last,a,g):
    # Explicit steady-state capital turnover: net PPE and operating NWC grow at g.
    # Includes noncash finance-lease additions within total required investment.
    # Capital AP grows at g and supplies investment WC credit; no principal subtraction.
    revenue=last['revenue']*(1+g)
    # Apply the same opening-net-PP&E depreciation policy as the forecast.
    # Rental expense also uses the actual opening ROU/lease schedules, rather
    # than silently reducing the effective depreciation/rental rates in 2031.
    da=last['ppe']*a['depreciation_rate']
    rent=last['operating_rou']*a['rou_amortization_rate']+last['operating_lease']*a['operating_lease_rate']
    gross_profit=revenue*a['gross_margin'][-1]
    sga=gross_profit*a['sga_to_gp'][-1]
    residual=revenue*a['other_cost_ratio']
    ebit=gross_profit-sga-residual-da-rent
    taxes=max(0,ebit)*a['tax_rate'];nopat=ebit-taxes
    additions=da+g*last['ppe']
    cap_ap_credit=g*last['capex_payables']
    wc=g*last['operating_nwc']
    operating_cash_investment=g*a['minimum_cash']
    reinvestment=additions-da-cap_ap_credit+wc+operating_cash_investment
    fcff=nopat-reinvestment
    if fcff<=0: raise ValueError('Unsupported nonpositive steady-state FCFF')
    invested=last['ppe']-last['capex_payables']+last['operating_nwc']+a['minimum_cash']
    return dict(year=2031,revenue=revenue,ebit=ebit,operating_cash_taxes=taxes,nopat=nopat,
        eligible_da=da,operating_lease_expense=rent,capital_investment=additions,capital_payable_credit=cap_ap_credit,
        change_operating_nwc=wc,operating_cash_investment=operating_cash_investment,
        net_reinvestment=reinvestment,fcff=fcff,invested_capital=invested,
        implied_return_on_capital=nopat/invested if invested>0 else None,
        convention='FY2031 EBIT rebuilt with forecast opening-asset D&A/rental policies; net capital ratios stabilize and subsequent operating cash flow grows at g. Investment normalization remains a judgment, not guidance.')

def equity_bridge(ev,inputs=None):
    b=dict(c.BRIDGE if inputs is None else inputs)
    shares=b['common_shares']+b['incremental_dilutive_awards']
    if shares<=0 or not math.isfinite(shares):raise ValueError('Invalid diluted shares')
    adjustments=[('June30 cash and equivalents',b['cash']),('Known July debt proceeds',b.get('known_debt_issuance',0)),
      ('Known subsequent OpenAI cash payment',-b.get('known_subsequent_investment_cash',0)),('Required operating cash',-b['operating_cash']),
      ('Marketable securities',b['securities']),('Debt incl current/short term',-b['debt']),
      ('Finance leases',-b['finance_leases']),('Facility financing',-b['facility_financing']),
      ('Non-operating asset supplement',b['nonoperating_assets']),('Other separate claims',-b['other_claims'])]
    equity=ev+sum(v for _,v in adjustments)
    return dict(operating_enterprise_value=ev,adjustments=[dict(item=k,value=v) for k,v in adjustments],
                equity_value=equity,diluted_shares=shares,per_share=equity/shares,
                excluded_operating_lease_liability=b['operating_leases'],
                basis='June30 balances plus disclosed July $25bn debt/cash and $21.3bn OpenAI payment; other intra-quarter changes unmodeled. July22 common shares plus Q2 incremental awards. Not exact September10 balances.')

def strategic_bridge(ev):
    """Report source-backed gross assets separately; do not invent a net appraisal.

    The $21.3bn subsequent purchase is added to investments and deducted from cash
    once, netting to zero before taxes. Tax cases are transparent bounds/proxies,
    not claimed issuer tax liabilities or liquidation proceeds.
    """
    core=equity_bridge(ev)
    gross=sum(c.STRATEGIC_ASSETS.values())
    old_gross=gross-c.STRATEGIC_ASSETS['subsequent_openai']
    cash_adjustment=0 # payment already deducted in core equity_bridge; never deduct twice
    cases=[]
    for label,haircut in [('No tax/liquidity haircut (gross carrying reference)',0),('22% of pre-existing gross assets haircut (conservative diagnostic)',.22)]:
        equity=core['equity_value']+gross+cash_adjustment-old_gross*haircut
        cases.append(dict(case=label,haircut=old_gross*haircut,equity_value=equity,per_share=equity/core['diluted_shares']))
    return dict(components=c.STRATEGIC_ASSETS,gross_assets=gross,additional_cash_adjustment=cash_adjustment,
                known_subsequent_payment_already_in_core=c.STRATEGIC_ASSETS['subsequent_openai'],
                cases=cases,status='Carrying-value references only: net investment taxes, restrictions, correlated AWS exposure and exact-date changes not appraised. No comprehensive verified equity point value.')

def dcf(cashflows,rate,g,terminal_fcff,times=None):
    if not all(math.isfinite(v) for v in cashflows+[rate,g,terminal_fcff]):raise ValueError('Nonfinite DCF input')
    if rate<=g or g<=-1 or rate<=-1:raise ValueError('Require WACC > growth > -100%')
    if terminal_fcff<=0:raise ValueError('Require supported positive terminal cash flow')
    times=times or list(range(1,len(cashflows)+1))
    if len(times)!=len(cashflows) or not times or any(not math.isfinite(t) or t<=0 for t in times):raise ValueError('Invalid cashflow timing')
    pv=[x/(1+rate)**t for x,t in zip(cashflows,times)]
    tv=terminal_fcff/(rate-g);pvt=tv/(1+rate)**times[-1]
    ev=sum(pv)+pvt
    return dict(pv_cashflows=pv,pv_explicit=sum(pv),terminal_value=tv,pv_terminal=pvt,
                enterprise_value=ev,terminal_dependence=pvt/ev if ev else None)

def value(rows,a,rate=None,g=c.TERMINAL_G,bridge=None):
    if not diagnose(rows,a)['accounting_valid']:raise ValueError('Accounting failure; valuation refused')
    if any(abs(r['fcff_gap'])>1e-6 for r in rows):raise ValueError('FCFF reconciliation failure')
    rate=wacc()['wacc'] if rate is None else rate
    end=date(2026,12,31);asof=date.fromisoformat(c.AS_OF)
    stub=(end-asof).days/365
    cashflows=[r['fcff']*(stub if i==0 else 1) for i,r in enumerate(rows)]
    times=[stub+i for i in range(5)]
    term=terminal(rows[-1],a,g)
    v=dcf(cashflows,rate,g,term['fcff'],times)
    return dict(**v,**equity_bridge(v['enterprise_value'],bridge),wacc=rate,terminal_growth=g,
        terminal=term,discount_times=times,discounted_period_fcff=cashflows,
        upside=equity_bridge(v['enterprise_value'],bridge)['per_share']/c.PRICE-1,
        timing='Sept10 2026; remaining 112/365 of modeled FY2026 FCFF, then full FY2027-2030. Uniform accrual proxy; excludes elapsed cashflows; does not forecast seasonality.')

def evaluate(case='base',override=None):
    a,rows=forecast(case,override);status=diagnose(rows,a)
    v=None;error=None
    if status['accounting_valid']:
        try:v=value(rows,a)
        except ValueError as e:error=str(e)
    return dict(case=case,reason=c.SCENARIOS[case]['reason'],inputs=a,rows=rows,**status,
                valuation=v,valuation_error=error,
                valuation_status='provisional' if v and status['funding_feasible'] else 'diagnostic only - infeasible or invalid')

def reverse(target,lower=-.01,upper=.30):
    """Solve a uniform gross-margin shift through statements; bounds are diagnostic."""
    if lower>=upper or target<=0:raise ValueError('Invalid reverse DCF bracket')
    def run(x):
        a,rows=forecast('base',{'gross_margin':[v+x for v in fresh()['gross_margin']]})
        status=diagnose(rows,a)
        try:v=value(rows,a)
        except ValueError:return None,status
        return v['per_share'],status
    lo,ls=run(lower);hi,hs=run(upper)
    result=dict(target=target,variable='Uniform additive gross-margin shift, decimal ratio',
      held_fixed='Revenue paths, capex, working capital policies, financing assumptions, WACC, g, bridge and shares.',
      bounds=[lower,upper],endpoint_prices=[lo,hi],solution=None)
    if lo is None or hi is None or not lo<=target<=hi:return dict(**result,status='No solution in stated bracket')
    for _ in range(150):
        mid=(lower+upper)/2;p,s=run(mid)
        if p is None:return dict(**result,status='Invalid interior cashflow path')
        if abs(p-target)<1e-7:
            result.update(solution=mid,repriced=p,funding_feasible=s['funding_feasible'],
                          gross_margin_path=[v+mid for v in fresh()['gross_margin']])
            return dict(**result,status='Conditional solution; not proof of feasible margins or mispricing')
        if p<target:lower=mid
        else:upper=mid
    raise ValueError('Reverse DCF failed to converge')

def peer_multiples(p):
    if p['ticker']=='AMZN' or p['decision'] not in ['use','qualify']:raise ValueError('Peer excluded')
    if p['price_date']!=c.AS_OF or p['published']>c.AS_OF:raise ValueError('Date/availability mismatch')
    for key in ['price','shares','revenue','eps']:
        if not isinstance(p[key],(float,int)) or not math.isfinite(p[key]) or p[key]<=0:raise ValueError('Invalid peer denominator/input')
    if not all(math.isfinite(p[k]) for k in ['ebit','da','cash','securities','debt','finance_leases','minority','restricted_securities']):raise ValueError('Nonfinite peer enterprise inputs')
    ebitda=p['ebit']+p['da']
    if ebitda<=0:raise ValueError('Nonpositive EBITDA')
    net_claims=p['debt']+p['finance_leases']+p['minority']-p['cash']-p['securities']+p['restricted_securities']
    ev=p['price']*p['shares']+net_claims
    return dict(**p,market_equity=p['price']*p['shares'],net_claims=net_claims,ev=ev,
                ebitda=ebitda,ev_revenue=ev/p['revenue'],ev_ebitda=ev/ebitda,pe=p['price']/p['eps'])

def comps():
    accepted=[];seen=set()
    for p in c.PEERS:
        if p['ticker'] in seen:continue
        seen.add(p['ticker']);accepted.append(peer_multiples(p))
    # Amazon annual accounting EBITDA excludes operating ROU addback (rental policy).
    target=dict(revenue=716924,ebit=79975,da=41860,eps=7.17)
    target['ebitda']=target['ebit']+target['da']
    implied=[]
    for p in accepted:
        implied.append(dict(ticker=p['ticker'],ev_revenue=equity_bridge(p['ev_revenue']*target['revenue'])['per_share'],
            ev_ebitda=equity_bridge(p['ev_ebitda']*target['ebitda'])['per_share'],pe=p['pe']*target['eps']))
    summary={m:dict(low=min(p[m] for p in implied),median=median(p[m] for p in implied),high=max(p[m] for p in implied)) for m in ['ev_revenue','ev_ebitda','pe']}
    leave=[]
    for p in accepted:
        remain=[q for q in implied if q['ticker']!=p['ticker']]
        leave.append(dict(removed=p['ticker'],remaining=len(remain),
          values={m:median(q[m] for q in remain) if remain else None for m in summary},
          interpretation='One remaining peer is a reference, not a range.'))
    return dict(peers=accepted,target=target,implied=implied,summary=summary,leave_one_out=leave,
        status='Qualified references; differing fiscal periods, dated share/balance proxies and unnormalized investment gains. Not a sum of the parts.')
