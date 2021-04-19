import abc


class StrategyInterface():
    def __init__(self):
        pass

    @abc.abstractmethod
    def getDistance(self, distanceStrategy) -> float:
        '''Must measure the distance between two statistical distributions
        '''
        pass
