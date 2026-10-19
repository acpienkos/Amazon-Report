"""Execute every dashboard page using Streamlit's real AppTest runtime."""
import sys,json,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE));sys.dont_write_bytecode=True
from streamlit.testing.v1 import AppTest
at=AppTest.from_file(str(HERE/'app.py'),default_timeout=60).run()
assert not at.exception,at.exception
pages=['Decision','Financial statements','FCFF & capital','Scenarios & funding','Sensitivity & reverse DCF','Comparable companies','Sources & validation']
results=[]
for page in pages:
    at.sidebar.radio[0].set_value(page).run()
    assert not at.exception,(page,at.exception)
    results.append(dict(page=page,status='PASS'))
(HERE/'evidence/app_test.json').write_text(json.dumps(dict(command='python -B project1/test_app.py',pages=results,passed=len(results),failed=0),indent=2),encoding='utf-8')
print(f'All {len(results)} dashboard pages executed successfully under Streamlit AppTest.')
