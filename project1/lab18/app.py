from pathlib import Path
import json
import pandas as pd
import streamlit as st
from engine import sec

ROOT = Path(__file__).parent
st.set_page_config(page_title='Buffett business screen', layout='wide')
st.title('Buffett business screen')
st.caption('Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.')
ticker = st.text_input('Ticker', 'COST').strip().upper()
offline = st.checkbox('Use saved SEC snapshot (offline)', value=True)
agent = st.text_input('SEC User-Agent (name and email)', sec.DEFAULT_AGENT)

@st.cache_data(ttl=3600)
def load(ticker, offline, agent):
    if offline:
        return json.loads((ROOT / 'sources' / f'{ticker}.json').read_text())
    return sec.fetch(ticker, ROOT / 'sources', agent)

try:
    if not __import__('re').fullmatch(r'[A-Z0-9.-]+', ticker):
        raise ValueError('Enter a valid ticker')
    report = sec.analyze(load(ticker, offline, agent), ticker)
except (OSError, ValueError, StopIteration) as e:
    st.error(f'Unable to load SEC facts: {e}')
    st.stop()
st.caption('Saved snapshot' if offline else 'Live SEC download (cached for one hour)')
st.subheader(report['company'])
chart = pd.DataFrame([{'Fiscal year end': r['fiscal_year_end'],
                      'Owner earnings': r['owner_earnings']['value'],
                      'Net income': r['net_income']['value']} for r in report['rows']]).set_index('Fiscal year end')
st.line_chart(chart / 1_000_000, y_label='USD millions')
table = []
for row in report['rows']:
    item = {'Fiscal year end': row['fiscal_year_end']}
    for key, value in row.items():
        if key != 'fiscal_year_end':
            item[key] = sec.display(key, value)
            item[key + ' source'] = value['tag']
    table.append(item)
st.caption('USD millions; ROE in percent; liabilities/equity as a ratio. Missing values are never zero-filled.')
st.dataframe(pd.DataFrame(table), hide_index=True)
st.table(pd.DataFrame(report['checks'].items(), columns=['Check', 'Result']))
printed = sec.render(report)
with st.expander('Script output and filing provenance'):
    st.code(printed)
memo_path = ROOT / 'memos' / f'{ticker}.md'
saved = memo_path.read_text(encoding='utf-8') if memo_path.exists() else ''
memo = st.text_area('AI-authored memo — edit here to probe unsupported numbers', saved, height=230, key='memo_' + ticker)
if memo:
    st.markdown(memo)
    if ticker == 'COST':
        st.caption('I trust the COST verdict as a historical business screen because the inputs are traceable and the checks are reproducible; they do not establish a durable moat or future performance.')
    flags = sec.unsupported_numbers(memo, report)
    if flags:
        st.error('Unsupported numbers: ' + ', '.join(f"{x['number']} (offset {x['offset']})" for x in flags))
    else:
        st.success('Every numeric token matches a printed financial value or fiscal end date. This does not verify the meaning of a claim.')
    st.download_button('Download memo', memo, file_name=f'{ticker}.md')
else:
    st.info('No saved AI memo for this ticker. Use the buffett-edgar skill on the printed output, save the memo, then reload, or paste the memo above.')
