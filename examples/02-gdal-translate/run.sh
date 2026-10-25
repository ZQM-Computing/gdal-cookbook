#!/usr/bin/env bash
# Demonstrates raster translation, format conversion, and subsetting.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="${OUTPUT_DIR:-$SCRIPT_DIR/output}"
mkdir -p "$OUTPUT_DIR"

gdal_create -outsize 256 256 -bands 3 -ot Byte -burn 128 \
  -a_srs EPSG:4326 -a_ullr -180 90 180 -90 "$OUTPUT_DIR/synthetic_raster.tif"
echo "[1/3] Synthetic 3-band GeoTIFF created (256x256)."
gdal_translate -of PNG -scale 0 255 0 255 \
  "$OUTPUT_DIR/synthetic_raster.tif" "$OUTPUT_DIR/synthetic_raster.png"
echo "[2/3] Translated GeoTIFF to PNG."
gdal_translate -srcwin 64 64 128 128 \
  "$OUTPUT_DIR/synthetic_raster.tif" "$OUTPUT_DIR/synthetic_subset.tif"
echo "[3/3] Extracted 128x128 pixel subset."
ls -lh "$OUTPUT_DIR"/synthetic_raster.* "$OUTPUT_DIR/synthetic_subset.tif"
