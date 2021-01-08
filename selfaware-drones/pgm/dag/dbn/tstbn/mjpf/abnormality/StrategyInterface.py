import abc

from pgm.dag.dbn.tstbn.mjpf.abnormality.distance import StrategyInterface


class StrategyInterface():
    def __init__(self):
        pass

    @abc.abstractmethod
    def getAbnormality(self, distanceStrategy:StrategyInterface)->float:
        '''The distance between two distributions
        '''
        pass