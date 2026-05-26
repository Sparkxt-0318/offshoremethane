"""OffshorePlume: methane super-emitter detection from open Sentinel-2 imagery.

Sub-packages:
    io             Earth Engine, Copernicus, IMEO MARS ingestion.
    retrieval      MBMP / SBMP methane retrieval (Varon et al. 2021).
    corrections    Sun-glint masking, water BRDF, water-vapor correction.
    quantification Integrated mass enhancement (IME) plume rate (Varon et al. 2018).
    ml             False-positive reduction CNN.
    validation     Cross-reference against MARS, TROPOMI, Carbon Mapper, BOEM.
    viz            Maps, plume composites, diagnostic plots.

See ``docs/decisions.md`` for the ADR log and ``docs/references.bib`` for
cited literature.
"""

__version__ = "0.1.0"

__all__ = ["__version__"]
