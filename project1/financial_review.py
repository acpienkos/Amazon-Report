"""Reproducible financial review and old-to-new attribution; not a student assessment."""
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE));sys.dont_write_bytecode=True
import json,zipfile,csv,re,hashlib
from datetime import datetime,timezone
import model as m
from source_tables import rows as source_rows

def main():
    with zipfile.ZipFile(HERE/'evidence/review_snapshot/before-review.zip') as z:
        old=json.loads(z.read('project1/outputs/valuation.json'))
    new=json.loads((HERE/'outputs/valuation.json').read_text())
    a,r=m.forecast();v=new['base']['valuation'];ov=old['base']['valuation']
    old_adjustment=sum(x['value'] for x in ov['adjustments']);shares=v['diluted_shares']
    times=ov['discount_times'];cash=[x['fcff']*(112/365 if i==0 else 1) for i,x in enumerate(r)]
    normalized_old_terminal=ov['terminal']['fcff']+(r[-1]['operating_income']-old['base']['rows'][-1]['operating_income'])*(1+m.c.TERMINAL_G)*.78
    normalized=m.dcf(cash,ov['wacc'],ov['terminal_growth'],normalized_old_terminal,times)
    terminal_only=m.dcf(cash,ov['wacc'],ov['terminal_growth'],v['terminal']['fcff'],times)
    wacc_next=m.dcf(cash,v['wacc'],v['terminal_growth'],v['terminal']['fcff'],times)
    waterfall=[dict(step='Prior published incomplete core subtotal',per_share=ov['per_share']),
       dict(step='Remove named FY2025 FTC settlement from recurring forecast costs',per_share=(normalized['enterprise_value']+old_adjustment)/shares),
       dict(step='Apply terminal opening-asset D&A/rental policies',per_share=(terminal_only['enterprise_value']+old_adjustment)/shares),
       dict(step='Include reported July notes in market-value debt proxy/WACC',per_share=(wacc_next['enterprise_value']+old_adjustment)/shares),
       dict(step='Known July debt/cash and OpenAI payment in core bridge',per_share=v['per_share'])]
    source_checks=[]
    expected={'Cost of sales':356414,'Fulfillment':109074,'Technology and infrastructure':108521,
              'Sales and marketing':47129,'General and administrative':11172,
              'Other operating expense (income), net':4639,'Operating income':79975,
              'Interest income':4381,'Interest expense':2274,'Other income (expense), net':15229,
              'Income before income taxes':97311,'Net income':77670}
    table=source_rows('amazon_2025')
    for label,value in expected.items():
        matches=[x for x in table if x and x[0]==label]
        # Match the final FY2025 number in the annual multi-year statement row,
        # not an arbitrary occurrence anywhere in the source document.
        matched=[]
        for x in matches:
            nums=[float(t.replace(',','')) for cell in x[1:] for t in re.findall(r'(?<![A-Za-z])\d[\d,]*(?:\.\d+)?',cell)]
            if nums and nums[-1]==value:matched.append(x)
        source_checks.append(dict(item=label,value=value,matched=bool(matched),source=m.c.K,locator='FY2025 consolidated annual statement row'))
    assert all(x['matched'] for x in source_checks),source_checks
    assert abs(716924-sum(expected[k] for k in ['Cost of sales','Fulfillment','Technology and infrastructure','Sales and marketing','General and administrative','Other operating expense (income), net'])-79975)<1e-6
    assert all(abs(y['fcff']-x['fcff']-y['revenue']*2500/716924*.78)<1e-6 for x,y in zip(old['base']['rows'],r)), 'FCFF change must equal sourced recurring-cost normalization, not financing/investment cash flows'
    review=dict(audited_at_utc=datetime.now(timezone.utc).isoformat(),source_checks=source_checks,
      old_per_share=ov['per_share'],old_wacc=ov['wacc'],new_core_per_share=v['per_share'],waterfall=waterfall,
      old_terminal=ov['terminal'],new_terminal=v['terminal'],strategic=new['strategic_investments'],
      old_funding=old['base']['funding_feasible'],new_funding=new['base']['funding_feasible'],
      new_funding_errors=new['base']['funding_errors'],recommendation=new['recommendation'],
      annual_fcff_change='Exactly after-tax named settlement normalization; no financing or nonoperating-purchase contamination',comprehensive_point_value_verified=False)
    (HERE/'evidence/financial_review.json').write_text(json.dumps(review,indent=2),encoding='utf-8')
    with (HERE/'outputs/review_waterfall.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['step','per_share']);w.writeheader();w.writerows(waterfall)
    debt=[dict(item='FY2025 modeled opening carrying debt',USDm=68851),
      dict(item='Observed H1 net term issuance cash',USDm=64246),
      dict(item='Model carrying proxy after H1 cash changes',USDm=133097),
      dict(item='Reported June30 carrying debt incl current/short',USDm=128894+3330+325),
      dict(item='Unmodeled carrying reconciliation residual - not a plug',USDm=128894+3330+325-133097),
      dict(item='Reported June30 face debt incl short',USDm=133320),
      dict(item='Known July note face/proceeds proxy',USDm=25000),
      dict(item='Core bridge debt face proxy',USDm=158320),
      dict(item='WACC notes/other market-debt proxy incl July',USDm=124980+25000),
      dict(item='WACC finance-lease/facility financing claims',USDm=13451+9315)]
    with (HERE/'outputs/debt_basis_reconciliation.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['item','USDm']);w.writeheader();w.writerows(debt)
    print('Financial review source-row checks passed;',len(source_checks),'rows. Old/new core:',ov['per_share'],v['per_share'])
if __name__=='__main__':main()
