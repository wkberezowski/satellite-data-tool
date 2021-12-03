import numpy as np
import h5py

matrix1 = np.random.random(size=(1000, 1000))
matrix2 = np.random.random(size=(1000, 1000))
matrix3 = np.random.random(size=(1000, 1000))
matrix4 = np.random.random(size=(1000, 1000))

# CREATING DATASETS IN HDF5
with h5py.File('data.h5', 'w') as hdf:
 hdf.create_dataset('dataset1', data=matrix1)
 hdf.create_dataset('dataset2', data=matrix2)
 
# KEY-VALUE
with h5py.File('data.h5', 'r') as hdf:
 listOfKeys = list(hdf.keys())
 data = hdf.get('dataset1')
 dataset1 = np.array(data)
 
# CREATING GROUPS AND SUBGROUPS
with h5py.File('hdf5Groups.h5', 'w') as hdf:
 G1 = hdf.create_group('Group1')
 G1.create_dataset('dataset1', data=matrix1)
 G1.create_dataset('dataset4', data=matrix4)
 
 G21= hdf.create_group('Group2/SubGroup1')
 G21.create_dataset('dataset3', data=matrix3)
 
 G22 = hdf.create_group('Group2/SubGroup2')
 G22.create_dataset('dataset2', data=matrix2)

# READING GROUPS AND SUBGROUPS
with h5py.File('hdf5Groups.h5', 'r') as hdf:
 baseItems = list(hdf.items())
 # print('Items in the base directory: {}'.format(baseItems))
 G1 = hdf.get('Group1')

# COMPRESSIONS
with h5py.File('hdf5GroupsCompressed.h5', 'w') as hdf:
 G1 = hdf.create_group('Group1')
 G1.create_dataset('dataset1', data=matrix1, compression='gzip', compression_opts=9)
 G1.create_dataset('dataset4', data=matrix4, compression='gzip', compression_opts=9)
 
 G21 = hdf.create_group('Group1/SubGroup1')
 G21.create_dataset('dataset3', data=matrix3, compression='gzip', compression_opts=9)
 
 G22 = hdf.create_group('Group2/SubGroup2')
 G22.create_dataset('dataset2', data=matrix2, compression='gzip', compression_opts=9)

# ATRIBUTES
with h5py.File('test.h5', 'w') as hdf:
 dataset1 = hdf.create_dataset('dataset1', data=matrix1)
 dataset2 = hdf.create_dataset('dataset2', data=matrix2)
 
 dataset1.attrs['CLASS'] = 'DATA MATRIX'
 dataset1.attrs['VERSION'] = '1.1'
 
with h5py.File('test.h5', 'r') as hdf:
 ls = list(hdf.keys())
 print('List of dataset keys in this file: {}'.format(ls))
 data = hdf.get('dataset1')
 dataset1 = np.array(data)
 print('Print shape of the dataset1: {}'.format(dataset1.shape))
 k = list(data.attrs.keys())
 v = list(data.attrs.values())
 
 print(k[0])
 print(v[0])
 print(data.attrs[k[0]])
 

