# Review measurement-to-parameter proposals

Run from the project root:

```sh
python3 scripts/review_measurement_mapping.py
```

The command reads `parameter_mapping.json` and imported capture batches. It prints a review report and writes nothing. To save a report explicitly, redirect stdout to a new report file. The checked-in report records the current empty intake; zero proposals means no measurements are ready, not that validation passed.

Add a parameter definition only when the endpoints and capture configuration are known. Each parameter needs `id`, `definition`, `quantity`, `side`, `endpoint_from`, `endpoint_to`, `vehicle` and `configuration`. Use the same fields and permitted values as the capture form. Coordinates also need `datum_id`. IDs use letters, digits, hyphens and underscores. No numerical value belongs in this definition: values come from the referenced observation.

Add one mapping object per proposed observation, with `parameter_id` and `observation_ref` in `batch_id/observation_id` form. Driver and passenger measurements require independent parameter definitions. Repeat observations can map to the same parameter. Definitions and capture metadata must match exactly; the script never guesses synonyms, reverses endpoint order, transforms datums, averages repetitions or interprets an SAE room specification as a trim width. If endpoint names differ, inspect the evidence and record a justified corrected capture batch; never rename a physical feature merely to pass the check.

The report checks original capture checksums, rechecks evidence and unit normalization, and compares quantity, side, vehicle, full seat/door/hatch configuration, endpoints and coordinate datum. A missing capture, stale evidence, incomplete observation or mismatched definition is `BLOCKED`. Metadata-compatible observations are `READY_FOR_REVIEW`, which still requires inspecting their evidence and any datum/calibration records. Matching text alone cannot prove identical physical endpoints. No B/C classification is accepted automatically, and model geometry stays unauthorized.

Repeated compatible observations with non-overlapping stated uncertainty bounds are `CONFLICT`. This is an inconsistency flag, not a statistical significance test. Overlapping bounds do not prove accuracy or independence. The script neither chooses a preferred measurement nor shrinks uncertainty by averaging. Resolve conflicts through evidence review or new independent measurements.

This workflow proposes owner-cabin parameters separately from immutable published source claims. It cannot replace the 2022 published comfortable loading-box dimensions with a 2023 trim measurement. Blender and the interactive preview continue using their explicit source mapping until a later reviewed model update is implemented. There is intentionally no `--apply` or geometry-approval switch.
