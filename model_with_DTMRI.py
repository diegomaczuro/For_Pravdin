# coding=utf-8
__author__ = 'Anastasia Bazhutina'

from vtk import *
from vtk.util.numpy_support import vtk_to_numpy
from sklearn.neighbors import KDTree
import warnings
import numpy as np

file_model_name = 'model.vtk' #имя файла с моделью(вектора из модели)
file_model_name_DTMRI = 'model_DTMRI.vtk' #имя файла с моделью(вектора из DTMRI)
file_data_name = 'full_vector_field.vtk' #имя файла со входным массивом
file_result_name = 'result-2.vtk' #имя файла результата

def write_points_model_in_file(file_name, points, vectors):
    """Запись в файл координат точек, скаляров для каждой точки, векторов в каждой точке

     Parameters
     ----------
     points :
         points - массив точек
    vectors :
        vectors - массив векторов
    """

    len1 = len(points)
    len2 = len(vectors)
    len3 = 0

    print 'start write to file'
    with open(file_name, 'w') as out_mesh:
        out_mesh.write("# vtk DataFile Version 2.0\n")
        out_mesh.write("Really cool data\n")
        out_mesh.write("ASCII\n")
        out_mesh.write("DATASET UNSTRUCTURED_GRID\n")
        out_mesh.write("POINTS {pcount} double\n".format(pcount=len1))
        for i in xrange(0, len1):
            out_mesh.write("{0} {1} {2}\n".format(points[i][0], points[i][1], points[i][2]))

        out_mesh.write("CELLS {pcount} {pcount2}\n".format(pcount=len1, pcount2=(len1 * 2)))
        for j in xrange(len1):
            out_mesh.write("1 {0}\n".format(j))
        out_mesh.write("CELL_TYPES {pcount}\n".format(pcount=len1))

        for k in xrange(len1):
            out_mesh.write("1\n")


        if len2 != 0:
            if len3 == 0:
                out_mesh.write("POINT_DATA {pcount}\n".format(pcount=len2))
            out_mesh.write("VECTORS DTMRIFiberOrientation double\n")
            for i in xrange(len2):
                out_mesh.write("{0} {1} {2}\n".format(vectors[i][0], vectors[i][1], vectors[i][2]))
        print 'end writing file'


warnings.filterwarnings("ignore")
reader = vtk.vtkGenericDataObjectReader()
reader.SetFileName(file_model_name)
reader.Update()
ug = reader.GetOutput()
points = ug.GetPoints()
coord_vector_model = vtk_to_numpy(ug.GetPointData().GetArray('DTMRIFiberOrientation'))
coord_points_model = vtk_to_numpy(points.GetData())

reader2 = vtk.vtkGenericDataObjectReader()
reader2.SetFileName(file_data_name)
reader2.Update()
ug2 = reader2.GetOutput()
points2 = ug2.GetPoints()
coord_vector_data = vtk_to_numpy(ug2.GetPointData().GetArray('DTMRIFiberOrientation'))
coord_points_data = vtk_to_numpy(points2.GetData())
find_vector_model = []
tree_data = KDTree(coord_points_data, leaf_size = 2, metric = 'euclidean')
for i in xrange(len(coord_points_model)):
    dist, ind = tree_data.query(coord_points_model[i], k=2)
    v = [0, 0, 0]
    for j in ind[0]:
        v += coord_vector_data[j]

    length_v = np.linalg.norm(v)
    find_vector_model.append(v/length_v)
write_points_model_in_file(file_model_name_DTMRI, coord_points_model, find_vector_model)
