"""Student-operated assessed exercise; never run by Codex.

No prediction is supplied. Actual runs require student-authored, Git-frozen
prediction and input choice. This check cannot certify absence of AI assistance.
"""
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE));sys.dont_write_bytecode=True
import argparse,json,subprocess,hashlib
from datetime import datetime,timezone
import model as m
import analysis

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--run',action='store_true');parser.add_argument('--restore-check',action='store_true');args=parser.parse_args()
    if args.run==args.restore_check:raise ValueError('Choose --run or --restore-check')
    plan=json.loads((HERE/'data/student-change.json').read_text())
    prediction=HERE/'evidence/student-only/prediction.md'
    if not prediction.exists():raise ValueError('Write your independent prediction first; none supplied by AI')
    if not isinstance(plan['new'],(int,float)) or not 0<plan['new']<1 or plan['new']==plan['old']:
        raise ValueError('Student must independently choose a distinct valid ratio')
    if plan['input']!='receivables_ratio' or abs(plan['old']-m.fresh()['receivables_ratio'])>1e-12:raise ValueError('Input/original value mismatch')
    git='C:/Program Files/Git/cmd/git.exe'
    def g(*args):return subprocess.run([git,'-c','safe.directory='+HERE.parent.as_posix(),*args],cwd=HERE.parent,capture_output=True,check=True).stdout
    commit=g('rev-parse','HEAD').decode().strip()
    files=['project1/model.py','project1/statements.py','project1/config.py','project1/student_exercise.py','project1/data/legacy_assumptions.csv','lab10/amazon_proforma.py','lab10/amazon_assumptions.csv','project1/data/student-change.json','project1/evidence/student-only/prediction.md']
    for name in files:
        saved=g('show',commit+':'+name).decode('utf-8').replace('\r\n','\n')
        actual=(HERE.parent/name).read_text(encoding='utf-8').replace('\r\n','\n')
        if saved!=actual:raise ValueError('Model/prediction not identical to committed snapshot: '+name)
    hashes={name:hashlib.sha256((HERE.parent/name).read_bytes()).hexdigest() for name in files}
    analysis.preserve_check()
    before=m.evaluate()
    result=dict(executed_at_utc=datetime.now(timezone.utc).isoformat(),repository_commit=commit,source_hashes=hashes,
                mode='changed' if args.run else 'restore-check',input=plan,before=before,
                authored_prediction_path=str(prediction),authorship_note='Student declaration required; program does not certify AI-off conduct.')
    if args.run:result['after']=m.evaluate(override={plan['input']:plan['new']})
    else:result['restored']=m.evaluate();result['restored_exact_match']=result['restored']==before
    for name,h in hashes.items():
        if hashlib.sha256((HERE.parent/name).read_bytes()).hexdigest()!=h:raise ValueError('Source changed during run')
    out=HERE/'evidence/student-only';out.mkdir(exist_ok=True)
    path=out/('changed-result.json' if args.run else 'restore-result.json')
    with path.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2,allow_nan=False)
    for label,case in [('before',before)]+([('after',result['after'])] if args.run else [('restored',result['restored'])]):
        print(label,'core subtotal',case['valuation']['per_share'],'funding',case['funding_feasible'])
        print([(r['year'],r['receivables'],r['change_operating_wc'],r['fcff'],r['cash']) for r in case['rows']])
    print('Saved actual execution:',path)
if __name__=='__main__':main()
