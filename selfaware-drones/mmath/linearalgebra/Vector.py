import numpy as np

from mmath.linearalgebra import Vector
from mmath.linearalgebra.Matrix import Matrix


class Vector(Matrix):
    '''Vector is a matrix of one column and multiple rows, but for simlicity, we remove array
    '''

    def __init__(self, components):
        newComponents = []
        # make each row an array
        for component in components:
            if type(component) == np.ndarray:
                # if component is an np.array already append it as it is. So it is already [[1] [2] [3]]
                if (component.shape[0] == 1):
                    newComponents.append(component)
            elif type(component) in (np.float64, float, int):
                # for lists like [1,2,3] or np.ndarray like [1 2 3]
                newComponents.append([component])
            else:
                raise Exception("Components are not understandable for Vector")
        npComps = np.asarray(newComponents)
        super().__init__(npComps)

    def getNpRow(self) -> np.ndarray:
        rows = []
        for row in self.getNpRows():
            rows.append(row[0])
        return np.asarray(rows)

    def getDistanceFrom(self, vec: Vector) -> float:
        return np.linalg.norm(self.getNpRow() - vec.getNpRow())

    # def __eq__(self, other:Vector)->bool:
    #     return Vector(super().__eq__(other))

    def __sub__(self, other: Vector) -> Vector:
        ''''''
        return Vector(super().__sub__(other))

    def __add__(self, other: Vector) -> Vector:
        ''''''
        return Vector(super().__add__(other))

    def __mul__(self, other: Vector) -> Vector:
        ''''''
        return Vector(super().__mul__(other))

    def getComponentByIndex(self, index: int):
        ''''''
        return self.getNpRows()[index][0]
