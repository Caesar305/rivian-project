# R1S measurement and capture procedure

Target: owner's 2023 vehicle. Revision 1 — datum features await photographs. The owner has authorized provisional online-reference modeling while physical data is collected.

**Begin with `START_HERE.md`.** The procedures below specify how to collect data; suggested target sizes, sampling intervals and photo counts are acquisition settings, not invented vehicle dimensions.

## 1. Coordinate system and repeatable datum

Use X forward, Y toward the driver side, Z upward. Left/right mean the vehicle sides when seated facing forward. All engineering coordinates and stored lengths are in millimeters. Keep measurements of each side independent.

We cannot name an exact structural contact point on your vehicle before seeing it. The first photos must identify fixed hard features that are accessible without disturbing safety-related fasteners. Good candidates are confirmed exposed fixed rail mounting features or rigid body/floor features. Sliding rail carriages, removable cargo panels, soft trim, seat cushions and carpet do not define the datum. Do not loosen seat, seatbelt or restraint hardware for this survey.

**Datum selection procedure once the photographs arrive:**

1. Label four fixed, repeatable hard points, two at a forward location and two rearward, on corresponding left/right structural features. Record exactly what is contacted: hole center, bolt center or a specified hard contact face. Confirm that these are suitable homologous features; appearance alone does not establish symmetry.
2. Select three non-collinear hard contact points to define the body-attached reference plane. A fourth independent hard point checks repeatability; it is not forced onto the plane. Record contact adapter thickness if used. This is a project datum, not a claimed Rivian factory body datum.
3. Survey the forward and rear left/right reference pairs. Their midpoints define a provisional longitudinal centerline, projected into the datum plane. Confirm alignment with additional paired fixed features. Do not make every trim-width midpoint equal to Y=0; that would erase real asymmetry. If centerline location cannot be established, retain a labeled provisional survey frame and withhold final XYZ release.
4. Set the origin at the rear-pair midpoint projected onto the reference plane. Define +X toward the projected forward midpoint. Let +Z be the upward plane normal and +Y complete the right-handed frame toward the driver's side. Thus Z=0 is body-attached and repeatable even if carpet elevations differ. X=0 is a recorded datum station, not an assumed axle or hatch location.
5. Store photos, contact definitions, raw survey coordinates, fitted plane, basis vectors and transformation matrix. Record residuals and repeatability. A self-leveling laser supplies a gravity reference in the temporary survey frame; gravity-horizontal is not automatically this body datum plane.

For raw survey point p, origin O and orthonormal basis eX/eY/eZ:

`X = dot(p − O, eX); Y = dot(p − O, eY); Z = dot(p − O, eZ)`

Record both raw and transformed data. Never overwrite raw observations when updating a transform.

```text
TOP VIEW — schematic only; no body shape or distances implied

                         FRONT  +X
                            ↑
 driver side +Y  ←  Y=0     │     →  passenger side −Y
                   forward reference-pair midpoint
                            │
                   rear reference-pair midpoint = X origin
                            │
                         REAR HATCH

CROSS-SECTION — looking forward from the rear

                           +Z ↑
 driver/left +Y     P_left     │      P_right    −Y passenger/right
                     •        │        •        same X, same Z
                     <---- measured width ---->
                      Y_left − Y_right
                  ───────── Z=0 ─────────       hard datum plane
               Floor elevations are measured above/below this plane.
```

**Practical measurement equipment:** a straight rigid rule or telescoping gauge, tape, carpenter's square, level, plumb line, straightedge, small removable target labels, and optional laser level/distance meter. A laser aimed directly at glass or dark/angled upholstery may measure the wrong surface; use a thin diffuse target and account for its offset. Tools need sufficient stated accuracy for the intended tolerance. A tape's 1 mm markings do not prove 1 mm accuracy.

