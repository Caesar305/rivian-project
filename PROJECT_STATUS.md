# Project status

Updated: 2026-09-10. Phase: provisional online references and measurement acquisition tooling. The target 2023 cabin is not yet reconstructed or validated.

## Completed

- Researched 69 dimensional claims from 21 source records, preserving conflicting definitions and model-year scope.
- Created the dimensional workbook, station survey, independent validation checks and initial capture instructions.
- Built and reopened a Blender 4.5.7 scene with 17 collections, three driven loading-box dimensions and separate reference rulers. Verified source dimensions and driver propagation. The scene contains no inferred trim surfaces.
- Built an interactive preview with 3D rotation, orthographic views, editable dimensions and carry-on translation. Online source values remain separate from local what-if values.
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

## Next concrete work

1. Implement an append-only owner-measurement import path with source file references, independent left/right observations, endpoint definitions, vehicle/seat configuration, units, uncertainty and datum registration. Reject incomplete records from geometry use while retaining raw observations. Keep it separate from the initial-data generator so new captures cannot be erased by a rebuild.
2. Add deliberate measurement-to-parameter mapping and a review report showing what can be updated, what conflicts, and what still lacks equivalent endpoints. No automatic promotion from an arbitrary measurement to a validated cabin dimension.
3. Generate preview defaults from the same source mapping used by Blender so updates cannot silently diverge; add meaningful checks for mismatched source definitions and missing values.
4. Continue only targeted research that can resolve a named geometry gap. Existing source coverage and rejected leads are in `outputs/research_findings.md`; do not repeatedly search for the same absent full cabin model.
5. When owner captures arrive, register the vehicle datum, add B/C records, reconstruct and independently validate the base cabin. Executive seats and finished rendering remain later gated phases under the owner's brief.

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
