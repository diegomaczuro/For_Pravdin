# coding=utf-8
__author__ = 'Anastasia Bazhutina'

from vtk import *
from vtk.util.numpy_support import vtk_to_numpy
from sklearn.neighbors import KDTree
import warnings


file_model_name = 'model.vtk' #имя файла с моделью
file_data_name = 'full_vector_field.vtk' #имя файла со входным массивом
file_result_name = 'result-2.vtk' #имя файла результата



def write_points_model_in_file(points, vectors):
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
    with open(file_result_name, 'w') as out_mesh:
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


def find_vectors(array):
    """ Parameters
        ----------
        array :
            массив точек
        return:
            запись в vtk файл тех точек с векторами, которые попали в стенку ЛЖ.

    """
    warnings.filterwarnings("ignore")
    reader = vtk.vtkGenericDataObjectReader()
    reader.SetFileName(file_model_name)
    reader.Update()
    ug = reader.GetOutput()
    points = ug.GetPoints()
    coord_vector_model = vtk_to_numpy(ug.GetPointData().GetArray('DTMRIFiberOrientation'))
    coord_points_model = vtk_to_numpy(points.GetData())
    find_coord_data = []
    find_vector_data = []
    tree_model = KDTree(coord_points_model, leaf_size = 5, metric = 'euclidean')
    print 'Start!'
    for i in xrange(len(array)):
        dist, ind = tree_model.query(array[i], k=5)
        min_length = min(dist[0])
        max_length = 0
        for j in xrange(len(ind)):
            dist2, ind2 = tree_model.query(coord_points_model[ind[j]], k=5)
            if max(dist2[0]) > max_length:
                max_length = max(dist2[0])
        if min_length < max_length/2:
            find_coord_data.append([array[i][0], array[i][1], array[i][2]])
            dist, ind = tree_model.query(array[i], k=1)
            find_vector_data.append([coord_vector_model[ind][0][0][0],
                                     coord_vector_model[ind][0][0][1],
                                     coord_vector_model[ind][0][0][2]])
    write_points_model_in_file(find_coord_data, find_vector_data)



reader = vtk.vtkGenericDataObjectReader()
reader.SetFileName(file_data_name)
reader.Update()
ug = reader.GetOutput()
points = ug.GetPoints()
coord_vector_data = vtk_to_numpy(ug.GetPointData().GetArray('DTMRIFiberOrientation'))
coord_points_data = vtk_to_numpy(points.GetData())

find_vectors(coord_points_data)


