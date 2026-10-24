-- Pattern 03: GDAL Vector Operations
-- Clip a vector layer to a bounding box
-- ogr2ogr -f "ESRI Shapefile" clipped.shp input.shp -clipsrc xmin ymin xmax ymax

-- Clip vector to polygon mask
-- ogr2ogr -f "GeoJSON" clipped.geojson input.geojson -clipsrc mask.shp -clipsrclayer mask

-- Dissolve features by attribute
-- ogr2ogr -dialect sqlite -sql "SELECT ST_Union(geometry) AS geometry, region FROM input GROUP BY region" dissolved.shp input.shp

-- Buffer features by distance
-- ogr2ogr -f "GPKG" buffered.gpkg input.gpkg -sql "SELECT ST_Buffer(geometry, 100) AS geometry, * FROM input"

-- Spatial join: intersect points with polygons
-- ogr2ogr -f "GeoJSON" joined.geojson points.geojson -sql "SELECT p.*, r.name AS region FROM points p JOIN regions r ON ST_Intersects(p.geometry, r.geometry)"

-- Filter features by attribute
-- ogr2ogr -f "GPKG" filtered.gpkg input.gpkg -where "population > 100000 AND status = 'active'"

-- Reproject vector on the fly
-- ogr2ogr -t_srs EPSG:32633 -f "GeoJSON" utm.geojson wgs84.geojson

-- Export to CSV with geometry as WKT
-- ogr2ogr -f "CSV" output.csv input.shp -lco GEOMETRY=AS_WKT

-- Create spatial index on GeoPackage
-- ogrinfo input.gpkg -sql "SELECT CreateSpatialIndex('input', 'geom')"

-- Validate geometry and fix invalid
-- ogr2ogr -f "GPKG" fixed.gpkg input.gpkg -sql "SELECT ST_MakeValid(geometry) AS geometry, * FROM input"