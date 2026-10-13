#!/usr/bin/env bash
# 05-batch-processing/run.sh
# Demonstrates batch raster processing with a shell loop over synthetic files.
set -euo pipefail

# Generate 5 synthetic rasters with varying pixel values.
for i in $(seq 1 5); do
  gdal_create -outsize 64 64 -bands 1 -ot Byte \
    -burn $((i * 40)) -a_srs EPSG:4326 \
    -a_ullr 0 10 10 0 \
    /tmp/batch_input_${i}.tif
done
echo "[1/3] Five synthetic input rasters created."

# Batch: compute statistics for each raster.
echo "[2/3] Computing per-band statistics..."
for f in /tmp/batch_input_*.tif; do
  echo "  -- $(basename "$f") --"
  gdalinfo -stats "$f" | grep -E "STATISTICS_(MINIMUM|MAXIMUM|MEAN)" || true
done

# Batch: convert all inputs to a single multi-band VRT.
gdalbuildvrt -separate /tmp/batch_stack.vrt /tmp/batch_input_*.tif
echo "[3/3] Stacked all rasters into a multi-band VRT."

echo "Done. Outputs:"
ls -lh /tmp/batch_input_*.tif /tmp/batch_stack.vrt
