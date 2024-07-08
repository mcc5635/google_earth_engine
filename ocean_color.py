import ee
import pandas as pd
import numpy as np
import geemap
import geemap.colormaps as cm



# Start authentication

try:
  ee.Initialize()
except Exception as e:
  ee.Authenticate()
  ee.Initialize()


Map = geemap.Map()


MODIS_OC_DS = ee.ImageCollection("NASA/OCEANDATA/MODIS-Aqua/L3SMI")

first_image = MODIS_OC_DS.first()
System_band = first_image.get('system:band_names')
print('system:band_names', System_band.getInfo())


