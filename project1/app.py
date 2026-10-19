"""Committee-facing local dashboard. Displays validated saved outputs; no live feeds."""
from pathlib import Path
import sys,json,html
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE));sys.dont_write_bytecode=True
import pandas as pd
import streamlit as st

st.set_page_config(page_title='AMZN | Investment Committee',page_icon='↗',layout='wide')
st.markdown('''<style>
.stApp {background: #f6f8fc; color:#182438;}
.block-container {padding-top:2rem; max-width:1480px;}
h1,h2,h3 {letter-spacing:-0.035em;}
[data-testid="stMetric"] {background:white;padding:1.1rem;border:1px solid #dfe5ef;border-radius:14px;}
[data-testid="stSidebar"] {background:#122239;}
[data-testid="stSidebar"] * {color:#eef3fa;}
.eyebrow {color:#42738f;font-size:12px;letter-spacing:.16em;font-weight:700;}
.hero {background:#122239;color:white;padding:28px 32px;border-radius:18px;margin-bottom:24px;}
.hero h1 {color:white;margin:0;font-size:38px;}.hero p {color:#d4e1ef;margin-bottom:0;}
.note {padding:14px 18px;border-left:4px solid #e7a634;background:#fff6e3;border-radius:6px;}
.data-table {overflow:auto;max-height:520px;border:1px solid #dfe5ef;border-radius:12px;background:white;margin:12px 0;}
.data-table table {border-collapse:collapse;width:100%;font-size:13px;}.data-table th {background:#e8eef5;position:sticky;top:0;text-align:left;}
.data-table td,.data-table th {padding:10px 12px;border-bottom:1px solid #e8edf4;white-space:normal;}
.data-table tr:nth-child(even) {background:#f8fafd;}
</style>''',unsafe_allow_html=True)
path=HERE/'outputs/valuation.json'
if not path.exists():st.error('Run python -B project1/analysis.py first.');st.stop()
d=json.loads(path.read_text(encoding='utf-8'));base=d['base']['valuation']
st.sidebar.markdown('## AMZN\nInvestment committee\n\nFIN 43900 · Edition B')
page=st.sidebar.radio('Evidence navigation',['Decision','Financial statements','FCFF & capital','Scenarios & funding','Sensitivity & reverse DCF','Comparable companies','Sources & validation'])
st.sidebar.caption(f"Valuation: {d['as_of']}\n\nGenerated: {d['generated_at_utc'][:19]} UTC")
st.sidebar.warning('Provisional educational analysis. No live market feed. Student evidence remains outstanding.')
st.markdown('<div class="hero"><div class="eyebrow">AMAZON · NASDAQ: AMZN</div><h1>Investment, cash returns & the price of growth</h1><p>Five-year integrated statements · signed FCFF · explicit funding constraints</p></div>',unsafe_allow_html=True)

def money(x):return f'${x:,.2f}'
def frame(rows):return pd.DataFrame(rows)
def show(df,index=False):
    # HTML/SVG rendering avoids the optional Arrow binary transport. Native
    # controls remain interactive; no Windows application policy is changed.
    st.markdown('<div class="data-table">'+df.to_html(index=index,border=0,escape=True,float_format=lambda x:f'{x:,.3f}')+'</div>',unsafe_allow_html=True)
def bars(df,x,y,title):
    x=x.split(':')[0];y=y.split(':')[0];values=df[y].tolist();lo=min(min(values),0);hi=max(max(values),0);span=max(hi-lo,1)
    def yy(v):return 245-(v-lo)/span*190
    svg=f'<svg viewBox="0 0 650 300" style="width:100%;background:white;border-radius:12px"><text x="24" y="25" font-size="15" fill="#182438">{html.escape(title)}</text><line x1="45" x2="625" y1="{yy(0)}" y2="{yy(0)}" stroke="#aabbcc"/>'
    for i,(_,r) in enumerate(df.iterrows()):
        val=float(r[y]);xx=65+i*110;top=min(yy(val),yy(0));height=max(1,abs(yy(val)-yy(0)))
        svg+=f'<rect x="{xx}" y="{top}" width="65" height="{height}" rx="4" fill="'+('#267e9c' if val>=0 else '#cd6155')+f'"><title>{int(r[x])}: {val:.2f}</title></rect><text x="{xx+32}" y="{top-7}" text-anchor="middle" font-size="12">{val:.1f}</text><text x="{xx+32}" y="275" text-anchor="middle" font-size="12">{int(r[x])}</text>'
    st.markdown(svg+'</svg>',unsafe_allow_html=True)

