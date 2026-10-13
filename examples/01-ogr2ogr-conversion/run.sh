#!/usr/bin/env bash
# 01-ogr2ogr-conversion/run.sh
# Demonstrates vector format conversion with ogr2ogr using synthetic GeoJSON data.
set -euo pipefail

# Create a synthetic GeoJSON point file (no external downloads needed).
cat > /tmp/synthetic_points.geojson <<'GEOJSON_EOF'
{
  "type": "FeatureCollection",
  "features": [
    {"type":"Feature","properties":{"id":1,"name":"ALPHA"},
     "geometry":{"type":"Point","coordinates":[-73.9857,40.7484]}},
    {"type":"Feature","properties":{"id":2,"name":"BRAVO"},
     "geometry":{"type":"Point","coordinates":[-118.2437,34.0522]}},
    {"type":"Feature","properties":{"id":3,"name":"CHARLIE"},
     "geometry":{"type":"Point","coordinates":[-87.6298,41.8781]}}
  ]
}
GEOJSON_EOF

echo "[1/3] Synthetic GeoJSON created."

# Convert GeoJSON to Shapefile (most common conversion pattern).
ogr2ogr -f "ESRI Shapefile" /tmp/synthetic_points.shp /tmp/synthetic_points.geojson
echo "[2/3] Converted GeoJSON to Shapefile."

# Convert GeoJSON to GeoPackage (modern, single-file alternative).
ogr2ogr -f "GPKG" /tmp/synthetic_points.gpkg /tmp/synthetic_points.geojson
echo "[3/3] Converted GeoJSON to GeoPackage."

echo "Done. Outputs:"
ls -lh /tmp/synthetic_points.{shp,shx,dbf,prj,gpkg} 2>/dev/null || true
