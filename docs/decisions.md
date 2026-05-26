# Architecture Decision Records (ADRs)

This log records every non-trivial methodological choice in OffshorePlume.
Each entry follows the Michael Nygard ADR template: **Status → Context →
Decision → Consequences → Alternatives considered**. The intent is to give
peer reviewers (and future-you) a paper trail when they ask "why did you
choose X."

Entries are append-only. To supersede a decision, add a new ADR that
references the old one and update the old entry's Status field to
`Superseded by ADR-NNNN`.

---

## ADR-0001 — Use Sentinel-2 MBMP rather than a full radiative-transfer methane retrieval

- **Status**: Accepted
- **Date**: 2026-05-26
- **Authors**: PI (high school sophomore lead), with model-in-the-loop assistance

### Context

The project's scientific goal is detection of methane super-emitter plumes
from offshore oil and gas infrastructure using only freely available
satellite imagery. The retrieval method must therefore work with
multispectral instruments that have broad bands overlapping the 2.3 µm
methane absorption feature (Sentinel-2 MSI Band 12; Landsat-8/9 SWIR2),
not narrow-band hyperspectral instruments such as PRISMA, EnMAP, or
EMIT, whose data are either lower cadence or restricted in coverage.

Two families of retrieval are in the published literature:

1. **Full radiative-transfer (RT) retrieval.** A forward model
   (typically MODTRAN or LBLRTM) computes top-of-atmosphere reflectance
   as a function of column methane, surface reflectance, viewing
   geometry, and ancillary atmospheric state (water vapor, aerosols,
   ozone). The retrieval inverts this forward model on a per-pixel
   basis, typically via an optimal-estimation (OE) or matched-filter
   approach. This is what Guanter et al. 2021 (PRISMA) and Thorpe et
   al. 2023 (EMIT) use, and what the operational methane retrievals
   for hyperspectral sensors generally do.

2. **Differential band-ratio retrieval (MBMP / SBMP).** As introduced by
   Varon et al. 2021 for Sentinel-2, the method exploits two empirical
   facts: (a) Sentinel-2 Band 12 (centered 2.19 µm) overlaps a strong
   methane absorption feature while Band 11 (1.61 µm) is approximately
   methane-transparent, and (b) surface reflectance is approximately
   stable across short revisit intervals. By differencing a target
   scene against a methane-free reference scene over the same geometry
   (single-band-multi-pass, SBMP) and optionally normalizing with the
   Band 11/12 ratio (multi-band-multi-pass, MBMP), one isolates the
   methane-induced absorption signal without needing a forward model.

### Decision

OffshorePlume implements the **MBMP** algorithm as the primary
retrieval, with **SBMP** as the fallback when a clean Band 11
reference is unavailable. We do *not* implement a full RT inversion.

### Consequences

#### Pros

- **Computational tractability.** MBMP is a closed-form arithmetic
  operation on top-of-atmosphere reflectance rasters. It runs in
  seconds per scene on a laptop. RT inversion takes minutes-to-hours
  per scene and demands a Jacobian and ancillary atmospheric state.
- **No proprietary dependencies.** MBMP needs only the public
  Sentinel-2 L1C product. Operational RT codes (e.g., the JPL
  matched-filter implementation for EMIT) are not all open source
  and are tuned to specific sensors.
- **Reproducibility.** The full retrieval can be re-derived from
  three equations in Varon et al. 2021 §3, which we cite inline in
  the code. Reviewers can audit the implementation by reading 200 lines
  of NumPy rather than evaluating an RT model's correctness.
- **Direct precedent.** Ehret et al. 2022 (*Environ. Sci. Technol.*)
  applied this exact method to 1,200+ Sentinel-2 scenes globally and
  documented its performance and failure modes. Our results are
  directly comparable to theirs.

#### Cons (acknowledged limitations, to be addressed in later ADRs)

- **No absolute methane column.** MBMP gives a relative enhancement
  ΔXCH4, not an absolute column. The Phase 5 IME quantification
  treats this enhancement as the plume signal above a zero local
  background, which is valid for high-contrast plumes but biases
  estimates low for diffuse emissions.
- **Reference-scene selection matters.** A reference scene with
  residual methane, different sun-glint geometry, or partial cloud
  contamination corrupts the retrieval. ADR-0003 will document the
  reference-scene selection algorithm.
- **Band 11 is not perfectly methane-transparent.** It has weak CH4
  and H2O absorption that contributes second-order error. Gorroño et
  al. 2023 quantify this; we will adopt their proposed offshore
  correction.
- **Offshore deployment is the explicit research contribution.** The
  Varon et al. method was validated on arid land scenes; offshore
  deployment requires new corrections (glint, wave noise, low water
  reflectance) that are the substance of Phase 2.

