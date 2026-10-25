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
            ["gdalinfo", "-stats", "-json", str(path)],
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
            ["ogrinfo", "-ro", "-al", str(path)],
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
        for name in ("ALPHA", "BRAVO", "CHARLIE"):
            assert name in result.stdout, f"Converted vector is missing feature name {name}: {path}"
        expected_points = (
            ("-73.9857", "40.7484"),
            ("-118.2437", "34.0522"),
            ("-87.6298", "41.8781"),
        )
        for longitude, latitude in expected_points:
            point_pattern = rf"POINT\s*\(\s*{re.escape(longitude)}\s+{re.escape(latitude)}\s*\)"
            assert re.search(point_pattern, result.stdout), (
                f"Converted vector is missing expected point ({longitude}, {latitude}): {path}"
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

    # The source is a constant-value raster with a known geotransform. Verify
    # pixel values and the shifted origin produced by the 64,64,128,128 window.
    for label, info in (("source", source_info), ("subset", subset_info)):
        for band in info["bands"]:
            assert band.get("minimum") == 128 and band.get("maximum") == 128, (
                f"{label} raster should contain only the synthetic value 128; band statistics: {band}"
            )
    source_gt = source_info["geoTransform"]
    subset_gt = subset_info["geoTransform"]
    assert source_gt == pytest.approx([-180, 360 / 256, 0, 90, 0, -180 / 256])
    assert subset_gt == pytest.approx([-90, 360 / 256, 0, 45, 0, -180 / 256]), (
        "srcwin subset must shift its origin by 64 source pixels in x and y"
    )

    # The three adjacent 128x128 tiles span x=-10..20 and y=0..10.
    # Check mosaic extent, dimensions, and the actual values from each source tile.
    mosaic_dir = copied_examples / "04-virtual-rasters" / "output"
    mosaic = assert_readable_raster(mosaic_dir / "synthetic_mosaic.tif")
    assert mosaic["size"] == [384, 128], f"Three adjacent 128x128 tiles should form a 384x128 mosaic: {mosaic['size']}"
    mosaic_gt = mosaic["geoTransform"]
    assert mosaic_gt == pytest.approx([-10, 30 / 384, 0, 10, 0, -10 / 128])
    mosaic_band = mosaic["bands"][0]
    assert mosaic_band.get("minimum") == 60 and mosaic_band.get("maximum") == 180, (
        f"Mosaic must retain all three input tile values (60, 120, 180); band statistics: {mosaic_band}"
    )

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

        assert len(info["size"]) == 2 and all(value > 0 for value in info["size"]), (
            f"{filename} has invalid dimensions after reprojection: {info.get('size')}"
        )
        geotransform = info.get("geoTransform")
        assert geotransform and len(geotransform) == 6, f"{filename} is missing a valid affine geotransform"
        assert geotransform[1] != 0 and geotransform[5] != 0, f"{filename} has zero pixel resolution: {geotransform}"
        band = info["bands"][0]
        assert band.get("maximum") == 200, (
            f"{filename} should preserve the synthetic source value 200; band statistics: {band}"
        )
        assert band.get("minimum", 0) >= 0, f"{filename} unexpectedly contains negative raster values: {band}"

    # Exercise nodata semantics with a synthetic raster containing a known hole.
    # The central polygon is burned to 0, which is also the declared nodata value.
    nodata_source = tmp_path / "nodata-source.tif"
    subprocess.run(
        [
            "gdal_create",
            "-q",
            "-of",
            "GTiff",
            "-outsize",
            "256",
            "256",
            "-bands",
            "1",
            "-ot",
            "UInt16",
            "-burn",
            "200",
            "-a_srs",
            "EPSG:4326",
            "-a_ullr",
            "-10",
            "10",
            "10",
            "-10",
            "-a_nodata",
            "0",
            str(nodata_source),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    hole_vector = tmp_path / "nodata-hole.geojson"
    hole_vector.write_text(
        '{"type":"FeatureCollection","features":[{"type":"Feature",'
        '"properties":{},"geometry":{"type":"Polygon","coordinates":'
        '[[[-2.5,-2.5],[2.5,-2.5],[2.5,2.5],[-2.5,2.5],[-2.5,-2.5]]]}}]}',
        encoding="utf-8",
    )
    subprocess.run(
        ["gdal_rasterize", "-burn", "0", str(hole_vector), str(nodata_source)],
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    nodata_output = tmp_path / "nodata-reprojected.tif"
    subprocess.run(
        [
            "gdalwarp",
            "-overwrite",
            "-srcnodata",
            "0",
            "-dstnodata",
            "0",
            "-t_srs",
            "EPSG:4326",
            "-r",
            "near",
            str(nodata_source),
            str(nodata_output),
        ],
        check=True,
        capture_output=True,
        text=True,
        timeout=60,
    )
    nodata_info = raster_info(nodata_output)
    nodata_band = nodata_info["bands"][0]
    assert nodata_band.get("noDataValue") == 0, (
        f"Reprojected raster must declare the requested nodata value 0: {nodata_band}"
    )
    assert nodata_band.get("minimum") == 200 and nodata_band.get("maximum") == 200, (
        f"Nodata pixels must be excluded from valid-data statistics: {nodata_band}"
    )

    def sample_pixel(path: Path, x: int, y: int) -> float:
        result = subprocess.run(
            ["gdallocationinfo", "-valonly", str(path), str(x), str(y)],
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return float(result.stdout.strip())

    assert sample_pixel(nodata_output, 128, 128) == 0, (
        "The central nodata region must remain nodata after reprojection"
    )
    assert sample_pixel(nodata_output, 32, 32) == 200, (
        "Valid pixels outside the nodata region must preserve the source value"
    )

    wgs84 = assert_readable_raster(reprojection_dir / "synthetic_wgs84.tif")
    assert wgs84["size"] == [512, 256]
    assert wgs84["geoTransform"] == pytest.approx([-180, 360 / 512, 0, 90, 0, -180 / 256])

    webmercator = assert_readable_raster(reprojection_dir / "synthetic_webmercator.tif")
    webmercator_corners = webmercator.get("cornerCoordinates", {})
    upper_left = webmercator_corners.get("upperLeft")
    lower_right = webmercator_corners.get("lowerRight")
    assert upper_left and lower_right, "Web Mercator output is missing corner coordinates"
    assert upper_left[0] < -20_000_000 and lower_right[0] > 20_000_000, (
        f"Web Mercator output does not span the expected projected world extent: {webmercator_corners}"
    )
    assert upper_left[1] > 20_000_000 and lower_right[1] < -20_000_000, (
        f"Web Mercator output does not span the expected projected latitude extent: {webmercator_corners}"
    )
