-- Pattern 01: Vector Format Conversion
-- GeoJSON to Shapefile
-- ogr2ogr -f "ESRI Shapefile" output.shp input.geojson

-- GeoJSON to GeoParquet
-- ogr2ogr -f "GeoParquet" output.parquet input.geojson

-- GeoJSON to GPKG
-- ogr2ogr -f "GPKG" output.gpkg input.geojson
