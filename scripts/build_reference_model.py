"""Run with Blender --background --python scripts/build_reference_model.py.

Creates a source-driven online-reference scene, not a cabin surface model.
Only source dimensions drive geometric lengths. Label sizes/camera offsets are
presentation settings and excluded from physical measurement and collision use.
"""
import json
from pathlib import Path
from itertools import product
from xml.sax.saxutils import escape
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs'
DB = json.loads((OUT / 'dimension_database.json').read_text())
CFG = json.loads((OUT / 'reference_model_config.json').read_text())
D = {d['id']: d for d in DB['dimensions']}

def mm(id):
    value = D[id]['value_mm']
    if value is None or value <= 0:
        raise ValueError(f'No positive source length for {id}')
    return value

def label(id):
    return f"{mm(id):.1f} mm / {mm(id)/25.4:.2f} in [{D[id]['classification']}; {id}]"

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 0.001
scene.unit_settings.length_unit = 'MILLIMETERS'
scene['status'] = CFG['status']
scene['validated_cabin'] = False
scene['fit_clearance_enabled'] = False
scene['datum'] = CFG['placement']['definition']
scene['axes'] = 'X forward; Y driver side; Z up; numeric coordinates in mm'

names = ['00_REFERENCE','01_SCAN','02_BODY','03_FLOOR','04_TRIM','05_FRONT_SEATS','06_EXECUTIVE_SEATS','07_THIRD_ROW','08_SEAT_RAILS','09_CONSOLE','10_SCREENS','11_TABLES','12_HUMANS','13_MEASUREMENTS','14_COLLISION','15_CAMERAS','16_LIGHTING']
collections = {}
for name in names:
    c = bpy.data.collections.new(name)
    scene.collection.children.link(c)
    collections[name] = c

def empty(name, collection):
    o = bpy.data.objects.new(name, None)
    collection.objects.link(o)
    return o

parameters = empty('SOURCE_PARAMETERS_mm', collections['13_MEASUREMENTS'])
ids = [CFG['loading_box'][k] for k in ['length_id','width_id','height_id']] + CFG['cargo_length_reference_ids'] + CFG['passenger_space_reference_ids']
for id in ids:
    parameters[id] = float(mm(id))
    parameters.id_properties_ui(id).update(description=f"{D[id]['name']} | {D[id]['classification']} | {D[id]['source_url']}", min=0.0)
parameters['editing'] = 'Changing a source value in Blender makes a local override, not a new verified measurement. Persist new measurements in the database and rebuild.'

def driver(owner, prop, index, expression, links):
    fc = owner.driver_add(prop, index)
    dr = fc.driver
    dr.type = 'SCRIPTED'
    for alias, id in links.items():
        var = dr.variables.new()
        var.name = alias
        var.type = 'SINGLE_PROP'
        var.targets[0].id = parameters
        var.targets[0].data_path = f'["{id}"]'
    dr.expression = expression

def wire(name, coords, edges, collection, color):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(coords, edges, [])
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    obj.display_type = 'WIRE'
    obj.color = (*color, 1)
    obj['collision_use'] = False
    return obj

LID, WID, HID = (CFG['loading_box'][k] for k in ['length_id','width_id','height_id'])
L, W, H = mm(LID), mm(WID), mm(HID)
coords = list(product([0.,1.],[-.5,.5],[0.,1.]))
edges = [(i,j) for i in range(8) for j in range(i+1,8) if sum(a!=b for a,b in zip(coords[i],coords[j])) == 1]
box = wire('PUBLISHED_COMFORTABLE_LOADING_BOX__NOT_CABIN', coords, edges, collections['00_REFERENCE'], (.13,.46,.7))
for axis,id in enumerate([LID,WID,HID]):
    driver(box,'scale',axis,'v',{'v':id})
box['dimension_ids'] = ','.join([LID,WID,HID])
box['dimension_class'] = json.dumps({id:D[id]['classification'] for id in [LID,WID,HID]})
box['placement_class'] = 'D — illustrative origin; no body registration'
box['definition'] = CFG['loading_box']['meaning']
box['source_url'] = D[LID]['source_url']
box['source_configuration'] = CFG['loading_box']['source_configuration']

# Hidden, individually selectable scalar references. Their locations are NOT
# installed seat positions or co-registered cargo boundaries.
for id in CFG['cargo_length_reference_ids'] + CFG['passenger_space_reference_ids']:
    c = bpy.data.collections.new(f'{id} | {D[id]["name"]}')
    collections['00_REFERENCE'].children.link(c)
    o = wire(f'{id}_UNREGISTERED_REFERENCE_SPAN', [(0,0,0),(1,0,0)], [(0,1)], c, (.8,.5,.16))
    driver(o,'scale',0,'v',{'v':id})
    o['dimension_id'] = id
    o['classification'] = D[id]['classification']
    o['source_url'] = D[id]['source_url']
    o['meaning'] = 'Isolated scalar reference. Placement/orientation illustrative, not an anatomical or physical cabin boundary.'
    c.hide_viewport = True
    c.hide_render = True

