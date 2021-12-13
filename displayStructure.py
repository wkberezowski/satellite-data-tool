import h5py
import netCDF4

def importHDF():
 dataframe = h5py.File('data\gpm_jan_2020.HDF5', 'r')
 grid = dataframe['Grid']
 gridKeys = list(grid.keys())
 sizes = []
 
 for key in gridKeys:
  sizes.append(grid[key].size)
 
 return gridKeys, sizes

def importNETCDF():
 dataframe = netCDF4.Dataset('./data/daymet_v3_prcp_monttl_2017_hi.nc4', 'r', format='NETCDF4')
 vars = list(dataframe.variables)
 sizes = []
 
 for var in vars:
  sizes.append(dataframe[var].size)
  
 return vars, sizes
