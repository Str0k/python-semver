"""Regression tests for executing :file:`semver/__main__.py` as a script.

The module docstring documents that the file can be run directly, for
example from an extracted wheel::

    $ python3 semver-3*-py3-none-any.whl/semver -h

When the module is executed as a plain script, the ``semver`` package is
not importable until its parent directory is inserted into ``sys.path``.
The module used to import :mod:`semver.cli` at module level *before* its
``main()`` function could set up that path, so the documented invocation
failed with ``ModuleNotFoundError: No module named 'semver'``.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

PKG_DIR = Path(__file__).resolve().parent.parent / "src" / "semver"
MAIN_PY = PKG_DIR / "__main__.py"


def _run_python(args, cwd):
    """Run a Python command without site-packages and ``PYTHONPATH``.

    This reproduces a fresh interpreter without an installed ``semver``, as a user would
    have who just extracted a wheel.
    """
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    return subprocess.run(
        [sys.executable, "-S", *args],
        capture_output=True,
        text=True,
        env=env,
        cwd=cwd,
    )


@pytest.mark.parametrize(
    "args,expected_in_stdout",
    [
        (("-h",), "usage:"),
        (("compare", "1.2.3", "2.1.3"), "-1"),
        (("check", "1.2.3"), ""),
        (("bump", "major", "1.2.3"), "2.0.0"),
    ],
)
def test_should_run_dunder_main_as_plain_script(args, expected_in_stdout, tmp_path):
    """Execute ``semver/__main__.py`` directly like documented."""
    result = _run_python([str(MAIN_PY), *args], str(tmp_path))
    assert result.returncode == 0, f"stdout: {result.stdout}\nstderr: {result.stderr}"
    assert "ModuleNotFoundError" not in result.stderr
    assert expected_in_stdout in result.stdout


def test_should_run_dunder_main_as_package_directory(tmp_path):
    """Execute the ``semver`` package directory like an extracted wheel."""
    result = _run_python([str(PKG_DIR), "-h"], str(tmp_path))
    assert result.returncode == 0, f"stdout: {result.stdout}\nstderr: {result.stderr}"
    assert "ModuleNotFoundError" not in result.stderr
    assert "usage:" in result.stdout
