#!/usr/bin/env bash
# Demonstrates vector format conversion with synthetic GeoJSON data.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="${OUTPUT_DIR:-$SCRIPT_DIR/output}"
mkdir -p "$OUTPUT_DIR"

cat > "$OUTPUT_DIR/synthetic_points.geojson" <<'GEOJSON_EOF'
{
  "type": "FeatureCollection",
  "features": [
    {"type":"Feature","properties":{"id":1,"name":"ALPHA"},"geometry":{"type":"Point","coordinates":[-73.9857,40.7484]}},
    {"type":"Feature","properties":{"id":2,"name":"BRAVO"},"geometry":{"type":"Point","coordinates":[-118.2437,34.0522]}},
    {"type":"Feature","properties":{"id":3,"name":"CHARLIE"},"geometry":{"type":"Point","coordinates":[-87.6298,41.8781]}}
  ]
}
GEOJSON_EOF

echo "[1/3] Synthetic GeoJSON created."
ogr2ogr -f "ESRI Shapefile" "$OUTPUT_DIR/synthetic_points.shp" "$OUTPUT_DIR/synthetic_points.geojson"
echo "[2/3] Converted GeoJSON to Shapefile."
ogr2ogr -f "GPKG" "$OUTPUT_DIR/synthetic_points.gpkg" "$OUTPUT_DIR/synthetic_points.geojson"
echo "[3/3] Converted GeoJSON to GeoPackage."
ls -lh "$OUTPUT_DIR"/synthetic_points.*
