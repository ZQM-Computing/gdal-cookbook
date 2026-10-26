#!/usr/bin/env bash
# Create a Cloud Optimized GeoTIFF with internal overviews and verify-ready metadata.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="${OUTPUT_DIR:-$SCRIPT_DIR/output}"
mkdir -p "$OUTPUT_DIR"

gdal_create -outsize 1024 1024 -bands 3 -ot Byte -burn 128 \
  -a_srs EPSG:4326 -a_ullr -180 90 180 -90 \
  "$OUTPUT_DIR/synthetic_source.tif"
echo "[1/2] Synthetic 3-band source raster created (1024x1024)."

gdal_translate -of COG \
  -co COMPRESS=DEFLATE \
  -co BLOCKSIZE=128 \
  -co OVERVIEWS=AUTO \
  "$OUTPUT_DIR/synthetic_source.tif" "$OUTPUT_DIR/synthetic_cog.tif"
echo "[2/2] Created Cloud Optimized GeoTIFF with generated overviews."
gdalinfo "$OUTPUT_DIR/synthetic_cog.tif"
