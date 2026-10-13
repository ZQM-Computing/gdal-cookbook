#!/usr/bin/env python3
"""
06-python-integration/run.py
Demonstrates GDAL Python bindings for raster I/O and reprojection using
synthetic data (no external downloads).
"""
import os
import numpy as np
from osgeo import gdal, osr

# 1. Create a synthetic raster in memory
driver = gdal.GetDriverByName("MEM")
ds = driver.Create("", 128, 128, 1, gdal.GDT_Byte)
ds.SetGeoTransform([0, 1, 0, 0, 0, -1])  # origin (0,0), 1-degree pixels

srs = osr.SpatialReference()
srs.ImportFromEPSG(4326)
ds.SetProjection(srs.ExportToWkt())

# Fill with a gradient pattern (synthetic data).
arr = np.tile(np.arange(128, dtype=np.uint8), (128, 1))
ds.GetRasterBand(1).WriteArray(arr)
print("[1/3] In-memory synthetic raster created (128x128, EPSG:4326).")

# 2. Reproject to Web Mercator
warp_opts = gdal.WarpOptions(
    dstSRS="EPSG:3857",
    resampleAlg=gdal.GRA_Bilinear,
    format="MEM",
)
reproj = gdal.Warp("", ds, options=warp_opts)
print("[2/3] Reprojected to EPSG:3857 (Web Mercator).")

# 3. Read back and verify
band = reproj.GetRasterBand(1)
data = band.ReadAsArray()
print(f"[3/3] Output size: {reproj.RasterXSize}x{reproj.RasterYSize}")
print(f"      Pixel value range: {data.min()}-{data.max()}")
print("Done.")
