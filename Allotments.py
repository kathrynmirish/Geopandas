import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

#import allotment data, remove blank lines and edit datatypes
allotments=pd.read_csv('Allotments.csv',usecols=["Postcode","AreaHectares"])
allotments=allotments.dropna()
allotments["AreaHectares"]=allotments["AreaHectares"].apply(float)


#import postcode/ward list
postcodes=pd.read_csv('pstoward.csv',usecols=["pcds","wd11nm"])
postcodes=postcodes.rename(columns={'pcds':'Postcode'})

#match postcode with ward
allotments=allotments.merge(postcodes,on='Postcode')
print(allotments.loc[allotments['wd11nm']=="Kirkstall"])

#summing hectares for wards
allotments=allotments.groupby(["wd11nm"]).sum()

#importing map of boundaries
leeds = gpd.read_file('https://ons-inspire.esriuk.com/arcgis/rest/services/Administrative_Boundaries/Wards_December_2016_Boundaries/MapServer/0/query?where=lad16nm+%3D+%27Leeds%27&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&f=geojson')

leeds=leeds.rename(columns={'wd16nm':'wd11nm'})
leeds=leeds.merge(allotments,on='wd11nm',how='outer')
leeds=leeds.fillna(0)

#plotting the map
leeds.plot(ax=leeds.boundary.plot(color='black'),column='AreaHectares',legend=True,cmap='OrRd')
plt.title('Hectares of allotments in Leeds')

#shortening the names of wards for readbility on map
for i in range(0,33):
    leeds["wd11nm"][i]=leeds["wd11nm"][i][0:4]

#adding labels to the wards
leeds["rep"]=leeds["geometry"].representative_point()
leeds_points=leeds.copy()
leeds_points.set_geometry("rep",inplace=True)
text=[]
for x, y, label in zip(leeds_points.geometry.x,leeds_points.geometry.y,leeds_points["wd11nm"]):
    text.append(plt.text(x,y,label,fontsize=5,ha='center',rotation='0'))
print(allotments)
plt.show()

'''Contains National Statistics data © Crown copyright and database right [2016]
Contains OS data © Crown copyright and database right [2016]'''