#!/usr/bin/env bash
# Rank 1: synthetic environmental GIS exhibit input preparation (GDAL/OGR).
# Desktop data preparation only. NOT a wetland field delineation, jurisdictional
# determination, Phase I ESA, boundary survey, certification or permit approval.
# All geometries and source records are synthetic. Verify real sources,
# retrieval dates, spatial uncertainties and field findings separately.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="${OUTPUT_DIR:-$SCRIPT_DIR/output}"
mkdir -p "$OUTPUT_DIR"
for name in source_constraints.geojson exhibit_constraints.gpkg source_register.json LIMITATIONS.txt; do
  if [[ -e "$OUTPUT_DIR/$name" ]]; then
    echo "Refusing to overwrite existing exhibit artifact: $OUTPUT_DIR/$name" >&2
    exit 2
  fi
done

cat > "$OUTPUT_DIR/source_constraints.geojson" <<'GEOJSON_EOF'
{
  "type": "FeatureCollection",
  "features": [
    {"type":"Feature","properties":{"source_id":"SYN-IND-1","constraint_type":"synthetic_wetland_indicator"},"geometry":{"type":"Polygon","coordinates":[[[-81.08,29.03],[-81.00,29.03],[-81.00,29.09],[-81.08,29.09],[-81.08,29.03]]]}},
    {"type":"Feature","properties":{"source_id":"SYN-IND-2","constraint_type":"synthetic_flood_indicator"},"geometry":{"type":"Polygon","coordinates":[[[-80.92,29.03],[-80.85,29.03],[-80.85,29.09],[-80.92,29.09],[-80.92,29.03]]]}}
  ]
}
GEOJSON_EOF

cat > "$OUTPUT_DIR/source_register.json" <<'SOURCE_EOF'
{
  "data": "synthetic",
  "dataset_name": "Illustrative environmental indicator polygons",
  "publisher": "ZQM synthetic demo",
  "retrieved_on": "2026-11-14",
  "version": "fixture-v1",
  "source_url": "https://example.org/synthetic/constraints",
  "known_limitations": "Fictitious source and features; no field work, authority, verified coverage or positional accuracy.",
  "source_crs": "EPSG:4326",
  "output_crs": "EPSG:2236",
  "clip_bbox_epsg_4326": [-81.07, 29.04, -81.01, 29.08],
  "uncertainty_flag": "synthetic-unverified"
}
SOURCE_EOF

cat > "$OUTPUT_DIR/LIMITATIONS.txt" <<'LIMITS_EOF'
SYNTHETIC desktop-only environmental GIS exhibit-preparation demonstration.
NOT a wetland delineation, jurisdictional determination, Phase I environmental
site assessment, survey, professional certification or permit approval.
This clipping/reprojection step does NOT establish data coverage, source
accuracy, environmental constraints or regulatory meaning. Validate source
retrieval dates, positional uncertainty, CRS, permitted use, and exclusions
with qualified professionals before any real-world decision.
The output is map-preparation data, NOT a completed client exhibit.
LIMITS_EOF

# -clipsrc applies a 4326 bbox to WGS84 source polygons; -t_srs transforms
# coordinates to Florida State Plane East 2236, US survey feet. Do not treat
# those coordinates as metres; record source+output units with every handoff.
ogr2ogr -f GPKG "$OUTPUT_DIR/exhibit_constraints.gpkg" "$OUTPUT_DIR/source_constraints.geojson" \
  -nln exhibit_constraints -clipsrc -81.07 29.04 -81.01 29.08 \
  -t_srs EPSG:2236 -lco SPATIAL_INDEX=YES

echo "Synthetic constraints clipped/reprojected for exhibit preparation."
ogrinfo -ro -so -al "$OUTPUT_DIR/exhibit_constraints.gpkg"
