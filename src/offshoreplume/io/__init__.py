"""Data ingestion.

Modules (to be filled in across phases):
    earthengine     Sentinel-2 L1C scene search + download via the GEE API.
    copernicus      Direct Sentinel-2 access from the Copernicus Data Space
                    (fallback when GEE rate-limits or is unavailable).
    era5            ERA5 reanalysis wind extraction for Phase 5 IME.
    mars            IMEO MARS validation alert ingestion.
    carbonmapper    Carbon Mapper open-data plume catalog ingestion.
    boem            BOEM venting/flaring incident reports (Gulf of Mexico).
"""
