# Rivian R1S dimensional research

Research date: 9 September 2026. Target: the owner's 2023 R1S, especially front seatbacks to rear hatch.

## Finding

Free public information supports an initial reference register and helps identify accessible geometry. It does **not** establish the measured cross-sections, floor elevations, seat attachments or motion envelopes necessary for a ±5 mm cabin model. This is a systematic first research pass across the requested source categories, not a claim that every public file has been found. No complete free, dimensionally validated 2023 cabin model or survey was located in this pass.

The dimension database stores source claims separately. Repeated quotations of one Rivian support response are not independent measurements. No dimensions qualify as **B** (measured on your vehicle) or **C** (derived from your calibrated photographs) yet.

## Classification and use

| Class | Meaning in this project |
|---|---|
| A | Verified OEM/published dimension, within its stated scope. This verifies the published claim, not its applicability to your individual vehicle. |
| B | Physical measurement from your R1S, with identifiable endpoints and configuration. |
| C | Derived from calibrated photography, with calibration and uncertainty references. |
| D | Estimated, unverified, relayed or unresolved claim. Never a silent geometry default. |

Confidence follows your 1–5 scale. A source can have confidence 5 yet be unsuitable for cabin geometry: for example an OEM mirror width or current-model specification. Relayed preproduction numbers remain D/1. External direct measurement on a different vehicle is published class A, not B. Missing entries have null values and no invented confidence. A converted value retains its source class; conversion does not make it a photographic derivation.

Each dimension also records measurement type, model-year scope, configuration, endpoint definition, uncertainty, conflict group and whether it may drive target-cabin geometry. **Every current source claim has `geometry_authorized: false`.** The unknown survey entries remain missing. Quantities in the brief are kept as separate D leads, even when a corroborating publication exists.

## Decisive conflicts

