# 2023 Rivian R1S cabin digital twin

A measurement-led reconstruction for a six-passenger executive interior, using the owner's physical vehicle as the final dimensional authority.

**Current state:** provisional online-reference modeling and acquisition planning. A source-driven Blender loading-envelope model now exists. Cabin surfaces, executive seats, scans and fit results remain pending. No commercial vehicle model is used.

The owner has authorized using online measurements now and readjusting after physical measurement. This supersedes the original blanket pause on all modeling. Online data can drive explicitly provisional references; physical cabin validation and the approval requirement for finished renders still apply.

Open [the Blender reference scene](outputs/R1S_provisional_reference.blend) or inspect [the orthographic reference sheet](outputs/provisional_reference_views.svg). [Model notes](outputs/provisional_model_notes.md) explain exactly what the geometry represents and how to update it.

The [interactive preview](outputs/r1s-working-preview.html) supports dimension changes, four views, drag rotation and a moving 22 × 14 × 9 inch carry-on reference. It is an inline HTML fragment with no network dependencies; Codex supplies its theme and controls styling. It checks containment in the published loading box, not clearance against vehicle surfaces. Edited values become class D local what-if values and do not alter the dimension register or Blender file. See [project status](PROJECT_STATUS.md) for tested behavior and the next work items.

## Start

Read [the first capture request](outputs/START_HERE.md). It specifies twelve initial photographs and eight measurement groups to establish the next survey step.

When captures arrive, use the [measurement intake instructions and blank form](data/measurements/README.md). The importer preserves raw observations in separate, immutable batches, reports missing metadata, and normalizes units without changing the online register or authorizing model geometry.

The [measurement mapping review](data/measurements/MAPPING.md) checks explicit observation-to-parameter proposals against endpoint definitions, configurations and evidence. It reports incompatible captures and conflicting repeats without averaging or applying them. The [current report](outputs/measurement_mapping_review.json) contains no proposals because owner captures are still pending.

The research package contains:

- [Research findings and conflicts](outputs/research_findings.md)
- [Coordinate system, measurement and capture procedure](outputs/measurement_and_capture_plan.md)
- [Dimension and field workbook](outputs/R1S_dimension_register.xlsx): 69 source claims, 21 sources, 99 station rows, 40 planned validation checks and 12 component requirements
- [Machine-readable dimension database](outputs/dimension_database.json)
- [Original owner brief](project_brief.txt)

The workbook holds a reference register, not an accepted engineering dataset. A published dimension retains its measurement definition and model-year scope. Every current source claim is excluded from driving target-cabin geometry. Missing physical measurements remain null/blank.

## Project rules

Use millimeters and X forward, Y driver-side, Z up. Select repeatable hard datum points from actual vehicle photographs and measurements. Preserve left/right differences and raw observations. Classify every future geometry-driving dimension as A, B, C or D with source and uncertainty. Continue provisional source-based work while critical geometry is missing, but do not claim fit or validation from those references. Validate the base cabin before executive-seat design. Finished rendering requires the owner's geometry approval.

## Structure

`outputs/` contains the current review package. `scripts/` contains reproducible builders. `work/` is local scratch space and is ignored by Git. Large original photographs and scans may be placed in `captures/raw/` and `scans/raw/`; those paths are ignored to avoid putting large raw datasets in ordinary Git. Their manifests and accepted measurement records should be versioned alongside the model when capture begins.

## Rebuild

Run `python3 scripts/build_data.py` to regenerate the initial JSON register. It uses Python's standard library. It overwrites the generated register, so migrate newly collected measurements into maintained input records before rebuilding after capture starts.

Run `node scripts/build_workbook.mjs` in an environment providing `@oai/artifact-tool`. The workbook builder reads the JSON, generates formulas and blank field sheets, checks conversion and tolerance logic, renders inspection previews to `work/`, and writes the workbook. The local Codex dependency runtime provided this package for the initial build; it is not vendored into this repository.

The initial builder intentionally produces blank acquisition/validation sheets; it is not a round-trip editor for subsequently completed field workbooks. Preserve filled workbooks as separate versioned acquisition records.

Run `blender --background --python scripts/build_reference_model.py` to rebuild the provisional scene and technical drawing from the dimension database and `outputs/reference_model_config.json`. The script checks dimensional extents and parameter propagation. Blender 4.5.7 was downloaded to local ignored `work/` for the initial build; no paid service is used.
