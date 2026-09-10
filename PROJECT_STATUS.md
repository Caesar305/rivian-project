# Project status

Updated: 2026-09-10. Phase: provisional online references and measurement acquisition tooling. The target 2023 cabin is not yet reconstructed or validated.

## Completed

- Researched 69 dimensional claims from 21 source records, preserving conflicting definitions and model-year scope.
- Created the dimensional workbook, station survey, independent validation checks and initial capture instructions.
- Built and reopened a Blender 4.5.7 scene with 17 collections, three driven loading-box dimensions and separate reference rulers. Verified source dimensions and driver propagation. The scene contains no inferred trim surfaces.
- Built an interactive preview with 3D rotation, orthographic views, editable dimensions and carry-on translation. Online source values remain separate from local what-if values.
- Implemented separate append-only measurement intake with a blank capture form, original source text and checksum, local evidence checksums, mm conversion, independent observation IDs, incomplete-data findings and explicit pending-review classification. Duplicate batch IDs cannot overwrite existing records; the importer cannot update model geometry.
- Added read-only measurement-to-parameter proposal review. It rechecks capture/evidence integrity, matches endpoint definitions, independent sides, vehicle and seat/door/hatch configurations, and coordinate datum IDs. Conflicting repeat bounds are reported without averaging or selecting a preferred observation. No geometry or classification is accepted automatically.
- Unified preview and Blender source resolution with unit, axis-role and measurement-definition checks. Regenerated the preview and Blender scene; both include the same source fingerprint. The preview defaults, source table and classification are generated from the register, while local what-if values remain D.
- Enabled the hourly “Continue Rivian digital twin” task. Continue useful work; pause when required owner input or geometry approval becomes the limiting dependency. This is a scheduled continuation, not an unbounded compute loop.

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

1. Inspect the still-unretrieved free sleeping-platform STEP lead from S005J: https://www.printables.com/fr/model/551407-rivian-r1s-sleeping-platform. Determine whether the actual files are available, their license and coordinate units, and whether any geometry offers useful accessory reference. Keep it separate from the cabin and do not treat product extents as trim or seat coordinates. Record the outcome once; do not repeatedly retry an inaccessible listing.
2. Continue only targeted research that can resolve a named geometry gap. Existing source coverage and rejected leads are in `outputs/research_findings.md`; do not repeatedly search for the same absent full cabin model. If the remaining leads cannot add usable geometry, pause for owner captures instead of extending tooling indefinitely.
3. When owner captures arrive, define capture-backed parameter endpoints/configurations, use the intake and mapping review, register the vehicle datum, accept B/C records deliberately, and reconstruct and independently validate the base cabin. Executive seats and finished rendering remain later gated phases under the owner's brief.

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

## Reproducibility and preservation

- Read the brief and latest owner instructions before changing scope.
- `scripts/build_data.py` regenerates the initial dataset; do not run it over newly acquired records without migrating and preserving them.
- Preview edits are local exploration only; they are not a measurement import mechanism.
- Keep original photos/scans in the ignored capture paths and version their provenance manifests rather than silently dropping their provenance.
- Commit and push completed work to the existing `main` branch without resetting or overwriting owner changes.
