import numpy as np
from mmath.linearalgebra import Matrix
import array


class Matrix():
    '''A matrix is formed of many rows'''
    def __init__(self, rows):
        self._rows = rows
        pass

    def __mul__(self, other:Matrix)->Matrix:
        pass

    def __add__(self, other:Matrix)->Matrix:
        pass

    def __getInverse(self)->Matrix:
        pass

    def __pow__(self, power, modulo=None)->Matrix:
        if power == -1:
            return self.getInverse()
        elif power == 'T':
            Matrix.transpose(self)

    def __sub__(self, other):
        pass


    def transpose(m:Matrix):
        '''Transpose'''
        pass

    def getIdentity(dimention:int)->Matrix:
        pass