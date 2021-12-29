from tkinter import *
from tkinter import filedialog
from data_viewer import *


# IMPORTING HDF5 FILE AND DISPLAYING ITS CONTENT


def open():
    global filename
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

            btn_open_as_csv = Button(display_frame, text="Open As CSV", command=open_and_save,
                                     bg=btns_color, width=50)

            btn_open_as_csv.grid(columnspan=3, pady=10, sticky='ns')

        add_to_list_btn = Button(display_frame, text='Add To List',
                                 background=btns_color, width=50, command=show_list)
        add_to_list_btn.grid(columnspan=3, pady=10, sticky='ns')


# SAVING TO CSV


def open_and_save():
    if filename[-4:].lower() == 'hdf5':
        data = hdf_handler(filename)
        dataviewer(data)
    elif filename[-3:-1].lower() == 'nc':
        data = netcdf_handler(filename)
        dataviewer(data)


# CLEARING ALL


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
