-- Pattern 05: GDAL Format Conversion
-- GeoTIFF to COG (Cloud Optimized GeoTIFF)
-- gdal_translate -of COG -co COMPRESS=DEFLATE -co OVERVIEWS=IGNORE_EXISTING input.tif output_cog.tif

-- Shapefile to GeoJSON
-- ogr2ogr -f "GeoJSON" output.geojson input.shp

-- GeoJSON to GeoParquet
-- ogr2ogr -f "Parquet" output.parquet input.geojson

-- GeoPackage to FlatGeobuf
-- ogr2ogr -f "FlatGeobuf" output.fgb input.gpkg

-- KML to GeoJSON
-- ogr2ogr -f "GeoJSON" output.geojson input.kml

-- CSV (with lat/lon) to GeoJSON
-- ogr2ogr -f "GeoJSON" output.geojson input.csv -oo X_POSSIBLE_NAMES=lon -oo Y_POSSIBLE_NAMES=lat

-- PostGIS to GeoPackage
-- ogr2ogr -f "GPKG" output.gpkg PG:"host=localhost dbname=gis user=postgres" -sql "SELECT * FROM roads"

-- GeoTIFF to PNG (8-bit)
-- gdal_translate -of PNG -scale 0 255 0 255 -ot Byte input.tif output.png

-- NetCDF to GeoTIFF
-- gdal_translate -of GTiff NETCDF:"input.nc":variable output.tif

-- HDF5 to GeoTIFF
-- gdal_translate -of GTiff HDF5:"input.h5"://variable output.tif

-- SQLite/SpatiaLite to GeoPackage
-- ogr2ogr -f "GPKG" output.gpkg input.sqlite

-- GeoJSON to TopoJSON
-- ogr2ogr -f "TopoJSON" output.json input.geojson

-- VRT to GeoTIFF (materialize virtual raster)
-- gdal_translate -of GTiff input.vrt output.tif