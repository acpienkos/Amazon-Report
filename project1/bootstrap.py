"""Preserve historical evidence and prepare the isolated project workspace."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import hashlib, json, shutil
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ORIGINALS = Path('C:/Users/acpie/Documents/Codex/2026-08-27/x20-i/outputs')

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    for name in ('data','outputs','evidence','tests','docs/historical','submission','sources','tmp/pdfs'):
        (HERE/name).mkdir(parents=True, exist_ok=True)
    manifest = HERE/'evidence/preservation_manifest.json'
    if manifest.exists():
        record = json.loads(manifest.read_text())
        assert all(digest(Path(p)) == h for p,h in record['sha256'].items())
        print('Existing historical manifest verified; not overwritten')
        return
    files = [p for folder in ['lab06','lab07','lab08','lab09','lab10','lab11','lab12','lab13']
             for p in (ROOT/folder).rglob('*') if p.is_file()]
    files += [ROOT/'dcf.py', ROOT/'Amazon_2026-09-03_report.md']
    files += [ORIGINALS/n for n in ('amazon-edition-a.md','amazon-edition-a-completed.md','lab-03-checkout-draft.md')]
    record = {'recorded_at_utc':datetime.now(timezone.utc).isoformat(),
              'sha256':{str(p):digest(p) for p in sorted(files)},
              'note':'Actual execution timestamp; not a historical authorship or submission timestamp.'}
    manifest.write_text(json.dumps(record,indent=2),encoding='utf-8')
    for n in ('amazon-edition-a.md','amazon-edition-a-completed.md','lab-03-checkout-draft.md'):
        shutil.copyfile(ORIGINALS/n, HERE/'docs/historical'/n)
        assert digest(ORIGINALS/n)==digest(HERE/'docs/historical'/n)
    shutil.copyfile(ROOT/'lab10/amazon_history.csv', HERE/'data/historical_reported.csv')
    shutil.copyfile(ROOT/'lab10/amazon_assumptions.csv', HERE/'data/legacy_assumptions.csv')
    print(f'Preserved {len(files)} historical files; original Edition A copied byte-for-byte.')

if __name__=='__main__': main()
