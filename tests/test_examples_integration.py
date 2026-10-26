"""Integration tests for the runnable GDAL/OGR cookbook examples.

These tests execute each shell example against isolated temporary output paths,
then assert useful output properties instead of treating a zero exit code as
proof that the spatial operation produced the intended artifact.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
GDAL_CLI = (
    "gdal_create",
    "gdalinfo",
    "gdal_translate",
    "gdalwarp",
    "gdalbuildvrt",
    "ogr2ogr",
    "ogrinfo",
)
EXAMPLES = {
    "01-ogr2ogr-conversion": (
        "synthetic_points.geojson",
        "synthetic_points.shp",
        "synthetic_points.gpkg",
    ),
    "02-gdal-translate": (
        "synthetic_raster.tif",
        "synthetic_raster.png",
        "synthetic_subset.tif",
    ),
    "03-gdalwarp-reprojection": (
        "synthetic_wgs84.tif",
        "synthetic_webmercator.tif",
        "synthetic_utm33n.tif",
    ),
    "04-virtual-rasters": (
        "synthetic_tile_1.tif",
        "synthetic_tile_2.tif",
        "synthetic_tile_3.tif",
        "synthetic_mosaic.vrt",
        "synthetic_mosaic.tif",
    ),
    "05-batch-processing": (
        "batch_input_1.tif",
        "batch_input_2.tif",
        "batch_input_3.tif",
        "batch_input_4.tif",
        "batch_input_5.tif",
        "batch_stack.vrt",
    ),
}


@pytest.fixture(scope="session", autouse=True)
def require_gdal_cli() -> None:
    missing = [name for name in GDAL_CLI if shutil.which(name) is None]
    if missing:
        pytest.skip(f"GDAL/OGR CLI integration tests require: {', '.join(missing)}")


@pytest.mark.parametrize(("example", "expected_outputs"), EXAMPLES.items())
def test_shell_example_runs_and_creates_nonempty_outputs(
    tmp_path: Path, example: str, expected_outputs: tuple[str, ...]
) -> None:
    output_dir = tmp_path / "outputs"
    env = os.environ.copy()
    env["OUTPUT_DIR"] = str(output_dir)
    script = ROOT / "examples" / example / "run.sh"

    result = subprocess.run(
        ["bash", str(script)],
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=120,
    )
    assert result.returncode == 0, f"{example} failed with output:\n{result.stdout}"

    for name in expected_outputs:
        path = output_dir / name
        assert path.is_file(), f"{example} did not create {name}. Output:\n{result.stdout}"
        assert path.stat().st_size > 0, f"{example} created an empty {name}"


def gdalinfo_json(path: Path) -> dict:
    result = subprocess.run(
        ["gdalinfo", "-json", str(path)],
        text=True,
        capture_output=True,
        check=False,
        timeout=30,
    )
    assert result.returncode == 0, f"gdalinfo failed for {path}: {result.stderr}"
    return json.loads(result.stdout)


def test_translate_example_has_expected_raster_dimensions_and_band_count(tmp_path: Path) -> None:
    output_dir = tmp_path / "translate"
    env = os.environ.copy()
    env["OUTPUT_DIR"] = str(output_dir)
    subprocess.run(
        ["bash", str(ROOT / "examples/02-gdal-translate/run.sh")],
        cwd=ROOT,
        env=env,
        check=True,
        capture_output=True,
        text=True,
        timeout=120,
    )

    source = gdalinfo_json(output_dir / "synthetic_raster.tif")
    subset = gdalinfo_json(output_dir / "synthetic_subset.tif")
    assert source["size"] == [256, 256]
    assert len(source["bands"]) == 3
    assert subset["size"] == [128, 128]
    assert len(subset["bands"]) == 3



def test_reprojection_example_uses_valid_regional_extent_and_expected_crs(tmp_path: Path) -> None:
    output_dir = tmp_path / "reprojection"
    env = os.environ.copy()
    env["OUTPUT_DIR"] = str(output_dir)
    subprocess.run(
        ["bash", str(ROOT / "examples/03-gdalwarp-reprojection/run.sh")],
        cwd=ROOT,
        env=env,
        check=True,
        capture_output=True,
        text=True,
        timeout=120,
    )

    expected_epsg = {
        "synthetic_wgs84.tif": "4326",
        "synthetic_webmercator.tif": "3857",
        "synthetic_utm33n.tif": "32633",
    }
    for filename, epsg_code in expected_epsg.items():
        info = gdalinfo_json(output_dir / filename)
        assert info["size"][0] > 0 and info["size"][1] > 0
        wkt = info.get("coordinateSystem", {}).get("wkt", "")
        assert f'ID["EPSG",{epsg_code}]' in wkt, f"{filename} should use EPSG:{epsg_code}; CRS WKT was: {wkt}"


def test_ogr_conversion_preserves_three_features(tmp_path: Path) -> None:
    output_dir = tmp_path / "vector"
    env = os.environ.copy()
    env["OUTPUT_DIR"] = str(output_dir)
    subprocess.run(
        ["bash", str(ROOT / "examples/01-ogr2ogr-conversion/run.sh")],
        cwd=ROOT, env=env, check=True, capture_output=True, text=True, timeout=120
    )

    result = subprocess.run(
        ["ogrinfo", "-ro", "-so", "-al", str(output_dir / "synthetic_points.gpkg")],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout
    assert "Feature Count: 3" in result.stdout
    assert "EPSG" in result.stdout or "WGS 84" in result.stdout


def test_vrt_examples_expose_expected_band_counts(tmp_path: Path) -> None:
    for example, output_name, expected_bands in (
        ("04-virtual-rasters", "synthetic_mosaic.vrt", 1),
        ("05-batch-processing", "batch_stack.vrt", 5),
    ):
        output_dir = tmp_path / example
        env = os.environ.copy()
        env["OUTPUT_DIR"] = str(output_dir)
        subprocess.run(
            ["bash", str(ROOT / "examples" / example / "run.sh")],
            cwd=ROOT, env=env, check=True, capture_output=True, text=True, timeout=120
        )
        info = gdalinfo_json(output_dir / output_name)
        assert len(info["bands"]) == expected_bands
