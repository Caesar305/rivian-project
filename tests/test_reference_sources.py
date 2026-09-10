"""Source binding checks; mutated values are synthetic and never saved."""
import copy
import json
from pathlib import Path
import re
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from reference_sources import ROOT, load, resolve
from build_preview import render


class ReferenceSourceTests(unittest.TestCase):
    def setUp(self):
        reference = load()
        self.database = copy.deepcopy(reference['database'])
        self.config = copy.deepcopy(reference['config'])
        self.template = (ROOT / 'templates/r1s-working-preview.html').read_text()

    def dimension(self, identifier='D056'):
        return next(r for r in self.database['dimensions'] if r['id'] == identifier)

    def test_saved_preview_matches_sources_and_contains_shared_values(self):
        reference = resolve(self.database, self.config)
        result = render(reference, self.template)
        self.assertEqual(result, (ROOT / 'outputs/r1s-working-preview.html').read_text())
        payload = json.loads(re.search(r'const reference=(.*);', result)[1])
        self.assertEqual(payload['dimensions_mm'], reference['dimensions_mm'])
        self.assertEqual(payload['source_fingerprint'], reference['source_fingerprint'])
        self.assertNotIn('@@', result)

    def test_changed_source_value_updates_all_defaults_and_fingerprint(self):
        previous = resolve(self.database, self.config)
        self.dimension().update(value=82, value_mm=2082.8)
        updated = resolve(self.database, self.config)
        result = render(updated, self.template)
        self.assertIn('value="2082.8"', result)
        self.assertIn('<td>2082.80</td><td>82.00</td>', result)
        self.assertNotEqual(updated['source_fingerprint'], previous['source_fingerprint'])

    def test_rejects_missing_nonfinite_negative_and_inconsistent_values(self):
        for value in (None, False, float('nan'), float('inf'), -1, 0, 99):
            with self.subTest(value=value):
                database = copy.deepcopy(self.database)
                next(r for r in database['dimensions'] if r['id'] == 'D056')['value_mm'] = value
                with self.assertRaises(ValueError):
                    resolve(database, self.config)
        self.database['dimensions'] = [r for r in self.database['dimensions'] if r['id'] != 'D056']
        with self.assertRaises(ValueError):
            resolve(self.database, self.config)

    def test_rejects_changed_scope_method_endpoints_and_axis_swap(self):
        for field in ('model_year_scope', 'measurement_type', 'endpoint_definition', 'configuration', 'source_id'):
            with self.subTest(field=field):
                database = copy.deepcopy(self.database)
                next(r for r in database['dimensions'] if r['id'] == 'D056')[field] = 'incompatible'
                with self.assertRaises(ValueError):
                    resolve(database, self.config)
        self.config['loading_box'].update(length_id='D055', width_id='D056')
        with self.assertRaises(ValueError):
            resolve(self.database, self.config)

    def test_duplicate_source_ids_and_missing_contract_are_rejected(self):
        self.database['dimensions'].append(copy.deepcopy(self.dimension()))
        with self.assertRaises(ValueError):
            resolve(self.database, self.config)
        self.database['dimensions'].pop()
        self.config['loading_box']['source_contract'] = {}
        with self.assertRaises(ValueError):
            resolve(self.database, self.config)

    def test_classification_change_is_visible_not_silently_A(self):
        self.dimension().update(classification='D', confidence=1)
        result = render(resolve(self.database, self.config), self.template)
        self.assertIn('Published loading envelope · A/D / confidence 1', result)


if __name__ == '__main__':
    unittest.main()
