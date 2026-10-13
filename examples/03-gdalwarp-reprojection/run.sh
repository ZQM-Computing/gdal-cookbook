#!/usr/bin/env bash
# 03-gdalwarp-reprojection/run.sh
# Demonstrates raster reprojection with gdalwarp using synthetic data.
set -euo pipefail

# Create a synthetic raster in WGS84 (EPSG:4326).
gdal_create -outsize 512 256 -bands 1 -ot UInt16 \
  -burn 200 -a_srs EPSG:4326 -a_ullr -180 90 180 -90 \
  /tmp/synthetic_wgs84.tif
echo "[1/3] Synthetic WGS84 raster created."

# Reproject to Web Mercator (EPSG:3857) - common for web maps.
gdalwarp -t_srs EPSG:3857 -r bilinear \
  /tmp/synthetic_wgs84.tif /tmp/synthetic_webmercator.tif
echo "[2/3] Reprojected WGS84 to Web Mercator (bilinear)."

# Reproject to UTM Zone 33N (EPSG:32633) with nearest-neighbour.
gdalwarp -t_srs EPSG:32633 -r nearest \
  /tmp/synthetic_wgs84.tif /tmp/synthetic_utm33n.tif
echo "[3/3] Reprojected WGS84 to UTM Zone 33N (nearest)."

echo "Done. Outputs:"
ls -lh /tmp/synthetic_wgs84.tif /tmp/synthetic_webmercator.tif /tmp/synthetic_utm33n.tif