For an XYZ survey, establish a rigid survey grid beside/through the cabin and use perpendicular projections to it. Measure longitudinal distance along the grid baseline, signed lateral distance from its reference plane, and vertical distance from its horizontal plane. Check the grid with a square and diagonal closure. Locate the hard datum targets in the same temporary grid, then transform to the body frame. If sightlines or tool setup cannot support this, report scalar spans with endpoints and photographs first; do not invent XYZ coordinates from them. A calibrated reconstruction can later tie visible targets into the frame, but that does not make photographically derived coordinates class B.

## 2. Record configuration before each session

Use one baseline session with unoccupied seats, unchanged front-seat positions, both rear doors closed for trim-width measurements, and row 3 upright. Record row 2's latched slide/recline position with actual distances to fixed targets, not “normal.” Record suspension setting, whether self-leveling moved the vehicle, and whether cargo panels/mats are installed.

Separate sessions: baseline seats up; row 3 folded; row 2 and row 3 folded; left door fully open; right door fully open; doors closed; hatch closed; front seats at additional movement limits. Give every configuration a unique ID. Fixed body targets stay in place. Moving seats/doors receive different target IDs and are excluded from body alignment.

Repeat each critical reading three times with the tool reset. Store raw readings, instrument/resolution, date, operator, endpoint photos, point IDs, contact/compression condition, uncertainty and configuration. If repeats span more than 3 mm (0.12 in), investigate before accepting a ±5 mm critical check. This is a proposed collection-quality trigger, not a guarantee of accuracy. Record soft-surface unloaded and loaded envelopes separately.

## 3. Station schedule

These are landmarks whose X positions must be measured. They are **not** equally spaced or assigned guessed coordinates. Establish them in one recorded seat configuration, then hold their X planes fixed for comparisons with moving seats. Left and right seat features may not share X; add separate stations where needed. Station I may overlap or precede another station; sort by measured X.

| Station | Exact plane selection | Priority/use |
|---|---|---|
| A | Plane through each front seatback's rearmost point in baseline; add planes through its lower and shoulder protrusions if different. | P1, front boundary, screen/table/knee space |
| B | Passenger row-2 cushion front-edge landmark; record driver-side difference. | P1, seat and aisle front |
| C | Midpoint in X between B and D for the baseline cushion; independently derive each side if required. | P1, chair/armrest compartment |
| D | Row-2 cushion rear-edge landmark in baseline. | P1, recline/third-row approach |
| E | Narrowest rear-door/C-pillar transition; add adjacent planes to capture curvature. | P1, entry bottleneck |
| F | Deepest usable third-row footwell region and its step edges. | P1, feet and rail intrusion |
| G | X midpoint of the third-row cushion's front and rear edges. | P1, knees and torso |
| H | Third-row cushion rear edge; separate backrest/hinge planes. | P1, retained folding mechanism |
| I | Measured midpoint of each wheel-house trim's longitudinal extent; add peak intrusion plane. | P2, side restrictions |
| J | X midpoint between the row-3 rear boundary and closed hatch at cargo-floor height. | P2, cargo |
| K | Rear aperture reference plane defined by fixed opening targets; closed hatch skin measured separately. | P1, opening and closure |

At every station record local floor and all reachable left/right surface intersections. Use global Z targets of 150, 300, 450, 600, 750 and 900 mm (5.91, 11.81, 17.72, 23.62, 29.53, 35.43 in), **where those levels are actually above the local floor**. Add the floor contact, beltline, armrest maximum intrusion, roof/glass boundary and headliner. Below-floor or blocked levels are marked unavailable, never replaced by zero. Add closely spaced samples around sharp changes; a coarse grid does not establish a ±5 mm curved surface.

At each `(X, Z)`, measure **Y_left and Y_right independently** from the survey frame. Width = Y_left − Y_right is an additional check. Do not split total width in half. Measure open-door and closed-door geometry in separate configurations. For overhangs, recesses and multiple intersections at one Z, record all relevant surfaces and identify the nearest collision boundary.

