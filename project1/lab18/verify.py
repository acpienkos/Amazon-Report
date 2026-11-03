"""Run verification and persist its actual result, propagating test failures."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import sys
import unittest
from datetime import datetime, timezone

ROOT = Path(__file__).parent
suite = unittest.defaultTestLoader.discover(str(ROOT / 'tests'))
stream = io.StringIO()
with contextlib.redirect_stderr(stream):
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
text = stream.getvalue()
(ROOT / 'evidence/tests.txt').write_text(text, encoding='utf-8')
summary = {'executed_utc': datetime.now(timezone.utc).isoformat(), 'tests_run': result.testsRun,
           'failures': len(result.failures), 'errors': len(result.errors), 'successful': result.wasSuccessful(),
           'source_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT / 'sources').iterdir() if p.is_file()}}
(ROOT / 'evidence/verification.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
print(text)
sys.exit(0 if result.wasSuccessful() else 1)
