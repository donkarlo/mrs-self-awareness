import array

import Obs
import ObsSerie


class ObsSerieBuilder():
    def __init__(self):
        self.__obsArr = array(Obs)

    def push(self, obs: Obs) -> None:
        self.__obsArr.append(obs)

    def getObsSerie(self) -> ObsSerie:
        self.__obsSerie = ObsSerie(self.__obsArr)
        return self.__obsSerie
