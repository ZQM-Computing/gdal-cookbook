# Rank 1: synthetic constraint layer preparation with GDAL

**SYNTHETIC only. Desktop GIS data preparation, not a wetland field delineation,
jurisdictional determination, Phase I ESA, survey, professional certification
or regulatory approval.** This shows only a source-to-exhibit layer step,
not a completed client figure or professional conclusion.

The script creates two fictitious source polygon features in WGS84
(EPSG:4326), clips to a fixed **synthetic** area, and reprojects the remaining
geometry into Florida State Plane East **EPSG:2236 (US survey feet)** using
`ogr2ogr`. It writes a GeoPackage, an explicit source/date/limitation
register, a source GeoJSON and a handoff limitations file. It does not use
actual NWI, FEMA or parcel sources.

Run from the repository root (GDAL/OGR 3.6+ and Bash required):

```sh
OUTPUT_DIR=/tmp/zqm-gdal-exhibit bash examples/09-exhibit-layer-prep/run.sh
ogrinfo -ro -so -al /tmp/zqm-gdal-exhibit/exhibit_constraints.gpkg
python -m pytest -q tests/test_examples_integration.py
```

The fixed bounding box intersects only the first synthetic source polygon.
The expected GeoPackage has **one** clipped polygon, projected output CRS
EPSG:2236, with source identifier `SYN-IND-1`. An existing destination is
refused rather than overwritten. The test suite asserts feature count,
CRS metadata, source register, and refusal of repeated writes.

Reviewers still need actual dataset coverage and positional accuracy,
validity/geometry QA, source ownership and permissible reuse, parcel-level
intersection rules, layout/legend/source-date requirements and final qualified
review. See the primary synthetic screening workflows in the
[PostGIS cookbook](https://github.com/ZQM-Computing/postgis-cookbook) and
[GeoPandas cookbook](https://github.com/ZQM-Computing/geopandas-cookbook).
