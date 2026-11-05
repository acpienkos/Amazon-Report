"""Persist actual test and packaged skill validation results; fail on any issue."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import contextlib, io, json, hashlib, unittest, subprocess
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent
stream=io.StringIO()
with contextlib.redirect_stderr(stream):
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.discover(str(ROOT/'tests')))
(ROOT/'evidence/tests.txt').write_text(stream.getvalue(),encoding='utf-8')
validator=ROOT/'tools/quick_validate.py'
skills=[]
for directory in sorted((ROOT/'.agents/skills').iterdir()):
    run=subprocess.run([sys.executable,'-B',str(validator),str(directory)],capture_output=True,text=True)
    skills.append({'name':directory.name,'exit_code':run.returncode,'output':run.stdout+run.stderr})
summary={'executed_utc':datetime.now(timezone.utc).isoformat(),'tests_run':result.testsRun,'failures':len(result.failures),
    'errors':len(result.errors),'successful':result.wasSuccessful() and all(s['exit_code']==0 for s in skills),'skills':skills,
    'sha256':{str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest()
        for p in ROOT.rglob('*') if p.is_file() and p.suffix not in ('.pyc',) and 'evidence' not in p.parts}}
(ROOT/'evidence/verification.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(stream.getvalue())
print(json.dumps(skills,indent=2))
sys.exit(0 if summary['successful'] else 1)
