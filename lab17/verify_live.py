"""Reproduce live checks, retaining raw official responses and request metadata."""
from datetime import date, datetime, timezone
from pathlib import Path
import json
import requests
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from asof_app import download_current, download_vintage, compare, latest

ROOT = Path(__file__).resolve().parent


def main():
    evidence = ROOT / 'evidence'
    evidence.mkdir(exist_ok=True)
    report = {'retrieved_at_utc': datetime.now(timezone.utc).isoformat(),
              'local_download_date': date.today().isoformat(), 'known': [], 'errors': []}
    def fetch(sid, cutoff=None):
        data = download_current(sid) if cutoff is None else download_vintage(sid, cutoff)
        label = 'current' if cutoff is None else cutoff.isoformat()
        (evidence / f'{sid}_{label}.csv').write_text(data.attrs['raw_csv'], encoding='utf-8')
        return data
    for sid, obs, value in [('BAA', '2026-09-01', 6.47),
                            ('FEDFUNDS', '2026-09-01', 3.75),
                            ('DGS10', '2026-10-02', 5.28),
                            ('MORTGAGE30US', '2026-10-01', 7.28)]:
        try:
            historical = fetch(sid, date(2026, 10, 5))
            current = fetch(sid)
            result = compare(current, historical)
            result.update(series=sid, cutoff='2026-10-05', expected_date=obs,
                          expected_value=value, url=historical.attrs['url'],
                          passed=latest(historical) == (obs, value))
            report['known'].append(result)
        except Exception as exc:
            report['errors'].append(f'{sid}: {exc}')
    try:
        old = fetch('PAYEMS', date(2025, 1, 15))
        now = fetch('PAYEMS')
        current_dec = float(now.loc['2024-12-01', 'value'])
        old_dec = float(old.loc['2024-12-01', 'value'])
        report['payems'] = dict(compare(now, old), december_historical=old_dec,
                                december_current=current_dec, difference=current_dec-old_dec,
                                url=old.attrs['url'],
                                passed=latest(old) == ('2024-12-01', 159536.0) and
                                current_dec < old_dec and compare(now, old)['revised'] > 0)
    except Exception as exc:
        report['errors'].append(f'PAYEMS: {exc}')
    try:
        old = fetch('BAA', date(2026, 9, 30))
        now = fetch('BAA')
        report['baa'] = dict(compare(now, old), url=old.attrs['url'],
                             current_url=now.attrs['url'],
                             current_missing=int(now.value.isna().sum()),
                             historical_missing=int(old.value.isna().sum()),
                             three_values=[{'date': d.date().isoformat(), 'value': float(v)}
                                           for d, v in now.value.tail(3).items()])
        # Bracket availability; this does not establish an exact publication date.
        report['baa_availability_probes'] = []
        for cutoff in [date(2026, 10, 1), date(2026, 10, 2)]:
            data = fetch('BAA', cutoff)
            report['baa_availability_probes'].append(dict(cutoff=cutoff.isoformat(),
                                                         latest=latest(data), url=data.attrs['url']))
        for sid in ['BAA', 'FEDFUNDS', 'DGS10', 'MORTGAGE30US', 'PAYEMS']:
            url = f'https://fred.stlouisfed.org/series/{sid}'
            response = requests.get(url, timeout=45)
            response.raise_for_status()
            (evidence / f'{sid}_page.html').write_text(response.text, encoding='utf-8')
        response = requests.get('https://fred.stlouisfed.org/data/BAA.txt', timeout=45)
        response.raise_for_status()
        (evidence / 'BAA_official_table.txt').write_text(response.text, encoding='utf-8')
        report['baa_table_url'] = response.url
    except Exception as exc:
        report['errors'].append(f'BAA/metadata: {exc}')
    (evidence / 'live_results.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
