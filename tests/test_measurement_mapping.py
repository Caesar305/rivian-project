"""Synthetic compatibility cases; no fixture represents a Rivian dimension."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from import_measurements import prepare, save
from review_measurement_mapping import review


class MappingTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / 'evidence.txt').write_text('Synthetic evidence only')
        self.record = {
            'id': 'test-1', 'name': 'Synthetic length', 'classification': 'B',
            'observer': 'Fixture', 'method': 'Synthetic', 'instrument': 'Synthetic',
            'captured_at': '2026-09-10T12:00:00-04:00',
            'vehicle': {'model': 'R1S', 'model_year': 2023, 'owner_vehicle': True},
            'configuration': {key: 'Synthetic state' for key in ('front_seats', 'second_row', 'third_row', 'doors', 'hatch')},
            'quantity': 'distance', 'value': 100, 'unit': 'mm', 'uncertainty': 2,
            'uncertainty_basis': 'Synthetic bound', 'endpoint_from': 'Synthetic A',
            'endpoint_to': 'Synthetic B', 'side': 'driver', 'evidence_paths': ['evidence.txt'],
        }
        parameter = {key: copy.deepcopy(self.record[key]) for key in
                     ('quantity', 'vehicle', 'configuration', 'endpoint_from', 'endpoint_to', 'side')}
        parameter.update(id='synthetic-length', definition='Synthetic test definition')
        self.config = {'schema_version': 1, 'parameters': [parameter],
                       'mappings': [{'parameter_id': 'synthetic-length', 'observation_ref': 'test/test-1'}]}

    def capture(self, records=None):
        path = self.root / 'input.json'
        path.write_text(json.dumps({'schema_version': 1, 'batch_id': 'test', 'observations': records or [self.record]}))
        return save(prepare(path, self.root), self.root)

    def test_compatible_is_review_only_and_files_unchanged(self):
        batch = self.capture()
        before = batch.read_bytes()
        result = review(self.config, self.root)
        self.assertEqual(result['summary']['READY_FOR_REVIEW'], 1)
        self.assertFalse(result['geometry_authorized'])
        self.assertFalse(result['mappings'][0]['geometry_authorized'])
        self.assertEqual(result['mappings'][0]['effective_classification'], 'D')
        self.assertEqual(before, batch.read_bytes())

    def test_incompatible_endpoints_side_and_configuration_are_blocked(self):
        self.capture()
        for key, value in [('endpoint_to', 'Different point'), ('side', 'passenger'),
                           ('configuration', {k: 'Different state' for k in self.record['configuration']})]:
            with self.subTest(key=key):
                config = copy.deepcopy(self.config)
                config['parameters'][0][key] = value
                row = review(config, self.root)['mappings'][0]
                self.assertEqual(row['status'], 'BLOCKED')
                self.assertTrue(any(key in issue for issue in row['issues']))

    def test_repeat_conflict_is_not_averaged(self):
        second = dict(self.record, id='test-2', value=110)
        self.capture([self.record, second])
        self.config['mappings'].append({'parameter_id': 'synthetic-length', 'observation_ref': 'test/test-2'})
        result = review(self.config, self.root)
        self.assertEqual(result['summary']['CONFLICT'], 2)
        self.assertEqual(result['conflicts'][0]['difference_mm'], 10)
        self.assertEqual(result['conflicts'][0]['combined_bound_mm'], 4)
        self.assertEqual([r['value_mm'] for r in result['mappings']], [100, 110])

    def test_touching_uncertainty_bounds_do_not_claim_validation(self):
        self.capture([self.record, dict(self.record, id='test-2', value=104)])
        self.config['mappings'].append({'parameter_id': 'synthetic-length', 'observation_ref': 'test/test-2'})
        result = review(self.config, self.root)
        self.assertEqual(result['summary']['READY_FOR_REVIEW'], 2)
        self.assertFalse(result['geometry_authorized'])

    def test_changed_evidence_and_altered_source_are_detected(self):
        batch = self.capture()
        (self.root / 'evidence.txt').write_text('Changed evidence')
        self.assertEqual(review(self.config, self.root)['summary']['BLOCKED'], 1)
        stored = json.loads(batch.read_text())
        stored['raw_json_text'] += ' '
        batch.write_text(json.dumps(stored))
        issues = review(self.config, self.root)['mappings'][0]['issues']
        self.assertTrue(any('checksum mismatch' in issue for issue in issues))

    def test_missing_unsafe_duplicate_and_empty_proposals(self):
        self.assertEqual(review(self.config, self.root)['summary']['BLOCKED'], 1)
        self.config['mappings'][0]['observation_ref'] = '../outside/test-1'
        self.assertEqual(review(self.config, self.root)['summary']['BLOCKED'], 1)
        self.config['mappings'] *= 2
        with self.assertRaises(ValueError):
            review(self.config, self.root)
        self.config['mappings'] = []
        self.assertEqual(review(self.config, self.root)['unmapped_parameters'], ['synthetic-length'])

    def test_datum_mismatch_blocks_coordinate_mapping(self):
        self.record.update(quantity='y', value=0, datum_id='datum-a')
        self.config['parameters'][0].update(quantity='y', datum_id='datum-b')
        self.capture()
        row = review(self.config, self.root)['mappings'][0]
        self.assertEqual(row['status'], 'BLOCKED')
        self.assertIn('datum_id does not match the parameter definition', row['issues'])


if __name__ == '__main__':
    unittest.main()
