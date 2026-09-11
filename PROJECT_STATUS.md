# Project status

Updated: 2026-09-11 UTC. Phase: waiting for owner captures. The target 2023 cabin is not yet reconstructed or validated. Hourly continuation is PAUSED to avoid repeated research or tooling work without new evidence.

## Completed

- Researched 69 dimensional claims from 21 source records, preserving conflicting definitions and model-year scope.
- Created the dimensional workbook, station survey, independent validation checks and initial capture instructions.
- Built and reopened a Blender 4.5.7 scene with 17 collections, three driven loading-box dimensions and separate reference rulers. Verified source dimensions and driver propagation. The scene contains no inferred trim surfaces.
- Built an interactive preview with 3D rotation, orthographic views, editable dimensions and carry-on translation. Online source values remain separate from local what-if values.
- Implemented separate append-only measurement intake with a blank capture form, original source text and checksum, local evidence checksums, mm conversion, independent observation IDs, incomplete-data findings and explicit pending-review classification. Duplicate batch IDs cannot overwrite existing records; the importer cannot update model geometry.
- Added read-only measurement-to-parameter proposal review. It rechecks capture/evidence integrity, matches endpoint definitions, independent sides, vehicle and seat/door/hatch configurations, and coordinate datum IDs. Conflicting repeat bounds are reported without averaging or selecting a preferred observation. No geometry or classification is accepted automatically.
- Unified preview and Blender source resolution with unit, axis-role and measurement-definition checks. Regenerated the preview and Blender scene; both include the same source fingerprint. The preview defaults, source table and classification are generated from the register, while local what-if values remain D.
- Inspected the S14 live files page and confirmed its single STEP accessory listing. The browser download event did not expose a usable local file; units, dimensions and contents remain uninspected. The outcome is documented in `outputs/free_reference_assessment.md`. No external CAD geometry was imported.
- The hourly “Continue Rivian digital twin” task was enabled for independent preparation, then paused on 2026-09-11 UTC when owner captures became the next useful dependency. The project is not complete.

## Preview verification

Checked in the live Codex browser on 2026-09-10:

- Initial dimensions: 2057.4 × 1079.5 × 711.2 mm. Centered carry-on reports inside the reference box with approximately 361.95 mm minimum side/end/top margin.
- Width changed to 300 mm: classification changes to D and reports 27.8 mm outside the reference box.
- Restore published dimensions: original dimensions and A source classification return.
- Travel at 0: reports 558.8 mm outside; travel at 50 returns to the centered, contained state.
- Top view renders the scaled envelope and centered carry-on without clipping at the inspected browser width.
- Dragging changes the 3D orientation. A zero-height input leaves the valid geometry unchanged and triggers native validation; restoring clears the invalid input.

These checks establish software behavior only. They do not validate vehicle fit. Source A applies to the reported loading-box measurements on the author's 2022 media vehicle; placement within the owner's vehicle remains class D.

## Measurement intake verification

Measurement intake is implemented in `scripts/import_measurements.py`; instructions and a blank form are under `data/measurements/`. Seven synthetic regression tests pass, covering signed/zero coordinates, independent sides, unit conversion, preservation of incomplete records, overwrite refusal, calibration/datum requirements, invalid values, unsafe paths and conversion overflow. The blank form was checked without saving a batch. No real observations have been imported. Datum/calibration IDs are captured for review, not yet registered or verified.

## Next concrete work

1. Await four owner overview photos: hatch looking forward with row 3 upright, the same view with row 3 folded, and one view through each rear doorway showing the second-row floor and seat bases. Include a rigid ruler near a hard floor/rail feature where practical; keep front seats and row 2 in the same recorded positions. This focused request is issued once at the pause, rather than repeatedly asking for the full survey.
2. On receipt, inspect the actual vehicle features, select repeatable datum candidates and mark the next exact measurement endpoints. Then use the intake/mapping workflow, register the datum and accept B/C records deliberately before reconstructing and independently validating the cabin. Executive seats and finished rendering remain later gated phases under the owner's brief.
3. If a local copy of `R1S_Sleep_Platform_V1.stp` becomes available, inspect its units and assembly separately as an accessory reference. Do not schedule retries of the same listing or infer cabin surfaces from platform dimensions.

## Mapping review verification

All 14 intake/mapping regression tests pass. Seven new mapping tests cover unchanged files during review, endpoint/side/configuration mismatches, coordinate-datum mismatches, conflicting and touching repeat bounds, changed evidence and source checksums, missing captures, unsafe references, duplicate proposals and unmapped parameters. Test measurements are synthetic and live only in temporary test directories.

`outputs/measurement_mapping_review.json` was generated from the current empty mapping catalogue. It contains zero proposals, not a validation pass. No owner-cabin parameters or real observations have been invented to populate the report. The review supports future proposals but deliberately does not apply values to Blender; that step depends on reviewed real captures.

## Shared-source verification

All 20 regression tests pass. The six source tests cover generated preview consistency, propagation of a synthetic source change, missing/non-finite/negative lengths, unit mismatch, changed measurement scope/definitions, swapped axes, duplicate source IDs, missing definition contracts and visible classification changes. Synthetic edits were not saved to the source register.

Rebuilt with Blender 4.5.7, confirmed driver propagation, then reopened the saved `.blend` and ran `scripts/verify_reference_model.py`: geometry dimensions, source parameter values, millimeter units, build report and preview match. In the browser, verified the new source fingerprint, a 300 mm width override reporting 27.8 mm outside the reference box, and restore returning the source defaults. No vehicle-dimensional validation was performed.

## Missing inputs

No owner measurement records, photographs or scans have been supplied. The initial request is `outputs/START_HERE.md`: twelve photographs and eight measurement groups. The full survey and tolerances are in `outputs/measurement_and_capture_plan.md`.

Unknown geometry includes structural datum, floor, closed-door trim, door openings, pillars, wheel houses, headliner, glass roof, seat bodies, seat attachments and hatch interior. Published passenger-room specifications and comfortable loading-box dimensions cannot locate these surfaces.

Do not ask for the same capture package on every run. Complete the independent tasks above first; if no useful work remains without owner captures, make one focused input request and pause the hourly continuation.

Pause action completed through the automation tool: `continue-rivian-digital-twin` status `PAUSED`. Resume useful work when owner evidence arrives; do not mark the cabin or overall project complete merely because preparation is finished.

## Reproducibility and preservation

- Read the brief and latest owner instructions before changing scope.
- `scripts/build_data.py` regenerates the initial dataset; do not run it over newly acquired records without migrating and preserving them.
- Preview edits are local exploration only; they are not a measurement import mechanism.
- Keep original photos/scans in the ignored capture paths and version their provenance manifests rather than silently dropping their provenance.
- Commit and push completed work to the existing `main` branch without resetting or overwriting owner changes.
