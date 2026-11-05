"""Freeze public instructions, philosophy and holdings with retrieval provenance."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, urllib.request, time

ROOT = Path(__file__).resolve().parent
BASE = 'https://raw.githubusercontent.com/CinderZhang/FIN43900-Fall2026/main/'
URLS = {p: BASE + 'lessons/week-11/' + p for p in [
    'README.md', 'student-prework.md', 'student-handout.md',
    'lab-18-legend-investor-as-skill.md', 'lab-19-legend-panel.md',
    'slides-session-19.md', 'open-ended-challenge.md']}
URLS['FAskills-README.md'] = 'https://raw.githubusercontent.com/CinderZhang/FAskills/main/README.md'
for p in ['warren_buffett.md', 'cathie_wood.md', 'michael_burry.md']:
    URLS[p] = 'https://raw.githubusercontent.com/CinderZhang/FAskills/main/financial-researcher/experts/' + p
URLS['codex-skills.html'] = 'https://developers.openai.com/codex/skills'
URLS['sec-api.html'] = 'https://www.sec.gov/search-filings/edgar-application-programming-interfaces'
URLS['streamlit.html'] = 'https://docs.streamlit.io/'
URLS['VT-vanguard.html'] = 'https://advisors.vanguard.com/investments/products/vt/vanguard-total-world-stock-etf'
URLS['VT-schwab-holdings.html'] = 'https://www.schwab.wallst.com/Prospect/Research/etfs/portfolio.asp?symbol=vt'

def main():
    target = ROOT / 'sources'
    target.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for name, url in URLS.items():
        try:
            request = urllib.request.Request(url, headers={'User-Agent': 'Andrew Pienkos apienkos@purdue.edu FIN43900 learning project'})
            with urllib.request.urlopen(request, timeout=40) as response:
                raw = response.read()
            (target / name).write_bytes(raw)
            manifest[name] = {'url': url, 'retrieved_utc': datetime.now(timezone.utc).isoformat(), 'sha256': hashlib.sha256(raw).hexdigest()}
            print(name, len(raw), flush=True)
        except Exception as e:
            manifest[name] = {'url': url, 'error': str(e)}
            print(name, str(e), flush=True)
        time.sleep(.2)
    (target / 'reference_provenance.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')

if __name__ == '__main__':
    main()
