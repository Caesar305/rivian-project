import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / 'outputs'
OUT.mkdir(exist_ok=True)
DATE = '2026-09-09'
sources = []
def source(id, name, url, scope, access, notes):
    sources.append(dict(id=id,name=name,url=url,model_year_scope=scope,access_status=access,accessed_date=DATE,notes=notes))
source('U01','Owner project brief','', 'Target 2023 R1S','Supplied text','Initial reference claims; no physical measurements or photographs supplied.')
source('S01','Rivian — Sizing Up the R1S','https://rivian.com/stories/sizing-up-the-r1s','Launch-era R1S; 2022 publication','Opened','OEM publication. Exterior and storage references only.')
source('S02','Rivian — current model comparison','https://rivian.com/en-US/compare?a=r1t-quad-launch&b=r1t-tri&c=r1t-dual','Current comparison; R1S column, not MY2023 certification','Indexed content inspected','Mirrors folded/extended and min/max height have separate definitions.')
source('S03','velosnow — received Rivian cargo specifications','https://www.reddit.com/r/Rivian/comments/vssjer/r1s_interieor_dimensions/','2022 support-email relay','Opened','Original recipient report; underlying OEM message not authenticated. D/1; not independent of reposts.')
source('S04','whyasky — received Rivian interior specifications, post 148','https://www.rivianforums.com/forum/threads/what-we-know-collecting-information-directly-from-rivian.827/page-10#post-15113','November 2020 preproduction; 7-passenger R1S column','Opened','Original recipient transcription; SAE codes supplied but measurement protocol not recovered. D/1.')
source('S05','Andrew P. Collins — usable cargo measured','https://www.thedrive.com/news/we-measured-the-2022-rivian-r1ss-cargo-storage-to-determine-its-usable-space','2022 media vehicle','Opened','Comfortable cuboid envelopes, not surface maxima; illustrated boxes not drawn to scale.')
source('S06','lmr — Rivian cargo dimensions relay','https://www.rivianforums.com/forum/threads/r1s-size-comparisons-to-other-suvs-and-trucks.5699/page-2','June 2022 relay','Indexed content inspected','Unverified endpoint/configuration; preserve conflict with S03.')
source('S07','NHTSA-hosted rollover measurement report lead','https://downloads.regulations.gov/NHTSA-2001-9663-0550/attachment_1.pdf','2023 R1S; test 27 March 2023','Indexed excerpt only; PDF open failed','Test 8398, page label C-32 in excerpt. D/1 pending document inspection. Different vehicle, never B.')
source('S08','BamBeds R1S platform manufacturer','https://bambeds.com/products/bambed-rivian-r1s','Gen 1 and Gen 2 options; dimensions not individually scoped','Opened','Published accessory dimensions only. Do not use to define body surfaces.')
source('S09','Rivian cargo cover','https://gearshop.rivian.com/products/r1s-cargo-cover','Current accessory listing; generation unspecified','Indexed content inspected','Product dimensions; not cargo width or mounting-point coordinates.')
source('S10','Rivian 2023 owner guide','https://assets.rivian.com/2md5qhoeajym/7Ao7NIFkLxOZtvdc7Fqh70/fff272692b97bdd50251339da18fa594/r1s-og-en-us-20230227.pdf','February 2023','Indexed content inspected','Stock component and operating reference; no cabin survey extracted.')
source('S11','Rivian MY2022–2024 owner guide','https://assets.rivian.com/2md5qhoeajym/7Ao7NIFkLxOZtvdc7Fqh70/c8c4a585ae141effce63b41ead2b8ce0/r1s-og-en-us-20240722.pdf','MY2022–2024; version 2024.27','Opened','No complete dimensional cabin/hardpoint table located.')
source('S12','Mojave — second-row removal','https://rivianforums.com/forum/threads/step-by-step-removal-of-second-row-in-r1s-diy-instructions-w-photos.23026/','January 2024 owner post','Indexed content inspected','Photographic concealed-part reference; no measurements accepted.')
source('S13','Leesa — third-row removal','https://www.rivianforums.com/forum/threads/diy-how-to-remove-3rd-row-from-gen-2-r1s-steps-and-photos.38049/','Explicitly Gen 2','Indexed content inspected','Exclude from MY2023 dimensional construction.')
source('S14','S005J — free sleeping-platform CAD','https://www.printables.com/fr/model/551407-rivian-r1s-sleeping-platform','Published August 2023','Listing inspected; files not downloaded','STEP assembly advertised, accessory only; CC BY-NC 4.0. English URL failed to open.')
source('S15','WeatherTech 2023 R1S cargo liner','https://www.weathertech.com/cargo-liner/2023_rivian_r1s/','2023 fit listing','Indexed content inspected','No engineering mesh or surface coordinates located.')
source('S16','LinerX R1S cargo liner','https://linerx.com/collections/rivian/products/linerx-cargo-liner-for-rivian-r1s','2022–2027 fit listing','Indexed content inspected','No open dimensioned contour or scan located.')
source('S17','Copart 2023 R1S lot 44236755','https://www.copart.com/lot/44236755/salvage-2023-rivian-r1s-adventure-ny-newburgh','2023; front-end damage','Listing indexed; no calibrated image analysis','Visual lead only; damaged vehicle not a dimensional reference.')
source('S18','Remeshy free miniature','https://remeshy.com/model/rivian-r1s-suv-model-da9f0673','Miniature; published April 2026','Listing inspected; no download','STL/GLB listing, AI mesh language; rejected for engineering geometry.')
source('S19','Rivian ADAS position statement','https://rts.i-car.com/images/pdf/oem-info/rivian/position-statements/71346x.pdf','All years; February 2025 document','Indexed content inspected','Public Rivian-authored repair information, not cabin dimension data.')
source('S20','Rivian material matrix MY2025+','https://www.rivianforums.com/forum/attachments/rivian_sg_r1s-material-matrix-rep-guide_2025_2b_2810-31-24_29-pdf.153799/','MY2025+','Indexed content inspected','Excluded from Gen 1 dimensional constraints.')

