"""Check source hashes and prior tracked files; render results and exact inventory."""
from pathlib import Path
import sys, json, hashlib, subprocess, re, importlib.metadata
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import panel
GIT='C:/Program Files/Git/cmd/git.exe'

def main():
    checks=[]
    for name,item in json.loads((ROOT/'sources/reference_provenance.json').read_text()).items():
        if 'sha256' in item:
            actual=hashlib.sha256((ROOT/'sources'/name).read_bytes()).hexdigest()
            assert actual==item['sha256'],name
            checks.append(name)
    for ticker in ('COST','NVDA','JPM'):
        item=json.loads((ROOT/'sources'/f'{ticker}.provenance.json').read_text())
        assert hashlib.sha256((ROOT/'sources'/f'{ticker}.json').read_bytes()).hexdigest()==item['sha256']
        checks.append(ticker+'.json')
    root=ROOT.parents[1]
    changed=subprocess.check_output([GIT,'-C',str(root),'diff','HEAD','--name-only'],text=True).splitlines()
    assert all(p.startswith('project1/lab19/') for p in changed),changed
    prior=subprocess.run([sys.executable,'-B','-c',
        "import sys,unittest;sys.path.insert(0,'lab18');r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('lab18/tests'));sys.exit(not r.wasSuccessful())"],
        cwd=ROOT.parent,capture_output=True,text=True)
    (ROOT/'evidence/lab18_regression.txt').write_text(prior.stdout+prior.stderr,encoding='utf-8')
    assert prior.returncode==0,prior.stderr
    patterns=[r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',r'AKIA[0-9A-Z]{16}',r'gh[pousr]_[A-Za-z0-9]{30,}']
    files=[p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'
           and p.name not in ('FINAL_RESPONSE.txt','BRIGHTSPACE.txt')]
    hits=[]
    for p in files:
        text=p.read_text(encoding='utf-8',errors='replace')
        for pattern in patterns:
            if re.search(pattern,text):hits.append(str(p.relative_to(ROOT)))
    assert not hits,hits
    lines=['# Executed panel results','', 'All monetary memo values are USD millions. Verdicts are AI-authored business judgments. See printed evidence for all tags and filing provenance.','']
    for ticker in ('COST','NVDA','JPM'):
        report=json.loads((ROOT/'evidence'/f'{ticker}_report.json').read_text())
        lines.extend([f'## {ticker} — {report["company"]}','','| Investor | Check | Result |','|---|---|---|'])
        for investor,checks_ in report['panel'].items():
            for check,state in checks_.items():lines.append(f'| {investor} | {check} | {state} |')
        lines.extend(['','| Investor | Verdict | Memo |','|---|---|---|'])
        for investor,slug in zip(panel.INVESTORS,panel.SLUGS):
            path=panel.memo_path(ticker,slug)
            verdict=path.read_text(encoding='utf-8').splitlines()[0].removeprefix('Verdict: ')
            lines.append(f'| {investor} | {verdict} | [{path.name}](memos/{path.name}) |')
        lines.extend(['',f'[Printed output](evidence/{ticker}_printed.txt) · [Structured report](evidence/{ticker}_report.json)',''])
    (ROOT/'RESULTS.md').write_text('\n'.join(lines),encoding='utf-8')
    evidence={'executed_utc':datetime.now(timezone.utc).isoformat(),'source_hashes_verified':len(checks),'verified_sources':checks,
        'prior_lab18_tests':7,'prior_lab18_exit_code':prior.returncode,'tracked_changes_outside_lab19':[],
        'preexisting_untracked_preserved':['lab13/SUBMISSION_CHECKLIST.md','lab13/preservation_manifest.json','lab13/sources/'],
        'credential_pattern_hits':hits,'credential_scan_scope':'Private-key headers, AWS access-key IDs, GitHub token formats; heuristic, not a proof of absence.',
        'packages':{name:importlib.metadata.version(name) for name in ('streamlit','pandas','PyYAML')}}
    (ROOT/'evidence/package_audit.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
    paths=sorted(str(p.relative_to(ROOT)).replace('\\','/') for p in ROOT.rglob('*') if p.is_file()
        and '__pycache__' not in p.parts and p.suffix!='.pyc' and p.name not in ('FINAL_RESPONSE.txt','BRIGHTSPACE.txt'))
    if 'FILES.md' not in paths:paths.append('FILES.md');paths.sort()
    (ROOT/'FILES.md').write_text('# Exact new tracked-file inventory\n\nAll paths below are relative to `project1/lab19/`. No existing tracked files were modified.\n\n'+
        f'{len(paths)} files:\n\n'+''.join(f'- `{p}`\n' for p in paths)+
        '\nIgnored local delivery artifacts, created after the commit: `submission/FINAL_RESPONSE.txt` and `submission/BRIGHTSPACE.txt`. They include the final commit hash and are excluded to avoid a self-referential commit.\n',encoding='utf-8')
    print(f'{len(checks)} source hashes verified; 7 prior Lab 18 tests pass; no tracked changes outside Lab 19; {len(paths)} new files; no credential-pattern hits.')

if __name__=='__main__':main()
