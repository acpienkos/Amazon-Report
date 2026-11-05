from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import json
import pandas as pd
import streamlit as st
import panel

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title='Legend Panel', layout='wide')
st.title('Legend Panel — Buffett, Cathie Wood and Burry')
st.caption('Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.')
ticker = st.text_input('Ticker', 'COST').strip().upper()
offline = st.checkbox('Use saved SEC snapshot (offline)', value=True)
agent = st.text_input('SEC User-Agent (name and email)', panel.sec.DEFAULT_AGENT)
threshold = st.selectbox('Cathie Wood revenue growth threshold', [.15, .05], format_func=lambda x: f'{x:.0%}')

@st.cache_data(ttl=3600)
def load(ticker, offline, agent):
    return json.loads((ROOT/'sources'/f'{ticker}.json').read_text()) if offline else panel.sec.fetch(ticker, ROOT/'sources', agent)

try:
    if not panel.sec.re.fullmatch(r'[A-Z0-9.-]+', ticker):
        raise ValueError('Invalid ticker')
    report = panel.analyze(load(ticker, offline, agent), ticker, threshold)
except (OSError, ValueError, StopIteration) as e:
    st.error(f'Unable to load SEC facts: {e}')
    st.stop()
st.subheader(report['company'])
st.caption('Saved SEC snapshot' if offline else 'Live SEC download, cached for one hour')
chart = pd.DataFrame([{'Fiscal year end': r['fiscal_year_end'], 'Owner earnings': r['owner_earnings']['value'],
    'Net income': r['net_income']['value']} for r in report['rows']]).set_index('Fiscal year end')
st.line_chart(chart/1_000_000, y_label='USD millions')
table = []
for row in report['rows']:
    item = {'Fiscal year end': row['fiscal_year_end']}
    for key, value in row.items():
        if key != 'fiscal_year_end':
            item[key] = panel.display(key, value)
            item[key+' source'] = value['tag']
    table.append(item)
st.caption('USD millions; ROE and R&D/revenue in percent; liabilities/equity as a ratio. Gaps remain gaps.')
st.dataframe(pd.DataFrame(table), hide_index=True)
st.table(pd.DataFrame([{'Investor': investor, 'Check': check, 'Result': state}
    for investor, checks in report['panel'].items() for check,state in checks.items()]))
st.write('Revenue growth a year: ' + ('not known' if report['growth'] is None else f"{report['growth']:.2%}"))
if threshold != .15:
    st.warning('Threshold probe: the saved memos describe the retained 15% baseline. Review the changed check separately.')
with st.expander('Script output and filing provenance'):
    st.code(panel.render(report))
for column, investor, slug in zip(st.columns(3), panel.INVESTORS, panel.SLUGS):
    with column:
        st.subheader(investor)
        path = panel.memo_path(ticker, slug)
        saved = path.read_text(encoding='utf-8') if path.exists() else ''
        memo = st.text_area('AI-authored memo — edit to probe numbers', saved, height=300, key=f'{ticker}_{slug}')
        if not memo:
            st.info('No saved AI memo. Invoke this investor skill, save the memo, then reload or paste it here.')
            continue
        verdict = next((line for line in memo.splitlines() if line.startswith('Verdict:')), 'Verdict: not supplied')
        st.write(verdict)
        st.markdown(memo)
        flags = panel.unsupported_numbers(memo, report)
        if flags:
            st.error('Unsupported numbers: ' + ', '.join(f"{x['number']} (offset {x['offset']})" for x in flags))
        else:
            st.success('Every numeric token matches printed output. Numeric membership does not verify the claim or its units/context.')
        st.download_button('Download memo', memo, file_name=path.name, key='download_'+slug)