by_source={s['id']:s for s in sources}
dims=[]
def add(name,value,unit,sid,cls='D',confidence=1,kind='reference_claim',config='Unspecified',endpoints='Unspecified',conflict='',notes=''):
    s=by_source[sid]
    factor={'mm':1,'in':25.4,'ft':304.8}.get(unit)
    vmm=round(value*factor,6) if factor is not None else None
    dims.append(dict(id=f'D{len(dims)+1:03}',name=name,value=value,unit=unit,value_mm=vmm,value_in=round(vmm/25.4,6) if vmm is not None else None,
      source_id=sid,source=s['name'],source_url=s['url'],classification=cls,confidence=confidence,measurement_type=kind,model_year_scope=s['model_year_scope'],configuration=config,
      endpoint_definition=endpoints,uncertainty_mm=None,conflict_group=conflict,geometry_authorized=False,status='REFERENCE_ONLY' if cls=='A' else 'UNVERIFIED',notes=notes))

initial=[('Overall length',200.8,'length'),('Wheelbase',121.1,'wheelbase'),('Exterior width lower',81.8,'exterior_width'),('Exterior width upper',82,'exterior_width'),('Overall height',77.3,'height'),
('Row 2 hip room',54.2,'r2_hip'),('Row 2 shoulder room',58.9,'r2_shoulder'),('Row 2 headroom',39.7,'r2_head'),('Row 2 nominal legroom',36.6,'r2_leg'),
('Row 3 hip room',42.8,'r3_hip'),('Row 3 shoulder room',51.1,'r3_shoulder'),('Row 3 headroom',38.6,'r3_head'),('Row 3 nominal legroom',32.8,'r3_leg'),
('Cargo length behind row 1',84.7,'cargo_r1_length'),('Cargo length behind row 2',57.8,'cargo_r2_length'),('Cargo length behind row 3 lower',21,'cargo_r3_length'),('Cargo length behind row 3 upper',21.8,'cargo_r3_length'),('Width between wheel housings claim',51.1,'cargo_width'),('Rear minimum-width photo claim',42.5,'cargo_width'),('Cargo height',33.7,'cargo_height')]
for name,v,c in initial:
    add(name,v,'in','U01',conflict=c,notes='Brief lead; endpoint/configuration must be established. No original measurement photo supplied.' if 'photo' in name else '')
