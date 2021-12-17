import h5py
import netCDF4


def import_hdf():
    dataframe = h5py.File('data\gpm_jan_2020.HDF5', 'r')
    grid = dataframe['Grid']
    grid_keys = list(grid.keys())
    sizes = []

    for key in grid_keys:
        sizes.append(grid[key].size)

    return grid_keys, sizes


def import_netcdf():
    dataframe = netCDF4.Dataset(
        './data/daymet_v3_prcp_monttl_2017_hi.nc4', 'r', format='NETCDF4')
    vars = list(dataframe.variables)
    sizes = []

    for var in vars:
        sizes.append(dataframe[var].size)

    return vars, sizes