| Issue | Values | Consequence |
|---|---|---|
| Exterior width | Launch-era Rivian: 81.8 in = 2077.72 mm, **mirrors folded**. Current Rivian comparison: 82.0 in = 2082.8 mm, also mirrors folded. | Neither is cabin width. Retain date/year scope; the 5.08 mm difference cannot be resolved by averaging. [Launch article](https://rivian.com/stories/sizing-up-the-r1s), [current comparison](https://rivian.com/en-US/compare?a=r1t-quad-launch&b=r1t-tri&c=r1t-dual). |
| Rear width | Brief: 51.1 in = 1297.94 mm between wheel housings; a relayed support response calls 1298 mm a **maximum** cargo width and gives 1084 mm = 42.68 in minimum. | The maximum, trim bottleneck and bare wheel housing are distinct surfaces and may occur at different heights. Measure X and Z with every width. [Original recipient's report](https://www.reddit.com/r/Rivian/comments/vssjer/r1s_interieor_dimensions/). |
| 42.5-inch photograph | The Drive measured a comfortable box envelope: width 1079.5 mm / 42.5 in, length 2057.4 mm / 81 in, height 711.2 mm / 28 in. | The author explicitly distinguishes this from maximum cabin dimensions; drawn boxes are not scaled geometry. The brief's original photo has not been supplied. [Author's measurement article](https://www.thedrive.com/news/we-measured-the-2022-rivian-r1ss-cargo-storage-to-determine-its-usable-space). |
| Cargo behind row 2 | Brief: 1468.12 mm / 57.8 in. Support relay: 1315 mm / 51.77 in. Another forum relay: 1465.58 mm / 57.7 in. | Difference of 153.12 mm between the first two is too large to treat as rounding. Seat travel, recline, date or endpoints may explain it, but none is established. Measure recorded configurations. [Support relay](https://www.reddit.com/r/Rivian/comments/vssjer/r1s_interieor_dimensions/), [2022 forum report](https://www.rivianforums.com/forum/threads/r1s-size-comparisons-to-other-suvs-and-trucks.5699/page-2). |
| Cargo behind row 3 | Brief 533.4–553.72 mm / 21–21.8 in; relayed response 553 mm / 21.77 in. | Even roughly 20 mm matters for luggage. Identify floor height, seatback recline and closed hatch surface. [Support relay](https://www.reddit.com/r/Rivian/comments/vssjer/r1s_interieor_dimensions/). |
| Wheelbase | 121.1 in converts to **3075.94 mm**. An indexed NHTSA test-report excerpt lists 121.6 in / 3088.64 mm for a 2023 R1S, with separate side measurements. | The 12.7 mm discrepancy is unresolved. The report PDF did not fully open in this pass; its values remain D discovery leads. Do not scale an interior scan from wheelbase. [Current OEM reference](https://rivian.com/en-US/compare?a=r1t-quad-launch&b=r1t-tri&c=r1t-dual), [government-hosted report lead](https://downloads.regulations.gov/NHTSA-2001-9663-0550/attachment_1.pdf). |
| Overall height | Brief: 77.3 in / 1963.42 mm. Current Rivian calls this **maximum** height and also publishes a minimum. | Record suspension state and roof/antenna endpoint. Height from ground does not define the interior datum. [Current OEM comparison](https://rivian.com/en-US/compare?a=r1t-quad-launch&b=r1t-tri&c=r1t-dual). |
| Passenger-room values | A November 2020 support-email transcription includes SAE-labeled hip, shoulder, headroom, legroom, couple-distance and seat-height values. | This predates production. Values and SAE codes are useful research leads; none specifies arbitrary door-to-door trim spacing or a measured occupant H-point in your vehicle. [Original poster, post 148](https://www.rivianforums.com/forum/threads/what-we-know-collecting-information-directly-from-rivian.827/page-10#post-15113). |
| Cargo volume | OEM launch article reports 17.6 ft³ behind row 3; support relay gives 499 L behind row 3 and 2499 L behind row 1, with 2966 L total enclosed storage. | Total storage includes a different collection of compartments from the rear cabin. Do not set model volume to a marketing aggregate. [OEM](https://rivian.com/stories/sizing-up-the-r1s), [relay](https://www.reddit.com/r/Rivian/comments/vssjer/r1s_interieor_dimensions/). |

Exact unit conversions above do not imply that the source was measured to hundredths of a millimeter.

## Source search coverage

| Category | Result and appropriate use |
|---|---|
| OEM documentation and owner's guides | Located [February 2023 owner's guide](https://assets.rivian.com/2md5qhoeajym/7Ao7NIFkLxOZtvdc7Fqh70/fff272692b97bdd50251339da18fa594/r1s-og-en-us-20230227.pdf) and [guide explicitly covering MY2022–2024](https://assets.rivian.com/2md5qhoeajym/7Ao7NIFkLxOZtvdc7Fqh70/c8c4a585ae141effce63b41ead2b8ce0/r1s-og-en-us-20240722.pdf). Useful for stock seat operation and component identification; no comprehensive cabin XYZ table was located. |
| Public repair and body information | Rivian-authored public position statements are available, including [ADAS repair information](https://rts.i-car.com/images/pdf/oem-info/rivian/position-statements/71346x.pdf). A [material matrix](https://www.rivianforums.com/forum/attachments/rivian_sg_r1s-material-matrix-rep-guide_2025_2b_2810-31-24_29-pdf.153799/) is explicitly MY2025+, so it is not a 2023 dimension source. No free authenticated Gen 1 cabin hardpoint table located. Paid/restricted archives were not accessed. |
| Owner cargo measurements | Located the original Drive measurement article and owner-published Rivian-response transcriptions. Preserved endpoint and publication limitations. No consensus class 3 was assigned from reposts. |
| Second-row removal | [Mojave's January 2024 documented removal](https://rivianforums.com/forum/threads/step-by-step-removal-of-second-row-in-r1s-diy-instructions-w-photos.23026/) shows concealed areas and wiring. Images help plan later inspection; they do not establish bolt XYZ coordinates or authorize a fabrication interface. |
| Third-row delete | [Owner removal thread](https://www.rivianforums.com/forum/threads/diy-how-to-remove-3rd-row-from-gen-2-r1s-steps-and-photos.38049/) explicitly covers Gen 2. Exclude from Gen 1 dimensional constraints. |
| Camping/platform builds | [S005J's free platform](https://www.printables.com/fr/model/551407-rivian-r1s-sleeping-platform) advertises a STEP assembly and printed brackets, published in 2023, CC BY-NC 4.0. This is an accessory assembly, not the cabin. Listing found; file contents not downloaded or validated. [Owner overlanding build](https://www.rivianforums.com/forum/threads/r1s-overlanding-v1-0-sleep-2-people-on-bed-platform-frame-w-full-size-spare-inside.23311/) provides further visual context. |
| Aftermarket storage | [BamBeds manufacturer](https://bambeds.com/products/bambed-rivian-r1s) lists platform dimensions and Gen 1/Gen 2 options. Treat product dimensions as product dimensions; the listing does not isolate every measurement by generation. No purchase proposed. |
| Floor/cargo liners | [WeatherTech 2023 cargo liner](https://www.weathertech.com/cargo-liner/2023_rivian_r1s/) and [LinerX](https://linerx.com/collections/rivian/products/linerx-cargo-liner-for-rivian-r1s) establish product coverage. No openly downloadable engineering floor surface or point cloud was found on the examined pages. Marketing references to scanning do not supply scan data. |
| Roof/accessory geometry | [Rivian cargo cover](https://gearshop.rivian.com/products/r1s-cargo-cover) has published product dimensions; these do not locate mounts or internal panels. Roof-rack and roof-cover searches produced accessory listings, not calibrated interior glass/headliner dimensions. |
| Salvage and auction photographs | [Copart's 2023 example](https://www.copart.com/lot/44236755/salvage-2023-rivian-r1s-adventure-ny-newburgh) offers uncalibrated photos from a front-damaged vehicle. Useful only for possible part identification. No metric dimensions were extracted. |
| OBJ/FBX/GLTF/GLB/STL | Searches found commercial vehicle assets and a [free STL/GLB miniature listing](https://remeshy.com/model/rivian-r1s-suv-model-da9f0673) with AI-generated mesh language. Reject as engineering cabin data. No commercial mesh used. |
| STEP/IGES | The free platform STEP is a relevant accessory lead. No authenticated free full-cabin STEP/IGES located. |
| PLY, LiDAR, photogrammetry and point clouds | No reusable full Gen 1 interior scan with scale controls, uncertainty and clear access terms located. Your own capture is the primary next source. |

The JSON source registry records URLs, dates/scopes and access limitations. A catalog listing is not proof that its files can be retrieved or that their license permits every downstream use.

S14 follow-up, 2026-09-11 UTC: the live files page was inspected and its single STEP listing confirmed. The browser emitted a download event, but no local file was exposed or located for CAD inspection. Units, extents and contents remain unknown. See [the reference assessment](free_reference_assessment.md); no cabin geometry was inferred from this accessory.

## Missing construction information

The following remain unmeasured: structural datum and centerline ties; rail/attachment coordinates; independent left/right trim profiles through row 2 and row 3; floor steps and humps; sill and door-opening curves; pillar volumes; real front-seatback envelopes; third-row cushion/back/folding hinge geometry; wheel-house trim and underlying structure; roof/glass/headliner surfaces; closed hatch inner surface; cargo boundaries in each configuration.

These block executive-seat width, aisle feasibility, rail travel, recline, footrest deployment, entry simulation and cargo packing. The prioritized field procedure is in `measurement_and_capture_plan.md`.

The brief's chair, cooler, screen and luggage numbers are **design requirements**, kept in a separate requirements table. They are not measured cabin dimensions. The 21–23 in seat-width desire remains 533.4–584.2 mm until the real chair's total envelope, including armrests and mechanism, is supplied. No chair was modeled.
