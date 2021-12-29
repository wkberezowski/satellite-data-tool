import h5py
import netCDF4
import numpy as np
import pandas as pd
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog


def display_hdf(filename):
    dataframe = h5py.File(filename, 'r')
    grid = dataframe['Grid']
    grid_keys = list(grid.keys())
    sizes = []

    for key in grid_keys:
        sizes.append(grid[key].size)

    return grid_keys, sizes


def display_netcdf(filename):
    dataframe = netCDF4.Dataset(
        filename, 'r', format='NETCDF4')
    vars = list(dataframe.variables)
    sizes = []

    for var in vars:
        sizes.append(dataframe[var].size)

    return vars, sizes


def hdf_handler(filename):
    dataframe = h5py.File(filename, 'r')

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

    return dataframe


def netcdf_handler(filename):
    # READ DATASET
    dataset = netCDF4.Dataset(
        filename, 'r', format='NETCDF4')

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

    return dataframe


def dataviewer(dataframe):
    root = Tk()
    root.title('Data Viewer')
    root.geometry('800x600')
    root.iconbitmap('./satellite.ico')
    root.configure(background='#F8F9FA')

    columns = dataframe.columns
    rows = dataframe.to_numpy().tolist()

    dataviewer_frame = Frame(root, background='#F8F9FA')
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

    def saving():
        file = filedialog.asksaveasfile(
            filetypes=[('CSV Files', '*.csv')], defaultextension='*.csv')
        dataframe.to_csv(file, index=False)

        if file:
            messagebox.showinfo('Saving', 'Saved successfuly')

    save_as_csv_btn = Button(root, text='Save To Drive',
                             command=saving, bg='#DEE2E6')
    save_as_csv_btn.pack(anchor=CENTER)

    dataviewer.pack()

    root.mainloop()
