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


# Data Filtering
selected_bands = 'chlor_a'
sY=2003
sM=1
sD=1
eY=2021
eM=9
eD=28
start_date = ee.Date.fromYMD(sY, sM, sD)
end_date = ee.Date.fromYMD(eY, eM, eD)
print(str(start_date))


count = ChlaDS.size()
valTest = count.getInfo()
print('Image count : ', str(valTest)+'\n')

# Compute average Chl-a for the whole period
DecadalMeanChla = ChlaDS.reduce(ee.Reducer.mean())

# Visualize calculated mean
val = cm.palettes.Spectral
palette=val.default

Vis = {
  'min': 0,
  'max': 0.5,
  'palette': palette
}

Map.setCenter(-30,14,5)
Map.addLayer(DecadalMeanChla, Vis, 'MeanChl-a')
Map.addLayer(ChlaDS.first(),Vis,'FirstImage')
Map

# Start time-series forecast
years = ee.List.sequence(sY, eY)
months = ee.List.sequence(sM, eM)

def getMonthlyMean(iy):













