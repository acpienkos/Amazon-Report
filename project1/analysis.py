"""Run the offline, reproducible Project 1 analysis and visible output export."""
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE));sys.dont_write_bytecode=True
import csv,json,hashlib,platform,subprocess
from datetime import datetime,timezone
import config as c
import model as m

LIMITATIONS=[
 'PROVISIONAL: annual FY2026 FCFF is accrued uniformly for the 112-day remaining stub. Amazon seasonality and actual H1 cashflows are not fully reconciled to an intra-year valuation.',
 'Bridge uses latest available June30 reported cash/debt/leases; it is not an exact September10 roll-forward. Test stale-balance alternatives before an investment.',
 'Core subtotal excludes strategic investment value. Separate gross carrying references include reported investments and known subsequent purchase; issuer tax basis, liquidity and economic value remain unappraised. No comprehensive verified equity point value.',
 'Gross-margin, capex taper, funding renewal, AWS/advertising decomposition and terminal reinvestment are analyst judgments; no probabilities assigned.',
 'Normalized operating cash tax equals 22% of positive EBIT; deferred taxes and NOL use are not explicitly scheduled. Reported paid taxes are not equivalent.',
 'Operating leases remain rent in EBIT/FCFF and are not deducted again. Finance leases/facility additions are investment; liabilities are deducted once. Content replacement/amortization net to zero in residual operating expense.',
 'Diluted shares use July22 common shares plus Q2 incremental awards; this is a proxy. Future compensation is cash-replaced, not actual Amazon policy.',
 'Beta 1.44 is the preserved September10 vendor observation; its historical estimation process could not be independently reconstructed. ERP 5% is a course assumption, not observed data.',
 'Full Brightspace assignment/rubric and the October19 announcement original posting were not accessed. Announcement is reproduced as user-supplied course evidence; early-AI recovery remains a separate clarification.',
 'New outputs are AI-assisted. No human AI-off prediction, assessed execution, actual recording or corrected transcript is claimed.'
]

def write_json(path,obj):
    path.write_text(json.dumps(obj,indent=2,allow_nan=False),encoding='utf-8')

def csv_write(path,rows):
    if not rows:return
    keys=list(dict.fromkeys(k for r in rows for k in r))
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)

def preserve_check():
    manifest=json.loads((HERE/'evidence/preservation_manifest.json').read_text())
    bad=[]
    for p,h in manifest['sha256'].items():
        target=Path(p)
        if not target.exists():
            normalized=p.replace('\\','/')
            marker='/amazon-report-upload/'
            target=(HERE.parent/normalized.split(marker,1)[1]) if marker in normalized else HERE/'docs/historical'/normalized.rsplit('/',1)[-1]
        if not target.exists() or hashlib.sha256(target.read_bytes()).hexdigest()!=h:bad.append(p)
    if bad:raise ValueError('Historical files modified: '+str(bad))
    return len(manifest['sha256'])

