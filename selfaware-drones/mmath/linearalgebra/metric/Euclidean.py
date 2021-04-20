from mmath.linearalgebra.Vector import Vector
from mmath.linearalgebra.metric.Distance import Distance


class Euclidean(Distance):
    def __init__(self, vec1: Vector, vec2: Vector):
        super(Euclidean, self).__init__(vec1, vec2)

    def getDistance(self):
        pass
