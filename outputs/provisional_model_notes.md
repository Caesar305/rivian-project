# Provisional online-reference model

The owner authorized starting from online measurements and readjusting after physical measurement. We can develop the parameter system, source links, scene organization and reference geometry immediately while collecting the information needed for a reliable cabin reconstruction.

## What exists

`R1S_provisional_reference.blend` contains the requested 17 collections. Its visible object is the published comfortable cargo-loading box measured by Andrew P. Collins on a 2022 media R1S with rows 2 and 3 folded: **2057.4 × 1079.5 × 711.2 mm (81 × 42.5 × 28 in)**, linked to records D056, D055 and D057. These are class A published measurements, confidence 4, on a different vehicle. They do not become class B just because a Blender object uses them. [Original measurement and methodology](https://www.thedrive.com/news/we-measured-the-2022-rivian-r1ss-cargo-storage-to-determine-its-usable-space).

The wire box is a loading reference, not a model of the floor, door panels or roof. Its rear-center-bottom display origin and centering are explicitly class D. The actual structural datum transform is still unknown.

Hidden subcollections contain independently selectable reference spans for cargo-length conflicts and passenger-space specifications. They are isolated scalar rulers with illustrative orientation and no established cabin placement. In particular, the two behind-row-2 claims remain separate: D030 = 1315 mm (51.77 in) and D058 = 1465.58 mm (57.7 in). The difference is 150.58 mm (5.93 in), with unresolved endpoint/configuration differences. [Recipient's support-email report](https://www.reddit.com/r/Rivian/comments/vssjer/r1s_interieor_dimensions/), [second source relay](https://www.rivianforums.com/forum/threads/r1s-size-comparisons-to-other-suvs-and-trucks.5699/page-2).

The three views in `provisional_reference_views.svg` show this same box, with mm/in labels. They are reference projections, not the requested final cabin cutaways or row-specific cross-sections. Different views use different drawing scales, preserving shape proportions within each view.

## Updating dimensions

1. In Blender, select `SOURCE_PARAMETERS_mm` in `13_MEASUREMENTS` and inspect its custom properties. The visible box has drivers for length, width and height. Each property has a source ID and provenance description. A local edit updates the box immediately but is an unverified override until recorded.
2. For a persistent update, import a separate owner capture with photos, endpoints, configuration and uncertainty using `scripts/import_measurements.py`. A physical measurement is claimed B but remains effectively D pending review. Use the measurement mapping review to propose its owner-cabin parameter. Preserve the original online claim.
3. Update `reference_model_config.json` only when the new measurement has equivalent meaning. A physical trim width cannot replace a comfortable-box width without changing the object's definition. The eventual true cabin surfaces will be separate geometry driven by measured stations and scans.
4. Run `python3 scripts/build_preview.py` and `blender --background --python-exit-code 1 --python scripts/build_reference_model.py`. Both resolve the same checked source mapping. They generate the preview, scene, drawing and build report. This is a deterministic reference-scene builder: save manual Blender edits under a separate filename before rebuilding, because it recreates the reference scene.

The preview template contains no independent loading-box dimensions. Generated defaults, source table and classification come from the source register. The Blender scene and its build report store the same source fingerprint as the preview, including definitions and provenance. `scripts/verify_reference_model.py`, run in Blender with the saved scene open, checks the actual saved dimensions and source parameters along with the report and preview. These are rebuild consistency checks, not physical calibration or automatic acceptance of owner measurements.

The build test checks the published box dimensions, temporarily changes length by 100 mm, confirms propagation, and restores the original. This is software verification, not vehicle-dimensional validation. The build report explicitly separates those states.

## What this advances

We now have a working Blender file, millimeter convention, collection structure, source-linked parameters, technical projections and a repeatable rebuild. Those can be reused as physical measurements arrive. Unknown floor steps, pillars, door openings and seat hardware remain explicit missing geometry. Until those exist, the model cannot establish maximum chair width, aisle feasibility, recline, luggage fit or actual cargo volume.

The initial workbook remains a source/measurement register. Its “Use in geometry” column refers to accepted **target-cabin engineering geometry**; “No” does not prohibit the provisional reference objects now authorized by the owner. This clarification preserves the original claims without promoting them to validated cabin data.
