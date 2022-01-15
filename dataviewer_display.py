from data_viewer import dataviewer
from tkinter import messagebox
import h5py
import netCDF4
import pandas as pd
import numpy as np


def dataviewer_display(list_of_values, filename, hdf_names, netcdf_names, clicked):

    if len(list_of_values) < 1:
        messagebox.showwarning(
            title='ERROR', message='There is nothing added to the list')
    else:
        try:

            #  HANDLING HDF FILES

            if any(substring in filename.lower() for substring in hdf_names):

                dataset = h5py.File(filename, 'r')

                grid = dataset['Grid']

                dataframe = pd.DataFrame(columns=list_of_values)

                for i in range(len(list_of_values)):
                    this_column = dataframe.columns[i]

                    if clicked.get() == 'ALL':
                        dataframe[this_column] = pd.Series(np.array(
                            list(grid['{}'.format(list_of_values[i])])).flatten())
                    else:
                        dataframe[this_column] = pd.Series(np.array(
                            list(grid['{}'.format(list_of_values[i])])).flatten()[:int(clicked.get())])

                    dataframe[this_column] = dataframe[this_column].mask(
                        dataframe[this_column] < -9990)

                dataviewer(dataframe)

            # HANDLING NETCDF FILES

            elif any(substring in filename.lower() for substring in netcdf_names):

                dataset = netCDF4.Dataset(
                    filename, 'r', format='NETCDF4')

                if dataset['PRODUCT']:
                    product = dataset['PRODUCT']
                    dataframe = pd.DataFrame(columns=list_of_values)

                    for i in range(len(list_of_values)):
                        this_column = dataframe.columns[i]

                        if clicked.get() == 'ALL':
                            dataframe[this_column] = pd.Series(np.array(
                                list(product['{}'.format(list_of_values[i])])).flatten())

                        else:
                            dataframe[this_column] = pd.Series(np.array(
                                list(product['{}'.format(list_of_values[i])])).flatten()[:int(clicked.get())])

                        if isinstance(dataframe[this_column], int):
                            dataframe[this_column] = dataframe[this_column].mask(
                                dataframe[this_column] < -9990)

                else:
                    dataframe = pd.DataFrame(columns=list_of_values)

                    for i in range(len(list_of_values)):
                        this_column = dataframe.columns[i]

                        if clicked.get() == 'ALL':
                            dataframe[this_column] = pd.Series(np.array(
                                list(dataset['{}'.format(list_of_values[i])])).flatten())

                        else:
                            dataframe[this_column] = pd.Series(np.array(
                                list(dataset['{}'.format(list_of_values[i])])).flatten()[:int(clicked.get())])

                        if isinstance(dataframe[this_column], int):
                            dataframe[this_column] = dataframe[this_column].mask(
                                dataframe[this_column] < -9990)

                dataviewer(dataframe)

        except ValueError as err:
            messagebox.showerror('ERROR', '{}'.format(err))