add('Overall length',200.8,'in','S01','A',5,'OEM_spec',endpoints='Overall exterior length',conflict='length')
add('Exterior width, mirrors folded',81.8,'in','S01','A',5,'OEM_spec',config='Mirrors folded',endpoints='Folded-mirror exterior envelope',conflict='exterior_width')
add('Cargo volume behind row 3',17.6,'ft3','S01','A',5,'OEM_volume',config='Row 3 upright',conflict='cargo_r3_volume')
for name,v,c,config in [('Wheelbase',121.1,'wheelbase','Current model'),('Exterior width, mirrors folded',82,'exterior_width','Mirrors folded'),('Exterior width, mirrors extended',88.4,'','Mirrors extended'),('Maximum exterior height',77.3,'height','Maximum height'),('Minimum exterior height',71.8,'height','Minimum height')]:
    add(name,v,'in','S02','A',5,'OEM_spec',config=config,conflict=c,notes='Current-model reference; not confirmed for target MY2023.')
for name,v,c in [('Cargo length behind row 3',553,'cargo_r3_length'),('Cargo maximum length behind row 2',1315,'cargo_r2_length'),('Cargo maximum length behind row 1',2152,'cargo_r1_length'),('Cargo maximum width behind row 3',1298,'cargo_width'),('Cargo maximum width behind row 2',1298,'cargo_width'),('Cargo maximum width behind row 1',1496,'cargo_width'),('Cargo minimum width',1084,'cargo_width'),('Cargo height',855,'cargo_height')]:
    add(name,v,'mm','S03',kind='relayed_OEM',conflict=c)
for name,v,c in [('Cargo volume behind row 3',499,'cargo_r3_volume'),('Cargo volume behind row 2',1323,'cargo_r2_volume'),('Cargo volume behind row 1',2499,'cargo_r1_volume'),('Total enclosed storage',2966,'total_storage')]:
    add(name,v,'L','S03',kind='relayed_OEM_volume',conflict=c)
for name,v,code,c in [('Row 2 effective legroom',931,'L51-2','r2_leg'),('Row 3 effective legroom',832,'L51-3','r3_leg'),('Row 1–2 couple distance',880,'L50-2',''),('Row 2–3 couple distance',750,'L50-3',''),('Row 2 shoulder room',1496,'W3-2','r2_shoulder'),('Row 3 shoulder room',1298,'W3-3','r3_shoulder'),('Row 2 hip room',1377,'W5-2','r2_hip'),('Row 3 hip room',1086,'W5-3','r3_hip'),('Row 2 elbow room',1515,'W31-2',''),('Row 3 elbow room',1296,'W31-3',''),('Row 2 seat height',350,'H30-2',''),('Row 3 seat height',310,'H30-3',''),('Row 2 effective headroom',1008,'H61-2-G','r2_head'),('Row 3 effective headroom',981,'H61-3-G','r3_head')]:
    add(name,v,'mm','S04',kind='relayed_SAE_spec',endpoints=code,conflict=c)
for name,v,c in [('Comfortable box width',42.5,'cargo_width'),('Comfortable box length',81,'cargo_r1_length'),('Comfortable box height',28,'cargo_height')]:
    add(name,v,'in','S05','A',4,'published_physical_envelope',config='Rows 2 and 3 folded',endpoints='Comfortable rectangular loading envelope; not trim surface distance',conflict=c)
