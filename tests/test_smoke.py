"""Phase 0 smoke tests.

These exist only to verify that the package is importable, the
sub-packages are wired up, and the CLI entry point responds to
--version. They do NOT exercise scientific behavior — that's the
job of the per-phase test modules added later.
"""

from __future__ import annotations

import importlib
from pathlib import Path

import pytest
import yaml

from offshoreplume.cli import main as cli_main


def test_package_imports_and_version():
    pkg = importlib.import_module("offshoreplume")
    assert isinstance(pkg.__version__, str)
    assert pkg.__version__.count(".") >= 1


@pytest.mark.parametrize(
    "subpkg",
    [
        "offshoreplume.io",
        "offshoreplume.retrieval",
        "offshoreplume.corrections",
        "offshoreplume.quantification",
        "offshoreplume.ml",
        "offshoreplume.validation",
        "offshoreplume.viz",
    ],
)
def test_subpackages_import(subpkg):
    importlib.import_module(subpkg)


def test_cli_help_returns_zero():
    assert cli_main(["--help"]) == 0


def test_cli_version_returns_zero():
    assert cli_main(["--version"]) == 0


def test_cli_unknown_arg_returns_nonzero():
    assert cli_main(["nonsense"]) != 0


def test_configs_parse():
    """Every YAML config in configs/ must be valid YAML."""
    repo_root = Path(__file__).resolve().parent.parent
    configs = list(repo_root.glob("configs/**/*.yaml"))
    assert configs, "expected at least one YAML config under configs/"
    for cfg in configs:
        with cfg.open() as f:
            yaml.safe_load(f)
