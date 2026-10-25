#!/usr/bin/env bash
# Demonstrates Virtual Raster (VRT) mosaicking with synthetic data.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="${OUTPUT_DIR:-$SCRIPT_DIR/output}"
mkdir -p "$OUTPUT_DIR"

for i in 1 2 3; do
  gdal_create -outsize 128 128 -bands 1 -ot Byte \
    -burn $((i * 60)) -a_srs EPSG:4326 \
    -a_ullr $((i * 10 - 20)) 10 $((i * 10 - 10)) 0 \
    "$OUTPUT_DIR/synthetic_tile_${i}.tif"
done
echo "[1/3] Three synthetic tiles created."
gdalbuildvrt "$OUTPUT_DIR/synthetic_mosaic.vrt" \
  "$OUTPUT_DIR/synthetic_tile_1.tif" "$OUTPUT_DIR/synthetic_tile_2.tif" "$OUTPUT_DIR/synthetic_tile_3.tif"
echo "[2/3] VRT mosaic built from 3 tiles."
gdal_translate -of GTiff "$OUTPUT_DIR/synthetic_mosaic.vrt" "$OUTPUT_DIR/synthetic_mosaic.tif"
echo "[3/3] Materialised VRT to GeoTIFF."
ls -lh "$OUTPUT_DIR"/synthetic_tile_*.tif "$OUTPUT_DIR"/synthetic_mosaic.*
