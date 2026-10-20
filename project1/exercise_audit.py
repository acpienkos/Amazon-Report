"""Read-only verification of student evidence; never executes its assessed runner."""
import hashlib
import json
import subprocess
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
FROZEN_COMMIT = '99b99d0141f9a52510d71494943864c8cf4b6f71'
SOURCE_FILES = [
    'project1/model.py', 'project1/statements.py', 'project1/config.py',
    'project1/student_exercise.py', 'project1/data/legacy_assumptions.csv',
    'lab10/amazon_proforma.py', 'lab10/amazon_assumptions.csv',
    'project1/data/student-change.json', 'project1/evidence/student-only/prediction.md',
]


def verify():
    checks = []
    def check(name, passed, detail=''):
        checks.append(dict(check=name, passed=bool(passed), detail=detail))
    try:
        folder = HERE / 'evidence/student-only'
        names = ['prediction.md', 'commit-receipt.md', 'changed-result.json',
                 'restore-result.json', 'reconciliation.md']
        check('Five student evidence files exist and are nonempty',
              all((folder / n).is_file() and (folder / n).stat().st_size for n in names))
        changed = json.loads((folder / 'changed-result.json').read_text(encoding='utf-8-sig'))
        restored = json.loads((folder / 'restore-result.json').read_text(encoding='utf-8-sig'))
        plan = json.loads((HERE / 'data/student-change.json').read_text(encoding='utf-8-sig'))
        check('Both runs and receipt identify the frozen commit',
              changed['repository_commit'] == restored['repository_commit'] == FROZEN_COMMIT
              and FROZEN_COMMIT in (folder / 'commit-receipt.md').read_text(encoding='utf-8-sig'))
        def git(*args):
            return subprocess.check_output(
                ['C:/Program Files/Git/cmd/git.exe', '-c',
                 'safe.directory=' + HERE.parent.as_posix(), *args], cwd=HERE.parent)
        committed_at = datetime.fromisoformat(git('show', '-s', '--format=%cI', FROZEN_COMMIT).decode().strip())
        check('Freeze precedes changed run and restore check',
              committed_at < datetime.fromisoformat(changed['executed_at_utc'])
              < datetime.fromisoformat(restored['executed_at_utc']))
        check('Recorded source inventory is complete',
              set(changed['source_hashes']) == set(restored['source_hashes']) == set(SOURCE_FILES))
        for name in SOURCE_FILES:
            actual = (HERE.parent / name).read_bytes()
            frozen = git('show', FROZEN_COMMIT + ':' + name)
            check('Frozen content and recorded hash: ' + name,
                  actual.replace(b'\r\n', b'\n') == frozen.replace(b'\r\n', b'\n')
                  and hashlib.sha256(actual).hexdigest() == changed['source_hashes'][name]
                  == restored['source_hashes'][name],
                  'Commit content normalized for LF/CRLF; recorded working-file hashes compared byte-for-byte.')
        check('Input and execution modes match preserved plan',
              changed['input'] == restored['input'] == plan
              and changed['mode'] == 'changed' and restored['mode'] == 'restore-check')
        check('Restoration is an exact baseline match',
              restored['restored_exact_match'] is True
              and changed['before'] == restored['before'] == restored['restored'])
        import model
        check('Saved baseline reproduces without assessed runner', changed['before'] == model.evaluate())
        check('Saved changed result reproduces with in-memory override',
              changed['after'] == model.evaluate(override={plan['input']: plan['new']}))
        check('Baseline saved output matches restored model',
              json.loads((HERE / 'outputs/valuation.json').read_text())['base'] == changed['before'])
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as exc:
        check('Student evidence verification completed', False, str(exc))
    return checks
