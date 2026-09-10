"""Open the saved .blend before running: Blender --background <file> --python <script>."""
import json
from pathlib import Path
import sys
import bpy

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from reference_sources import load
from build_preview import render

reference = load(ROOT)
fingerprint = reference['source_fingerprint']
scene = bpy.context.scene
assert scene['source_fingerprint'] == fingerprint, 'Saved Blender source mapping is stale'
assert scene.unit_settings.system == 'METRIC'
assert abs(scene.unit_settings.scale_length - 0.001) < 1e-9
box = bpy.data.objects['PUBLISHED_COMFORTABLE_LOADING_BOX__NOT_CABIN']
parameters = bpy.data.objects['SOURCE_PARAMETERS_mm']
bpy.context.view_layer.update()
for index, record in enumerate(reference['box']):
    assert abs(box.dimensions[index] - record['value_mm']) < 0.001
    assert parameters[record['id']] == record['value_mm']
assert not scene['validated_cabin'] and not scene['fit_clearance_enabled']
report = json.loads((ROOT / 'outputs/reference_model_build_report.json').read_text())
assert report['source_fingerprint'] == fingerprint, 'Build report is stale'
expected = render(reference, (ROOT / 'templates/r1s-working-preview.html').read_text())
assert (ROOT / 'outputs/r1s-working-preview.html').read_text() == expected, 'Preview is stale'
print('PASS: saved Blender geometry, source parameters, build report and preview agree: ' + fingerprint)
