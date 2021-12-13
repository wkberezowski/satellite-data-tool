from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from numpy.core.fromnumeric import ptp
from displayStructure import importHDF, importNETCDF
from save_as_csv import hdf5_to_csv, netCDF_to_csv
import csv

# DEFINING COLORS
primaryColor = '#F8F9FA'
accentColor = '#E9ECEF'
btnsColor = '#DEE2E6'

# IMPORTING HDF5 FILE AND DISPLAYING ITS CONTENT
def open():
  global titleLabel 
  filetypes = (('HDF5 files', '*.HDF5'), ('netCDF files', '*.nc4'))
  filename = filedialog.askopenfilename(initialdir='./data', title='Select a file', filetypes=filetypes)
  
  if filename:
    titleLabel = Label(displayFrame, text=filename, background=accentColor)
    titleLabel.grid(row=0, columnspan=2)
    nameLabel = Label(displayFrame, text='Name', background=primaryColor, width=50)
    nameLabel.grid(row=1, column=0)
    sizeLabel = Label(displayFrame, text='Size', background=primaryColor, width=50)
    sizeLabel.grid(row=1, column=1)
        
    if filename[-4:].lower() == 'hdf5':
      vars, sizes = importHDF()
    elif filename[-3:-1].lower() == 'nc':
      vars, sizes = importNETCDF()
      
    clearAll()
      
    for i in range(len(vars)):
      keyLabel = Label(displayFrame, text=vars[i], background=accentColor)
      keyLabel.grid(row=i+2, column=0, sticky='ns', pady=2)
      sizeLabel = Label(displayFrame, text=sizes[i], background=accentColor)
      sizeLabel.grid(row=i+2, column=1, pady=2)
    
def save():
  messagebox.showinfo('Saving', 'Saved successfuly')
  # hdf5_to_csv()

def clearAll():
  titleLabel.grid_forget()
  for label in displayFrame.grid_slaves():
    if int(label.grid_info()['row']) > 1:
      label.grid_forget()

# SETTING UP WINDOWS
root = Tk()
root.title('Satellite Data Tool')
root.iconbitmap('./satellite.ico')

# SETTING UP GRID, FRAMES AND BUTTONS
root.rowconfigure(0, minsize=600, weight=1)
root.columnconfigure(1, minsize=600, weight=1)

displayFrame = Frame(root, background=accentColor)
displayFrame.grid(row=0, column=1, sticky='nsew')
btnsFrame = Frame(root, background=primaryColor)
btnsFrame.grid(row=0, column=0, sticky='ns')
btnOpen = Button(btnsFrame, text="Open", command=open, bg=btnsColor)
btnOpen.grid(row=0, column=0, sticky='ew', padx=10, pady=(0, 5))
btnSave = Button(btnsFrame, text="Save As", command=save, bg=btnsColor)
btnSave.grid(row=1, column=0, sticky='ew', padx=10, pady=(5, 5))
btnClear = Button(btnsFrame, text="Clear All", command=clearAll, bg=btnsColor)
btnClear.grid(row=2, column=0, sticky='ew', padx=10, pady=(5, 0))

# SETTING UP LABELS FOR DISPLAYING THE CONTNET OF THE FILE
displayFrame.columnconfigure(0, minsize=100, weight=1)
displayFrame.columnconfigure(1, minsize=100, weight=1)
root.mainloop()