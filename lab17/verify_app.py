"""Live Streamlit AppTest verification; no browser/visual verification claimed."""
from pathlib import Path
from datetime import date
import json
import requests
from streamlit.testing.v1 import AppTest

root = Path(__file__).resolve().parent
result = {'browser_available': False}
response = requests.get('http://localhost:8517/_stcore/health', timeout=15)
response.raise_for_status()
result['server_health'] = response.text
app = AppTest.from_file(str(root / 'asof_app.py'), default_timeout=90).run()
assert not app.exception, str(app.exception)
assert not app.error, [e.value for e in app.error]
assert len(app.dataframe) == 1 and len(app.dataframe[0].value) == 4
result['default_rows'] = len(app.dataframe[0].value)
app.sidebar.date_input[1].set_value(date(2026, 10, 5)).run()
assert not app.exception and not app.error
result['known_answer_table'] = app.dataframe[0].value.to_dict(orient='records')
app.sidebar.text_input[0].set_value('PAYEMS, NO_SUCH_SERIES_XYZ').run()
app.sidebar.date_input[1].set_value(date(2025, 1, 15)).run()
assert not app.exception
assert any('NO_SUCH_SERIES_XYZ' in e.value for e in app.error)
assert len(app.dataframe[0].value) == 5
result['invalid_id_isolated'] = True
result['payems_table'] = app.dataframe[0].value.to_dict(orient='records')
result['exceptions'] = len(app.exception)
(root / 'evidence' / 'app_results.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2))
