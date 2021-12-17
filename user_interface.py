from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from display_structure import import_hdf, import_netcdf
from save_as_csv import hdf5_to_csv, netCDF_to_csv

# DEFINING COLORS
primary_color = '#F8F9FA'
accent_color = '#E9ECEF'
btns_color = '#DEE2E6'

# IMPORTING HDF5 FILE AND DISPLAYING ITS CONTENT


def open():
    global filename
    filetypes = (('HDF5 files', '*.HDF5'), ('netCDF files', '*.nc4'))
    filename = filedialog.askopenfilename(
        initialdir='./data', title='Select a file', filetypes=filetypes)

    if filename:
        btn_save.config(state=DISABLED)
        for label in display_frame.grid_slaves():
            label.grid_forget()

        title_label = Label(display_frame, text=filename,
                            background=accent_color)
        title_label.grid(row=0, columnspan=2)

        name_label = Label(display_frame, text='Name',
                           background=primary_color, width=50, relief='groove')
        name_label.grid(row=1, column=0, sticky='nsew')
        size_label = Label(display_frame, text='Size',
                           background=primary_color, width=50, relief='groove')
        size_label.grid(row=1, column=1, sticky='nsew')

        if filename[-4:].lower() == 'hdf5':
            vars, sizes = import_hdf()
        elif filename[-3:-1].lower() == 'nc':
            vars, sizes = import_netcdf()

        for i in range(len(vars)):
            key_label = Label(
                display_frame, text=vars[i], background=accent_color)
            key_label.grid(row=i+2, column=0, sticky='nsew', pady=2)
            size_label = Label(
                display_frame, text=sizes[i], background=accent_color)
            size_label.grid(row=i+2, column=1, pady=2)

        btn_save.config(state=NORMAL)


def save():
    if filename[-4:].lower() == 'hdf5':
        hdf5_to_csv()
    elif filename[-3:-1].lower() == 'nc':
        netCDF_to_csv()

    messagebox.showinfo('Saving', 'Saved successfuly')


def clear_all():
    for label in display_frame.grid_slaves():
        label.grid_forget()
    btn_save.config(state=DISABLED)


# SETTING UP WINDOWS
root = Tk()
root.title('Satellite Data Tool')
root.iconbitmap('./satellite.ico')

# SETTING UP GRID, FRAMES AND BUTTONS
root.rowconfigure(0, minsize=600, weight=1)
root.columnconfigure(1, minsize=600, weight=1)

display_frame = Frame(root, background=accent_color)
display_frame.grid(row=0, column=1, sticky='nsew')
btns_frame = Frame(root, background=primary_color)
btns_frame.grid(row=0, column=0, sticky='ns')
btn_open = Button(btns_frame, text="Open", command=open, bg=btns_color)
btn_open.grid(row=0, column=0, sticky='ew', padx=10, pady=(5, 5))
btn_save = Button(btns_frame, text="Save As", command=save,
                  bg=btns_color, state=DISABLED)
btn_save.grid(row=1, column=0, sticky='ew', padx=10, pady=(5, 5))
btn_clear = Button(btns_frame, text="Clear All",
                   command=clear_all, bg=btns_color)
btn_clear.grid(row=2, column=0, sticky='ew', padx=10, pady=(5, 0))

# SETTING UP LABELS FOR DISPLAYING THE CONTNET OF THE FILE
display_frame.columnconfigure(0, minsize=100, weight=1)
display_frame.columnconfigure(1, minsize=100, weight=1)

root.mainloop()