At each X, also measure a floor/ceiling profile across Y: centerline, both intended foot/rail corridors once defined, floor step edges, sill transitions and wheel-house edges. Record the Y locations instead of assuming a regular floor. Headliner and panoramic glass require multiple Y samples; a center roof height alone is insufficient.

## 4. Prioritized construction measurements

| Priority | Required data | How to capture it |
|---|---|---|
| P0 | Datum, reference targets, configuration | First photo batch; then survey fixed hard targets and independent diagonals. |
| P1 | Seat width and center aisle | Independent side profiles at B/C/D/E, especially cushion, armrest and shoulder levels. Include inward door handles, pockets, buckles and vents. Width must cover the entire seat sweep, not one appealing section. |
| P1 | Third-row entry | Both opening outlines; sill top/step; B/C-pillar surfaces; door open angle and inside panel; footwell and row-3 cushion front. Sample each aperture perimeter at corners, curvature changes and multiple horizontal heights. |
| P1 | Mounting and rail space | Fixed attachment centers/contact faces, their Z heights, floor steps, wiring/duct/trim obstructions and available longitudinal corridor. Hidden attachment geometry stays unknown until properly exposed and measured. |
| P1 | Recline and footrest space | Full front-seatback and console envelopes; row-3 front surface; floor; door/pillar boundaries. Front seat slide, height and recline combinations need separate positions and measured pivots/sweeps. |
| P1 | Factory row-3 folding | Both seat halves upright and folded, hinge/pivot locations if accessible, latch positions, headrests, hinge covers and intermediate sweep. A folded endpoint alone does not verify unobstructed folding. |
| P2 | Wheel housings and cargo | Each side's trim separately, width profile by X/Z, floor levels, cargo panel states and **closed** hatch boundary. Distinguish structural housing from visible trim. |
| P2 | Roof and headliner | Glass perimeter, crossmembers, grab handles, roof transitions and lowest intrusions over seating/entry paths. |
| P3 | Screens, tables and cooler | Defer actual component sizing until base geometry is validated. Later measure full hardware, mounts, hinges, thickness, cable exits and complete moving envelopes. |

This is a geometric feasibility model. Seat mounting, belts/airbags and electrical integration require separate engineering; a collision-free package does not establish a safe installation. The present first batch requires no disassembly.

## 5. Photogrammetry capture

**Pilot first:** capture about 30–50 overlapping images of one rear-door/floor/C-pillar area with fixed targets and two independently measured scale spans. We will check sharpness, texture, exposure, reconstruction connectivity and scale before you shoot hundreds.

Use the main camera lens at a fixed zoom; avoid panoramas, portrait-depth effects, automatic macro/lens switching and digital zoom. Preserve original resolution and metadata. With sufficient diffuse light, begin around 1/125 s or faster for handheld capture, then inspect actual sharpness. Lock exposure/white balance during a lighting-consistent pass. Lock focus within a useful distance range; if near/far regions require refocusing, record separate camera groups. Do not sacrifice sharpness simply to keep a focus lock.

