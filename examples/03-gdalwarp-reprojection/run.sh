#!/usr/bin/env bash
# Demonstrates raster reprojection with synthetic data.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="${OUTPUT_DIR:-$SCRIPT_DIR/output}"
mkdir -p "$OUTPUT_DIR"

gdal_create -outsize 512 256 -bands 1 -ot UInt16 -burn 200 \
  -a_srs EPSG:4326 -a_ullr -180 90 180 -90 "$OUTPUT_DIR/synthetic_wgs84.tif"
echo "[1/3] Synthetic WGS84 raster created."
gdalwarp -t_srs EPSG:3857 -r bilinear \
  "$OUTPUT_DIR/synthetic_wgs84.tif" "$OUTPUT_DIR/synthetic_webmercator.tif"
echo "[2/3] Reprojected WGS84 to Web Mercator (bilinear)."
gdalwarp -t_srs EPSG:32633 -r near \
  "$OUTPUT_DIR/synthetic_wgs84.tif" "$OUTPUT_DIR/synthetic_utm33n.tif"
echo "[3/3] Reprojected WGS84 to UTM Zone 33N (nearest-neighbour)."
ls -lh "$OUTPUT_DIR"/synthetic_*.tif
