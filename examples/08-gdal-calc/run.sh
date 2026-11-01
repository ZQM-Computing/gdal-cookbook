#!/usr/bin/env bash
# Demonstrate deterministic raster algebra with gdal_calc.py.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="${OUTPUT_DIR:-$SCRIPT_DIR/output}"
mkdir -p "$OUTPUT_DIR"

gdal_create -q -of GTiff -outsize 128 128 -bands 1 -ot Float32 \
  -burn 10 -a_srs EPSG:4326 -a_ullr -10 10 10 -10 \
  "$OUTPUT_DIR/input_a.tif"
gdal_create -q -of GTiff -outsize 128 128 -bands 1 -ot Float32 \
  -burn 3 -a_srs EPSG:4326 -a_ullr -10 10 10 -10 \
  "$OUTPUT_DIR/input_b.tif"

gdal_calc.py --overwrite --quiet \
  -A "$OUTPUT_DIR/input_a.tif" -B "$OUTPUT_DIR/input_b.tif" \
  --calc="A * 2 + B" --type=Float32 --NoDataValue=-9999 \
  --outfile="$OUTPUT_DIR/algebra_result.tif"

echo "Created raster algebra result: 2 * 10 + 3 = 23 for every pixel."
gdalinfo "$OUTPUT_DIR/algebra_result.tif"
