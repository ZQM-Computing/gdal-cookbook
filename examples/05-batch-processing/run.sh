#!/usr/bin/env bash
# Demonstrates batch raster processing with a shell loop over synthetic files.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="${OUTPUT_DIR:-$SCRIPT_DIR/output}"
mkdir -p "$OUTPUT_DIR"

for i in $(seq 1 5); do
  gdal_create -outsize 64 64 -bands 1 -ot Byte \
    -burn $((i * 40)) -a_srs EPSG:4326 -a_ullr 0 10 10 0 \
    "$OUTPUT_DIR/batch_input_${i}.tif"
done
echo "[1/3] Five synthetic input rasters created."
echo "[2/3] Computing per-band statistics..."
for f in "$OUTPUT_DIR"/batch_input_*.tif; do
  echo "  -- $(basename "$f") --"
  gdalinfo -stats "$f" | grep -E "STATISTICS_(MINIMUM|MAXIMUM|MEAN)" || true
done
gdalbuildvrt -separate "$OUTPUT_DIR/batch_stack.vrt" "$OUTPUT_DIR"/batch_input_*.tif
echo "[3/3] Stacked all rasters into a multi-band VRT."
ls -lh "$OUTPUT_DIR"/batch_input_*.tif "$OUTPUT_DIR/batch_stack.vrt"
