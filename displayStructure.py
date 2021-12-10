import h5py
import numpy as np
import pandas as pd

def importHDF():
 dataframe = h5py.File('data\gpm_jan_2020.HDF5', 'r')
 grid = dataframe['Grid']
 gridKeys = list(grid.keys())
 sizes = []
 
 for key in gridKeys:
  sizes.append(grid[key].size)
 
 return gridKeys, sizes
 