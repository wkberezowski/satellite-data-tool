from tkinter import *
from tkinter import filedialog
from tkinter import font
from data_viewer import *
import h5py
import netCDF4
import pandas as pd
import numpy as np


# IMPORTING FILE AND DISPLAYING ITS CONTENT

hdf_names = ['.h5', '.hdf5']
netcdf_names = ['.nc4', '.nc']


def open():
    global filename
    global add_to_list
    global clicked
    global clear_checkboxes
    filetypes = [('HDF5 files', '*.HDF5'),
                 ('HDF5 files', '*.h5'),
                 ('netCDF files', '*.nc4'),
                 ('netCDF files', '*.nc'),
                 ]
    filename = filedialog.askopenfilename(
        initialdir='./data', title='Select a file', filetypes=filetypes)

    # DISPLAYING THE STRUCTURE OF THE FILE

    if filename:
        for label in display_frame.grid_slaves():
            label.grid_forget()

        title_label = Label(display_frame, text=filename,
                            background=accent_color)
        title_label.grid(row=0, columnspan=3)

        checkbox_label = Label(
            display_frame, text='Add To DataViewer', background=primary_color)
        checkbox_label.grid(row=1, column=0, pady=2, sticky='nsew')

        name_label = Label(display_frame, text='Name',
                           background=primary_color)
        name_label.grid(row=1, column=1, pady=2, sticky='nsew')

        size_label = Label(display_frame, text='Size',
                           background=primary_color)
        size_label.grid(row=1, column=2, pady=2, sticky='nsew')

        if any(substring in filename.lower() for substring in hdf_names):
            vars, sizes = display_hdf(filename)

        elif any(substring in filename.lower() for substring in netcdf_names):
            vars, sizes = display_netcdf(filename)

        # CREATING CHECKBUTTONS

        checkbuttons = {}
        checkbox_list = []

        for i in range(len(vars)):
            key_checkbox = Checkbutton(
                display_frame, background=accent_color, onvalue=vars[i], offvalue='')
            key_checkbox.grid(row=i+2, column=0, pady=2, sticky='nsew')

            checkbuttons[i] = key_checkbox
            checkbox_list.append(key_checkbox)

            key_label = Label(
                display_frame, text=vars[i], background=accent_color)
            key_label.grid(row=i+2, column=1, pady=2, sticky='nsew')

            size_label = Label(
                display_frame, text=sizes[i], background=accent_color)
            size_label.grid(row=i+2, column=2, pady=2, sticky='nsew')

        # CLEARING CHECKBOXES

        def clear_checkboxes():
            for i in checkbox_list:
                i.deselect()
            list_label.configure(
                text='Columns in DataViewer', font='Helvetica 9 italic')

        # ADDING CHECKED ITEMS TO LIST

        def add_to_list():
            value_list = []
            for i in range(len(checkbuttons)):
                checkbutton = checkbuttons[i]
                varname = checkbutton.cget('variable')
                value = display_frame.getvar(varname)

                if value != '':
                    value_list.append(value)
            return value_list

        # SHOWING LIST ON THE SCREEN

        def show_list():
            value_list = add_to_list()
            if len(value_list) < 1:
                messagebox.showwarning(
                    title='ERROR', message='There is nothing to add to the list')
            else:
                list_label.configure(text='{}'.format(
                    value_list), font='Helvetica 9')
                btn_open_in_dataviewer.configure(state=NORMAL)

        # ADD TO LIST BUTTON

        add_to_list_btn = Button(display_frame, text='Add To List',
                                 background=btns_color, width=10, command=show_list)
        add_to_list_btn.grid(row=len(vars) + 2, column=0, pady=5, sticky='ns')

        # CLEAR CHECKBOXES BUTTON

        btn_clear_checkboxes = Button(
            display_frame, text='Clear', command=clear_checkboxes, bg=btns_color, width=10)
        btn_clear_checkboxes.grid(row=len(vars) + 3, sticky='ns', pady=5)

        list_label = Label(
            display_frame, text='Columns in DataViewer', background=primary_color)
        list_label.grid(row=len(vars) + 4, columnspan=3, sticky='nsew')
        list_label.configure(font='Helvetica 9 italic')

        # OPEN IN DATAVIEWER BUTTON

        btn_open_in_dataviewer = Button(display_frame, text="Open In DataViewer",
                                        command=open_in_dataviewer, bg=btns_color, width=20, state=DISABLED)
        btn_open_in_dataviewer.grid(
            row=len(vars) + 5, columnspan=3, pady=10, sticky='ns')

        # SELECTING THE NUMBER OF ROWS

        options = ['ALL',
                   '500',
                   '1000',
                   '1500', ]

        clicked = StringVar()
        clicked.set(options[0])
        dropdown = OptionMenu(display_frame, clicked, *options)
        dropdown.config(bg=btns_color)
        dropdown.grid(row=len(vars) + 5, column=1, padx=175, sticky='e')

