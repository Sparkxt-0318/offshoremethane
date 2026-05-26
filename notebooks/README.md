# Notebooks

One numbered notebook per phase. Each notebook ends with two blocks
that are transcribed into `docs/methods.md` and `docs/results.md`
when the phase is signed off.

Planned notebooks:

| Notebook | Phase | Description |
|----------|-------|-------------|
| `01_baseline_land_validation.ipynb` | 1 | Reproduce Ehret et al. 2022 MBMP detections at Hassi Messaoud. Pearson r vs published values, target > 0.7. |
| `02_offshore_adaptation.ipynb`      | 2 | Glint masking, water-surface reflectance correction, wave denoising. Validate against three documented offshore events. |
| `03_ml_false_positive_reduction.ipynb` | 3 | CNN classifier, k-fold cross-validation, model card. |
| `04_production_scan.ipynb`          | 4 | Full pipeline over all four configured regions (priority: ECS, GoM, PG, NS). |
| `05_quantification.ipynb`           | 5 | IME plume rate estimates with uncertainty. |
| `06_paper_figures.ipynb`            | 6 | Curated final figures for the manuscript. |

Notebooks are executed headlessly via the corresponding `make phaseN`
target. Outputs go to `data/intermediate/` or `data/processed/`.
