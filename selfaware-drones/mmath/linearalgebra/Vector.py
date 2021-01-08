import array
from mmath.linearalgebra import Matrix


class Vector(Matrix):
    """Vector is a matrix of one column and multiple rows
    """
    def __init__(self,rows:array):
        super().__init__()