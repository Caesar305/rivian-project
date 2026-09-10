"""Generate the inline preview from the same checked source mapping as Blender."""
import argparse
from html import escape
import json
import re
import sys

from reference_sources import ROOT, AXES, load


def render(reference, template):
    box = reference['box']
    comparison = [reference['dimensions'][i] for i in ('D030', 'D058')]
    classes = sorted(set(r['classification'] for r in box))
    confidence = min(r['confidence'] for r in box)
    label = f'Published loading envelope · {"/".join(classes)} / confidence {confidence}'
    payload = {'dimensions_mm': reference['dimensions_mm'],
               'source_dimension_ids': [r['id'] for r in box],
               'source_class': '/'.join(classes), 'classification_label': label,
               'source_fingerprint': reference['source_fingerprint']}
    replacements = {axis.upper() + '_MM': str(value) for axis, value in zip(AXES, reference['dimensions_mm'])}
    replacements.update(CLASSIFICATION=escape(label), SOURCE_URL=escape(box[0]['source_url'], quote=True),
                        REFERENCE_JSON=json.dumps(payload, allow_nan=False).replace('<', '\\u003c'))
    rows = []
    for label_text, record in zip(['Loading length', 'Loading width', 'Loading height', 'Behind row 2', 'Behind row 2'], box + comparison):
        values = (f'{label_text} · {record["id"]}', f'{record["value_mm"]:.2f}',
                  f'{record["value_mm"]/25.4:.2f}', record['classification'])
        rows.append('        <tr>' + ''.join('<td>' + escape(value) + '</td>' for value in values) + '</tr>')
    replacements['SOURCE_ROWS'] = '\n'.join(rows)
    tokens = re.findall(r'@@([A-Z_]+)@@', template)
    if set(tokens) != set(replacements):
        raise ValueError('Preview template tokens do not match the source builder')
    return re.sub(r'@@([A-Z_]+)@@', lambda match: replacements[match[1]], template)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if the saved preview differs from its template and sources')
    args = parser.parse_args()
    try:
        reference = load()
        result = render(reference, (ROOT / 'templates/r1s-working-preview.html').read_text())
        destination = ROOT / 'outputs/r1s-working-preview.html'
        if args.check:
            if not destination.exists() or destination.read_text() != result:
                raise ValueError('Preview is stale; run scripts/build_preview.py')
        else:
            destination.write_text(result)
        print(f'Preview {"checked" if args.check else "built"}: {reference["source_fingerprint"]}')
    except (OSError, ValueError, KeyError) as error:
        print(f'Preview build failed: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