def registers():
    with (HERE/'data/legacy_assumptions.csv').open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f))
    out=[]
    for r in rows:
        key=r['Assumption']
        value=json.loads(r['Value'])
        unit='USD million'
        if any(z in key for z in ['ratio','rate','yield','growth','margin','sga_to_gp']):unit='decimal ratio; annual for rates/growth'
        if key in ['cash_settled_compensation','positive_only']:unit='boolean accounting policy'
        if key in ['inventory_days','days_per_year']:unit='days'
        if key in ['first_year','last_year']:unit='calendar year'
        if key=='shares':unit='million common shares - historical only'
        out.append(dict(input=key,value=r['Value'],classification=r['Label'],units=unit,
            rationale=r['Reason'],source=r['Exact source or calculation'],
            period='FY2025 history / FY2026-2030 forecast; see exact source',
            availability='Source-specific; FY2025 filing Feb6 and Q2 filing July30 2026',
            disposition='Reused for statements only; FCFE rate, shares and positive-only setting not used in FCFF valuation' if key in ['cost_of_equity','shares','positive_only','market_price'] else 'Reused, judgment subject to challenge',
            sensitivity='See scenarios.json; structural assumptions and omission limits in convention_decisions.md'))
        if key=='other_cost_ratio':
            out[-1].update(value=float(json.loads(r['Value']))-c.NORMALIZATION_FTC/716924,
              classification='reported-to-normalized adjustment',rationale='Exclude only named FY2025 FTC settlement2500 from recurring residual cost; retain other charges and ongoing litigation risk.',source=c.K+' | Note1 Q3 FTC settlement; legacy ratio preserved in legacy_assumptions.csv')
    for key,val in c.WACC_INPUTS.items():
        out.append(dict(input=key,value=val,classification='preserved estimate / assumption; see WACC sources',units='USD million for capital; decimals for rates; beta dimensionless',
            rationale='Lab06 CAPM components, same dated market close, finance claims added consistently',source='../lab06/lab06.md; sources/treasury.html; sources/amazon_debt.html; sources/amazon_2026q2.html',
            period=c.AS_OF,availability='All inputs available by Sep10 except retrospective analyst judgment',disposition='Qualified: beta method unverified; market debt proxy',sensitivity='WACC +/-1 percentage point; never a new market estimate'))
    for key,val in [('terminal_growth',c.TERMINAL_G),('aws_growth_path',c.AWS_GROWTH),('advertising_growth_path',c.AD_GROWTH)]:
        out.append(dict(input=key,value=json.dumps(val),classification='analyst judgment',units='decimal annual rate',rationale='Legacy terminal g; AWS and ads slow from reported H1/Q2 rates. Decomposition preserves consolidated legacy base revenue.',source='config.py; sources/amazon_2025.html; sources/amazon_2026q2.html',period='2026-2030 / steady-state',availability='Constructed during Edition B; not contemporaneous forecast',disposition='Provisional, not management guidance',sensitivity='Scenario paths and g grid'))
    for key,val in c.BRIDGE.items():
        out.append(dict(input='bridge_'+key,value=val,classification='reported proxy / judgment',units='million shares for share fields; otherwise USD million',rationale='Latest available June30 balances; cash floor inherited; excluded investments not worth zero',source=c.SEC+'; ../lab10/sources.md',period='June30 / July22 2026',availability='July30 2026',disposition='Provisional stale balance/dilution proxy',sensitivity='Convention alternatives; operating cash floor; investment supplement'))
    csv_write(HERE/'data/assumptions.csv',out)
    with (HERE/'data/assumptions.csv').open('a',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(out[0]))
        w.writerow(dict(input='nonoperating_investments',value=json.dumps(c.NONOPERATING_INVESTMENTS),classification='Known2026 cash uses; future undisclosed purchases assumed0',units='USD million per year',rationale='H1 acquisition/nonmarketable39767 plus subsequentOpenAI21300; nonoperating uses affect funding, not FCFF',source=c.SEC,period='FY2026-2030',availability='Q2 filing July30 2026',disposition='Known omission corrected; future commitments remain a risk',sensitivity='Funding cases; strategic appraisal separately qualified'))
    csv_write(HERE/'data/peer_inputs.csv',c.PEERS)
    write_json(HERE/'data/scenarios.json',c.SCENARIOS)
    write_json(HERE/'data/valuation_inputs.json',dict(as_of=c.AS_OF,price=c.PRICE,wacc=c.WACC_INPUTS,bridge=c.BRIDGE,terminal_growth=c.TERMINAL_G))
    normalization=[
      dict(item='Reported net income',reported=77670,adjustment=0,normalized=77670,unit='USDm',reason='Reported annual net income; starting point of operating-income bridge.'),
      dict(item='Remove equity-method loss after tax',reported=-554,adjustment=554,normalized=0,unit='USDm',reason='Nonoperating equity-method activity: NI +554 +19087 tax -17336 other net nonoperating income = EBIT79975.'),
      dict(item='FY2025 EBIT',reported=79975,adjustment=2500,normalized=82475,unit='USDm',reason='Exclude only identified Q3 FTC settlement from recurring outlook; reported history and opening balances unchanged.'),
      dict(item='Nonoperating income net',reported=15229+4381-2274,adjustment=-(15229+4381-2274),normalized=0,unit='USDm',reason='Operating valuation excludes other income, investment interest and financing interest; use normalized NOPAT, not GAAP NI.'),
      dict(item='Operating tax proxy',reported='not separately reported',adjustment='22% of normalized EBIT',normalized=82475*.22,unit='USDm',reason='Provision-as-cash judgment; not a claimed reported cash-tax number.'),
      dict(item='Normalized NOPAT',reported='not reported',adjustment='77670 +554 +19087 -17336 +2500 -18144.5',normalized=82475*.78,unit='USDm',reason='Reported NI to normalized economic NOPAT; does not restate reported retained earnings.'),
      dict(item='Net cash capex',reported=131819,adjustment=-3499,normalized=128320,unit='USDm',reason='Gross purchases less proceeds/incentives; asset-addition and payable reconciliations separate.'),
      dict(item='FY2025 net PP&E',reported=357025,adjustment=0,normalized=357025,unit='USDm',reason='Audited opening assets retained; no synthetic fair-value reset.'),
      dict(item='FY2025 total assets',reported=818042,adjustment=0,normalized=818042,unit='USDm',reason='Reclassification does not alter total.'),
      dict(item='FY2025 total equity',reported=411065,adjustment=0,normalized=411065,unit='USDm',reason='Reported opening equity retained. Economic NOPAT normalization is not booked as GAAP equity.'),
      dict(item='Trade / capital AP',reported=121909,adjustment='split 94909 / 27000',normalized=121909,unit='USDm',reason='Capital AP separated from operating working capital; not new debt.'),
    ]
    csv_write(HERE/'data/normalization.csv',normalization)