# DISPLAYING THE STRUCTURE OF HDF FILE


def display_hdf(filename):
    dataframe = h5py.File(filename, 'r')
    grid = dataframe['Grid']
    grid_keys = list(grid.keys())
    sizes = []

    for key in grid_keys:
        sizes.append(grid[key].size)

    return grid_keys, sizes

# DISPLAYING THE STRUCTURE OF NETCDF FILE


def display_netcdf(filename):
    dataframe = netCDF4.Dataset(
        filename, 'r', format='NETCDF4')
    if dataframe.groups:
        groups = list(dataframe.groups)
        for group in groups:
            if dataframe[group].variables:
                vars = list(dataframe[group].variables)
                sizes = []

                for var in vars:
                    sizes.append(dataframe[group][var].size)

                return vars, sizes

    else:
        vars = list(dataframe.variables)
        sizes = []

        for var in vars:
            sizes.append(dataframe[var].size)

        return vars, sizes


# OPENING DATAVIEWER


def open_in_dataviewer():
    list_of_values = add_to_list()

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

                dataframe = pd.DataFrame(columns=list_of_values)

                for i in range(len(list_of_values)):
                    this_column = dataframe.columns[i]

                    if clicked.get() == 'ALL':
                        dataframe[this_column] = pd.Series(np.array(
                            list(dataset['{}'.format(list_of_values[i])])).flatten())
                    else:
                        dataframe[this_column] = pd.Series(np.array(
                            list(dataset['{}'.format(list_of_values[i])])).flatten()[:int(clicked.get())])

                    dataframe[this_column] = dataframe[this_column].mask(
                        dataframe[this_column] < -9990)

                dataviewer(dataframe)

        except ValueError as err:
            messagebox.showerror('ERROR', '{}'.format(err))


# CLEARING APP SCREEN


def close_file():
    for label in display_frame.grid_slaves():
        label.grid_forget()


# SETTING UP MAIN WINDOW
# DEFINING COLORS
primary_color = '#F8F9FA'
accent_color = '#E9ECEF'
btns_color = '#DEE2E6'

# SETTING UP WINDOWS
root = Tk()
root.title('Satellite Data Tool')
root.iconbitmap('./satellite.ico')

app_width = 1500
app_height = 750

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2.25) - (app_height / 2)

menu = 100
display = app_width - menu

root.geometry('{}x{}+{}+{}'.format(app_width, app_height, int(x), int(y)))

# SETTING UP GRID, FRAMES AND BUTTONS
root.rowconfigure(0,  weight=1)
root.columnconfigure(0,  weight=1)
root.columnconfigure(1,  weight=20)

btns_frame = Frame(root, background=primary_color)
btns_frame.grid(row=0, column=0, sticky='nsew')

display_frame = Frame(root, background=accent_color)
display_frame.grid(row=0, column=1, sticky='nsew')

btns_frame.columnconfigure(0, weight=1)

btn_open = Button(btns_frame, text="Open",
                  command=open, bg=btns_color, width=15)
btn_open.grid(row=0, column=0, sticky='ns', padx=10, pady=7)

btn_close_file = Button(btns_frame, text="Close File",
                        command=close_file, bg=btns_color, width=15)
btn_close_file.grid(row=1, column=0, sticky='ns', padx=10, pady=7)

btn_close_app = Button(btns_frame, text='Close App',
                       command=root.destroy, bg=btns_color, width=15)
btn_close_app.grid(row=2, column=0, sticky='ns', padx=10, pady=7)


# SETTING UP LABELS FOR DISPLAYING THE CONTNET OF THE FILE
display_frame.columnconfigure(0, weight=3)
display_frame.columnconfigure(1, weight=4)
display_frame.columnconfigure(2, weight=3)

root.mainloop()
