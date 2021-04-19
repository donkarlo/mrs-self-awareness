from array import array

from mmath.linearalgebra import Vector
from state import State as ParentState


class State(ParentState):
    def __init__(self, position: Vector, velocity: Vector):
        '''We just want to estimate [position,vector]

        todo
        ----
        Concat both postion and velocity in one vector
        '''
        self.__position = position
        self.__velocity = velocity
        super(State, self).__init__()

    def __getConcatArray(self) -> array:
        pass
