# GDAL/OGR Command-Line Cookbook

<!-- ZQM-START -->
<!-- markdownlint-disable MD033 -->
<p align="center">
  <strong>ZQM Computing — Geospatial Engineering & Scientific Computing</strong><br>
  <a href="https://github.com/ZQM-Computing">ZQM Computing</a>
</p>
<!-- markdownlint-enable MD033 -->
<!-- ZQM-END -->

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg) ![GitHub](https://img.shields.io/github/stars/ZQM-Computing/gdal-cookbook?style=social)
[![CI](https://github.com/ZQM-Computing/gdal-cookbook/actions/workflows/ci.yml/badge.svg)](https://github.com/ZQM-Computing/gdal-cookbook/actions/workflows/ci.yml)

A practical **GDAL/OGR command-line cookbook** for geospatial data engineering: vector and raster conversion, reprojection, clipping, mosaicking, format inspection, and repeatable batch processing. The examples are aimed at GIS analysts and data engineers building reproducible data pipelines. Synthetic fixtures and CI help verify documented workflows; the integration suite executes the five GDAL/OGR shell examples in isolated temporary directories and checks representative raster dimensions, band counts, vector feature counts, and non-empty outputs. The Python-binding example remains a separate environment-dependent workflow; check GDAL versions, CRS assumptions, nodata handling, and input/output paths against your data before production use.

## Repository role and status

**Status:** Active, public.

**What this repository is:** GDAL/OGR command-line patterns — the conversion, reprojection, clipping, and mosaicking moves that show up in every geospatial data pipeline.

**What it contributes:** Part of the ZQM Computing geospatial portfolio. This repository provides examples and guidance for the tools and workflows described below; validate each example against your own data, software versions, and operating environment before adopting it. The umbrella index for the series is [geospatial-cookbooks](https://github.com/ZQM-Computing/geospatial-cookbooks).

**Standing:** This repository is maintained independently. Automated checks cover only the paths and environments configured in its workflows; they do not establish production readiness or operational certification.

## Who this is for

Geospatial developers, GIS analysts, and data engineers who move raster and vector data between formats, projections, and systems. GDAL is the quiet dependency under half the industry; these patterns make its CLI second nature.

## Prerequisites

- GDAL >= 3.6 with command-line utilities (`gdal-bin`)
- Python 3.11+ with GDAL bindings for the Python example (`python3-gdal`)
- Bash

```bash
# Ubuntu
sudo apt-get install gdal-bin python3-gdal
```

## Quickstart

```bash
cd examples/01-ogr2ogr-conversion
chmod +x run.sh
./run.sh
```

Each shell example generates synthetic data and writes its outputs to that example's `output/` directory. The Python example uses GDAL's Python bindings and NumPy; install compatible bindings before running `python examples/06-python-integration/run.py`.

## Usage

Each pattern is a self-contained, runnable example. Start from the
[Quickstart](#quickstart), then open any entry in the [Patterns](#patterns)
list and run it end to end. Copy the pattern into your own project and
swap in your data — the patterns are reference implementations, not a
package to install.

## Patterns

| # | Example | What it demonstrates |
|---|---------|----------------------|
| 01 | `01-ogr2ogr-conversion` | Vector format conversion with `ogr2ogr` on synthetic GeoJSON |
| 02 | `02-gdal-translate` | Raster translation, format conversion, and subsetting |
| 03 | `03-gdalwarp-reprojection` | Raster reprojection between coordinate systems with `gdalwarp` |
| 04 | `04-virtual-rasters` | VRT mosaicking — treating many files as one virtual raster |
| 05 | `05-batch-processing` | Shell-loop batch processing over a directory of rasters |
| 06 | `06-python-integration` | `osgeo.gdal` Python API: in-memory raster, gradient fill, read/write |

## Repository layout

```text
gdal-cookbook/
├── examples/
│   ├── 01-ogr2ogr-conversion/run.sh
│   ├── 02-gdal-translate/run.sh
│   ├── 03-gdalwarp-reprojection/run.sh
│   ├── 04-virtual-rasters/run.sh
│   ├── 05-batch-processing/run.sh
│   └── 06-python-integration/run.py
├── tests/
│   └── test_patterns.py     # exact inventory, syntax, and runtime artifact checks
├── pyproject.toml
├── README.md
├── LICENSE
└── CONTRIBUTING.md
```

## Validation

```bash
python -m pip install pytest ruff
python -m ruff check examples tests
python -m ruff format --check examples tests
python -m pytest -q
```

The suite checks the exact example inventory, shell syntax, Python syntax, and that examples do not download unpinned external data. CI also enforces Ruff lint and formatting checks across `examples/` and `tests/`. With the required GDAL CLI tools installed, it also executes all five shell examples against synthetic data and verifies the generated raster/vector artifacts. CI installs `gdal-bin` and runs this integration path. The Python bindings example is syntax-checked only; its runtime requires a Python environment with matching GDAL bindings and NumPy.

## Roadmap

- `gdal_calc.py` raster algebra patterns
- COG creation flags (`-of COG`) as a bridge to [cog-cookbook](https://github.com/ZQM-Computing/cog-cookbook)
- ogr2ogr spatial filtering (`-spat`, `-clipsrc`) walkthrough

## Contributing

See [CONTRIBUTING.md](https://github.com/ZQM-Computing/gdal-cookbook/blob/main/CONTRIBUTING.md). Report security issues to <zqmcomputing@gmail.com> — please do not open a public issue for those.

## More from this series

- [postgis-cookbook](https://github.com/ZQM-Computing/postgis-cookbook) — PostGIS SQL examples: spatial indexing, joins & KNN, SRID management, vector tiles, data quality, partitioning
- [duckdb-spatial-cookbook](https://github.com/ZQM-Computing/duckdb-spatial-cookbook) — DuckDB Spatial patterns for analytical geospatial SQL: GeoParquet, spatial joins, KNN, H3 aggregation — no server required
- [pgrouting-cookbook](https://github.com/ZQM-Computing/pgrouting-cookbook) — pgRouting network analysis on PostGIS: shortest path, driving distance, isochrones, turn restrictions, traffic-aware routing
- [geopandas-cookbook](https://github.com/ZQM-Computing/geopandas-cookbook) — GeoPandas/Shapely patterns for Python geospatial workflows: spatial joins, CRS handling, overlays, interpolation, performance
- [stac-cookbook](https://github.com/ZQM-Computing/stac-cookbook) — STAC patterns for geospatial data discovery: catalogs, item validation, search API, bulk operations, cloud deployment
- [maplibre-cookbook](https://github.com/ZQM-Computing/maplibre-cookbook) — MapLibre GL JS patterns for frontend vector tile rendering: custom layers, 3D terrain, performance tuning, interactive maps
- [cog-cookbook](https://github.com/ZQM-Computing/cog-cookbook) — Cloud Optimized GeoTIFF patterns: creation, validation, TiTiler serving, xarray integration, performance benchmarking
- [geoparquet-cookbook](https://github.com/ZQM-Computing/geoparquet-cookbook) — GeoParquet patterns for columnar geospatial analytics: partitioning, predicate pushdown, DuckDB/Spark integration
- [h3-cookbook](https://github.com/ZQM-Computing/h3-cookbook) — H3 hexagonal grid patterns: indexing, aggregation, visualization, grid comparisons, performance benchmarks
- [qgis-resources](https://github.com/ZQM-Computing/qgis-resources) — QGIS expressions, PyQGIS snippets, Processing scripts, styles, and QField field-collection guides
- [geospatial-api-reference](https://github.com/ZQM-Computing/geospatial-api-reference) — OGC API – Features reference implementation with FastAPI and PostGIS backends
- [ollama-fleet-cookbook](https://github.com/ZQM-Computing/ollama-fleet-cookbook) — Ollama fleet operations: model management, health checks, load-spreading, VRAM budgeting, dependency-light RAG
- [proxmox-ceph-operations](https://github.com/ZQM-Computing/proxmox-ceph-operations) — Proxmox VE + Ceph operations runbooks: health checks, backup discipline, OSD replacement, upgrade checklists
- [geospatial-cookbooks](https://github.com/ZQM-Computing/geospatial-cookbooks) — Umbrella index for ZQM Computing geospatial cookbooks

## Documentation and validation

For setup instructions, reproducible examples, data provenance, CRS/SRID assumptions, security guidance, and dependency labels, follow the [ZQM geospatial repository documentation standard](https://github.com/ZQM-Computing/geospatial-cookbooks/blob/main/docs/repository-documentation-standard.md).

The configured CI workflow is the source of truth for automated checks. A passing workflow establishes only that its checks passed for that commit; it does not certify production deployment or prove that every dependency and operating environment was covered.

## License

MIT — see LICENSE file.

*Part of [ZQM Computing](https://github.com/ZQM-Computing) — geospatial engineering, scientific computing, and infrastructure patterns; the geospatial arm of [ZQM Labs](https://zqmlabs.com), makers of Z's Quests & Mischief location games.*
