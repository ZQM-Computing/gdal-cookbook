"""Structural and runtime tests for the GDAL/OGR cookbook examples."""

import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = ROOT / "examples"
EXPECTED = {
    "01-ogr2ogr-conversion/run.sh",
    "02-gdal-translate/run.sh",
    "03-gdalwarp-reprojection/run.sh",
    "04-virtual-rasters/run.sh",
    "05-batch-processing/run.sh",
    "06-python-integration/run.py",
}
GDAL_TOOLS = ["ogr2ogr", "ogrinfo", "gdal_create", "gdal_translate", "gdalwarp", "gdalbuildvrt", "gdalinfo"]


def test_exact_example_inventory():
    """The expected examples exist with non-empty entry points."""
    actual = {
        f"{directory.name}/{entry.name}"
        for directory in EXAMPLES_DIR.iterdir()
        if directory.is_dir()
        for entry in directory.glob("run.*")
    }
    assert actual == EXPECTED
    for relative in EXPECTED:
        assert (EXAMPLES_DIR / relative).stat().st_size > 0


def test_shell_scripts_parse():
    """Every shell entry point passes Bash's parser."""
    bash = shutil.which("bash")
    if not bash:
        pytest.skip("bash is unavailable")
    for script in sorted(EXAMPLES_DIR.glob("*/run.sh")):
        subprocess.run([bash, "-n", str(script)], check=True, capture_output=True, text=True)


def test_python_example_compiles_without_bytecode_artifacts():
    source = (EXAMPLES_DIR / "06-python-integration/run.py").read_text(encoding="utf-8")
    compile(source, "examples/06-python-integration/run.py", "exec")
    assert 'if __name__ == "__main__":' in source


def test_no_external_data_downloads():
    """Examples should stay deterministic and not fetch unpinned external data."""
    for relative in EXPECTED:
        text = (EXAMPLES_DIR / relative).read_text(encoding="utf-8").lower()
        assert "wget " not in text, f"{relative} contains wget"
        assert "curl " not in text, f"{relative} contains curl"


@pytest.mark.integration
def test_all_shell_examples_execute(tmp_path):
    """Execute all five GDAL/OGR shell examples and verify their artifacts."""
    missing = [name for name in GDAL_TOOLS if not shutil.which(name)]
    if missing:
        pytest.skip(f"GDAL CLI tools unavailable: {', '.join(missing)}")

    copied_examples = tmp_path / "examples"
    shutil.copytree(EXAMPLES_DIR, copied_examples)
    for example in sorted(EXPECTED):
        if not example.endswith(".sh"):
            continue
        script = copied_examples / example
        subprocess.run(
            ["bash", str(script)],
            cwd=tmp_path,
            check=True,
            capture_output=True,
            text=True,
            timeout=120,
        )

    outputs = {
        "01-ogr2ogr-conversion": [
            "output/synthetic_points.geojson",
            "output/synthetic_points.gpkg",
            "output/synthetic_points.shp",
        ],
        "02-gdal-translate": [
            "output/synthetic_raster.tif",
            "output/synthetic_raster.png",
            "output/synthetic_subset.tif",
        ],
        "03-gdalwarp-reprojection": [
            "output/synthetic_wgs84.tif",
            "output/synthetic_webmercator.tif",
            "output/synthetic_utm33n.tif",
        ],
        "04-virtual-rasters": ["output/synthetic_mosaic.vrt", "output/synthetic_mosaic.tif"],
        "05-batch-processing": ["output/batch_stack.vrt", "output/batch_input_1.tif", "output/batch_input_5.tif"],
    }
    def raster_info(path: Path) -> dict:
        result = subprocess.run(
            ["gdalinfo", "-json", str(path)],
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        import json

        return json.loads(result.stdout)

    def assert_readable_raster(path: Path) -> dict:
        assert path.is_file() and path.stat().st_size > 0, f"Missing or empty raster: {path}"
        info = raster_info(path)
        assert len(info.get("size", [])) == 2 and all(value > 0 for value in info["size"]), (
            f"Invalid raster dimensions: {path}"
        )
        assert info.get("bands"), f"Raster has no bands: {path}"
        return info

    def assert_vector_has_features(path: Path) -> None:
        assert path.is_file() and path.stat().st_size > 0, f"Missing or empty vector: {path}"
        result = subprocess.run(
            ["ogrinfo", "-ro", "-al", "-so", str(path)],
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert "Feature Count:" in result.stdout, f"No readable layer metadata: {path}"
        counts = [
            int(line.split(":", 1)[1].strip())
            for line in result.stdout.splitlines()
            if line.strip().startswith("Feature Count:")
        ]
        assert counts == [3], f"Expected exactly 3 converted point features in {path}; got {counts}"
        assert re.search(r'(?:ID|AUTHORITY)\["EPSG",\s*"?4326"?\]', result.stdout), (
            f"Expected converted vector to retain EPSG:4326 CRS: {path}"
        )

    for example, paths in outputs.items():
        for relative in paths:
            path = copied_examples / example / relative
            if relative.endswith((".geojson", ".gpkg", ".shp")):
                assert_vector_has_features(path)
            elif relative.endswith(".vrt"):
                info = assert_readable_raster(path)
                assert info.get("size") and info.get("bands"), f"VRT has no raster data: {path}"
            else:
                assert_readable_raster(path)

    # Assert semantic properties as well as mere file readability.
    translate_dir = copied_examples / "02-gdal-translate" / "output"
    source_info = assert_readable_raster(translate_dir / "synthetic_raster.tif")
    assert source_info["size"] == [256, 256]
    assert len(source_info["bands"]) == 3

    subset_info = assert_readable_raster(translate_dir / "synthetic_subset.tif")
    assert subset_info["size"] == [128, 128], "srcwin output must be exactly 128x128 pixels"
    assert len(subset_info["bands"]) == 3

    reprojection_dir = copied_examples / "03-gdalwarp-reprojection" / "output"
    expected_epsg = {
        "synthetic_wgs84.tif": "4326",
        "synthetic_webmercator.tif": "3857",
        "synthetic_utm33n.tif": "32633",
    }
    for filename, epsg in expected_epsg.items():
        info = assert_readable_raster(reprojection_dir / filename)
        wkt = info.get("coordinateSystem", {}).get("wkt", "")
        assert f'ID["EPSG",{epsg}]' in wkt, f"{filename} should carry EPSG:{epsg}; found CRS WKT: {wkt}"
