"""Shared fixtures/helpers for link-validation tests.

The validation scripts use hyphenated filenames (link-extractor.py,
simple-validator.py) that aren't importable as normal modules, so we load them
by path with importlib.
"""
import importlib.util
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent.parent


def load_script(filename: str):
    """Load a hyphenated script module by filename from scripts/link-validation/."""
    path = _SCRIPTS / filename
    spec = importlib.util.spec_from_file_location(path.stem.replace("-", "_"), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
