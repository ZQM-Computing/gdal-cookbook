-- Pattern 06: GDAL Python API Usage
-- Open a raster dataset
-- ds = gdal.Open('input.tif')
-- band = ds.GetRasterBand(1)
-- arr = band.ReadAsArray()

-- Create a new raster in memory
-- driver = gdal.GetDriverByName('MEM')
-- ds = driver.Create('', xsize, ysize, bands, gdal.GDT_Float32)

-- Set geotransform and projection
-- ds.SetGeoTransform([xmin, xres, 0, ymax, 0, -yres])
-- srs = osr.SpatialReference(); srs.ImportFromEPSG(4326)
-- ds.SetProjection(srs.ExportToWkt())

-- Write array to band
-- band = ds.GetRasterBand(1)
-- band.WriteArray(arr)
-- band.SetNoDataValue(-9999)

-- Reproject raster with gdal.Warp
-- gdal.Warp('out.tif', 'in.tif', dstSRS='EPSG:3857', resampleAlg=gdal.GRA_Bilinear)

-- Translate / subset raster
-- gdal.Translate('out.tif', 'in.tif', srcWin=[xoff, yoff, xsize, ysize])

-- Open vector layer
-- ds = ogr.Open('input.shp')
-- layer = ds.GetLayer(0)
-- for feat in layer: print(feat.GetField('name'))

-- Create new vector layer
-- driver = ogr.GetDriverByName('GeoJSON')
-- ds = driver.CreateDataSource('out.geojson')
-- layer = ds.CreateLayer('points', srs, ogr.wkbPoint)
-- field = ogr.FieldDefn('name', ogr.OFTString); layer.CreateField(field)

-- OGR SQL query
-- result = ds.ExecuteSQL("SELECT * FROM input WHERE pop > 1000")

-- Geometry operations
-- geom = ogr.CreateGeometryFromWkt('POINT(0 0)')
-- buffered = geom.Buffer(10.0)
-- print(buffered.ExportToWkt())

-- Coordinate transformation
-- src_srs = osr.SpatialReference(); src_srs.ImportFromEPSG(4326)
-- dst_srs = osr.SpatialReference(); dst_srs.ImportFromEPSG(3857)
-- transform = osr.CoordinateTransformation(src_srs, dst_srs)
-- x, y, z = transform.TransformPoint(lon, lat)

-- Rasterize vector to raster (Python)
-- gdal.Rasterize('out.tif', 'input.shp', burnValues=[1], xRes=30, yRes=30)

-- Polygonize raster (Python)
-- gdal.Polygonize(src_band, None, dst_layer, -1, [], callback=None)