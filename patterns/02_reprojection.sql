-- Pattern 02: Reprojection
-- Reproject raster to EPSG:4326
-- gdalwarp -t_srs EPSG:4326 input.tif output.tif

-- Reproject vector to EPSG:3857
-- ogr2ogr -t_srs EPSG:3857 output.shp input.shp
