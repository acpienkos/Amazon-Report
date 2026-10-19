"""Actual AI-executed README-command run in the separately provisioned fresh runtime."""
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE));sys.dont_write_bytecode=True
import subprocess,time,json,urllib.request,argparse
from datetime import datetime,timezone
parser=argparse.ArgumentParser();parser.add_argument('--runtime',default='.cold-runtime',choices=['.cold-runtime','.review-runtime']);args=parser.parse_args()
python=HERE/args.runtime/'python.exe'
commands=[[str(python),'-B','project1/analysis.py'],[str(python),'-B','project1/tests/test_project.py'],[str(python),'-B','project1/test_app.py']]
record={'started_at_utc':datetime.now(timezone.utc).isoformat(),'environment':'Isolated official Python3.13.7 embedded archive; project1/requirements.txt installed separately in '+args.runtime+'; no copied site-packages. Installation log records initial setup; reruns reuse only that pinned environment.',
        'operator':'Codex; technical cold run, not a claimed independent human observation','commands':[],'first_failure':None,'status':'RUNNING'}
start=time.monotonic()
for cmd in commands:
    t=time.monotonic();p=subprocess.run(cmd,cwd=HERE.parent,capture_output=True,text=True,encoding='utf-8',errors='replace')
    record['commands'].append(dict(command=cmd,exit_code=p.returncode,seconds=time.monotonic()-t,stdout=p.stdout,stderr=p.stderr))
    if p.returncode and record['first_failure'] is None:record['first_failure']=dict(command=cmd,error=p.stderr or p.stdout)
server_command=[str(python),'-m','streamlit','run','project1/app.py','--server.address','127.0.0.1','--server.port','8502','--server.headless','true','--browser.gatherUsageStats','false']
with (HERE/'evidence/cold-server.log').open('w',encoding='utf-8') as log:
    server=subprocess.Popen(server_command,cwd=HERE.parent,stdout=log,stderr=subprocess.STDOUT)
    try:
        health=None
        for i in range(35):
            try:
                with urllib.request.urlopen('http://127.0.0.1:8502/_stcore/health',timeout=2) as response:health=response.read().decode()
                if health=='ok':break
            except Exception:pass
            time.sleep(.3)
        record['server']=dict(command=server_command,health=health,status='PASS' if health=='ok' else 'FAIL')
        if health!='ok' and record['first_failure'] is None:record['first_failure']='Server did not return ok'
    finally:
        server.terminate();server.wait(timeout=20)
record.update(status='PASS' if record['first_failure'] is None else 'FAIL',elapsed_seconds=time.monotonic()-start,finished_at_utc=datetime.now(timezone.utc).isoformat())
(HERE/'evidence/cold_run.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
text='# README-only technical cold run\n\n'+record['status']+'; operator: Codex, not independent student/partner evidence.\n\nEnvironment: '+record['environment']+'\n\nStarted '+record['started_at_utc']+'; finished '+record['finished_at_utc']+f"; elapsed {record['elapsed_seconds']:.2f}s.\n\nFirst failure in this fresh run: "+str(record['first_failure'])+'\n\n'
for r in record['commands']:text+='Command: '+' '.join(r['command'])+f"\n\nExit {r['exit_code']}; {r['seconds']:.2f}s\n\n"+r['stdout']+'\n\n'+r['stderr']+'\n\n'
text+='Server: '+str(record['server'])+'\n\nInitial development failure, before this fresh run: native PyArrow DLL blocked by Windows Application Control. Changed dashboard to HTML/SVG rendering inside Streamlit; no Windows security configuration was changed. AppTest then passed all seven pages. See environment_failures.md. A real independently observed human cold run remains pending if required by the brief.'
(HERE/'evidence/cold_run.md').write_text(text,encoding='utf-8')
print(record['status'],f"{record['elapsed_seconds']:.2f}s",record['server'])
raise SystemExit(0 if record['status']=='PASS' else 1)
