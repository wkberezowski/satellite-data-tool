import netCDF4 
import pandas as pd
import numpy as np

# READ DATASET
dataset = netCDF4.Dataset('./data/daymet_v3_prcp_monttl_2017_hi.nc4', 'r', format='NETCDF4')

# DONT KNOW IF ITS BETTER TO USE LON/LAT OR Y/X
lon = dataset['lon'][:, 0]
lat = dataset['lat'][0]
prcp = dataset['prcp'][0]


lonValues = np.repeat(list(lon), lat.size)
latValues = list(lat) * lon.size
prcpValues = np.array(list(prcp)).flatten()

dataframe = pd.DataFrame({'lon': lonValues,
                          'lat': latValues,
                          'prcp': prcpValues})

dataframe.columns = ['{} in {}'.format(dataset['lon'].standard_name, dataset['lon'].units), '{} in {}'.format(dataset['lat'].standard_name, dataset['lat'].units), '{} in {}'.format(dataset['prcp'].long_name, dataset['prcp'].units)]

dataframe.to_csv('percipitation-from-netCDF.csv', index=False) 