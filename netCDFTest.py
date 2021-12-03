import netCDF4 
import pandas as pd

dataset = netCDF4.Dataset('data\daymet_v3_prcp_monttl_2017_hi.nc4')

# PRINTING DIMENSIONS
for dim in dataset.dimensions:
 # print(dim)
 pass

lat = dataset.variables['lat'][:]
lon = dataset.variables['lon'][:]
prcp = dataset.variables['prcp'][:]

dataSeries = pd.Series(prcp)

dataSeries.to_csv('prcp.csv', index=True, header=True)