### Alternatives considered

1. **Full RT inversion via libRadtran or 6SV.** Rejected for cost,
   complexity, and lack of demonstrated benefit at Sentinel-2's
   spectral resolution — the broad bands wash out the information that
   RT inversion would extract from a hyperspectral measurement.
2. **Matched-filter retrieval (Thompson et al. 2015) ported to
   Sentinel-2.** Rejected because matched filters need a per-pixel
   spectral covariance matrix, which is degenerate when only one
   absorbing band is available. The Varon MBMP method is the
   2-band-specific equivalent.
3. **Hyperspectral-only retrieval (PRISMA, EnMAP, EMIT).** Rejected
   for the production scan because revisit times are too sparse for
   offshore monitoring (PRISMA is targeted, not systematic; EMIT
   covers land only). We may use EMIT scenes opportunistically as
   independent validation in Phase 4 where the orbit happens to cross
   our AOI.

---

## ADR-0002 — Reproducibility and integrity ground rules

- **Status**: Accepted
- **Date**: 2026-05-26

### Context

The PI is a high school sophomore targeting *Environmental Science &
Technology Letters* / *Remote Sensing of Environment* and Regeneron
STS. The work will be subject to expert peer review. Methane retrieval
has many opportunities for silent failure (atmospheric artifacts
misread as plumes, sun-glint false positives, miscalibrated radiometric
scaling). The PI is operating with model-in-the-loop assistance, which
introduces an additional risk: large language models can fabricate
citations, invent numerical results, and produce plausible-looking but
hollow analysis.

### Decision

The project adopts the following non-negotiable ground rules:

1. **No fabricated data.** Failed queries, missing scenes, and offline
   validation sources are logged in the notebook with the exact error
   and a written note in the discussion section. Synthetic placeholder
   data may be used only when explicitly labeled `SYNTHETIC — FOR
   PIPELINE TEST ONLY` in both filename and figure caption.
2. **No silent simplifications.** Every approximation, empirical
   threshold, or rejected edge case gets a new ADR entry.
3. **Conservative claims.** A detection is reported as "confirmed"
   only when (a) the ML confidence score exceeds the documented
   threshold AND (b) at least one independent source (IMEO MARS,
   Carbon Mapper, TROPOMI anomaly, or published case study)
   corroborates. Borderline cases are reported as "candidates" with
   explicit caveats.
4. **Reproducibility from raw data.** `make all` reproduces the final
   detection database bit-identically from raw Sentinel-2 scenes,
   given only the GEE auth token and the validation-source
   credentials. Pre-computed intermediate files are convenience
   artifacts, not load-bearing.
5. **Phase gates.** No phase begins until the prior phase's notebook
   has been reviewed end-to-end by the PI and the review note is
   appended to the relevant ADR.
6. **Citation discipline.** Every algorithm, empirical constant, and
   validation source is cited via `docs/references.bib` with a DOI.
   No `Ref` placeholder citations.
7. **Statistical hygiene.** All metrics are reported with uncertainty.
   No precision without recall. No accuracy on imbalanced data —
   precision/recall/F1/AUROC instead.
8. **Test coverage.** Every retrieval and correction function has a
   unit test. The full pipeline has an integration test on a small
   example AOI that runs in under five minutes.

### Consequences

These rules will slow early iteration. They are designed to be slow:
the alternative is a paper that gets retracted, or worse, an STS
submission that an expert reviewer can dismiss in ten minutes.

### Alternatives considered

A less strict integrity policy (e.g., "best effort, document
exceptions later") was rejected because in the model-in-the-loop
workflow, "later" reliably means "never."

---

<!-- ADRs below are stubs to be filled in as decisions are made.
     Delete the stub and write the full entry when the decision is taken. -->

## ADR-0003 — Reference-scene selection for MBMP (stub)

- **Status**: Pending — to be written in Phase 1.
- **Date**: TBD
- **Context placeholder**: How do we choose the methane-free reference
  scene for MBMP differencing? Trade-offs between temporal proximity
  (minimizes surface change) and geometric similarity (minimizes
  glint differences).

## ADR-0004 — Glint masking threshold (stub)

- **Status**: Pending — to be written in Phase 2.

## ADR-0005 — CNN architecture and training data balance (stub)

- **Status**: Pending — to be written in Phase 3.

## ADR-0006 — IME wind-coefficient choice and uncertainty propagation (stub)

- **Status**: Pending — to be written in Phase 5.

## ADR-0007 — Detection-confirmation threshold and confidence calibration (stub)

- **Status**: Pending — to be written in Phase 4.
