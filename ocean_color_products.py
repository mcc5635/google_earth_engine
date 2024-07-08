import ee
import pandas as pd
import numpy as np
import geemap
import geemap.colormaps as cm
Map = geemap.Map()

ee.Authenticate()
ee.Initialize()

MODIS_OC_DS = ee.ImageCollection("NASA/OCEANDATA/MODIS-Aqua/L3SMI")

first_image = MODIS_OC_DS.first()
Bname = first_image.get('system:band_names')
print('system:band_names', Bname.getInfo())

selected_bands = 'chlor_a'
sY=2003
sM=1
sD=1
eY=2021
eM=12
eD=31
start_date = ee.Date.fromYMD(sY, sM, sD)
end_date   = ee.Date.fromYMD(eY, eM, eD)

ChlaDS = MODIS_OC_DS.select(selected_bands).filter(ee.Filter.date(start_date, end_date))

count = ChlaDS.size()
valCount=count.getInfo()
print('Image Count:', str(valCount)+\'n')


DecadalMeanChla= ChlaDS.reduce(ee.Reducer.mean())

val= cm.palettes.Spectral
palette=val.default

Vis = {
  'min': 0,
  'max': 0.65,
  'palette': palette
}

Map.setCenter(-30,14,5)
Map.addLayer(DecadalMeanChla, Vis, 'MeanChl-a')
Map

myears = range(sY,eY+1)
nmonths = range(1,12+1)
years = ee.List.sequence(sY, eY)
months = ee.List.sequence(sM, eM)

