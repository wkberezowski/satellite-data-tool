import h5py
import numpy as np
import pandas as pd

def hdf5_to_csv():
 dataframe = h5py.File('data\gpm_jan_2020.HDF5', 'r')

 grid = dataframe['Grid']

 lonValues = np.repeat(list(grid['lon']), 1800)
 latValues = list(grid['lat']) * 3600
 percipitationValues = np.array(list(grid['precipitation'])).flatten()

 dataframe = pd.DataFrame({'lon': lonValues,
                         'lat': latValues,
                         'Precipitation': percipitationValues
                         })

 dataframe.columns = [grid['lon'].attrs['standard_name'].decode() + ' (' + grid['lon'].attrs['units'].decode() + ')',
                    grid['lat'].attrs['standard_name'].decode() + ' (' + grid['lat'].attrs['units'].decode() + ')',
                   'Precipitation (' + grid['precipitation'].attrs['units'].decode() + ')'
                    ]

 dataframe['Precipitation (mm/hr)'] = dataframe['Precipitation (mm/hr)'].mask(dataframe['Precipitation (mm/hr)'] == -9999.900391, 0)

 dataframe.to_csv('percipitation-from-hdf.csv', index=False)