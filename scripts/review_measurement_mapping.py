"""Read-only compatibility review of explicit observation-to-parameter proposals."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

from import_measurements import ROOT, IDENTIFIER, inspect_observation, number, nonblank, reject_constant, unique_keys


def decode(text):
    return json.loads(text, parse_constant=reject_constant, object_pairs_hook=unique_keys)


def load_observation(reference, root):
    parts = reference.split('/') if isinstance(reference, str) else []
    if len(parts) != 2 or not all(IDENTIFIER.fullmatch(part) for part in parts):
        raise ValueError('Observation reference must be batch_id/observation_id')
    batch_id, observation_id = parts
    path = (root / 'data/measurements/batches' / f'{batch_id}.json').resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError('Batch path escapes the project')
    envelope = decode(path.read_text())
    if envelope.get('schema_version') != 1 or envelope.get('batch_id') != batch_id:
        raise ValueError('Batch identity or schema mismatch')
    raw = envelope['raw_json_text']
    if hashlib.sha256(raw.encode('utf-8')).hexdigest() != envelope['source_sha256']:
        raise ValueError('Original capture checksum mismatch')
    source = decode(raw)
    if source.get('schema_version') != 1 or source.get('batch_id') != batch_id:
        raise ValueError('Original capture identity or schema mismatch')
    original = [r for r in source['observations'] if r.get('id') == observation_id]
    stored = [r for r in envelope['observations'] if r.get('id') == observation_id]
    if len(original) != 1 or len(stored) != 1:
        raise ValueError('Observation is missing or ambiguous')
    current = inspect_observation(original[0], root)
    issues = list(current['issues'])
    if current != stored[0]:
        issues.append('Capture assessment or evidence changed since import; review and import a new batch')
    return original[0], current, issues


def validate_parameter(parameter):
    if not isinstance(parameter, dict) or not isinstance(parameter.get('id'), str) or not IDENTIFIER.fullmatch(parameter['id']):
        raise ValueError('Each parameter needs a safe id')
    for key in ('definition', 'endpoint_from', 'endpoint_to'):
        if not nonblank(parameter.get(key)):
            raise ValueError(f'{parameter["id"]}: missing {key}')
    if parameter.get('quantity') not in ('distance', 'x', 'y', 'z'):
        raise ValueError('Parameter quantity must be distance, x, y or z')
    if parameter.get('side') not in ('driver', 'passenger', 'center', 'cross_cabin'):
        raise ValueError('Parameter must specify an independent side or cross_cabin')
    if parameter.get('vehicle') != {'model': 'R1S', 'model_year': 2023, 'owner_vehicle': True}:
        raise ValueError('Parameter must target the owner\'s 2023 R1S')
    config = parameter.get('configuration')
    if not isinstance(config, dict) or any(not nonblank(config.get(k)) for k in ('front_seats', 'second_row', 'third_row', 'doors', 'hatch')):
        raise ValueError('Parameter needs explicit seat, door and hatch configuration')
    if parameter['quantity'] != 'distance' and not nonblank(parameter.get('datum_id')):
        raise ValueError('Coordinate parameter requires a datum_id')


def review(config, root=ROOT):
    if not isinstance(config, dict) or config.get('schema_version') != 1:
        raise ValueError('Expected mapping schema_version: 1')
    if not isinstance(config.get('parameters'), list) or not isinstance(config.get('mappings'), list):
        raise ValueError('Expected parameters and mappings lists')
    parameters = {}
    for parameter in config['parameters']:
        validate_parameter(parameter)
        if parameter['id'] in parameters:
            raise ValueError('Duplicate parameter id')
        parameters[parameter['id']] = parameter
    rows, seen = [], set()
    for mapping in config['mappings']:
        if not isinstance(mapping, dict) or not isinstance(mapping.get('parameter_id'), str) or not isinstance(mapping.get('observation_ref'), str):
            raise ValueError('Each mapping needs parameter_id and observation_ref strings')
        pair = (mapping['parameter_id'], mapping['observation_ref'])
        if pair in seen:
            raise ValueError('Duplicate mapping proposal')
        seen.add(pair)
        parameter = parameters.get(pair[0])
        issues, normalized = [], {}
        if parameter is None:
            issues.append('Parameter definition is missing')
        try:
            original, normalized, capture_issues = load_observation(pair[1], root)
            issues.extend(capture_issues)
            if parameter:
                for field in ('quantity', 'side', 'vehicle', 'configuration', 'endpoint_from', 'endpoint_to'):
                    if original.get(field) != parameter.get(field):
                        issues.append(f'{field} does not match the parameter definition')
                if parameter['quantity'] != 'distance' and original.get('datum_id') != parameter.get('datum_id'):
                    issues.append('datum_id does not match the parameter definition')
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
            issues.append(f'Cannot verify observation: {error}')
        rows.append({
            'parameter_id': pair[0], 'observation_ref': pair[1],
            'status': 'BLOCKED' if issues else 'READY_FOR_REVIEW',
            'value_mm': normalized.get('value_mm'),
            'uncertainty_mm': normalized.get('uncertainty_mm'),
            'claimed_classification': normalized.get('claimed_classification'),
            'effective_classification': 'D', 'geometry_authorized': False,
            'issues': issues,
        })
    conflicts = []
    # Compare only matching definitions; different sides/configurations are not repeats.
    candidates = [row for row in rows if row['status'] == 'READY_FOR_REVIEW']
    for index, left in enumerate(candidates):
        for right in candidates[index + 1:]:
            if left['parameter_id'] != right['parameter_id']:
                continue
            delta = abs(left['value_mm'] - right['value_mm'])
            bound = left['uncertainty_mm'] + right['uncertainty_mm']
            if not number(delta) or not number(bound):
                raise ValueError('Comparison arithmetic overflow')
            if delta > bound:
                conflicts.append({'parameter_id': left['parameter_id'],
                                  'observations': [left['observation_ref'], right['observation_ref']],
                                  'difference_mm': delta, 'combined_bound_mm': bound})
                for row in (left, right):
                    row['status'] = 'CONFLICT'
                    row['issues'].append('Repeated observations have non-overlapping uncertainty bounds')
    mapped = {row['parameter_id'] for row in rows}
    return {
        'schema_version': 1, 'mode': 'REVIEW_ONLY', 'geometry_authorized': False,
        'summary': {state: sum(row['status'] == state for row in rows)
                    for state in ('READY_FOR_REVIEW', 'BLOCKED', 'CONFLICT')},
        'unmapped_parameters': sorted(set(parameters) - mapped),
        'mappings': rows, 'conflicts': conflicts,
        'next_action': 'Define capture-backed parameters and explicit mappings.' if not rows else
                       'Review evidence, endpoint equivalence, datum/calibration and conflicts before accepting any dimension.',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=ROOT / 'data/measurements/parameter_mapping.json')
    args = parser.parse_args()
    try:
        result = review(decode(args.config.read_text()))
        print(json.dumps(result, indent=2, allow_nan=False))
    except (OSError, ValueError) as error:
        print(f'Mapping review failed: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