add('Cargo length behind row 2',57.7,'in','S06',kind='relayed_OEM',conflict='cargo_r2_length')
for name,v in [('Wheelbase reported',121.6),('Left wheelbase reported',121.55),('Right wheelbase reported',121.65)]:
    add(name,v,'in','S07',kind='indexed_test_report_lead',config='Standard ride height; driver load per excerpt',conflict='wheelbase',notes='Full PDF inspection pending.')
for name,v in [('Platform length',78.5),('Platform width between rails',34.6),('Platform upper headroom maximum',29),('Platform underneath height from product floor',7.4),('Platform underneath height at cargo basin',21.7)]:
    add(name,v,'in','S08','A',4,'accessory_dimension',config='Product installation; generation mapping unresolved')
for name,v in [('Cargo cover width',4.3),('Cargo cover minimum length',1.5),('Cargo cover maximum length',3.3)]:
    add(name,v,'ft','S09','A',5,'accessory_dimension')

requirements=[]
def req(name,low,high,unit,notes):
    requirements.append(dict(name=name,min_value=low,max_value=high,unit=unit,min_mm=low*25.4 if unit=='in' else low if unit=='mm' else None,max_mm=high*25.4 if unit=='in' else high if unit=='mm' else None,source_id='U01',type='OWNER_DESIGN_REQUIREMENT',notes=notes))
req('Chair desired total width',21,23,'in','Feasibility pending; include arms and mechanism. Do not force.')
req('Cooler initial width',200,250,'mm','Delete if third-row access suffers.')
req('Cooler initial length',400,600,'mm','Starting envelope only.')
req('Cooler initial height',450,600,'mm','Starting envelope only.')
req('Cooler desired volume',10,15,'L','Internal refrigerated volume; not exterior envelope.')
req('Display nominal diagonal',14,14,'in','Diagonal only; bezel, aspect ratio and thickness unknown.')
for n,values in [('Carry-on',(22,14,9)),('Medium suitcase',(26,18,11))]:
    for axis,v in zip(['length','width','depth'],values):req(n+' '+axis,v,v,'in','Owner test envelope; clarify inclusion of handles/wheels.')

checks=[
('Row 2 width at B, cushion level','P1',5),('Row 2 width at C, armrest level','P1',5),('Row 2 width at D, shoulder level','P1',5),
('B left floor elevation','P1',5),('B right floor elevation','P1',5),('D left floor elevation','P1',5),('D right floor elevation','P1',5),
('Left rail corridor longitudinal span','P1',5),('Right rail corridor longitudinal span','P1',5),('Fixed mount pair lateral spacing','P1',5),
('Left fixed mount longitudinal spacing','P1',5),('Right fixed mount longitudinal spacing','P1',5),('Left front seatback to row 3 front gap','P1',5),('Right front seatback to row 3 front gap','P1',5),
('Left rear-door width, sill +300 mm','P1',5),('Right rear-door width, sill +300 mm','P1',5),('Left rear-door clear height at defined station','P1',5),('Right rear-door clear height at defined station','P1',5),
('Left C-pillar inner Y at marked point','P1',5),('Right C-pillar inner Y at marked point','P1',5),('Third-row footwell depth left','P1',5),('Third-row footwell depth right','P1',5),
('Third-row cushion front Z left','P1',5),('Third-row cushion front Z right','P1',5),('Third-row folded upper envelope Z left','P1',5),('Third-row folded upper envelope Z right','P1',5),
('Row 2 ceiling Z at centerline','P2',10),('Row 3 ceiling Z at centerline','P2',10),('Left wheel-house peak inner Y','P2',10),('Right wheel-house peak inner Y','P2',10),
('Narrow rear-trim width at shared X/Z','P2',10),('Cargo depth, row 3 up, hatch closed','P2',10),('Cargo depth, row 3 folded, row 2 fixed','P2',10),('Hatch clear width at marked height','P2',10),('Hatch clear height at centerline','P2',10),
('Left sill step Z relative to datum','P1',5),('Right sill step Z relative to datum','P1',5),('Forward-left to rear-right holdout diagonal','P1',5),('Forward-right to rear-left holdout diagonal','P1',5),('Independent vertical control span','P1',5)]
validation=[]
for i,(name,priority,tolerance) in enumerate(checks,1):
    validation.append(dict(id=f'V{i:02}',name=name,priority=priority,real_mm=None,model_mm=None,difference_mm=None,percent_error=None,tolerance_mm=tolerance,uncertainty_mm=None,source=None,confidence=None,classification=None,configuration=None,point_a=None,point_b=None,measurement_algorithm=None,holdout=True,status='NOT_MEASURED'))

