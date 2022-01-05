from tkinter import *
from tkinter import filedialog
from data_viewer import *
import h5py
import netCDF4
import pandas as pd
import numpy as np


# IMPORTING HDF5 FILE AND DISPLAYING ITS CONTENT


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


def open():
    global filename
    global add_to_list
    filetypes = (('HDF5 files', '*.HDF5'), ('netCDF files', '*.nc4'))
    filename = filedialog.askopenfilename(
        initialdir='./data', title='Select a file', filetypes=filetypes)

    if filename:
        for label in display_frame.grid_slaves():
            label.grid_forget()

        title_label = Label(display_frame, text=filename,
                            background=accent_color)
        title_label.grid(row=0, columnspan=3)

        checkbox_label = Label(display_frame, text='Add To DataViewer',
                               background=primary_color)
        checkbox_label.grid(row=1, column=0, pady=2, sticky='nsew')

        name_label = Label(display_frame, text='Name',
                           background=primary_color)
        name_label.grid(row=1, column=1, pady=2, sticky='nsew')

        size_label = Label(display_frame, text='Size',
                           background=primary_color)
        size_label.grid(row=1, column=2, pady=2, sticky='nsew')

        if filename[-4:].lower() == 'hdf5':
            vars, sizes = display_hdf(filename)
        elif filename[-3:-1].lower() == 'nc':
            vars, sizes = display_netcdf(filename)

        checkbuttons = {}

        for i in range(len(vars)):
            key_checkbox = Checkbutton(
                display_frame, background=accent_color, onvalue=vars[i], offvalue='')
            key_checkbox.grid(row=i+2, column=0, pady=2, sticky='nsew')

            checkbuttons[i] = key_checkbox

            key_label = Label(
                display_frame, text=vars[i], background=accent_color)
            key_label.grid(row=i+2, column=1, pady=2, sticky='nsew')

            size_label = Label(
                display_frame, text=sizes[i], background=accent_color)
            size_label.grid(row=i+2, column=2, pady=2, sticky='nsew')

        def add_to_list():
            value_list = []
            for i in range(len(checkbuttons)):
                checkbutton = checkbuttons[i]
                varname = checkbutton.cget('variable')
                value = display_frame.getvar(varname)

                if value != '':
                    value_list.append(value)
            return value_list

        def show_list():
            value_list = add_to_list()
            list_label = Label(display_frame, text='{}'.format(value_list),
                               background=primary_color)
            list_label.grid(columnspan=3, pady=2, sticky='nsew')

            btn_open_as_csv = Button(display_frame, text="Open As CSV", command=open_in_dataviewer,
                                     bg=btns_color, width=50)

            btn_open_as_csv.grid(columnspan=3, pady=10, sticky='ns')

        add_to_list_btn = Button(display_frame, text='Add To List',
                                 background=btns_color, width=50, command=show_list)
        add_to_list_btn.grid(columnspan=3, pady=10, sticky='ns')


# OPENING DATAVIEWER


def open_in_dataviewer():
    list_of_values = add_to_list()
    print(list_of_values)

    #  HANDLING HDF FILES

    if filename[-4:].lower() == 'hdf5':
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

        dataviewer(dataframe)

    # HANDLING NETCDF FILES

    elif filename[-3:-1].lower() == 'nc':
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

        dataviewer(dataframe)


# CLEARING APP SCREEN


def clear_all():
    for label in display_frame.grid_slaves():
        label.grid_forget()


# DEFINING COLORS
primary_color = '#F8F9FA'
accent_color = '#E9ECEF'
btns_color = '#DEE2E6'

# SETTING UP WINDOWS
root = Tk()
root.title('Satellite Data Tool')
root.iconbitmap('./satellite.ico')

app_width = 1200
app_height = 600

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2) - (app_height / 2)

menu = 100
display = app_width - menu

root.geometry('{}x{}+{}+{}'.format(app_width, app_height, int(x), int(y)))

# SETTING UP GRID, FRAMES AND BUTTONS
root.rowconfigure(0,  weight=1)
root.columnconfigure(0, minsize=25,  weight=1)
root.columnconfigure(1,  weight=20)

btns_frame = Frame(root, background=primary_color)
btns_frame.grid(row=0, column=0, sticky='nsew')

display_frame = Frame(root, background=accent_color)
display_frame.grid(row=0, column=1, sticky='nsew')

btns_frame.columnconfigure(0, weight=1)

btn_open = Button(btns_frame, text="Open",
                  command=open, bg=btns_color)
btn_open.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

btn_clear = Button(btns_frame, text="Clear All",
                   command=clear_all, bg=btns_color)
btn_clear.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)


# SETTING UP LABELS FOR DISPLAYING THE CONTNET OF THE FILE
display_frame.columnconfigure(0, weight=1)
display_frame.columnconfigure(1, weight=10)
display_frame.columnconfigure(2, weight=5)

root.mainloop()
