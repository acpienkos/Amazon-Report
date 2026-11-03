"""Keyless EDGAR extraction. All monetary calculations use reported USD values."""
import argparse
from datetime import date, datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import time
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[4]
TAGS = {
    'revenue': ('RevenueFromContractWithCustomerExcludingAssessedTax', 'Revenues'),
    'net_income': ('NetIncomeLoss',),
    'operating_cash_flow': ('NetCashProvidedByUsedInOperatingActivities',),
    'capital_spending': ('PaymentsToAcquirePropertyPlantAndEquipment', 'PaymentsToAcquireProductiveAssets'),
    'equity': ('StockholdersEquity',),
    'liabilities': ('Liabilities',),
}
FLOWS = set(TAGS) - {'equity', 'liabilities'}
DEFAULT_AGENT = 'Andrew Pienkos apienkos@purdue.edu FIN43900 learning project'


def download(url, user_agent):
    if '@' not in user_agent or len(user_agent.split()) < 2:
        raise ValueError('SEC User-Agent must contain your name and email')
    for attempt in range(3):
        try:
            time.sleep(0.2)
            req = Request(url, headers={'User-Agent': user_agent, 'Accept-Encoding': 'identity'})
            with urlopen(req, timeout=45) as response:
                return response.read()
        except OSError:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)


def fetch(ticker, directory, user_agent=DEFAULT_AGENT):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    ticker = ticker.upper()
    if not re.fullmatch(r'[A-Z0-9.-]+', ticker):
        raise ValueError('Invalid ticker')
    mapping = download('https://www.sec.gov/files/company_tickers.json', user_agent)
    cik = next((v['cik_str'] for v in json.loads(mapping).values() if v['ticker'] == ticker), None)
    if cik is None:
        raise ValueError(f'Ticker not found: {ticker}')
    url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{int(cik):010d}.json'
    raw = download(url, user_agent)
    (directory / 'company_tickers.json').write_bytes(mapping)
    (directory / f'{ticker}.json').write_bytes(raw)
    (directory / f'{ticker}.provenance.json').write_text(json.dumps({
        'url': url, 'retrieved_utc': datetime.now(timezone.utc).isoformat(),
        'sha256': hashlib.sha256(raw).hexdigest(), 'user_agent': user_agent,
    }, indent=2), encoding='utf-8')
    return json.loads(raw)


def annual(fact):
    """Accept 52/53-week or calendar annual flows, never quarterly/YTD flows."""
    if not fact.get('start'):
        return False
    return 350 <= (date.fromisoformat(fact['end']) - date.fromisoformat(fact['start'])).days <= 380


def candidates(data, tag):
    return [f for f in data.get('facts', {}).get('us-gaap', {}).get(tag, {}).get('units', {}).get('USD', [])
            if f.get('form') == '10-K']


def fiscal_ends(data):
    # Annual flow end dates identify fiscal years; fy labels can refer to the
    # filing year even for comparative facts. Never group by those labels.
    ends = {f['end'] for key in FLOWS for tag in TAGS[key] for f in candidates(data, tag) if annual(f)}
    return sorted(ends)[-5:]


def select(data, key, end):
    for tag in TAGS[key]:
        eligible = [f for f in candidates(data, tag) if f['end'] == end
                    and (annual(f) if key in FLOWS else not f.get('start'))]
        if eligible:
            f = max(eligible, key=lambda x: (x.get('filed', ''), x.get('accn', ''), x.get('start', '')))
            return {'value': f['val'], 'tag': 'us-gaap:' + tag,
                    'filed': f.get('filed'), 'accession': f.get('accn'), 'start': f.get('start')}
    return {'value': None, 'tag': 'not found'}


