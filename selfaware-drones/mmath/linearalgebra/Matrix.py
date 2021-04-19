from typing import List
from collections.abc import Iterable

import numpy as np
from mmath.linearalgebra import Matrix
import array


class Matrix():
    '''todo: Each matrix is composed of columns of vectors. As such replace the inheritence between matrix and vector with composition'''
    def __init__(self, vecs:Iterable, vecsDir:str="HORIZONTAL"):
        '''A matrix is formed of many rows'''
        self.__vecs:np.ndarray = None
        if type(vecs) is List:
            self.__vecs = np.asarray(vecs)
        elif type(vecs) is np.ndarray:
            self.__vecs = vecs

    # def __eq__(self, other:Matrix)->bool:
    #     ''''''
    #     if np.allclose(self.getNpRows(),other.getNpRows(),rtol=1e-07, atol=1e-08):
    #         return True
    #     return False
    def __mul__(self, other:Matrix)->Matrix:
        ''''''
        npResult = None
        if type(other) in (float,np.float64,int):
            npResult = other*self.__vecs
        elif type(other) in (Matrix):
            npResult = np.dot(self.__vecs, other)
        else:
            raise Exception("Matrix multi dosent understand how to treat 'Other' datat type")
        npResult = Matrix(npResult)
        return npResult

    def __add__(self, other:Matrix)->Matrix:
        npAdd = np.add(self.getNpRows(), other.getNpRows())
        addMat = Matrix(npAdd)
        return addMat

    def __getInverse(self)->Matrix:
        pass

    def __pow__(self, power, modulo=None)->Matrix:
        if power == -1:
            return self.getInverse()
        elif power == 'T':
            Matrix.transpose(self)

    def __sub__(self, other:Matrix)->Matrix:
        '''over writes subtract'''
        npSub = np.subtract(self.getNpRows(), other.getNpRows())
        subMat = Matrix(npSub)
        return subMat

    def __getitem__(self, index:int):
        '''for brackets []'''
        return self.__vecs[index]

    def getNpRowByIndex(self,index:int):
        return self.__vecs[index]

    def getNpColByIndex(self,colIndex:int)->np.ndarray:
        return self.__vecs[:, colIndex]

    def transpose(m:Matrix)->Matrix:
        '''Transpose'''
        pass

    def getIdentity(dimention:int)->Matrix:
        pass

    def getNpRows(self)->np.ndarray:
        return self.__vecs

    def getRowsNum(self)->int:
        return self.__vecs.shape[0]

    def getColsNum(self)->int:
        return self.__vecs.shape[1]


