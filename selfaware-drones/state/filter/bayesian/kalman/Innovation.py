from mmath.linearalgebra import Matrix, Vector
from pgm.dag.dbn.tstbn.mjpf.abnormality import StrategyInterface as AbnormalityStrgy
from state.State import State
from state.obs.Obs import Obs


class Innovation(AbnormalityStrgy):
    '''y^{~}_{k} = z_k-Hx^{^-}_{k}

    Parameters
    ----------

    Returns
    _______

    '''

    def __init__(self
                 , processMatrix: Matrix
                 , currentObservation: Obs
                 , priorCurrentEstimatedState: State):
        self._processMatrix = processMatrix
        self.__currentObservation = currentObservation
        self.__priorCurrentEstimatedState = priorCurrentEstimatedState

    def getInnovation(self) -> Vector:
        yK = self.__currentObservation - self.__processMatrix * self._priorCurrentEstimatedState
        return yK
