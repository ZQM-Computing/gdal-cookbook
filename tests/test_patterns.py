"""
tests/test_patterns.py
Sanity checks that every example script exists and is non-empty.
Run with:  pytest tests/test_patterns.py -v
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = REPO_ROOT / "examples"

EXPECTED_SCRIPTS = [
    "01-ogr2ogr-conversion/run.sh",
    "02-gdal-translate/run.sh",
    "03-gdalwarp-reprojection/run.sh",
    "04-virtual-rasters/run.sh",
    "05-batch-processing/run.sh",
    "06-python-integration/run.py",
]


def test_examples_dir_exists():
    """The examples directory must exist."""
    assert EXAMPLES_DIR.is_dir(), f"Missing: {EXAMPLES_DIR}"


def test_all_example_scripts_present():
    """All six example scripts must be present."""
    for rel in EXPECTED_SCRIPTS:
        path = EXAMPLES_DIR / rel
        assert path.is_file(), f"Missing example: {rel}"


def test_shell_scripts_non_empty():
    """Every .sh file must be at least 20 lines."""
    for rel in EXPECTED_SCRIPTS:
        if rel.endswith(".sh"):
            path = EXAMPLES_DIR / rel
            lines = path.read_text().splitlines()
            assert len(lines) >= 20, f"{rel} has only {len(lines)} lines (<20)"


def test_shell_scripts_have_shebang():
    """Every .sh file must start with a shebang."""
    for rel in EXPECTED_SCRIPTS:
        if rel.endswith(".sh"):
            path = EXAMPLES_DIR / rel
            first = path.read_text().splitlines()[0]
            assert first.startswith("#!"), f"{rel} missing shebang"


def test_python_script_has_main_guard():
    """The Python example should use a __main__ guard."""
    path = REPO_ROOT / "06-python-integration/run.py"
    text = path.read_text()
    assert "__main__" in text, "Python example missing __main__ guard"


def test_no_external_downloads():
    """No script should reference wget/curl for data downloads."""
    for rel in EXPECTED_SCRIPTS:
        path = EXAMPLES_DIR / rel
        text = path.read_text().lower()
        assert "wget " not in text, f"{rel} contains wget"
        assert "curl " not in text, f"{rel} contains curl"
