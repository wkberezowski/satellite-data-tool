import h5py
import numpy as np
import pandas as pd
import netCDF4
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk


def hdf_viewer():
    global dataframe
    dataframe = h5py.File('data\gpm_jan_2020.HDF5', 'r')

    grid = dataframe['Grid']

    lon_values = list(grid['lon'][:1000])
    lat_values = list(grid['lat'][:1000])
    percip_values = np.array(list(grid['precipitation'])).flatten()

    dataframe = pd.DataFrame({'lon': lon_values,
                              'lat': lat_values,
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

    print(type(dataframe['longitude (degrees_east)']))


def dataviewer():
    root = Tk()
    root.title('DataViewer')
    root.geometry('800x600')
    root.iconbitmap('./satellite.ico')

    table_margin = Frame(root)
    table_margin.pack(side=TOP)
    scrollbar_x = Scrollbar(table_margin, orient=HORIZONTAL)
    scrollbar_y = Scrollbar(table_margin, orient=VERTICAL)
    tree = ttk.Treeview(table_margin, columns=('Lat', 'Lon', 'Percip'),
                        yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    scrollbar_y.config(command=tree.yview)
    scrollbar_y.pack(side=RIGHT, fill=Y)
    scrollbar_x.config(command=tree.xview)
    scrollbar_x.pack(side=BOTTOM, fill=X)
    tree.heading('Lon', text="Longitude", anchor=W)
    tree.heading('Lat', text="Latitude", anchor=W)
    tree.heading('Percip', text="Percipitation", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=200)
    tree.column('#2', stretch=NO, minwidth=0, width=200)
    tree.column('#3', stretch=NO, minwidth=0, width=300)
    tree.pack()

    root.mainloop()


hdf_viewer()

dataviewer()
