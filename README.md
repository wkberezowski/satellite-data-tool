# Python app for proccessing numerical, satellite data saved in various formats.

## User can upload data in HDF5 or netCDF format. The app will display the structure of the file and display chosen datasets in a detailed view. From there the user can explore the datasets using a spreadsheet-like view, analyze the automatically counted statistics and generate five different kinds of charts. 

The GUI of the application was created using Tkinter. Handling the dedicated formats was implemented with the help of h5py and netcdf4 modules. Pandas and NumPy were also used for manipulating the data. The visualizations are done in Matplotlib.

