from tkinter import *
from tkinter import filedialog
import h5py
import netCDF4

from dataviewer_screen import dataviewer_screen


# DEFINING FILE EXTENSION
hdf_names = ['.h5', '.hdf5']
netcdf_names = ['.nc4', '.nc']

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

# SETTING UP LABELS FOR DISPLAYING THE CONTNET OF THE FILE
display_frame.columnconfigure(0, weight=3)
display_frame.columnconfigure(1, weight=4)
display_frame.columnconfigure(2, weight=3)


# FUNCTION FOR OPENING A FILE

def open():

    filetypes = [('HDF5 files', '*.HDF5'),
                 ('HDF5 files', '*.h5'),
                 ('netCDF files', '*.nc4'),
                 ('netCDF files', '*.nc'),
                 ]
    filename = filedialog.askopenfilename(
        initialdir='./data', title='Select a file', filetypes=filetypes)

    if filename:

        # CLOSE FILE ALSO RESETS GRID
        close_file()

        # DEFINING GENERAL LABELS

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

        checkboxes = {}
        checkbox_list = []

        # FUNCTION FOR DISPLAYING GENERAL CONTENT OF A FILE

        def display_content(vars, sizes):
            for i in range(len(vars)):
                var_checkbox = Checkbutton(
                    display_frame, background=accent_color, onvalue=vars[i], offvalue='')
                var_checkbox.grid(row=i+2, column=0,
                                  pady=2, sticky='nsew')

                checkboxes[i] = var_checkbox
                checkbox_list.append(var_checkbox)

                key_label = Label(
                    display_frame, text=vars[i], background=accent_color)
                key_label.grid(row=i+2, column=1,
                               pady=2, sticky='nsew')

                size_label = Label(
                    display_frame, text=sizes[i], background=accent_color)
                size_label.grid(row=i+2, column=2,
                                pady=2, sticky='nsew')

            # CLEARING CHECKBOXES FUNCTION

            def clear_checkboxes():
                for i in checkbox_list:
                    i.deselect()

            # CLEAR CHECKBOXES BUTTON

            btn_clear_checkboxes = Button(
                display_frame, text='Clear', command=clear_checkboxes, bg=btns_color, width=10)
            btn_clear_checkboxes.grid(row=len(vars) + 2, pady=5)

        # DISPLAYING HDF FILE

        if any(substring in filename.lower() for substring in hdf_names):
            dataset = h5py.File(filename, 'r')
            grid = dataset['Grid']
            vars = list(grid.keys())
            sizes = []

            for var in vars:
                sizes.append(grid[var].size)

            display_content(vars, sizes)

        # DISPLAYING NETCDF FILE

        elif any(substring in filename.lower() for substring in netcdf_names):
            dataset = netCDF4.Dataset(filename, 'r', format='NETCDF4')

            if dataset['PRODUCT']:
                product = dataset['PRODUCT']
                vars = list(product.variables)
                sizes = []

                for var in vars:
                    sizes.append(product[var].size)

                display_content(vars, sizes)

            else:
                vars = list(dataset.variables)
                sizes = []

                for var in vars:
                    sizes.append(dataset[var].size)

                display_content(vars, sizes)

        # OPTIONS FOR DROPDOWN MENU
        options = ['ALL',
                   '500',
                   '1000',
                   '1500', ]

        clicked = StringVar()
        clicked.set(options[0])
        dropdown = OptionMenu(display_frame, clicked, *options)
        dropdown.config(bg=btns_color)
        dropdown.grid(row=len(vars) + 2, column=1, padx=175, sticky='e')

        # OPENING IN DATAVIEWER

        def open_in_dataviewer():
            def add_to_list():
                value_list = []
                for i in range(len(checkboxes)):
                    checkbutton = checkboxes[i]
                    varname = checkbutton.cget('variable')
                    value = display_frame.getvar(varname)

                    if value != '':
                        value_list.append(value)
                return value_list

            list_of_values = add_to_list()
            dataviewer_screen(list_of_values, filename,
                              hdf_names, netcdf_names, clicked)

        # OPEN IN DATAVIEWER BUTTON

        btn_open_in_dataviewer = Button(display_frame, text="Open In DataViewer",
                                        command=open_in_dataviewer, bg=btns_color, width=20)
        btn_open_in_dataviewer.grid(
            row=len(vars) + 2, columnspan=3, pady=10)


#  BUTTON FOR OPENING A FILE
btn_open = Button(btns_frame, text="Open",
                  command=open, bg=btns_color, width=15)
btn_open.grid(row=0, column=0, sticky='ns', padx=10, pady=7)

# FUNCTION FOR CLOSING A FILE


def close_file():
    for label in display_frame.grid_slaves():
        label.grid_forget()

# BUTTON FOR CLOSING A FILE


btn_close_file = Button(btns_frame, text="Close File",
                        bg=btns_color, width=15)
btn_close_file.grid(row=1, column=0, sticky='ns', padx=10, pady=7)

# BUTTON FOR CLOSING THE APP

btn_close_app = Button(btns_frame, text='Close App',
                       command=root.destroy, bg=btns_color, width=15)
btn_close_app.grid(row=2, column=0, sticky='ns', padx=10, pady=7)


root.mainloop()
