from array import *

from mmath.linearalgebra import Vector


class Observation(Vector):
    """Observation, many observations from different sensors may result in fewer states
    """

    def __init__(self, timeStamp:int, vector:Vector):
        self.__timeStamp = timeStamp
