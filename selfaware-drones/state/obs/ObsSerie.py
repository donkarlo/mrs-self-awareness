from typing import List

from data.state.obs.Obs import Obs


class ObsSerie():
    """A time serie of obs vectors
    """

    def __init__(self, obsArr:List[Obs]):
        self.__obsArr = obsArr

    def getByIdx(self, index: int) -> int:
        return self.__obsArr[index]

    def getObsArr(self):
        return self.__obsArr