station_names=[('A','Rear of front seats'),('B','Row 2 cushion front'),('C','Row 2 cushion midpoint'),('D','Row 2 cushion rear'),('E','Rear door/C-pillar transition'),('F','Third-row footwell'),('G','Third-row cushion midpoint'),('H','Third-row cushion rear'),('I','Wheel-house midpoint/peak'),('J','Cargo midpoint'),('K','Hatch aperture')]
stations=[]
for sid,name in station_names:
    for level in ['floor',150,300,450,600,750,900,'beltline','headliner']:
        stations.append(dict(station=sid,landmark=name,sample=str(level),target_z_mm=level if isinstance(level,int) else None,x_mm=None,z_mm=None,y_left_mm=None,y_right_mm=None,configuration=None,point_photo_ids=None,status='NOT_MEASURED'))

first_names=['Door trim width, row 2 cushion-front level','Door trim width, row 2 armrest level','Left front seatback to row 3 front','Right front seatback to row 3 front','Left rear-door opening dimensions','Right rear-door opening dimensions','Narrow rear trim and floor widths','Cargo depth, row 3 up, hatch closed']
first=[]
for i,name in enumerate(first_names,1):
    first.append(dict(id=f'F{i:02}',name=name,reading_1_mm=None,reading_2_mm=None,reading_3_mm=None,second_span_mm=None,height_reference=None,configuration=None,endpoint_photo_ids=None,tool=None,notes=None))

db=dict(schema_version='1.0',project='2023 Rivian R1S cabin digital twin',research_date=DATE,phase='Research and provisional online-reference modeling; no validated cabin',
 workflow_revision=dict(provisional_online_reference_authorized=True,owner_instruction='Use online measurements now and readjust after physical measurement.',geometry_authorized_field_meaning='Accepted target-cabin engineering geometry; provisional reference objects are controlled separately by reference_model_config.json'),
 classification_legend={'A':'Verified OEM/published claim within stated scope','B':'Measured on owner vehicle','C':'Derived from calibrated photography','D':'Estimated/unverified/unresolved'},
 confidence_legend={'5':'OEM or direct physical measurement','4':'Strong published/reference measurement','3':'Independent owner measurements agree','2':'Photographically derived','1':'Approximate/unverified'},
 coordinate_system=dict(length_unit='mm',positive_x='forward',positive_y='driver side',positive_z='up',origin=None,datum_plane=None,datum_status='PENDING_OWNER_PHOTOS',transform=None),
 sources=sources,dimensions=dims,owner_design_requirements=requirements,first_measurements=first,station_observations=stations,validation_plan=validation,
 acceptance=dict(critical_tolerance_mm=5,major_surface_tolerance_mm=10,exterior_reference_tolerance_mm=15,geometry_approved=False,critical_missing_data_blocks_design=True))
OUT.joinpath('dimension_database.json').write_text(json.dumps(db,indent=2)+'\n')
assert len({d['id'] for d in dims})==len(dims)
assert all(not d['geometry_authorized'] for d in dims)
assert all(d['source_id'] in by_source for d in dims)
assert all(v['real_mm'] is None and v['model_mm'] is None for v in validation)
print(json.dumps({'dimensions':len(dims),'sources':len(sources),'validation_checks':len(validation),'station_rows':len(stations),'requirements':len(requirements)}))
