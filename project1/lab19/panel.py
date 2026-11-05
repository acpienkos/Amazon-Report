"""Deterministic shared-fact panel. AI judgments are saved separately as Markdown."""
import argparse
import json
import math
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from engine import sec

ROOT = Path(__file__).resolve().parent
INVESTORS = ('Buffett', 'Cathie Wood', 'Burry')
SLUGS = ('buffett', 'cathie-wood', 'burry')

def result(value, predicate):
    return 'not known' if value is None else ('pass' if predicate(value) else 'fail')

def cathie_checks(rows, growth, threshold):
    """Missing inputs never pass; the R&D test only needs the latest year."""
    rd = rows[-1]['rd_to_revenue']['value'] if rows else None
    return {f'Revenue growth at least {threshold:.0%} a year': result(growth, lambda x: x >= threshold),
            'Latest R&D at least 5% of revenue': result(rd, lambda x: x >= .05)}

def analyze(data, ticker, threshold=.15):
    if not math.isfinite(threshold) or threshold < 0:
        raise ValueError('Growth threshold must be finite and nonnegative')
    report = sec.analyze(data, ticker)
    rows = report['rows']
    for row in rows:
        rd, revenue = (row[k]['value'] for k in ('research_and_development', 'revenue'))
        row['rd_to_revenue'] = {'value': rd / revenue if rd is not None and revenue is not None and revenue > 0 else None,
            'tag': f"{row['research_and_development']['tag']} / {row['revenue']['tag']}"}
    revenues = [r['revenue']['value'] for r in rows]
    growth = None
    if len(rows) == 5 and all(v is not None and v > 0 for v in revenues):
        # Require five consecutive fiscal-year observations, not five arbitrary dates.
        dates = [sec.date.fromisoformat(r['fiscal_year_end']) for r in rows]
        if all(350 <= (b-a).days <= 380 for a,b in zip(dates, dates[1:])):
            growth = (revenues[-1] / revenues[0]) ** .25 - 1
    ocf = [r['operating_cash_flow']['value'] for r in rows]
    income = [r['net_income']['value'] for r in rows]
    cash_test = None if len(rows) != 5 or any(v is None for v in ocf + income) else all(a >= b for a,b in zip(ocf, income))
    leverage = rows[-1]['liabilities_to_equity']['value'] if rows else None
    report.update(growth=growth, growth_threshold=threshold, panel={
        'Buffett': report['checks'],
        'Cathie Wood': cathie_checks(rows, growth, threshold),
        'Burry': {'Operating cash flow at least net income every year': result(cash_test, bool),
                  'Latest liabilities no more than twice equity': result(leverage, lambda x: x <= 2)},
    })
    return report

def display(key, item):
    if key == 'rd_to_revenue':
        return 'not found' if item['value'] is None else f"{item['value']:.2%}"
    if key == 'liabilities_to_equity':
        return item.get('missing', 'not known') if item['value'] is None else f"{item['value']:.2f}"
    return sec.display(key, item)

def render(report):
    lines = [f"{report['ticker']} | {report['company']}", 'Amounts: USD millions; ROE and R&D/revenue: percent; liabilities/equity: ratio']
    for row in report['rows']:
        lines.append(row['fiscal_year_end'])
        for key, item in row.items():
            if key != 'fiscal_year_end':
                lines.append(f"  {key}: {display(key, item)} [{item['tag']}]" +
                    (f" filed={item['filed']} accession={item['accession']}" if item.get('filed') else ''))
    lines.append('Revenue growth a year: ' + ('not known' if report['growth'] is None else f"{report['growth']:.2%}"))
    lines.append(f"Growth threshold: {report['growth_threshold']:.0%}")
    lines.append('R&D threshold: 5%')
    for investor, checks in report['panel'].items():
        lines.extend(f'{investor} | {check} | {state}' for check,state in checks.items())
    return '\n'.join(lines) + '\n'

def unsupported_numbers(memo, report):
    allowed = set()
    for row in report['rows']:
        allowed.add(row['fiscal_year_end'])
        for key, item in row.items():
            if key != 'fiscal_year_end' and item['value'] is not None:
                allowed.update(sec.NUMBER.findall(display(key, item)))
    if report['growth'] is not None:
        allowed.add(f"{report['growth']:.2%}")
    allowed.update((f"{report['growth_threshold']:.0%}", '5%'))
    return [{'number': m.group(), 'offset': m.start()} for m in sec.NUMBER.finditer(memo) if m.group() not in allowed]

def memo_path(ticker, slug):
    return ROOT / 'memos' / f'{ticker}_{slug}.md'

def main(investor=None, default_threshold=.15):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('ticker')
    parser.add_argument('--offline', action='store_true')
    parser.add_argument('--growth-threshold', type=float, default=default_threshold)
    parser.add_argument('--user-agent', default=sec.os.environ.get('SEC_USER_AGENT', sec.DEFAULT_AGENT))
    args = parser.parse_args()
    ticker = args.ticker.upper()
    if not sec.re.fullmatch(r'[A-Z0-9.-]+', ticker):
        parser.error('Invalid ticker')
    data = json.loads((ROOT/'sources'/f'{ticker}.json').read_text()) if args.offline else sec.fetch(ticker, ROOT/'sources', args.user_agent)
    report = analyze(data, ticker, args.growth_threshold)
    output = render(report)
    suffix = '' if args.growth_threshold == .15 else '_probe'
    (ROOT/'evidence'/f'{ticker}{suffix}_report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    (ROOT/'evidence'/f'{ticker}{suffix}_printed.txt').write_text(output, encoding='utf-8')
    print(output)
    if investor:
        print('Memo task:', investor, '— read the printed facts, apply SKILL.md, save an AI-authored memo. No scripted verdict.')

if __name__ == '__main__':
    main()
