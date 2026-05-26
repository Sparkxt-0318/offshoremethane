# OffshorePlume — phase-driven Makefile.
#
# Conventions:
#   - `make setup` provisions the Python env via uv (preferred) or poetry.
#   - `make lint`, `make typecheck`, `make test` are the local quality gates.
#   - `make phaseN` runs the Phase N notebook(s) end-to-end and writes outputs.
#   - Every phase target depends on prior-phase outputs where applicable so
#     `make all` rebuilds the full pipeline from raw data.

SHELL := /bin/bash
PYTHON ?= python3
UV ?= uv
PKG := offshoreplume

.PHONY: help setup setup-poetry env-info lint format typecheck test test-fast \
        clean clean-cache nuke phase0 phase1 phase2 phase3 phase4 phase5 phase6 all \
        gee-auth notebooks docs-check

help:
	@echo "OffshorePlume Makefile targets:"
	@echo ""
	@echo "  setup           Create venv and install deps via uv (lockfile-driven)"
	@echo "  setup-poetry    Alternative: install via poetry"
	@echo "  env-info        Print Python and key library versions"
	@echo "  gee-auth        Run earthengine authenticate (interactive)"
	@echo ""
	@echo "  lint            ruff check"
	@echo "  format          ruff format"
	@echo "  typecheck       mypy on src/"
	@echo "  test            pytest (full suite)"
	@echo "  test-fast       pytest -m 'not slow and not integration'"
	@echo ""
	@echo "  phase0          Verify scaffold and env (smoke import test)"
	@echo "  phase1          Baseline MBMP reimplementation on Hassi Messaoud"
	@echo "  phase2          Offshore adaptation (glint, BRDF, wave denoising)"
	@echo "  phase3          ML false-positive reduction CNN"
	@echo "  phase4          Production scan across configured regions"
	@echo "  phase5          IME plume rate quantification"
	@echo "  phase6          Final docs + reproducibility audit"
	@echo "  all             phase0 -> phase6"
	@echo ""
	@echo "  clean-cache     Remove pytest/ruff/mypy caches"
	@echo "  clean           clean-cache + remove __pycache__"
	@echo "  nuke            clean + remove .venv and data/intermediate"

setup:
	$(UV) sync --extra dev
	@echo "Env ready. Activate with: source .venv/bin/activate"

setup-poetry:
	poetry install --with dev
	@echo "Env ready. Activate with: poetry shell"

env-info:
	@$(PYTHON) -c "import sys; print('Python:', sys.version)"
	@$(PYTHON) -c "import numpy, pandas, rasterio, xarray, geopandas; \
		print('numpy:', numpy.__version__); \
		print('pandas:', pandas.__version__); \
		print('rasterio:', rasterio.__version__); \
		print('xarray:', xarray.__version__); \
		print('geopandas:', geopandas.__version__)" || true
	@$(PYTHON) -c "import ee; print('earthengine-api:', ee.__version__)" || true
	@$(PYTHON) -c "import torch; print('torch:', torch.__version__)" || true

gee-auth:
	earthengine authenticate

lint:
	ruff check src tests

format:
	ruff format src tests

typecheck:
	mypy src

test:
	pytest

test-fast:
	pytest -m "not slow and not integration"

# --- Phase targets ---------------------------------------------------
# Each phase runs the corresponding notebook(s) headlessly via jupyter
# nbconvert and persists outputs under data/intermediate/ or data/processed/.

phase0:
	@echo ">> Phase 0 smoke test: importing $(PKG)"
	$(PYTHON) -c "import $(PKG); print('OK', $(PKG).__version__)"
	pytest -m "not slow and not integration" -q

phase1:
	@echo ">> Phase 1 not yet implemented. See docs/decisions.md for current status."
	@exit 1

phase2:
	@echo ">> Phase 2 not yet implemented."
	@exit 1

phase3:
	@echo ">> Phase 3 not yet implemented."
	@exit 1

phase4:
	@echo ">> Phase 4 not yet implemented."
	@exit 1

phase5:
	@echo ">> Phase 5 not yet implemented."
	@exit 1

phase6:
	@echo ">> Phase 6 not yet implemented."
	@exit 1

all: phase0 phase1 phase2 phase3 phase4 phase5 phase6

# --- Housekeeping ----------------------------------------------------

clean-cache:
	rm -rf .pytest_cache .ruff_cache .mypy_cache

clean: clean-cache
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".ipynb_checkpoints" -prune -exec rm -rf {} +

nuke: clean
	rm -rf .venv data/intermediate/*
