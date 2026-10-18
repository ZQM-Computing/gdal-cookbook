# GDAL/OGR Command-Line Patterns

<!-- ZQM-START -->
<p align="center">
  <strong>ZQM Computing — Geospatial Engineering & Scientific Computing</strong><br>
  <a href="https://github.com/ZQM-Computing">ZQM Computing</a> •
  <a href="https://github.com/ZQM-Labs">ZQM Labs</a>
</p>
<!-- ZQM-END -->

[![CI](https://github.com/ZQM-Computing/gdal-patterns/actions/workflows/ci.yml/badge.svg)](https://github.com/ZQM-Computing/gdal-patterns/actions/workflows/ci.yml)

Production-tested GDAL/OGR patterns for geospatial data conversion, reprojection, clipping, and mosaicking — the command-line moves that show up in every data pipeline.

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

Each `run.sh` is self-contained and works on synthetic data it generates itself. The Python example runs with `python examples/06-python-integration/run.py`.

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

```
gdal-patterns/
├── examples/
│   ├── 01-ogr2ogr-conversion/run.sh
│   ├── 02-gdal-translate/run.sh
│   ├── 03-gdalwarp-reprojection/run.sh
│   ├── 04-virtual-rasters/run.sh
│   ├── 05-batch-processing/run.sh
│   └── 06-python-integration/run.py
├── tests/
│   └── test_patterns.py     # every script exists, is non-empty, is executable
├── pyproject.toml
├── README.md
├── LICENSE
└── CONTRIBUTING.md
```

## Validation

```bash
pip install pytest
pytest            # checks script presence, size, and executability
```

CI runs `ruff check` / `ruff format --check` and the pytest suite on every push and pull request.

## Roadmap

- `gdal_calc.py` raster algebra patterns
- COG creation flags (`-of COG`) as a bridge to [cog-patterns](https://github.com/ZQM-Computing/cog-patterns)
- ogr2ogr spatial filtering (`-spat`, `-clipsrc`) walkthrough

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Report security issues to zqmcomputing@gmail.com — please do not open a public issue for those.

## More from this series

- [postgis-patterns](https://github.com/ZQM-Computing/postgis-patterns) — Production PostGIS patterns: spatial indexing, joins & KNN, SRID management, vector tiles, data quality, partitioning
- [duckdb-spatial-patterns](https://github.com/ZQM-Computing/duckdb-spatial-patterns) — DuckDB Spatial patterns for analytical geospatial SQL: GeoParquet, spatial joins, KNN, H3 aggregation — no server required
- [pgrouting-patterns](https://github.com/ZQM-Computing/pgrouting-patterns) — pgRouting network analysis on PostGIS: shortest path, driving distance, isochrones, turn restrictions, traffic-aware routing
- [geopandas-patterns](https://github.com/ZQM-Computing/geopandas-patterns) — GeoPandas/Shapely patterns for Python geospatial workflows: spatial joins, CRS handling, overlays, interpolation, performance
- [stac-patterns](https://github.com/ZQM-Computing/stac-patterns) — STAC patterns for geospatial data discovery: catalogs, item validation, search API, bulk operations, cloud deployment
- [maplibre-patterns](https://github.com/ZQM-Computing/maplibre-patterns) — MapLibre GL JS patterns for frontend vector tile rendering: custom layers, 3D terrain, performance tuning, interactive maps
- [cog-patterns](https://github.com/ZQM-Computing/cog-patterns) — Cloud Optimized GeoTIFF patterns: creation, validation, TiTiler serving, xarray integration, performance benchmarking
- [geoparquet-patterns](https://github.com/ZQM-Computing/geoparquet-patterns) — GeoParquet patterns for columnar geospatial analytics: partitioning, predicate pushdown, DuckDB/Spark integration
- [h3-patterns](https://github.com/ZQM-Computing/h3-patterns) — H3 hexagonal grid patterns: indexing, aggregation, visualization, grid comparisons, performance benchmarks
- [qgis-resources](https://github.com/ZQM-Computing/qgis-resources) — QGIS expressions, PyQGIS snippets, Processing scripts, styles, and QField field-collection guides
- [geospatial-api-reference](https://github.com/ZQM-Computing/geospatial-api-reference) — OGC API – Features reference implementation with FastAPI and PostGIS backends
- [ollama-fleet-patterns](https://github.com/ZQM-Computing/ollama-fleet-patterns) — Ollama fleet operations: model management, health checks, load-spreading, VRAM budgeting, dependency-light RAG
- [proxmox-ceph-operations](https://github.com/ZQM-Computing/proxmox-ceph-operations) — Proxmox VE + Ceph operations runbooks: health checks, backup discipline, OSD replacement, upgrade checklists
- [geospatial-patterns](https://github.com/ZQM-Computing/geospatial-patterns) — Umbrella index for all ZQM geospatial pattern repos

## Documentation and validation

For setup instructions, reproducible examples, data provenance, CRS/SRID assumptions, security guidance, and dependency labels, follow the [ZQM geospatial repository documentation standard](https://github.com/ZQM-Computing/geospatial-patterns/blob/main/docs/repository-documentation-standard.md).

The configured CI workflow is the source of truth for automated checks. A passing workflow establishes only that its checks passed for that commit; it does not certify production deployment or prove that every dependency and operating environment was covered.

## License

MIT — see LICENSE file.

## Related repositories

- [ZQM Geospatial Patterns](https://github.com/ZQM-Computing/geospatial-patterns) — umbrella index of all geospatial pattern repos
- [postgis-patterns](https://github.com/ZQM-Computing/postgis-patterns) — production PostGIS patterns & best practices
- [duckdb-spatial-patterns](https://github.com/ZQM-Computing/duckdb-spatial-patterns) — DuckDB Spatial patterns for analytical geospatial SQL
- [geospatial-api-reference](https://github.com/ZQM-Computing/geospatial-api-reference) — OGC API - Features with FastAPI + PostGIS
- [qgis-resources](https://github.com/ZQM-Computing/qgis-resources) — QGIS expressions, PyQGIS, styles, and QField guides
- [proxmox-ceph-operations](https://github.com/ZQM-Computing/proxmox-ceph-operations) — Proxmox VE + Ceph operations runbooks
- [ollama-fleet-patterns](https://github.com/ZQM-Computing/ollama-fleet-patterns) — Ollama fleet operations & a minimal RAG reference

*Part of [ZQM Computing](https://github.com/ZQM-Computing) — geospatial engineering, scientific computing, and infrastructure patterns.*

## License

MIT — see [LICENSE](LICENSE).

<!-- ZQM-FOOTER-START -->
---

<p align="center">
  <em>Play more. Plan less.</em><br>
  <a href="https://zqmlabs.com">zqmlabs.com</a> •
  <a href="https://github.com/ZQM-Labs">ZQM Labs</a> •
  <a href="https://github.com/ZQM-Computing">ZQM Computing</a>
</p>
<!-- ZQM-FOOTER-END -->
