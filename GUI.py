from tkinter import *
from tkinter import filedialog
from displayStructure import importHDF
from save_as_csv import hdf5_to_csv
import csv

# DEFINING COLORS
primaryColor = '#F8F9FA'
accentColor = '#E9ECEF'
btnsColor = '#DEE2E6'

# IMPORTING HDF5 FILE AND DISPLAYING ITS CONTENT
def open():
 root.filename = filedialog.askopenfilename(initialdir='./data', title='Select a file', filetypes=(('HDF5', '*.HDF5'), ('netCDF', '*.nc4')))
 
 keys, sizes = importHDF()

 nameLabel = Label(displayFrame, text='Name', background=primaryColor, width=30)
 nameLabel.grid(row=0, column=0)
 sizeLabel = Label(displayFrame, text='Size', background=primaryColor, width=30)
 sizeLabel.grid(row=0, column=1)
 for i in range(len(keys)):
  keyLabel = Label(displayFrame, text=keys[i], background=accentColor)
  keyLabel.grid(row=i+1, column=0, sticky='nw', pady=2)
  sizeLabel = Label(displayFrame, text=sizes[i], background=accentColor)
  sizeLabel.grid(row=i+1, column=1, pady=2)
  
def save():
 confirmation = Tk()
 confirmation.iconbitmap('./satellite.ico')
 confirmation.title('Saving') 
 confirmation.geometry('300x120')
 
 label = Label(confirmation, text='Saved succesfully!', height=5, width=15)
 label.pack()
 label.config(anchor=CENTER)
 closeBtn = Button(confirmation, text='OK', width=15, command=confirmation.destroy)
 closeBtn.pack()
 closeBtn.config(anchor=CENTER)
 
 # hdf5_to_csv()
  

# SETTING UP WINDOWS
root = Tk()
root.title('Satellite Data Tool')
root.iconbitmap('./satellite.ico')
root.geometry('600x400')

# SETTING UP GRID, FRAMES AND BUTTONS
root.rowconfigure(0, minsize=800, weight=1)
root.columnconfigure(1, minsize=800, weight=1)

displayFrame = Frame(root, background=accentColor)
btnsFrame = Frame(root, background=accentColor)
btnOpen = Button(btnsFrame, text="Open", command=open, bg=primaryColor)
btnSave = Button(btnsFrame, text="Save As...", command=save, bg=primaryColor)
btnOpen.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
btnSave.grid(row=1, column=0, sticky='ew', padx=10)
btnsFrame.grid(row=0, column=0, sticky='ns')
displayFrame.grid(row=0, column=1, sticky='nsew')

# SETTING UP LABELS FOR DISPLAYING THE CONTNET OF THE FILE
nameLabel = Label(displayFrame, text='Name', background=primaryColor, width=30, )
nameLabel.grid(row=0, column=0, padx=(5, 0), pady=10)
sizeLabel = Label(displayFrame, text='Size', background=primaryColor, width=30)
sizeLabel.grid(row=0, column=1, padx=(0, 5), pady=10)

root.mainloop()