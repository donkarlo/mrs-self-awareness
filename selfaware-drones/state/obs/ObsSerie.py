import numpy as np

from state.obs import Obs

class ObsSerie():
    """A time serie of obs vectors
    """
    def __init__(self, obsArr=[]):
        self.__obsArr = obsArr

    def getByIdx(self, index:int)->int:
        return self.__obsArr[index]

    def getObsArr(self):
        return self.__obsArr