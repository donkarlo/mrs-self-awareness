from state.obs.ObsSerie import ObsSerie
from state.obs.ThreeDPosVelObs import ThreeDPosVelObs


class ThreeDPosVelObsSerieBuilder():
    '''Just a builder for ObsSerie, it just appends!!'''

    def __init__(self):
        ''''''
        self.__obsArr = []

    def append(self, threeDPosVel: ThreeDPosVelObs) -> None:
        ''''''
        self.__obsArr.append(threeDPosVel)
        print(self.__obsArr)

    def getObsSerie(self) -> ObsSerie:
        ''''''
        self.__obsSerie = ObsSerie(self.__obsArr)
        return self.__obsSerie
