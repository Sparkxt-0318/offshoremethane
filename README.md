# OffshorePlume

**Detection and quantification of offshore methane super-emitter plumes from open Sentinel-2 imagery.**

OffshorePlume is a research-grade, reproducible computational pipeline for finding methane plumes over offshore oil and gas infrastructure using only freely available satellite imagery. It implements the multi-band-multi-pass (MBMP) retrieval of [Varon et al. 2021][varon2021], extended with glint masking, water-surface reflectance correction, and a CNN-based false-positive filter to handle the offshore regime that has been severely under-monitored since the loss of MethaneSAT in June 2025.

## Why this project exists

- TROPOMI (Sentinel-5P) maps methane globally at ~7 km — too coarse to attribute emissions to individual platforms.
- Carbon Mapper and GHGSat resolve point sources at ~30 m but are commercial/limited-access and rarely cover offshore.
- MethaneSAT was intended to fill the mid-resolution gap; it failed in June 2025.
- Sentinel-2 is open, global, 10–20 m, and has Bands 11/12 spanning a methane absorption feature near 2.19 µm.

[SkyTruth (Aug 2025)][skytruth2025] demonstrated that Sentinel-2 MBMP can detect offshore plumes despite sun-glint complications. No peer-reviewed study has yet produced a validated, region-wide offshore methane detection database from open imagery alone. This project closes that gap.

## Status

| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Repo scaffold, environment, decision log | **in progress** |
| 1 | Baseline MBMP on Hassi Messaoud land emitter | not started |
| 2 | Offshore adaptation (glint, BRDF, wave denoise) | not started |
| 3 | CNN false-positive reduction | not started |
| 4 | Production scan: ECS → GoM → Persian Gulf → North Sea | not started |
| 5 | IME plume rate quantification | not started |
| 6 | Paper outline + reproducibility audit | not started |

See `docs/decisions.md` (ADR log) for methodology choices and `docs/references.bib` for the literature trail.

## Repository layout

```
offshoreplume/
├── data/
│   ├── raw/             # Sentinel-2 scenes (gitignored)
│   ├── intermediate/    # Computed enhancement images (gitignored)
│   └── processed/       # Detection database, validation results (committed if small)
├── src/offshoreplume/
│   ├── io/              # GEE, Copernicus, IMEO MARS ingestion
│   ├── retrieval/       # MBMP / SBMP implementation
│   ├── corrections/     # Glint, BRDF, water vapor
│   ├── quantification/  # IME plume rate
│   ├── ml/              # False-positive CNN
│   ├── validation/      # MARS / TROPOMI / Carbon Mapper cross-checks
│   └── viz/             # Plots, plume composites, regional maps
├── notebooks/           # One notebook per phase, numbered 01_ … 06_
├── tests/               # pytest unit + integration tests
├── configs/             # YAML configs for regions, scenes, validation sets
├── docs/                # methods.md, results.md, decisions.md, references.bib
├── pyproject.toml       # PEP 621 metadata; uv- and poetry-compatible
├── Makefile             # phaseN targets
└── README.md
```

## Setup

### 1. Python environment

Python **3.11** is required (cartopy and torch wheel constraints). Either `uv` or `poetry` works; `uv` is faster:

```bash
# With uv (recommended)
make setup

# Or with poetry
make setup-poetry
```

Verify:

```bash
make env-info
make phase0   # smoke test: imports package and runs fast tests
```

### 2. Google Earth Engine access

The retrieval reads Sentinel-2 L1C scenes from the Earth Engine catalog. You need a (free) GEE account:

1. Sign up: <https://earthengine.google.com/signup/>. Approval typically takes < 24 h.
2. Create or link a Google Cloud project to GEE.
3. Authenticate once on this machine:

   ```bash
   make gee-auth
   ```

   This stores a refresh token under `~/.config/earthengine/`. Do **not** commit the credentials directory — it is gitignored.

### 3. Validation data sources

The pipeline validates detections against several independent sources. None require payment, but each requires registration:

| Source | Purpose | Access |
|--------|---------|--------|
| [IMEO MARS][mars] | Confirmed super-emitter alerts (2022–) | Free account at <https://methanedata.unep.org> |
| [Carbon Mapper Open Data][cm] | Aircraft & Tanager-1 plume catalog | Free at <https://data.carbonmapper.org> |
| [TROPOMI L3 CH4][tropomi] | Coarse-resolution corroboration | Public via GEE (`COPERNICUS/S5P/OFFL/L3_CH4`) |
| [BOEM venting/flaring reports][boem] | Gulf of Mexico ground truth | Public CSV at <https://www.data.boem.gov> |
| [SkyTruth Methane Tracker][st] | Case studies, alert archive | Public at <https://skytruth.org> |

API keys (where used) belong in a local `.env` file, never committed. See `configs/validation/imeo_mars.yaml` for environment variable names.

## Reproducing the pipeline

The full pipeline is driven from the Makefile and is designed to run end-to-end from raw scenes:

```bash
make setup
make gee-auth
make all   # runs phase0 -> phase6 sequentially
```

Each phase writes outputs to `data/intermediate/` or `data/processed/`. The detection database (`data/processed/detections_<region>_<daterange>.parquet`) is the headline artifact and is what cross-references against external sources.

### Expected runtime and cost

- **Compute**: All retrieval runs on Google Earth Engine's free tier. CNN training fits on a single T4-class GPU (Colab free tier is sufficient).
- **Storage**: ~5–20 GB of intermediate enhancement rasters per region.
- **Wall time** (rough, will be refined with first runs): Phase 1 ~1 day; Phase 2 ~2 days; Phase 3 ~3 days; Phase 4 ~5 days (per region, parallelizable); Phase 5 ~1 day; Phase 6 ~3 days.
- **Dollars**: $0 if Colab free GPU suffices; ~$20–80 if a paid GPU hour or two is needed for CNN training.

## Reproducibility ground rules

The full list lives in `docs/decisions.md` (ADR-0002). Highlights:

1. No fabricated data. Missing scenes, failed queries, and offline validation sources are logged, not papered over.
2. Every methodological choice has an ADR entry with rationale and rejected alternatives.
3. Detections are "confirmed" only when the ML confidence exceeds the documented threshold **and** at least one independent source corroborates. Borderline cases are reported as candidates.
4. Phase gates require PI review of the phase notebook before the next phase begins.
5. Every algorithm step cites the paper that introduced it via `docs/references.bib`.

## How to cite

Citation block will be filled in once the manuscript is drafted (Phase 6). For now, reference the repository commit hash and the date of the detection database file.

## License

MIT. See `LICENSE` (to be added).

---

[varon2021]: https://doi.org/10.5194/amt-14-2771-2021
[skytruth2025]: https://skytruth.org/2025/08/breaking-ground-in-offshore-methane-detection/
[mars]: https://methanedata.unep.org
[cm]: https://data.carbonmapper.org
[tropomi]: https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S5P_OFFL_L3_CH4
[boem]: https://www.data.boem.gov
[st]: https://skytruth.org