def lines(df):
    colors=['#267e9c','#e4a33b','#9c6ac6','#cd6155'];keys=[k for k in df.columns if k!='year'];lo=min(0,min(df[k].min() for k in keys));hi=max(df[k].max() for k in keys);span=max(hi-lo,1)
    svg='<svg viewBox="0 0 900 350" style="width:100%;background:white;border-radius:12px">'
    for j,k in enumerate(keys):
        pts=' '.join(f'{70+i*185},{275-(float(v)-lo)/span*220}' for i,v in enumerate(df[k]))
        svg+=f'<polyline points="{pts}" fill="none" stroke="{colors[j]}" stroke-width="3"/><text x="{35+j*215}" y="325" font-size="12" fill="{colors[j]}">{k}</text>'
    for i,y in enumerate(df['year']):svg+=f'<text x="{70+i*185}" y="300" font-size="12">{y}</text>'
    svg+=f'<text x="10" y="40" font-size="12">{hi:.1f} bn</text><text x="10" y="275" font-size="12">{lo:.1f} bn</text></svg>'
    st.markdown(svg,unsafe_allow_html=True)

if page=='Decision':
    cols=st.columns(4)
    cols[0].metric('Core diagnostic subtotal',money(base['per_share']))
    cols[1].metric('Dated market close',money(d['price']))
    cols[2].metric('WACC / perpetual growth',f"{base['wacc']:.2%} / {base['terminal_growth']:.1%}")
    cols[3].metric('Committee action',d['recommendation'].upper())
    st.markdown('### Decision and committee ask')
    st.write(d['recommendation_reason']);st.info(d['committee_ask'])
    left,right=st.columns([1.5,1])
    with left:
        st.markdown('### The operating thesis')
        st.write('AWS and advertising offer growth and operating leverage. Infrastructure spending converts those prospects into near-term cash outflows. The question is whether durable operating returns and feasible funding justify the price—not whether reported earnings grow.')
        st.write('The reviewed action changes from watch/defer to do not initiate at the dated price. The corrected base fails funding. Non-operating gains stay outside FCFF; reported strategic assets now have a separate carrying-value bridge, not a claimed fair-value appraisal.')
        bars(frame([dict(year=r['year'],FCFF_USDbn=r['fcff']/1000) for r in d['base']['rows']]),'year:O','FCFF_USDbn:Q','Signed annual operating FCFF · USD billions')
    with right:
        st.markdown('### What would change the decision?');st.write(d['reversal_trigger'])
        st.markdown('### Range coverage')
        st.write(f"Only these low/base/high cases pass funding: {', '.join(d['funded_case_names'])}. Its core reference is {money(d['valid_low_high_range'][0])}; a single funded case is not a range. Base and low values are diagnostic only.")
        st.markdown('### Monitor')
        st.write('Infrastructure cash outlays; incremental operating cash conversion; AWS growth and margins; securities depletion; financing availability; terminal reinvestment; investment-asset tax claims.')
    st.warning('The corrected base fails funding. Core values exclude strategic assets; separate carrying references are not a net fair-value appraisal. Uniform remaining-year accrual, dated balance proxies and a judgmental terminal transition remain material. Do not present a precise full-company downside.')
    st.markdown('### Strategic investment bridge | carrying references, not fair-value bounds')
    show(frame(d['strategic_investments']['cases']))
    st.caption(d['strategic_investments']['status'])

