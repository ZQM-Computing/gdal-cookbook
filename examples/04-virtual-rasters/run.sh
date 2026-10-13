#!/usr/bin/env bash
# 04-virtual-rasters/run.sh
# Demonstrates Virtual Raster (VRT) mosaicking with synthetic data.
set -euo pipefail

# Create three small synthetic tiles that will form a mosaic.
for i in 1 2 3; do
  gdal_create -outsize 128 128 -bands 1 -ot Byte \
    -burn $((i * 60)) -a_srs EPSG:4326 \
    -a_ullr $((i * 10 - 20)) 10 $((i * 10 - 10)) 0 \
    /tmp/synthetic_tile_${i}.tif
done
echo "[1/3] Three synthetic tiles created."

# Build a VRT mosaic (no data copied - just a virtual index).
gdalbuildvrt /tmp/synthetic_mosaic.vrt /tmp/synthetic_tile_{1,2,3}.tif
echo "[2/3] VRT mosaic built from 3 tiles."

# Translate the VRT to a real GeoTIFF (materialise the mosaic).
gdal_translate -of GTiff /tmp/synthetic_mosaic.vrt /tmp/synthetic_mosaic.tif
echo "[3/3] Materialised VRT to GeoTIFF."

echo "Done. Outputs:"
ls -lh /tmp/synthetic_tile_*.tif /tmp/synthetic_mosaic.{vrt,tif}
