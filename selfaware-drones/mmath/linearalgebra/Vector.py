import numpy as np
from mmath.linearalgebra.Matrix import Matrix


class Vector(Matrix):
    '''Vector is a matrix of one column and multiple rows, but for simlicity, we remove array
    '''
    def __init__(self,components:list):
        #make each row an array
        for componentCounter,component in components:
            if component.GetType().IsPrimitive:
                components[componentCounter] = np.asarray(component)
        super(Vector, self).__init__(components)