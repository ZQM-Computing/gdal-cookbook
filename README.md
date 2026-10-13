# GDAL/OGR Command-Line Patterns

Production-tested GDAL/OGR patterns for geospatial data conversion, reprojection, clipping, and mosaicking.

## Who this is for

Geospatial developers, GIS analysts, and data engineers who work with raster and vector data.

## What's inside

- `examples/` — Runnable scripts with sample data
- `tests/` — Validation tests for each pattern

## Patterns

| # | Pattern | Description |
|---|---------|-------------|
| 1 | ogr2ogr conversion | Format conversion and reprojection |
| 2 | gdal_translate | Raster format conversion and compression |
| 3 | gdalwarp reprojection | Reproject rasters between CRS |
| 4 | Virtual rasters | VRT for large dataset mosaicking |
| 5 | Batch processing | Shell scripts for bulk operations |
| 6 | Python integration | osgeo.gdal Python API examples |

## Requirements

- GDAL >= 3.6
- Python 3.11+
- Shell (bash)

## Quick start

```bash
# Install GDAL (Ubuntu)
sudo apt-get install gdal-bin python3-gdal

# Run an example
cd examples/01-ogr2ogr-conversion
./run.sh
```

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

*Part of [ZQM Labs](https://github.com/ZQM-Computing) — games, gear & a little mischief.*

