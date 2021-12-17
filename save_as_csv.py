import h5py
import numpy as np
import pandas as pd
import netCDF4


def hdf5_to_csv():
    dataframe = h5py.File('data\gpm_jan_2020.HDF5', 'r')

    grid = dataframe['Grid']

    lon_values = np.repeat(list(grid['lon']), 1800)
    lat_values = list(grid['lat']) * 3600
    percip_values = np.array(list(grid['precipitation'])).flatten()

    dataframe = pd.DataFrame({'lon': lon_values,
                              'lat': lat_values,
                              'Precipitation': percip_values
                              })

    dataframe.columns = [grid['lon'].attrs['standard_name'].decode() +
                         ' (' + grid['lon'].attrs['units'].decode() + ')',
                         grid['lat'].attrs['standard_name'].decode(
    ) + ' (' + grid['lat'].attrs['units'].decode() + ')',
        'Precipitation (' +
        grid['precipitation'].attrs['units'].decode() + ')'
    ]

    dataframe['Precipitation (mm/hr)'] = dataframe['Precipitation (mm/hr)'].mask(
        dataframe['Precipitation (mm/hr)'] == -9999.900391, 0)

    dataframe.to_csv('percipitation-from-hdf.csv', index=False)


def netCDF_to_csv():
    # READ DATASET
    dataset = netCDF4.Dataset(
        './data/daymet_v3_prcp_monttl_2017_hi.nc4', 'r', format='NETCDF4')

    # DONT KNOW IF ITS BETTER TO USE LON/LAT OR Y/X
    lon = dataset['lon'][:, 0]
    lat = dataset['lat'][0]
    prcp = dataset['prcp'][0]

    lon_values = np.repeat(list(lon), lat.size)
    lat_values = list(lat) * lon.size
    percip_values = np.array(list(prcp)).flatten()

    dataframe = pd.DataFrame({'lon': lon_values,
                              'lat': lat_values,
                              'prcp': percip_values})

    dataframe.columns = ['{} in {}'.format(dataset['lon'].standard_name, dataset['lon'].units), '{} in {}'.format(
        dataset['lat'].standard_name, dataset['lat'].units), '{} in {}'.format(dataset['prcp'].long_name, dataset['prcp'].units)]

    dataframe.to_csv('percipitation-from-netCDF.csv', index=False)
