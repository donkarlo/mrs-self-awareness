from mmath.linearalgebra import Vector
from mmath.linearalgebra.Matrix import Matrix
from state.State import State


class ProcessModel():
    def __init__(self
                 , processMatrix: Matrix = None
                 , controlMatrix: Matrix = None
                 , processNoiseCov: Matrix = None
                 , prevState: State = None
                 , prevControl: Vector = None
                 , prevProcessNoise: Vector = None
                 ):
        ''' x_k=Fx_{k-1}+Bu_{k-1}+w_{k-1}

        Parameters
        ----------
        __f:Matrix
            is F
        __b:Matrix
            is B
        '''
        self.__processMatrix = processMatrix
        self.__controlMatrix = controlMatrix
        self.__processNoiseCov = processNoiseCov
        self.setPreviousState(prevState, prevControl, prevProcessNoise)

    def setPreviousState(self
                         , prevState: State = None
                         , prevControl: Vector = None
                         , prevProcessNoise: Vector = None) -> None:
        """Setting the previous situation
        Prev stands for previous

        Parameters
        ----------

        Returns
        -------
        """
        self.__prevState = prevState
        self.__preControl = prevControl
        self.__prevProcessNoise = prevProcessNoise

    def getCurrentState(self
                        , prevState: State = None
                        , prevInput: Vector = None
                        , prevProcessNoise: Vector = None) -> State:
        """Get current state based on previous one
        """
        self.setPreviousState(prevState, prevInput, prevProcessNoise)
        fPrevState = self.__processMatrix * self.__prevState
        bPrevInput = self.__controlMatrix * self.__prevNoise
        curState = fPrevState + bPrevInput + self.__prevW
        return curState

    def getProcessMatrix(self) -> Matrix:
        return self.__processMatrix

    def getProcessNoiseCov(self) -> Matrix:
        return self.__processNoiseCov

    def getProcessMatrix(self):
        '''Train it if does not exist'''
        pass