def year_row(data, end):
    row = {'fiscal_year_end': end}
    row.update({key: select(data, key, end) for key in TAGS})
    ni, equity, ocf, capex, debt = [row[k]['value'] for k in
                                   ('net_income', 'equity', 'operating_cash_flow', 'capital_spending', 'liabilities')]
    row['roe'] = {'value': ni / equity if ni is not None and equity is not None and equity > 0 else None,
                  'tag': f"{row['net_income']['tag']} / {row['equity']['tag']}", 'missing': 'not known'}
    row['owner_earnings'] = {'value': ocf - capex if ocf is not None and capex is not None else None,
                             'tag': f"{row['operating_cash_flow']['tag']} - {row['capital_spending']['tag']}"}
    row['liabilities_to_equity'] = {'value': debt / equity if debt is not None and equity is not None and equity > 0 else None,
                                    'tag': f"{row['liabilities']['tag']} / {row['equity']['tag']}", 'missing': 'not known'}
    return row


def checks(rows):
    def check(values, predicate):
        if len(rows) != 5 or any(v is None for v in values):
            return 'not known'
        return 'pass' if predicate(values) else 'fail'
    roe = [r['roe']['value'] for r in rows]
    oe = [r['owner_earnings']['value'] for r in rows]
    return {'ROE at least 15% every year': check(roe, lambda v: all(x >= .15 for x in v)),
            'Owner earnings positive every year': check(oe, lambda v: all(x > 0 for x in v)),
            'Owner earnings grew first to last': check(oe, lambda v: v[-1] > v[0])}


def analyze(data, ticker):
    rows = [year_row(data, end) for end in fiscal_ends(data)]
    return {'ticker': ticker.upper(), 'company': data.get('entityName'), 'rows': rows, 'checks': checks(rows)}


def display(key, item):
    if item['value'] is None:
        return item.get('missing', 'not found')
    if key == 'roe':
        return f"{item['value'] * 100:.1f}%"
    if key == 'liabilities_to_equity':
        return f"{item['value']:.3f}"
    return f"{item['value'] / 1_000_000:,.0f}"


def render(report):
    lines = [f"{report['ticker']} | {report['company']}", 'Amounts: USD millions; ROE: percent; liabilities/equity: ratio']
    for row in report['rows']:
        lines.append(row['fiscal_year_end'])
        for key, item in row.items():
            if key != 'fiscal_year_end':
                lines.append(f"  {key}: {display(key, item)} [{item['tag']}]"
                             + (f" filed={item['filed']} accession={item['accession']}" if item.get('filed') else ''))
    lines.extend(f'{k}: {v}' for k, v in report['checks'].items())
    return '\n'.join(lines) + '\n'


# Numeric token auditing is conservative and preserves units/precision/sign.
# Dates are single tokens; a year inside a filing accession cannot whitelist a claim.
NUMBER = re.compile(r'(?<![\w])(?:\d{4}-\d{2}-\d{2}|[-+]?\d+(?:,\d{3})*(?:\.\d+)?(?:%|\b))')


def allowed_numbers(report):
    tokens = set()
    for row in report['rows']:
        tokens.add(row['fiscal_year_end'])
        for key, item in row.items():
            if key != 'fiscal_year_end' and item['value'] is not None:
                tokens.update(NUMBER.findall(display(key, item)))
    return tokens


def unsupported_numbers(memo, report):
    allowed = allowed_numbers(report)
    return [{'number': m.group(), 'offset': m.start()} for m in NUMBER.finditer(memo) if m.group() not in allowed]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('ticker')
    p.add_argument('--offline', action='store_true', help='Use explicitly saved SEC snapshot')
    p.add_argument('--data-dir', type=Path, default=ROOT / 'sources')
    p.add_argument('--output-dir', type=Path, default=ROOT / 'evidence')
    p.add_argument('--user-agent', default=os.environ.get('SEC_USER_AGENT', DEFAULT_AGENT))
    a = p.parse_args()
    ticker = a.ticker.upper()
    data = json.loads((a.data_dir / f'{ticker}.json').read_text()) if a.offline else fetch(ticker, a.data_dir, a.user_agent)
    report = analyze(data, ticker)
    a.output_dir.mkdir(parents=True, exist_ok=True)
    (a.output_dir / f'{ticker}_report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    output = render(report)
    (a.output_dir / f'{ticker}_printed.txt').write_text(output, encoding='utf-8')
    print(output)


if __name__ == '__main__':
    main()
