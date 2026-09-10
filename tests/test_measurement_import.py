"""Synthetic intake fixtures only: these are not Rivian measurements."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('intake', Path(__file__).resolve().parents[1] / 'scripts/import_measurements.py')
intake = importlib.util.module_from_spec(spec)
spec.loader.exec_module(intake)


class MeasurementImportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'evidence.txt').write_text('Synthetic evidence for importer testing only.')
        self.record = {
            'id': 'synthetic-driver', 'name': 'Synthetic coordinate, not vehicle data',
            'classification': 'B', 'vehicle': {'model': 'R1S', 'model_year': 2023, 'owner_vehicle': True},
            'observer': 'Test fixture', 'captured_at': '2026-09-10T12:00:00-04:00',
            'method': 'Synthetic', 'instrument': 'Synthetic', 'quantity': 'y',
            'value': -10, 'unit': 'in', 'uncertainty': 0.1,
            'uncertainty_basis': 'Synthetic test bound', 'endpoint_from': 'Synthetic datum',
            'endpoint_to': 'Synthetic point', 'side': 'driver', 'datum_id': 'synthetic-datum',
            'configuration': {k: 'Synthetic state' for k in ('front_seats', 'second_row', 'third_row', 'doors', 'hatch')},
            'evidence_paths': ['evidence.txt'],
        }

    def prepare(self, records=None, batch='synthetic-batch'):
        source = self.root / 'input.json'
        source.write_text(json.dumps({'schema_version': 1, 'batch_id': batch, 'observations': records or [self.record]}))
        return intake.prepare(source, self.root)

    def test_normalization_preserves_sides_and_never_approves(self):
        passenger = copy.deepcopy(self.record)
        passenger.update(id='synthetic-passenger', side='passenger', value=11)
        envelope = self.prepare([self.record, passenger])
        left, right = envelope['observations']
        self.assertEqual(left['value_mm'], -254)
        self.assertAlmostEqual(right['value_mm'], 279.4)
        self.assertAlmostEqual(left['uncertainty_mm'], 2.54)
        for observation in (left, right):
            self.assertTrue(observation['metadata_complete'])
            self.assertFalse(observation['geometry_authorized'])
            self.assertEqual(observation['effective_classification'], 'D')
        self.assertEqual(left['evidence'][0]['sha256'], hashlib.sha256((self.root / 'evidence.txt').read_bytes()).hexdigest())

    def test_missing_data_is_retained_without_zero_substitution(self):
        self.record.update(value=None, uncertainty=None, evidence_paths=['missing.jpg'])
        envelope = self.prepare()
        record = envelope['observations'][0]
        self.assertIsNone(record['value_mm'])
        self.assertIsNone(record['uncertainty_mm'])
        self.assertFalse(record['metadata_complete'])
        target = intake.save(envelope, self.root)
        stored = json.loads(target.read_text())
        self.assertIsNone(json.loads(stored['raw_json_text'])['observations'][0]['value'])

    def test_batch_is_immutable_and_source_text_exact(self):
        envelope = self.prepare()
        target = intake.save(envelope, self.root)
        first = target.read_bytes()
        self.record['value'] = 999
        with self.assertRaises(FileExistsError):
            intake.save(self.prepare(), self.root)
        self.assertEqual(target.read_bytes(), first)
        self.assertEqual(len(list(target.parent.iterdir())), 1)
        self.assertEqual(hashlib.sha256(envelope['raw_json_text'].encode()).hexdigest(), envelope['source_sha256'])

    def test_zero_coordinate_is_valid_but_zero_distance_is_not(self):
        self.record['value'] = 0
        self.assertTrue(self.prepare()['observations'][0]['metadata_complete'])
        self.record['quantity'] = 'distance'
        record = self.prepare()['observations'][0]
        self.assertFalse(record['metadata_complete'])
        self.assertIsNone(record['value_mm'])

    def test_calibration_and_datum_are_required_for_coordinates(self):
        self.record.update(classification='C', datum_id=None)
        issues = self.prepare()['observations'][0]['issues']
        self.assertTrue(any('datum_id' in issue for issue in issues))
        self.assertTrue(any('calibration_id' in issue for issue in issues))

    def test_unsafe_paths_ids_duplicates_and_nonfinite_values(self):
        self.record['evidence_paths'] = ['../outside.jpg']
        self.assertTrue(any('inside the project' in issue for issue in self.prepare()['observations'][0]['issues']))
        with self.assertRaises(ValueError):
            self.prepare(batch='../escape')
        with self.assertRaises(ValueError):
            self.prepare([self.record, self.record])
        source = self.root / 'invalid.json'
        for text in ('{"schema_version":1,"schema_version":1}', '{"value":NaN}', '{"value":Infinity}'):
            source.write_text(text)
            with self.assertRaises(ValueError):
                intake.prepare(source, self.root)

    def test_overflow_cannot_become_geometry(self):
        self.record.update(value=1e308, uncertainty=1e308)
        record = self.prepare()['observations'][0]
        self.assertIsNone(record['value_mm'])
        self.assertIsNone(record['uncertainty_mm'])
        self.assertFalse(record['metadata_complete'])


if __name__ == '__main__':
    unittest.main()