def run_analysis():
    preserved=preserve_check();registers()
    cases=[m.evaluate(k) for k in c.SCENARIOS]
    base=cases[0];a=base['inputs'];rows=base['rows'];v=base['valuation']
    grid=[]
    for rate in [v['wacc']-.01,v['wacc'],v['wacc']+.01]:
        for g in [.015,.025,.035]:
            result=m.value(rows,a,rate,g) if rate>g else None
            grid.append(dict(wacc=rate,g=g,per_share=result['per_share'] if result else None))
    valid=[k['valuation']['per_share'] for k in cases[:3] if k['funding_feasible'] and k['accounting_valid'] and k['valuation']]
    coverage=[k['case'] for k in cases[:3] if not k['funding_feasible']]
    recommendation='do not initiate'
    # Conservative evidence rule: no initiation while major convention/evidence limitations persist.
    reason='For a fund with no position, do not initiate at the dated market price on present evidence. The corrected base fails funding and the full equity appraisal is incomplete; this is a no-purchase decision, not proof of 80% mispricing or a short recommendation.'
    alternatives=[]
    for name,b in [('All cash treated excess',dict(c.BRIDGE,operating_cash=0)),('Double-count operating lease debt (REJECTED)',dict(c.BRIDGE,debt=c.BRIDGE['debt']+c.BRIDGE['operating_leases']))]:
        z=m.equity_bridge(v['enterprise_value'],b)
        alternatives.append(dict(case=name,per_share=z['per_share'],disposition='Not base; operating cash judgment' if 'REJECTED' not in name else 'Reject: rental cost already in EBIT/FCFF'))
    # A valuation sensitivity to a missing asset is not an assertion of that asset value.
    alternatives.append(dict(case='Per $10bn net nonoperating asset supplement',per_share=v['per_share']+10000/v['diluted_shares'],disposition='Unit sensitivity only; supplement remains unvalued'))
    # Challenge the terminal capital-intensity reset with the old final-year cash
    # investment intensity. Not a steady-state solution: explicitly a diagnostic.
    last=rows[-1];g=c.TERMINAL_G
    carry_fcff=(last['nopat']+last['depreciation']-last['operating_investment']-g*last['operating_nwc'])*(1+g)-g*a['minimum_cash']
    if carry_fcff>0:
        alt=m.dcf(v['discounted_period_fcff'],v['wacc'],g,carry_fcff,v['discount_times'])
        alternatives.append(dict(case='Carry FY2030 investment intensity into terminal (diagnostic)',per_share=m.equity_bridge(alt['enterprise_value'])['per_share'],
          disposition='Avoids immediate capital-turnover reset but not a fully reconciled perpetual asset schedule; shows terminal-model risk.'))
    data=dict(generated_at_utc=datetime.now(timezone.utc).isoformat(),as_of=c.AS_OF,price=c.PRICE,
      price_source=c.PRICE_SOURCE,forecast_years=list(range(2026,2031)),status='PROVISIONAL EDUCATIONAL VALUATION',
      recommendation=recommendation,recommendation_reason=reason,
      reversal_trigger='Reassess only after supported signed-flow value and funding survive conservative reinvestment/operating cases, and the dated price offers an evidence-supported margin of safety.',
      committee_ask='Do not authorize a new position now. Reopen only after documented funding covers investment commitments, operating cash returns support reinvestment, and a complete dated asset/tax/share bridge supports value above the purchase price with a defensible margin of safety.',
      wacc=m.wacc(),base=base,cases=cases,valid_low_high_range=[min(valid),max(valid)],
      excluded_infeasible_cases=coverage,sensitivity=grid,reverse_dcf=m.reverse(c.PRICE),comparables=m.comps(),
      convention_alternatives=alternatives,strategic_investments=m.strategic_bridge(v['enterprise_value']),
      funded_case_names=[q['case'] for q in cases[:3] if q['funding_feasible'] and q['valuation']],
      valuation_label='Diagnostic operating-business/liquid-asset subtotal; excludes strategic assets and base funding fails',
      limitations=LIMITATIONS,preserved_file_count=preserved,
      environment=dict(python=platform.python_version(),platform=platform.platform()),
      historical_fcfe=dict(per_share=32.67314175381166,range=[23.87,50.49],basis='Lab10/11 positive-only FCFE, 10% cost of equity; NOT new FCFF result'))
    write_json(HERE/'outputs/valuation.json',data)
    write_json(HERE/'outputs/visible_output.json',data)
    flat=[{k:x for k,x in r.items() if k!='opening'} for r in rows]
    for r in flat:
        r['total_assets']=m.legacy.number(r,'total_assets');r['total_liabilities']=m.legacy.number(r,'total_liabilities');r['liabilities_equity']=m.legacy.number(r,'liabilities_equity')
    csv_write(HERE/'outputs/statements.csv',flat)
    csv_write(HERE/'outputs/fcff_reconciliation.csv',[{k:r[k] for k in ['year','operating_income','operating_cash_taxes','eligible_da','economic_asset_additions','investment_working_capital_credit','operating_investment','change_operating_wc','fcff','fcff_from_cfo','fcff_gap']} for r in rows])
    csv_write(HERE/'outputs/scenarios.csv',[dict(case=q['case'],accounting_valid=q['accounting_valid'],funding_feasible=q['funding_feasible'],status=q['valuation_status'],per_share=q['valuation']['per_share'] if q['valuation'] else None,min_cash=min(r['cash'] for r in q['rows']),funding_errors='; '.join(q['funding_errors']),reason=q['reason']) for q in cases])
    csv_write(HERE/'outputs/sensitivity.csv',grid)
    csv_write(HERE/'outputs/enterprise_equity_bridge.csv',[dict(item='Operating enterprise value',value=v['enterprise_value'])]+v['adjustments']+[dict(item='Common equity value',value=v['equity_value'])])
    csv_write(HERE/'outputs/comparables.csv',data['comparables']['peers'])
    print(f"{data['status']} | as of {c.AS_OF} | {recommendation}")
    print(f"FCFF base ${v['per_share']:.2f}; valid low/base/high subset ${min(valid):.2f}-${max(valid):.2f}; WACC {v['wacc']:.6%}; g {v['terminal_growth']:.2%}")
    print('Infeasible low/base/high cases:',coverage)
    return data

if __name__=='__main__':run_analysis()