elif page=='Financial statements':
    selected=st.selectbox('Forecast case',[x['case'] for x in d['cases']]);case=next(x for x in d['cases'] if x['case']==selected)
    st.write(case['reason']);st.caption('USD millions. Forecasts are conditional analyst judgments, not management guidance.')
    if not case['funding_feasible']:st.error('Funding-infeasible path: statement figures and value are diagnostics. '+'; '.join(case['funding_errors']))
    groups={
      'Income statement':['revenue','cost_of_sales','gross_profit','sga','other_operating_cost','depreciation','operating_lease_expense','operating_income','interest_income','interest_expense','income_tax','net_income'],
      'Balance sheet':['cash','securities','inventory','receivables','ppe','operating_rou','goodwill','other_assets','trade_payables','capex_payables','operating_accruals','unearned','operating_lease','finance_lease','financing_obligation','debt','revolver','other_liabilities','equity'],
      'Cash-flow statement':['net_income','depreciation','change_operating_wc','operating_cash_flow','capex','nonoperating_investment_purchase','securities_sale','investing_cash_flow','debt_net_change','finance_lease_principal','financing_principal','revolver_draw','revolver_repayment','financing_cash_flow','net_cash_change','cash'],
      'Business drivers':['aws_revenue','advertising_revenue','retail_and_other_revenue','revenue'],
      'Investment and lease schedules':['ppe_additions','change_capex_payables','finance_lease_addition','finance_lease_principal','financing_addition','financing_principal','operating_lease_addition','rou_amortization','operating_lease_cash']}
    tabs=st.tabs(list(groups))
    for tab,(name,keys) in zip(tabs,groups.items()):
        with tab:
            f=pd.DataFrame({str(r['year']):{k:r[k] for k in keys} for r in case['rows']})
            show(f,index=True)
    st.caption('AWS/advertising decomposition is illustrative and preserves the consolidated base. Retail and other is residual; it is not a full segment profitability model.')
    st.markdown('### Reported-to-normalized FY2025 bridge');show(pd.read_csv(HERE/'data/normalization.csv'))

elif page=='FCFF & capital':
    t1,t2,t3=st.tabs(['Operating cash flows','WACC & terminal value','Enterprise to equity'])
    with t1:
        st.latex(r'FCFF = EBIT-Tax_{operating}+D\&A-Investment-\Delta NWC')
        show(pd.read_csv(HERE/'outputs/fcff_reconciliation.csv'))
        st.write('Financed asset additions are investment. Capital-payable growth is an investment working-capital credit. Borrowing and reserve liquidation never enter operating FCFF. Negative years remain signed.')
        st.info(base['timing'])
    with t2:
        show(frame([dict(component=k,value=v) for k,v in d['wacc'].items()]))
        show(frame([dict(component=k,value=v) for k,v in base['terminal'].items() if isinstance(v,(float,int))]))
        st.metric('PV terminal / operating EV',f"{base['terminal_dependence']:.1%}")
        st.warning('The terminal schedule moves to constant margin/capital-turnover ratios. Its investment reduction is a material hypothesis, not established guidance. See the terminal challenge and alternatives.')
    with t3:
        show(pd.read_csv(HERE/'outputs/enterprise_equity_bridge.csv'))
        st.write(base['basis']);st.metric('Diluted valuation shares · millions',f"{base['diluted_shares']:,.6f}")
        st.caption('Operating lease liability excluded from debt deduction because rental economics remain in EBIT/FCFF. Strategic investments are excluded from this core subtotal and added separately below.')
        show(frame(d['strategic_investments']['cases']))
        show(frame(d['convention_alternatives']))

elif page=='Scenarios & funding':
    scenarios=pd.read_csv(HERE/'outputs/scenarios.csv');show(scenarios)
    selected=st.selectbox('Trace a case',[x['case'] for x in d['cases']]);case=next(x for x in d['cases'] if x['case']==selected)
    f=frame([dict(year=r['year'],cash_USDbn=r['cash']/1000,securities_USDbn=r['securities']/1000,revolver_USDbn=r['revolver']/1000,FCFF_USDbn=r['fcff']/1000) for r in case['rows']])
    lines(f)
    if case['funding_feasible']:st.success('Funding checks pass under the stated financing assumptions. This does not establish self-funding or future market access.')
    else:st.error('Funding fails: '+'; '.join(case['funding_errors'])+'. Valuation remains diagnostic only.')
    show(frame([dict(year=r['year'],EBIT=r['operating_income'],FCFF=r['fcff'],term_issuance=r['debt_net_change'],cash=r['cash'],securities_sales=r['securities_sale']) for r in case['rows']]))
    st.write('The corrected base now fails funding: the committee decision is do not initiate at the dated price. Reopen only with documented funding, supported investment returns, and a complete dated equity bridge. A cash-floor breach is a modeled funding problem, not proof of issuer default.')

