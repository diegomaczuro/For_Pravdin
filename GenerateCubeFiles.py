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
file_txt_name1 = 'heartbin1.txt'
file_txt_name2 = 'angles1.txt'

#тут вектора взяты из DTMRI
file_bin_name3 = 'heartbin2.bin'
file_bin_name4 = 'angles2.bin'
file_txt_name3 = 'heartbin2.txt'
file_txt_name4 = 'angles2.txt'

file_model_name = 'model.vtk' #имя файла с моделью
file_model_name_DTMRI = 'model_DTMRI.vtk' #имя файла с моделью(вектора из DTMRI)
file_data_name = 'full_vector_field.vtk' #имя файла со входным массивом
file_result_name = 'result.vtk' #имя файла результата
from find_vector import *
SCALE_CHAR  = 127.0
#define F2C(_f) ( (signed char) floorf(((_f)* SCALE_CHAR +.5)) )   /* scale  real values to char */

def F2C(x, y, z):
    #dt = np.dtype('int8')
    #arr = np.array([int(math.floor(x*SCALE_CHAR + 0.5)), int(math.floor(y*SCALE_CHAR + 0.5)),
    #                       int(math.floor(z*SCALE_CHAR + 0.5))], dtype=dt)
    return struct.pack('bbb', int(math.floor(x*SCALE_CHAR + 0.5)), int(math.floor(y*SCALE_CHAR + 0.5)),
                           int(math.floor(z*SCALE_CHAR + 0.5)))
    #return arr

def write_binary_file(file_name, array, len_el):
    #len_el - длина элемента массива, в файл пишем либо о и 1, либо вектор
    with open(file_name, 'wb') as out_mesh:
        if len_el == 1:
            for i in xrange(len(array)):
                out_mesh.write("{0}".format(struct.pack('b', int(array[i]))))

        elif len_el == 3:
            for m in xrange(0,3):
                for i in xrange(len(array)):
                    a = array[i]
                    vec = int(math.floor(a[m]*SCALE_CHAR + 0.5))
                    #out_mesh.write(F2C(x, y, z))
                    #out_mesh.write("{0}".format(struct.pack('b', vec)))
                    srt_bin = 'b'
                    bin = struct.pack(srt_bin, vec)
                    out_mesh.write(bin)


def write_bin(fname, s):
    f = open(fname, "wb")
    myfmt = 'b' * len(s)
    bin = struct.pack(myfmt, *(s))
    f.write(bin)
    f.close()


def write_txt(file_name1, file_name2, find_coord_data, find_vector_data):
    np.savetxt(file_name1, find_coord_data, fmt='%d')
    np.savetxt(file_name2, find_vector_data, fmt='%f')



reader = vtk.vtkGenericDataObjectReader()
reader.SetFileName(file_model_name)
reader.Update()
ug = reader.GetOutput()
points = ug.GetPoints()
coord_vector_model = vtk_to_numpy(ug.GetPointData().GetArray('DTMRIFiberOrientation'))
coord_points_model = vtk_to_numpy(points.GetData())
# define array
max_ = np.zeros((3))
min_ = np.zeros((3))

# Find min and max for generate point in cube
max_[0] = np.max(coord_points_model[:,0])
max_[1] = np.max(coord_points_model[:,1])
max_[2] = np.max(coord_points_model[:,2])

min_[0] = np.min(coord_points_model[:,0])
min_[1] = np.min(coord_points_model[:,1])
min_[2] = np.min(coord_points_model[:,2])

min_cube = np.min(min_)
max_cube = np.max(max_)
array_cube_x = np.linspace(min_cube-0.3, max_cube+0.3,  np.round((max_cube - min_cube+0.6)/0.03)+1)#0.03)+1)
array_cube_y = np.linspace(min_cube-0.3, max_cube+0.3,  np.round((max_cube - min_cube+0.6)/0.03)+1)#0.03)+1)
array_cube_z = np.linspace(min_cube-0.3, max_cube+0.3,  np.round((max_cube - min_cube+0.6)/0.03)+1)#0.03)+1)
cube_point = np.zeros((len(array_cube_x)*len(array_cube_y)*len(array_cube_z),3))
counter = 0
print 'x0=', array_cube_x[0], 'y0=',array_cube_y[0],  'z0=', array_cube_z[0], 'cm'
print'side =', array_cube_x[-1] - array_cube_x[0], 'cm'
print 'N=', len(array_cube_x), 'cm'
print 'dr = ', (array_cube_x[-1] - array_cube_x[0])/len(array_cube_x), 'cm'
print 'x0=', array_cube_x[0]*10, 'y0=',array_cube_y[0]*10,  'z0=', array_cube_z[0]*10, 'mm'
print'side =', (array_cube_x[-1] - array_cube_x[0])*10, 'mm'
print 'dr = ', (array_cube_x[-1] - array_cube_x[0])*10/len(array_cube_x), 'mm'
for i in xrange(len(array_cube_x)):
    for j in xrange(len(array_cube_y)):
        for k in xrange(len(array_cube_z)):
            cube_point[counter,:] = np.array([array_cube_x[i],array_cube_y[j],array_cube_z[k]])
            counter +=1

print len(cube_point[:,0]),array_cube_x[1]-array_cube_x[0]
print cube_point
print 'x0 = ', cube_point[0], 'y0 = ', cube_point[0], 'z0 = ', cube_point[0]


#find_coord_data, find_vector_data = find_vectors(cube_point, coord_vector_model, coord_points_model)

#запись в текстовый файл
#write_txt(file_txt_name1, file_txt_name2, find_coord_data, find_vector_data)

#angles1 = np.floor(np.reshape(find_vector_data, 3 * len(find_coord_data)) * 127 + 0.5)

#write_bin('p.bin', find_coord_data)
#write_bin('v.bin', angles1)

#запись в бинарный файл
#write_binary_file(file_bin_name1, find_coord_data, 1)
#write_binary_file(file_bin_name2, find_vector_data, 3)
#
reader3 = vtk.vtkGenericDataObjectReader()
reader3.SetFileName(file_model_name_DTMRI)
reader3.Update()
ug3 = reader3.GetOutput()
points3 = ug3.GetPoints()
coord_vector_model_DTMRI = vtk_to_numpy(ug3.GetPointData().GetArray('DTMRIFiberOrientation'))
coord_points_model_DTMRI = vtk_to_numpy(points3.GetData())

find_coord_data2, find_vector_data2 = find_vectors(cube_point, coord_vector_model_DTMRI, coord_points_model_DTMRI)




#запись в текстовый файл
#write_txt(file_txt_name3, file_txt_name4, find_coord_data2, find_vector_data2)

#запись в бинарный файл
#write_binary_file(file_bin_name3, find_coord_data2, 1)
#write_binary_file(file_bin_name4, find_vector_data2, 3)

#write_binary_file(file_bin_name1, [1,0], 1)
#write_binary_file(file_bin_name2, [[0.6, -0.1, 0.1], [0.3,-0.9, 0.3]], 3)