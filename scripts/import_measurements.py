"""Preserve an owner capture batch without promoting it to model geometry."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sys
import tempfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}\Z")


def number(value):
    try:
        return type(value) in (int, float) and math.isfinite(value)
    except OverflowError:
        return False


def nonblank(value):
    return isinstance(value, str) and bool(value.strip())


def reject_constant(value):
    raise ValueError(f"Non-finite JSON number: {value}")


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def inspect_observation(record, root):
    """Assess metadata completeness; completeness is never engineering approval."""
    issues = []
    required_text = ('name', 'observer', 'method', 'instrument', 'endpoint_from',
                     'endpoint_to', 'uncertainty_basis')
    for key in required_text:
        if not nonblank(record.get(key)):
            issues.append(f"Missing {key}")
    claimed = record.get('classification')
    if claimed not in ('B', 'C', 'D'):
        issues.append('Owner capture classification must be B, C or D; OEM claims use the source register')
    if claimed == 'D':
        issues.append('Estimated/unverified observation requires resolution')
    if record.get('side') not in ('driver', 'passenger', 'center', 'cross_cabin'):
        issues.append('Specify driver, passenger, center or cross_cabin; do not mirror observations')
    vehicle = record.get('vehicle', {})
    if not isinstance(vehicle, dict) or vehicle.get('model') != 'R1S' or vehicle.get('model_year') != 2023 or vehicle.get('owner_vehicle') is not True:
        issues.append('Confirm observation is from the owner\'s 2023 R1S')
    config = record.get('configuration', {})
    for key in ('front_seats', 'second_row', 'third_row', 'doors', 'hatch'):
        if not isinstance(config, dict) or not nonblank(config.get(key)):
            issues.append(f'Missing configuration.{key}')
    try:
        captured = datetime.fromisoformat(record.get('captured_at', '').replace('Z', '+00:00'))
        if captured.utcoffset() is None:
            raise ValueError('Missing timezone')
    except (ValueError, AttributeError, TypeError):
        issues.append('captured_at must be an ISO timestamp with timezone')
    unit = record.get('unit')
    factor = {'mm': 1.0, 'in': 25.4}.get(unit) if isinstance(unit, str) else None
    if factor is None:
        issues.append('Unit must be mm or in')
    quantity = record.get('quantity')
    if quantity not in ('distance', 'x', 'y', 'z'):
        issues.append('Quantity must be distance, x, y or z')
    value = record.get('value')
    valid_value = number(value) and (quantity in ('x', 'y', 'z') or (quantity == 'distance' and value > 0))
    if not valid_value:
        issues.append('Provide a finite value; distances must be positive, coordinates may be signed or zero')
    uncertainty = record.get('uncertainty')
    valid_uncertainty = number(uncertainty) and uncertainty > 0
    if not valid_uncertainty:
        issues.append('Provide positive uncertainty in the observation unit')
    if quantity in ('x', 'y', 'z') and not nonblank(record.get('datum_id')):
        issues.append('Coordinate observation requires a datum_id for later registration review')
    if claimed == 'C' and not nonblank(record.get('calibration_id')):
        issues.append('Photographic derivation requires a calibration_id for later scale review')
    evidence = record.get('evidence_paths')
    hashes = []
    if not isinstance(evidence, list) or not evidence:
        issues.append('Attach at least one local evidence file')
        evidence = []
    for relative in evidence:
        if not nonblank(relative):
            issues.append('Evidence paths must be nonempty strings')
            continue
        path = (root / relative).resolve()
        if Path(relative).is_absolute() or not path.is_relative_to(root.resolve()):
            issues.append(f'Evidence must be inside the project: {relative}')
            continue
        try:
            payload = path.read_bytes()
        except OSError:
            issues.append(f'Evidence file unavailable: {relative}')
            continue
        hashes.append({'path': relative, 'sha256': hashlib.sha256(payload).hexdigest(), 'bytes': len(payload)})
    normalized_value = value * factor if valid_value and factor else None
    normalized_uncertainty = uncertainty * factor if valid_uncertainty and factor else None
    if normalized_value is not None and not math.isfinite(normalized_value):
        normalized_value = None
        issues.append('Unit conversion overflow')
    if normalized_uncertainty is not None and not math.isfinite(normalized_uncertainty):
        normalized_uncertainty = None
        issues.append('Uncertainty conversion overflow')
    return {
        'id': record['id'], 'claimed_classification': claimed,
        'effective_classification': 'D', 'review_state': 'PENDING_HUMAN_REVIEW',
        'metadata_complete': not issues, 'geometry_authorized': False,
        'value_mm': normalized_value, 'uncertainty_mm': normalized_uncertainty,
        'evidence': hashes, 'issues': issues,
    }


def prepare(source, root=ROOT):
    source_bytes = Path(source).read_bytes()
    raw = source_bytes.decode('utf-8')
    data = json.loads(raw, parse_constant=reject_constant, object_pairs_hook=unique_keys)
    if not isinstance(data, dict) or data.get('schema_version') != 1:
        raise ValueError('Expected an object with schema_version: 1')
    batch_id = data.get('batch_id')
    if not isinstance(batch_id, str) or not IDENTIFIER.fullmatch(batch_id):
        raise ValueError('batch_id must use 1–80 letters, digits, underscores or hyphens')
    records = data.get('observations')
    if not isinstance(records, list) or not records:
        raise ValueError('observations must be a nonempty list')
    seen = set()
    for record in records:
        if not isinstance(record, dict) or not isinstance(record.get('id'), str) or not IDENTIFIER.fullmatch(record['id']):
            raise ValueError('Every observation needs a safe, nonempty id')
        if record['id'] in seen:
            raise ValueError(f'Duplicate observation id: {record["id"]}')
        seen.add(record['id'])
    return {
        'schema_version': 1, 'batch_id': batch_id,
        'imported_at': datetime.now(timezone.utc).isoformat(),
        'source_filename': Path(source).name,
        'source_sha256': hashlib.sha256(source_bytes).hexdigest(),
        'raw_json_text': raw,
        'observations': [inspect_observation(record, root) for record in records],
    }


def save(envelope, root=ROOT):
    """Atomically publish a whole batch, refusing to replace any existing batch."""
    directory = root / 'data' / 'measurements' / 'batches'
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / (envelope['batch_id'] + '.json')
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=directory, prefix='.', suffix='.tmp', delete=False) as stream:
        scratch = Path(stream.name)
        try:
            json.dump(envelope, stream, indent=2, ensure_ascii=False, allow_nan=False)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        except BaseException:
            scratch.unlink(missing_ok=True)
            raise
    try:
        # Unlike rename/replace, link fails if target exists, including concurrent imports.
        os.link(scratch, target)
    finally:
        scratch.unlink(missing_ok=True)
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--check', action='store_true', help='Assess the batch without saving it')
    args = parser.parse_args()
    try:
        envelope = prepare(args.source)
        output = None if args.check else str(save(envelope))
        print(json.dumps({'saved': output, 'observations': envelope['observations']}, indent=2, allow_nan=False))
    except (OSError, ValueError) as error:
        print(f'Import failed: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
