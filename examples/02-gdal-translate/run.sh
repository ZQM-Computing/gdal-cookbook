#!/usr/bin/env bash
# 02-gdal-translate/run.sh
# Demonstrates raster translation, format conversion, and subsetting with gdal_translate.
set -euo pipefail

# Build a small synthetic GeoTIFF using gdal_create (no downloads).
gdal_create -outsize 256 256 -bands 3 -ot Byte \
  -burn 128 -a_srs EPSG:4326 -a_ullr -180 90 180 -90 \
  /tmp/synthetic_raster.tif
echo "[1/3] Synthetic 3-band GeoTIFF created (256x256)."

# Translate to PNG (format conversion + data type coercion).
gdal_translate -of PNG -scale 0 255 0 255 \
  /tmp/synthetic_raster.tif /tmp/synthetic_raster.png
echo "[2/3] Translated GeoTIFF to PNG."

# Subset with -srcwin (pixel window: xoff yoff xsize ysize).
gdal_translate -srcwin 64 64 128 128 \
  /tmp/synthetic_raster.tif /tmp/synthetic_subset.tif
echo "[3/3] Extracted 128x128 pixel subset."

echo "Done. Outputs:"
ls -lh /tmp/synthetic_raster.{tif,png} /tmp/synthetic_subset.tif
