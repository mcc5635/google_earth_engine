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
    def createMean(im):
      sDate = ee.Date.fromYMD(iy, im, sD)
      eDate = sDate.advance(1, 'month')
      monthFiltered = ChlaDS.filter(ee.Filter.date(sDate,
      msum = monthFiltered.reduce(ee.Reducer.mean())
      return msum.set({
    return months.map(createMean)


monthlyChla = ee.ImageCollection.fromImages(years.map(getMonthlyMean).flatten())

count = monthlyChla.size()
valCount=count.getInfo()
print('Monthly Mean Image Count :', str(valCount)+'\n')

first_iamge = monthlyChla.first()
Map.setCenter(-30,14,5)
Map.addLayer(first_image, Vis, 'MonthlyChl-a')
Map

seas_shapefile_path = "./../seas/boxMed.geojson"
                                            
def getTM4RoI(imgcol):
  def iter_func(image, newlist):
      date = ee.Number.parse(image.date().format("YYYYMMdd"))
      stat = image.reduceRegion(
          reducer = ee.Reducer.mean(),
          geometry = seas,
          scale = 5000,
          maxPixels = 1e15)
      newlist = ee.List(newlist)
      res = newlist.add([date, stat])
      return ee.List(res)
  ymd = imgcol.iterate(iter_func, ee.List([]))
  return list(ee.List(ymd).getInfo())
inList = getTM4RoI(monthlyChla)

# Return list to dataframe
def Convert2TM_DF(inList):
    newList =[]
    for i, item in enumerate(inList):
        if np.any(item[1].get('chlor_a_mean')):
            newList.append([item[0],item[1].get('chlor_a_mean')])
    DF=pd.DataFrame(newList,columns=['Dates' ,'Chl-a'])
    datetime_series = pd.to_datetime(DF['Dates'],format='%Y%m%d')
    DF.drop('Dates', axis=1, inplace=True)
    DF.set_index(datetime_series, inplace=True,drop=True)
    DF.mask(DF.eq('None')).dropna()
    return DF

TM_Chla = Convert2TM_DF(inList)
TM_Chla

# Return Chl-a monthly mean visualization
ax_=TM_Chla.plot(kind='line',
                    legend= False,
                    ylabel='Chl-a [\mu g m^{-3}]',
                    xlabel='Date',
                    title='Monthly mean of Chl-a in the Mediterranean')