for name, location, scale, rotation in [
    ('TOP_ORTHO',(L/2,0,5000),3000,(0,0,0)),
    ('PASSENGER_SIDE_ORTHO',(L/2,-5000,H/2),3000,None),
    ('REAR_ORTHO',(-5000,0,H/2),2000,None),
]:
    data = bpy.data.cameras.new(name)
    cam = bpy.data.objects.new(name,data)
    collections['15_CAMERAS'].objects.link(cam)
    cam.location = location
    cam.rotation_euler = (Vector((L/2,0,H/2))-cam.location).to_track_quat('-Z','Y').to_euler()
    data.type = 'ORTHO'; data.ortho_scale = scale; data.clip_end = 100000
scene.camera = bpy.data.objects['TOP_ORTHO']

note = bpy.data.texts.new('READ_ME_FIRST')
note.write('PROVISIONAL ONLINE REFERENCE\n\n'+json.dumps(CFG,indent=2)+'\n\nSource dictionary:\n'+json.dumps({id:D[id] for id in ids},indent=2))
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type == 'VIEW_3D':
            area.spaces.active.clip_end = 100000
            area.spaces.active.region_3d.view_distance = 3500
            area.spaces.active.region_3d.view_location = (L/2,0,H/2)
            area.spaces.active.overlay.show_floor = False
bpy.context.view_layer.update()
assert all(abs(float(box.dimensions[i])-v)<.001 for i,v in enumerate([L,W,H]))
original = parameters[LID]
parameters[LID] = original + 100
parameters.update_tag(); bpy.context.view_layer.update()
assert abs(float(box.dimensions.x)-(original+100)) < .001, 'Parameter propagation failed'
parameters[LID] = original
parameters.update_tag(); bpy.context.view_layer.update()
assert abs(float(box.dimensions.x)-original) < .001
assert not any(collections[n].objects for n in ['02_BODY','03_FLOOR','06_EXECUTIVE_SEATS','14_COLLISION'])
bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'R1S_provisional_reference.blend'), compress=True)

# A technical drawing sheet, calculated from the same source IDs. Drawing
# placement, font size and stroke widths have no vehicle-dimensional meaning.
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1200" viewBox="0 0 1600 1200">',
 '<rect width="1600" height="1200" fill="#f8fafc"/>',
 '<style>text{font-family:Arial,sans-serif;fill:#172b3b}.small{font-size:18px}.label{font-size:21px}.head{font-size:25px;font-weight:bold}.box{fill:#e2eff8;stroke:#287ca7;stroke-width:3}.dim{stroke:#617687;stroke-width:1.5}</style>',
 '<text x="55" y="58" font-size="34" font-weight="bold">R1S — provisional online reference</text>',
 '<text x="55" y="91" class="label">Published comfortable loading box · rows 2 and 3 folded · 2022 media vehicle</text>',
 '<text x="55" y="122" class="small">No body datum, trim surfaces, seat locations or fit clearance established. Dimensions are source claims.</text>']
def text(x,y,s,cls='label'):
    svg.append(f'<text x="{x}" y="{y}" class="{cls}">{escape(s)}</text>')
def rect(x,y,w,h):
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="box"/>')
def line(x1,y1,x2,y2):svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="dim"/>')
def hdim(x,y,w,s):
    line(x,y,x+w,y);line(x,y-8,x,y+8);line(x+w,y-8,x+w,y+8);text(x,y-14,s,'small')

s=.40
text(55,177,'TOP ORTHOGRAPHIC','head')
rect(55,245,L*s,W*s)
hdim(55,227,L*s,label(LID))
text(55,245+W*s+29,'Width: '+label(WID),'small')
text(55,245+W*s+54,'Rear  X=0                                               +X toward front →','small')
text(55,245+W*s+79,'Upper edge: +Y driver side. Centering is illustrative [D].','small')
text(985,177,'REAR ORTHOGRAPHIC','head')
rect(985,245,W*s,H*s)
hdim(985,227,W*s,label(WID))
text(985,245+H*s+29,'Height: '+label(HID),'small')
text(985,245+H*s+56,'+Z up; +Y driver side is left','small')
text(55,815,'PASSENGER-SIDE ORTHOGRAPHIC','head')
rect(55,880,L*.28,H*.28)
hdim(55,863,L*.28,label(LID))
text(55,1121,'Each view preserves proportions; the side view uses a smaller drawing scale. No trim/roof profile is implied.','small')
text(985,645,'CARGO-LENGTH CONFLICT','head')
text(985,681,'Behind row 2:','label')
text(985,712,label('D030'),'small')
text(985,742,label('D058'),'small')
text(985,778,'Difference: '+f"{abs(mm('D058')-mm('D030')):.2f} mm / {abs(mm('D058')-mm('D030'))/25.4:.2f} in",'small')
text(985,815,'Different source claims; configuration','small')
text(985,841,'and endpoints remain unresolved.','small')
text(985,885,'Update via source records and parameter links.','small')
text(985,918,'No clearance or cargo-volume result claimed.','small')
text(55,1160,'Source: Andrew P. Collins / The Drive (S05). Full provenance and alternate reference spans are embedded in the .blend.','small')
svg.append('</svg>')
(OUT/'provisional_reference_views.svg').write_text('\n'.join(svg))
manifest = dict(status=CFG['status'],dimensions_mm={'length':L,'width':W,'height':H},source_dimension_ids=[LID,WID,HID],
               parameter_update_test='PASS: temporary +100 mm change propagated and was restored',
               geometry_validation='NOT PERFORMED — no owner measurements',fit_clearance_enabled=False,
               generated_files=['R1S_provisional_reference.blend','provisional_reference_views.svg'])
(OUT/'reference_model_build_report.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest))
