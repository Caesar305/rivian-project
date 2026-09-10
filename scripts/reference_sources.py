"""Shared source resolution for Blender, technical drawings and the preview."""
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AXES = ('length', 'width', 'height')


def finite_positive(value):
    try:
        return type(value) in (int, float) and math.isfinite(value) and value > 0
    except OverflowError:
        return False


def resolve(database, config):
    dimensions = {}
    for record in database['dimensions']:
        if record['id'] in dimensions:
            raise ValueError(f'Duplicate dimension: {record["id"]}')
        dimensions[record['id']] = record
    box_config = config['loading_box']
    required = {'source_id', 'measurement_type', 'model_year_scope', 'configuration', 'endpoint_definition'}
    if set(box_config.get('source_contract', {})) != required or any(not isinstance(v, str) or not v.strip() for v in box_config['source_contract'].values()):
        raise ValueError('Loading box needs a complete source definition contract')
    if set(box_config.get('axis_names', {})) != set(AXES):
        raise ValueError('Loading box needs three named axis definitions')
    ids = [box_config[axis + '_id'] for axis in AXES]
    selected = ids + config['cargo_length_reference_ids'] + config['passenger_space_reference_ids']
    for identifier in selected:
        if identifier not in dimensions:
            raise ValueError(f'Missing source dimension: {identifier}')
        record = dimensions[identifier]
        if not finite_positive(record.get('value_mm')) or not finite_positive(record.get('value')):
            raise ValueError(f'Invalid source length: {identifier}')
        factor = {'mm': 1, 'in': 25.4}.get(record.get('unit'))
        if factor is None or not math.isclose(record['value'] * factor, record['value_mm'], abs_tol=1e-4, rel_tol=0):
            raise ValueError(f'Source unit conversion mismatch: {identifier}')
        if record.get('classification') not in ('A', 'B', 'C', 'D') or type(record.get('confidence')) is not int or record['confidence'] not in range(1, 6):
            raise ValueError(f'Invalid provenance classification: {identifier}')
        if not isinstance(record.get('source_url'), str) or not record['source_url'].startswith('https://'):
            raise ValueError(f'Missing HTTPS provenance: {identifier}')
    box = [dimensions[identifier] for identifier in ids]
    for axis, record in zip(AXES, box):
        if record['name'] != box_config['axis_names'][axis]:
            raise ValueError(f'Wrong dimension mapped to {axis}')
        for field, expected in box_config['source_contract'].items():
            if record.get(field) != expected:
                raise ValueError(f'{record["id"]}: incompatible {field}; review the source definition before remapping')
    # Hash includes definitions/classification as well as values, never only lengths.
    content = {'config': config, 'dimensions': [dimensions[i] for i in sorted(set(selected))]}
    digest = hashlib.sha256(json.dumps(content, sort_keys=True, allow_nan=False).encode()).hexdigest()
    return {'database': database, 'config': config, 'dimensions': dimensions,
            'box': box, 'dimensions_mm': [r['value_mm'] for r in box], 'source_fingerprint': digest}


def load(root=ROOT):
    return resolve(json.loads((root / 'outputs/dimension_database.json').read_text()),
                   json.loads((root / 'outputs/reference_model_config.json').read_text()))
