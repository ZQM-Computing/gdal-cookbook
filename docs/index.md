# GDAL Patterns

Production-tested **GDAL/OGR** command-line patterns for raster and vector geospatial data processing — conversion, reprojection, clipping, mosaicking, and batch processing.

## Who this is for

Geospatial developers and data engineers who process large raster and vector datasets. GDAL is the foundational geospatial data translation library — mastering its CLI unlocks every format conversion and transformation workflow.

## What you'll find

- **Conversion** — GeoJSON ↔ Shapefile ↔ GeoParquet ↔ GPKG via ogr2ogr
- **Translation** — Raster format conversion via gdal_translate
- **Reprojection** — Coordinate system transforms via gdalwarp
- **Virtual rasters** — VRT mosaicking for large datasets
- **Batch processing** — Parallel processing patterns for large-scale operations

## Quick start

```bash
git clone https://github.com/ZQM-Computing/gdal-cookbook.git
cd gdal-cookbook
bash examples/01-ogr2ogr-conversion/run.sh
```

## Examples

| # | Example | Description |
|---|---------|-------------|
| 01 | OGR2OGR Conversion | Vector format conversion |
| 02 | GDAL Translate | Raster format conversion |
| 03 | GDAL Warp | Reprojection and resampling |
| 04 | Virtual Rasters | VRT mosaicking |
| 05 | Batch Processing | Parallel processing |

## Cross-references

- [geopandas-cookbook](https://github.com/ZQM-Computing/geopandas-cookbook) — Python vector data processing
- [geoparquet-cookbook](https://github.com/ZQM-Computing/geoparquet-cookbook) — GeoParquet read/write
- [geospatial-cookbooks](https://github.com/ZQM-Computing/geospatial-cookbooks) — Umbrella index
