from linearalgebra import Vector
from linearalgebra.Matrix import Matrix
from state.State import State


class ProcessModel():
    def __init__(self
                 , curProcessMatrix: Matrix = None
                 , prevStateVector: State = None
                 , curProcessNoiseCovMatrix: Matrix = None
                 , prevProcessNoiseVector: Vector = None
                 , curControlMatrix: Matrix = None
                 , prevControlVector: Vector = None
                 ):
        ''' x_k=Fx_{k-1}+Bu_{k-1}+w_{k-1}

        Parameters
        ----------
        __f:Matrix
            is F
        __b:Matrix
            is B
        '''
        self.__processMatrix:Matrix = curProcessMatrix
        self.__controlMatrix:Matrix = curControlMatrix
        self.__processNoiseCovVector:Matrix = curProcessNoiseCovMatrix
        self.updatePreviousState(prevStateVector, prevControlVector, prevProcessNoiseVector)

    def updatePreviousState(self
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
        self.__prevStateVector = prevState
        self.__preControlVector = prevControl
        self.__prevProcessNoiseVector = prevProcessNoise

    def getCurrentState(self
                        , prevStateVector: State = None
                        , prevInputVector: Vector = None
                        , prevProcessNoiseMatrix: Vector = None) -> State:
        """Get current state based on previous one
        """
        self.updatePreviousState(prevStateVector, prevInputVector, prevProcessNoiseMatrix)
        fPrevState = self.__processMatrix * self.__prevStateVector
        bPrevInput = self.__controlMatrix * self.__prevNoise
        curState = fPrevState + bPrevInput + self.__prevW
        return curState

    def getProcessMatrix(self) -> Matrix:
        return self.__processMatrix

    def getProcessNoiseCov(self) -> Matrix:
        return self.__processNoiseCovVector

    def getProcessMatrix(self):
        '''Train it if does not exist'''
        pass
