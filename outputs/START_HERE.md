# Rivian R1S digital twin — first capture

2023 vehicle · Phase 0/1 handoff · 9 September 2026

**A provisional online-reference Blender scene now exists; the cabin is not validated.** The owner authorized starting with online dimensions and readjusting later. See `provisional_model_notes.md`. No seat width, aisle clearance, recline limit or cargo volume has been inferred from published passenger-space figures. No commercial vehicle model was acquired or used.

The research register distinguishes published claims from dimensions that can actually constrain your cabin. Read `research_findings.md` for conflicts and sources, `measurement_and_capture_plan.md` for the full procedure, and use `R1S_dimension_register.xlsx` for the dimension register, measurement sheets and future validation. `dimension_database.json` preserves machine-readable provenance.

## Send this first

Start with the photographs below. They let us identify repeatable hard datum features before asking you to survey the entire cabin. Keep the factory seats installed for this first batch. Your brief mentions a supplied measurement photograph, but the only attachment received was text: please also attach the original measurement photo if you have it.

**Tell me:** trim/interior, build month if known, whether seats or trim have been modified, phone/camera model, available measuring tools, and the computer/OS/GPU available for reconstruction. A full VIN is unnecessary.

Park on a firm level surface, use one recorded suspension setting, empty loose cargo and remove removable floor mats. Record front-seat positions using your normal driving and front-passenger settings. Do not move the seats between baseline pictures. A wide overview plus a close view is preferable to one distorted panorama.

| Photo IDs | What to photograph |
|---|---|
| P01–P02 | Hatch looking forward: one with row 3 upright, one with row 3 folded. Keep row 2 unchanged. |
| P03–P04 | Each rear doorway looking across row 2, showing floor, seat base and opposite door trim. |
| P05–P06 | Each rear doorway approximately square-on, showing the entire opening, sill, B-pillar and C-pillar. |
| P07–P08 | Low views under/around each second-row seat base showing exposed fixed rails, mounting covers and floor steps. Do not remove fasteners. |
| P09–P10 | Cargo floor hard-edge/rail mounting areas on both sides, plus any accessible fixed hard features suitable for repeatable targets. Include surrounding context. |
| P11 | Roof/headliner above row 2 and the transition toward row 3. |
| P12 | Roof/headliner above row 3, glass boundaries and hatch header. |

Include a rigid ruler in the same local region where practical. These first pictures locate features; they are not a calibrated scan. Use original full-resolution files, not screenshots or messaging-app reductions.

## First measurements — after, or alongside, those photographs

These are reconnaissance distances, not a completed XYZ survey. Mark both endpoints with small removable labels and photograph each span and its readout. Take three independent readings, lifting and resetting the tool each time; report all three in millimeters. Do not round to a convenient inch. Use a level rigid/telescoping rule where possible. A tape must be straight, supported and lightly tensioned.

| ID | Exact request |
|---|---|
| F01 | **Closed rear-door trim width at the front edge of the second-row cushion.** With row 2 in a recorded latched position, establish one transverse plane through the passenger cushion's front edge. Transfer that plane across the cabin with a square/laser. At the measured height of that cushion's front upper surface, measure a horizontal span between the nearest inside door-trim surfaces. Record the height above a labeled local floor point and photograph it. Do not press into padding. |
| F02 | **Closed rear-door width at armrest level, in the same transverse plane.** Identify and record the actual height used. Measure the inside projections, not window glass. If an armrest lies outside this plane, photograph it and record its own station separately. |
| F03–F04 | **Front-to-third-row available length on each side.** With row 3 upright and the front seats at the recorded baseline, measure the horizontal longitudinal gap from the rearmost front-seatback surface to the foremost third-row cushion edge at the third-row cushion-front height. Use a level rule to project the seatback to that height. Record the lateral line and both endpoint photos. If row 2 blocks a straight measurement, leave blank; do not measure a bent tape over it. |
| F05–F06 | **Both rear-door openings at sill + 300 mm (11.81 in).** Doors fully open. Measure the horizontal clear front-to-rear opening between the nearest trim/seal boundaries at this height. Also take a vertical clear height from the sill top to the nearest header at the midpoint of this width. Mark the sill point and both ends. These are local sill offsets, not global Z coordinates. |
| F07 | **Narrow rear-trim width.** With row 3 folded, measure across the most inward left and right cupholder/armrest projections wherever they overlap longitudinally. Record the exact height and location. Separately measure a floor-level width in that same plane. If their narrowest points are at different X locations, report each location rather than taking a diagonal. |
| F08 | **Cargo depth with row 3 upright and both hatch parts closed.** Along the vehicle centerline at the cargo floor's height, measure horizontally from the rearmost third-row seatback surface to the nearest inner face of the closed rear closure. Use an interior-accessible rule/laser target. If you cannot see/reach both endpoints, leave blank and send photographs. The open lower tailgate edge is not the closed-hatch boundary. |

If a door needs opening to position the tool, close and latch it before taking a closed-door measurement. Keep yourself and the tool clear of closure movement.

**The next decision:** select and document the actual hard datum points, then issue the fixed station/target map on your own photographs. No detailed cabin or executive-seat geometry will be substituted for missing measurements.
