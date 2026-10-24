-- Pattern 04: GDAL Raster Processing
-- Compute statistics (min/max/mean/std)
-- gdalinfo -stats input.tif

-- Generate histogram
-- gdalinfo -hist input.tif

-- Hillshade from DEM
-- gdaldem hillshade dem.tif hillshade.tif -z 2 -az 315 -alt 45

-- Slope map (degrees)
-- gdaldem slope dem.tif slope.tif

-- Aspect map
-- gdaldem aspect dem.tif aspect.tif

-- Terrain Ruggedness Index (TRI)
-- gdaldem TRI dem.tif tri.tif

-- Raster calculator: NDVI
-- gdal_calc.py -A nir.tif -B red.tif --outfile=ndvi.tif --calc="(A-B)/(A+B)" --NoDataValue=-9999

-- Reclassify raster values
-- gdal_calc.py -A input.tif --outfile=reclass.tif --calc="(A>100)*2+(A<=100)*1"

-- Rasterize vector to raster (burn values)
-- gdal_rasterize -a value -tr 30 30 -of GTiff -te xmin ymin xmax ymax input.shp output.tif

-- Polygonize raster to vector
-- gdal_polygonize.py input.tif -f GeoJSON output.geojson

-- Contour generation from DEM
-- gdal_contour -a elevation dem.tif contours.shp -i 10.0

-- Mosaic with overlap (blend)
-- gdalbuildvrt -srcnodata 0 mosaic.vrt tile_*.tif && gdal_translate mosaic.vrt mosaic.tif

-- Fill NoData holes
-- gdal_fillnodata.py input.tif output.tif -md 100

-- Resample raster to new resolution
-- gdalwarp -tr 30 30 -r bilinear input.tif resampled.tif

-- Crop raster to shapefile extent
-- gdalwarp -cutline mask.shp -crop_to_cutline input.tif cropped.tif