elif page=='Sensitivity & reverse DCF':
    st.warning('This grid values the funding-infeasible base and excludes strategic investment value. Cells are core diagnostics, not investable full-company price targets.')
    f=frame(d['sensitivity'])
    heat=f.pivot(index='wacc',columns='g',values='per_share')
    heat.index=[f'WACC {x:.2%}' for x in heat.index];heat.columns=[f'g {x:.1%}' for x in heat.columns]
    st.markdown('### WACC × perpetual-growth sensitivity · USD/share')
    wvals=sorted(f['wacc'].unique());gvals=sorted(f['g'].unique());low=f['per_share'].min();span=max(f['per_share'].max()-low,1)
    svg='<svg viewBox="0 0 850 340" style="width:100%;background:white;border-radius:12px">'
    for j,g in enumerate(gvals):svg+=f'<text x="{280+j*210}" y="35" text-anchor="middle" font-size="15">Growth {g:.1%}</text>'
    for i,w in enumerate(wvals):
        svg+=f'<text x="20" y="{100+i*85}" font-size="15">WACC {w:.2%}</text>'
        for j,g in enumerate(gvals):
            val=float(f[(f['wacc']==w)&(f['g']==g)]['per_share'].iloc[0]);alpha=.15+.65*(val-low)/span
            svg+=f'<rect x="{180+j*210}" y="{55+i*85}" width="195" height="72" rx="7" fill="rgba(38,126,156,{alpha})"/><text x="{278+j*210}" y="{99+i*85}" text-anchor="middle" font-size="22">${val:.2f}</text>'
    st.markdown(svg+'</svg>',unsafe_allow_html=True)
    show(heat,index=True)
    st.caption('Growth changes terminal reinvestment as well as the Gordon denominator. WACC changes discounting; financing cash flows do not become FCFF.')
    st.markdown('### Market-implied operating expectations');r=d['reverse_dcf'];st.write(r['status']);st.json(r)
    st.warning('The wide solver bracket is diagnostic. A solved gross margin is a conditional arithmetic requirement, not an economically plausible forecast or proof of mispricing.')

elif page=='Comparable companies':
    comp=d['comparables'];st.write(comp['status'])
    show(frame([{k:p[k] for k in ['ticker','price','period_end','shares','ev','ebitda','ev_revenue','ev_ebitda','pe','qualification']} for p in comp['peers']]))
    st.markdown('### Implied AMZN values · USD/share');show(frame(comp['implied']))
    show(frame([dict(multiple=k,**v) for k,v in comp['summary'].items()]))
    st.markdown('### Leave-one-out policy check');st.json(comp['leave_one_out'])
    st.info('EV multiples use a debt/cash/lease bridge. P/E directly values equity. Fiscal periods and investment gains differ; do not average these outputs with DCF without a supported policy.')

else:
    st.markdown('### Material assumptions and sources');show(pd.read_csv(HERE/'data/assumptions.csv'))
    summary=HERE/'evidence/validation_summary.json'
    if summary.exists():st.json(json.loads(summary.read_text()))
    st.markdown('### Limitations and unresolved evidence')
    for text in d['limitations']:st.write('• '+text)
    st.markdown('### Historical and course provenance')
    st.write('Original September1 Edition A is preserved byte-for-byte. October19 question is a later development. No checkpoint receipt or AI-free authorship is asserted. The user supplied Dr. Z’s October19 direction to preserve originals and continue; separate early-AI recovery clarification is recorded.')
    st.download_button('Download saved analysis JSON',path.read_bytes(),'amzn-project1-valuation.json','application/json')
    st.download_button('Download statement CSV',(HERE/'outputs/statements.csv').read_bytes(),'amzn-statements.csv','text/csv')
st.caption('FIN 43900 · Educational analysis · AI-assisted, student review required · Amounts USD millions unless otherwise stated')
