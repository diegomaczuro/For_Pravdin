# coding=utf-8
__author__ = 'Anastasia Bazhutina'

from vtk import *
from vtk.util.numpy_support import vtk_to_numpy
from sklearn.neighbors import KDTree
import warnings
import numpy as np
import math
import struct

#тут вектора взяты из модели
file_bin_name1 = 'heartbin1.bin'
file_bin_name2 = 'angles1.bin'

#тут вектора взяты из DTMRI
file_bin_name3 = 'heartbin2.bin'
file_bin_name4 = 'angles2.bin'

file_model_name = 'model.vtk' #имя файла с моделью
file_model_name_DTMRI = 'model_DTMRI.vtk' #имя файла с моделью(вектора из DTMRI)
file_data_name = 'full_vector_field.vtk' #имя файла со входным массивом
file_result_name = 'result.vtk' #имя файла результата

a = []
l = 0
with open(file_bin_name1, "rb") as f:
    byte = f.read(1)
    print byte
    while byte != "":
        # Do stuff with byte.
        byte = f.read(1)
        if byte == struct.pack('b',1):
            #print byte
            #print '0'
            #a.append(1)
            l += 1
        #else:
            #a.append(0)
print l
#
#N = int((len(a))**(1./3))
#b = np.zeros((len(a),3))
#print l
#
#n = 0
#m = 0
#l = 0
#with open(file_bin_name2, "rb") as f:
#    byte = f.read(1)
#    print byte
#    while byte != "":
#        byte = f.read(1)
#        if n == 2:
#            m += 1
#            n = 0
#            l += 1
#        if m < len(a):
#            if a[m] != 0:
#                b[m][n] = 1
#                l += 1
#            else:
#                b[m][n] = 0
#
#            n += 1
#
#
#
#print l
#l = 0
#for i in xrange(len(a)):
#    k = sum(b[i])
#    if a[i] == 0 and k != 0:
#        print 'error!'
#        l += 1
#        print b[i]
#
#print l
#