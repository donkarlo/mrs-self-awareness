from state import Gs as StateGs
from trajectory.Point import Point

'''
In Baydouns paper it is shown as X tilda
'''


class GS(StateGs):
    def __init__(self, position: Point, velocity: Point):
        self.__position = position
        self.__velocity = velocity
