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

def getMonthlyMean(iy):
  def createMean(im):
      sDate = ee.Date.fromYMD(iy, im, sD)
      eDate = sDate.advance(1, 'month')
      monthFiltered = ChlaDS.filter(ee.Filter.date(sDate, eDate))
      msum = monthFiltered.reduce(ee.Reducer.mean())
      return msum.set({
          'system:time_start': sDate.millis(),
          'system:time_end': eDate.millis(),
          'year': 1y,
          'month': 1m,
          'date': sDate.millis()
      })
  return months.map(createMean)

monthlyChla = ee.ImageCollection.fromImages(years.map(getMonthlyMean).flatten())

count = monthlyChla.size()
valCount = count.getInfo()
print('Monthly Mean Image Count:', str(valCount)+'\n')

first_image = monthlyChla.first()
Map.setCenter(-30,14,5)

iname=ee.Date(first_image.get('system:time_start')).format("yyyy-MM-dd")

Map.addLayer(first_image, Vis, iname.getInfo())
Map

# Run compute function 
def getMonthlyClimatology(mm):
  img = monthlyChla.filter(ee.Filter.calendarRange(sY,eY, 'year'))
  msum = img.reduce(ee.Reducer.mean())
  timeStamp = ee.Date.fromYMD(sY,mm,1)
  return msum.set({
        'system:time_start': timeStamp.millis(),
        'system:time_end':   timeStamp.millis(),
        'year': sY,
        'month': mm,
        'date': timeStamp.millis()
  })

MonthlyClim = ee.ImageCollection.fromImages(months.map(getMonthlyClimatology).flatten())

# QA Check
count - MonthlyClim.size()
valCount = count.getInfo()
print('Number of months count: ', str(valCount)+'\n')

first_image = MonthlyClim.first()

iname=(first_image.get('month').getInfo())
Map.addLayer(first_image, Vis, 'Monthly Climatology of: '+str(iname))
Map

def getYearlyMean(yy):
  img = monthlyChla.filter(ee.Filter.calendarRange(yy,yy , 'year')).filter(ee.Filter.calendarRange(sM, eM, 'month'))
  ymean = img.reduce(ee.Reducer.mean())
  timeStamp = ee.Date.fromYMD(yy,sM,1)
  return ymean.set({
       'system:time_start': timeStamp.millis(),
       'system:time_end':   timeStamp.millis(),
       'year': yy,
       'month': sM,
       'date': timeStamp.millis()
  })

yearlymean= ee.ImageCollection.fromImages(years.map(getYearlyMean).flatten())

# QA Band Verification

count = yearlymean.size()
valCount=count.getInfo()
print('Number of years count: ', str(valCount)+'\n')

first_image = yearlymean.first()

iname=iname=(first_image.get('year').getInfo())

Map.addLayer(first_image, Vis, str(iname))
Map






















