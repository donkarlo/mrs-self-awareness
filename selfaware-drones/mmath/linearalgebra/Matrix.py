import numpy
from mmath.linearalgebra import Matrix


class Matrix():
    def __init__(self):
        pass

    def __mul__(self, other):
        pass

    def __add__(self, other):
        pass

    def __getInverse(self, m:Matrix = None)->Matrix:
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