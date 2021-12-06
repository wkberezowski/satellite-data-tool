import netCDF4 
import pandas as pd
import numpy as np

# READ DATASET
dataset = netCDF4.Dataset('./data/daymet_v3_prcp_monttl_2017_hi.nc4', 'r', format='NETCDF4')