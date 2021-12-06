import netCDF4 
import pandas as pd
import numpy as np

# CREATE DATASET
dataset = netCDF4.Dataset('netCDF_test.nc4', 'w', format='NETCDF4')

# ADD DIMENSIONS
time = dataset.createDimension('time', None)
lat = dataset.createDimension('lat', 10)
lon = dataset.createDimension('lon', 10)

# ADD VARIABLES
times = dataset.createVariable('time', 'f4', ('time',))
lats = dataset.createVariable('lat', 'f4', ('lat',))
lons = dataset.createVariable('lon', 'f4', ('lon',))
value = dataset.createVariable('value', 'f4', ('time', 'lat', 'lon'))

value.units = 'Unknown'

# ASSIGN LATITUDE AND LONGITUDE VALUES
lats[:] = np.arange(40.0, 50.0, 1.0)
lons[:] = np.arange(-110.0, -100.0, 1.0)

# ASSIGN NetCDF DATA VALUES
value[0, :, :] = np.random.uniform(0, 100, size=(10, 10))

print('var size after adding first data', value.shape)
xval = np.linspace(0.5, 5, 10)
yval = np.linspace(0.5, 5, 10)
value[1, :, :] = np.array(xval.reshape(-1, 1) + yval)
dataset.close()
