import h5py
import numpy as np
import pandas as pd
import netCDF4
from tkinter import *
from tkinter import ttk


def hdf_handler():
    dataframe = h5py.File('data\gpm_jan_2020.HDF5', 'r')

    grid = dataframe['Grid']

    lon_values = list(grid['lon'])
    lat_values = list(grid['lat'])
    percip_values = np.array(list(grid['precipitation'])).flatten()

    dataframe = pd.DataFrame({'lon': lon_values[:1000],
                              'lat': lat_values[:1000],
                              'percip': percip_values[:1000]
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

    # dataframe.to_csv('percipitation-from-hdf.csv', index=False)

    return dataframe


def netcdf_handler():
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

    dataframe = pd.DataFrame({'lon': lon_values[:1000],
                              'lat': lat_values[:1000],
                              'prcp': percip_values[:1000]})

    dataframe.columns = ['{} in {}'.format(dataset['lon'].standard_name, dataset['lon'].units), '{} in {}'.format(
        dataset['lat'].standard_name, dataset['lat'].units), '{} in {}'.format(dataset['prcp'].long_name, dataset['prcp'].units)]

    # dataframe.to_csv('percipitation-from-netCDF.csv', index=False)

    return dataframe


def dataviewer(dataframe):
    root = Tk()
    root.title('DataViewer')
    root.geometry('800x600')
    root.iconbitmap('./satellite.ico')

    columns = dataframe.columns
    rows = dataframe.to_numpy().tolist()

    dataviewer_frame = Frame(root)
    dataviewer_frame.pack(pady=20)

    scroll = Scrollbar(dataviewer_frame)
    scroll.pack(side=RIGHT, fill=Y)

    dataviewer = ttk.Treeview(
        dataviewer_frame, yscrollcommand=scroll.set, selectmode=NONE)

    scroll.config(command=dataviewer.yview)

    dataviewer['columns'] = list(columns)
    dataviewer['show'] = 'headings'

    for column in dataviewer['columns']:
        dataviewer.heading(column, text=column)

    for row in rows:
        dataviewer.insert('', 'end', values=row)

    dataviewer.pack()

    root.mainloop()


hdf_data = hdf_handler()
netcdf_data = netcdf_handler()
# dataviewer(hdf_data)