Move the camera between shots so depth can be triangulated. Aim for **about 80% overlap** in the direction of travel and 70–80% between elevation passes. For a surface strip of visible width W, camera progression projected onto that strip should be approximately 0.2W for 80% overlap; adapt to range and geometry. Overlap is coverage, not a fixed time interval. Use oblique views from both directions in addition to near-normal views. The [Meshroom capture guidance](https://meshroom-manual.readthedocs.io/en/latest/capturing/capturing.html) supports fixed focal length, diffuse lighting and strong overlapping coverage.

Suggested coverage budget per static configuration, adjusted after the pilot:

| Pass | Coverage |
|---|---|
| Low | 60–100 images of floor, sills, bases, rails and third-row footwell from both doors and hatch. |
| Mid | 60–100 images of trim, pillar transitions, door pockets and seatback boundaries. |
| High | 60–100 images looking at headliner, roof edges, handles and upper pillars. |
| Local detail | 20–40 additional views for each poorly visible hinge, wheel-house corner or floor step. |

Counts are planning estimates. A smaller complete sharp set is better evidence than a large disconnected one. Every difficult area needs tie images linking it to fixed body targets in the main set. Inspect dark recesses at full resolution before leaving the vehicle.

**Scale and targets:** place uniquely labeled matte targets on stable supported surfaces, distributed front/rear, left/right and low/high. Avoid putting all controls on one plane. Use rigid bars with precisely identified endpoint marks and independently measure their actual mark-to-mark lengths; nominal meter-stick branding or print size is not calibration. Include longitudinal, lateral and vertical spans at multiple locations. Keep at least some additional spans out of scale fitting for later checks.

AprilTags or ArUco tags are optional useful identifiers. Use one documented dictionary with unique IDs, flat rigid backing, white margins and measured printed black-square side length. Record dictionary, ID, actual size and any backing offset. Never wrap a scale tag around curved trim. Tag detection still requires explicit integration with calibration/registration; dropping tags into COLMAP photographs does not automatically establish metric scale. [OpenCV marker documentation](https://docs.opencv.org/4.13.0/d5/dae/tutorial_aruco_detection.html).

**Materials:** glass, glossy black trim and uniform upholstery may reconstruct poorly. Photograph solid borders and measure the physical glass/headliner separately. Use non-damaging, removable matte target patches after checking surface compatibility. Do not infer actual glass from reflected scenery or fit a smooth roof to fill an unsupported hole. Record any temporary covering thickness; a scan of a cover is a scan of the cover.

**Moving geometry:** never combine seats-up and seats-folded photos into one static reconstruction without masking the moving parts. Build each state separately, align using fixed body targets, then isolate moving assemblies. The same applies to doors, hatch, headrests and cushions. Capture closed-door panels from inside as a separate set; open-door panels cannot be treated as the cabin's closed boundary.

Suggested filenames: `S01_BASE_UP_IMG0001.jpg`, `S02_ROW3_FOLDED_IMG0001.jpg`, `S03_RIGHT_DOOR_OPEN_IMG0001.jpg`. Keep a manifest with original filename, session/configuration, camera/lens, relevant targets and excluded/moving regions. Keep untouched originals and derived files separately.

## 6. Optional phone LiDAR

First confirm the phone model and whether it has LiDAR. The capture app must permit usable mesh/point-cloud export with units or enough information to resolve scale. Before a full scan, test a small export and ensure it opens; app export restrictions vary, and no paid service is assumed here.

Keep the vehicle and relevant parts static. Scan slowly around one compartment at a time, maintaining visible overlap and revisiting starting targets to expose drift. Capture row 2, row 3 and cargo as separate overlapping segments, including the floor and roof edges. Avoid rapid turns, windows and mirrors as tracking anchors. Do a second pass in the reverse direction. Export raw point clouds if available, mesh plus textures, app/version, units, device model and session notes.

Compare repeated scans and independent tape/rigid-bar controls. Treat phone LiDAR as supplemental measured sensor data with an explicitly recorded method. Under the requested A–D taxonomy, keep unvalidated LiDAR-derived dimensions **D** until their acceptance rule is agreed; do not mislabel them C, which is reserved for calibrated photography. It is not a basis for small holes, rail faces or a claimed ±5 mm fit by itself.

## 7. Reconstruction and Blender handoff

Use a pilot to choose the actual free software path for your hardware. COLMAP supports sparse reconstruction and a dense workflow through depth/normal maps, fusion and surface reconstruction. [COLMAP tutorial](https://colmap.github.io/tutorial.html). GPU support depends on build/platform; verify the installed build before promising dense processing on a Mac. [Installation documentation](https://colmap.github.io/install.html). Meshroom's documented MVS path requires an NVIDIA CUDA GPU; CPU draft meshing is not equivalent evidence of dense-surface accuracy. [Meshroom requirements](https://meshroom-manual.readthedocs.io/en/latest/first-steps/install/requirements.html).

Deliver, when actual captures exist: original image manifest; camera calibration and poses; sparse point cloud; dense point cloud; raw mesh; scale/control file; alignment transform; residual report; masked/missing-region map. Preserve raw outputs unchanged.

Register with multiple measured point pairs distributed in three dimensions. [CloudCompare alignment](https://www.cloudcompare.org/doc/wiki/index.php/Align) supports point-pair registration and optional global scale fitting. Use one isotropic scale plus rigid rotation/translation. Check scale independently in X, Y and Z and across front/rear subsets. If one axis or region disagrees, investigate reconstruction drift, lens calibration or control errors; do not stretch the cabin differently in each axis.

Blender convention for this project: numeric coordinates in mm, `unit_system = 'METRIC'`, `scale_length = 0.001`, `length_unit = 'MILLIMETERS'`, so 1000 coordinate units represent 1000 mm. These unit settings do **not** rescale imported vertices. Convert each imported dataset explicitly from its recorded units and verify several known spans. [Blender unit behavior](https://docs.blender.org/manual/id/4.5/scene_layout/scene/properties.html).

Use the requested collections 00_REFERENCE through 16_LIGHTING, retaining all names in the brief. Raw scans stay in 01_SCAN. Future engineered objects must reference source dimension IDs and accepted station/point records. Unsupported patches remain absent or separately labeled D; they cannot enter a critical collision boundary unnoticed. A provisional Blender reference file now represents the published loading box and isolated scalar references; it does not yet supply the engineered cabin surfaces.

## 8. Validation gate

The workbook supplies **40 planned independent checks**, with real/model values blank. These are planned tests, not successful validation results. Reserve holdout measurements before fitting the scan/surfaces. Reusing only fit controls cannot independently demonstrate accuracy.

For each check record the exact points/surface measurement algorithm and configuration, raw observations, source/class/confidence, measured/model lengths in mm and inches, signed difference `model − real`, absolute difference, percentage error `100 × (model − real)/real` when real is nonzero, tolerance, uncertainty and disposition. For zero-valued coordinates, use mm error and leave percentage error undefined.

Targets from your brief: critical seating/floor ±5 mm (0.20 in), major interior surfaces ±10 mm (0.39 in), exterior reference ±15 mm (0.59 in). A conservative proposed release criterion is `absolute error + measurement uncertainty ≤ tolerance`; state the uncertainty definition used. If uncertainty has not been established, do not claim tolerance compliance just because a nominal error is small.

Critical surfaces also need local scan-to-model distance maps and physical spot checks at high curvature, hinge corners and narrow passages. An average or RMS alone can hide a local collision. Stop for missing data or critical failures; correct or remeasure before executive-seat design. The first accepted geometry review will include the five requested orthographic views/cross-sections plus dimension and error tables. Seat boxes, entry paths and cargo capacity follow only when their input geometry exists.

Later occupant and package studies remain pending: define anthropometric population, posture, clothing and reach data; do not create a 95th-percentile person by setting every body dimension to its individual 95th percentile. Chair supplier geometry and articulation are also needed. Evaluate all four entry options, all seat modes and retained third-row folding with swept volumes; static endpoint checks are insufficient.

Cargo will use bounded usable voids with the hatch closed, specified seat state and stated inclusion of underfloor storage, reported in L and ft³ with boundary uncertainty. Luggage remains at the brief's 558.8 × 355.6 × 228.6 mm (22 × 14 × 9 in) and 660.4 × 457.2 × 279.4 mm (26 × 18 × 11 in), with handles/wheels included or explicitly added. No packing result or volume is claimed now.

Unreal rendering remains contingent on your geometry approval. Export scale and axis conversion will be verified with a known-length test object and asymmetric left/right markers before any finished interior rendering.
