import h5py
import numpy as np
import pandas as pd

dataset = h5py.File('data\gpm_jan_2020.HDF5', 'r')

grid = dataset['Grid']
print(grid.keys())

print("Longitude data: {}".format(grid['lon']))
print("Longitude data attributes: {}".format(list(grid['lon'].attrs)))
print("Name: {}".format(grid['lon'].attrs['standard_name'].decode()))
print("Unit: {}".format(grid['lon'].attrs['units'].decode()))

lonValues = np.repeat(list(grid['lon']), 1800)
latValues = list(grid['lat']) * 3600
percipitationValues = np.array(list(grid['precipitation'])).flatten()

dataset = pd.DataFrame({'lon': lonValues,
                        'lat': latValues,
                        'Precipitation': percipitationValues
                        })

dataset.columns = [grid['lon'].attrs['standard_name'].decode() + ' (' + grid['lon'].attrs['units'].decode() + ')',
                   grid['lat'].attrs['standard_name'].decode() + ' (' + grid['lat'].attrs['units'].decode() + ')',
                  'Precipitation (' + grid['precipitation'].attrs['units'].decode() + ')'
                   ]

dataset['Precipitation (mm/hr)'] = dataset['Precipitation (mm/hr)'].mask(dataset['Precipitation (mm/hr)'] == -9999.900391, 0)

dataset.to_csv('percipitation_jan_2020.csv', index=False)
