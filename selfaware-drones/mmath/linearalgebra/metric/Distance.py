import abc

from mmath.linearalgebra.Vector import Vector


class Distance:
    def __init__(self, vec1: Vector, vec2: Vector):
        self._vec1 = vec1
        self._vec2 = vec2

    @abc.abstractmethod
    def getDistance(self) -> float:
        pass
