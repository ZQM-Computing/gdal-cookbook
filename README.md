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
