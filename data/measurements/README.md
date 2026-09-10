# Owner measurement intake

Copy `blank_capture.json` into a new file under `captures/raw/`, replace its IDs, and fill the fields from an actual capture. Null means unknown, never zero. Keep one observation per independently measured side and repeat; use a new ID for each. A distance spanning the cabin uses `cross_cabin`, not a mirrored pair. Observation references are qualified as `batch_id/observation_id`.

From the repository root, assess without saving:

```sh
python3 scripts/import_measurements.py captures/raw/my-capture.json --check
```

Remove `--check` to preserve a batch under `data/measurements/batches/`. A successful import preserves incomplete observations as well as complete ones; read each observation's `issues`. Exit code 0 means the import/check operation succeeded, not that the dimensions are valid. Malformed JSON, ambiguous duplicate keys/IDs and unsafe batch IDs are rejected before any batch is written. An existing batch ID is never overwritten, even if the new content is identical. Corrections require a new batch ID and a note referencing the prior observation; retain both for review.

Each stored batch includes the original JSON text, source checksum, normalized millimeter values, local evidence checksums and metadata findings. Source evidence paths must resolve inside this repository; paths escaping via symlinks are rejected. Raw photographs remain in the ignored capture directories: keep a separate backup because checksums do not preserve image content. Filenames alone do not prove measurement accuracy.

Use `B` for direct physical measurements, `C` for calibrated photographic derivations, or `D` for estimates. The import preserves this as the **claimed** classification. The effective classification stays D pending review, and `geometry_authorized` stays false even when all metadata is complete. A named datum/calibration must later be inspected and registered; providing its ID does not validate it. No confidence score is assigned automatically. The online database, Blender scene and preview are never modified by this importer.

Distances must be positive; signed x/y/z coordinates may be negative or zero. Units are `mm` or `in`. Uncertainty is a positive absolute bound in the same unit, with an explanation of how it was obtained. Missing uncertainty is an incomplete observation, not an assumed perfect measurement. Record exact endpoint features, instrument, observer, timestamp with timezone, and all seat/door/hatch configurations. Coordinate values need a datum ID; class C observations also need a calibration ID. Subsequent review must verify these references and the evidence itself before accepting geometry.

The initial-data builder writes only the online register under `outputs/`; it does not touch this separate intake directory. Do not copy synthetic test fixtures into real capture batches.

After import, use the [mapping review workflow](MAPPING.md) to propose which observation describes which owner-cabin parameter. This is a separate read-only review, not automatic acceptance or a model update.
