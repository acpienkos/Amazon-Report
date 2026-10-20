"""Verify that evidence tampering is rejected using memory-only substitutions."""
import sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import copy
import json
import unittest
from unittest.mock import patch
import exercise_audit as audit


class EvidenceAuditTests(unittest.TestCase):
    def test_preserved_evidence_passes(self):
        checks = audit.verify()
        self.assertTrue(all(c['passed'] for c in checks), checks)

    def reject_modified_json(self, filename, mutate, expected_check):
        original_read = Path.read_text
        target = audit.HERE / 'evidence/student-only' / filename
        data = json.loads(original_read(target, encoding='utf-8-sig'))
        changed = copy.deepcopy(data)
        mutate(changed)
        def read(path, *args, **kwargs):
            return json.dumps(changed) if path == target else original_read(path, *args, **kwargs)
        with patch.object(Path, 'read_text', read):
            checks = audit.verify()
        self.assertTrue(any(c['check'] == expected_check and not c['passed'] for c in checks), checks)

    def test_wrong_commit_rejected(self):
        self.reject_modified_json('changed-result.json',
            lambda d: d.update(repository_commit='0' * 40),
            'Both runs and receipt identify the frozen commit')

    def test_false_restore_rejected(self):
        self.reject_modified_json('restore-result.json',
            lambda d: d.update(restored_exact_match=False),
            'Restoration is an exact baseline match')

    def test_missing_source_hash_rejected(self):
        self.reject_modified_json('changed-result.json',
            lambda d: d['source_hashes'].pop('project1/model.py'),
            'Recorded source inventory is complete')

    def test_altered_changed_output_rejected(self):
        self.reject_modified_json('changed-result.json',
            lambda d: d['after']['valuation'].update(per_share=999),
            'Saved changed result reproduces with in-memory override')

    def test_bad_source_hash_rejected(self):
        self.reject_modified_json('changed-result.json',
            lambda d: d['source_hashes'].update({'project1/model.py': '0' * 64}),
            'Frozen content and recorded hash: project1/model.py')


if __name__ == '__main__':
    unittest.main(verbosity=2)
