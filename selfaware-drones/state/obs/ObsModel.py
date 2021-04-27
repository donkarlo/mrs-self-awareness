from mmath.linearalgebra import Vector
from mmath.linearalgebra.Matrix import Matrix
from state import State
from state.filter.kalman import Innovation
from state.obs import Obs


class ObsModel():
    '''z_k=Hx_{k}+v_{k}, v_{k}~N(0,R)

    '''

    def __init__(self
                 , observationMatrix: Matrix
                 , observationNoiseCov: Matrix):
        self.__observationMatrix = observationMatrix
        self.__observationNoiseCov = observationNoiseCov

    def getStateByObservation(self
                              , observation: Obs
                              , onservationNoise: Vector = None) -> State:
        pass

    def getObservationByState(self
                              , state: State
                              , onservationNoise: Vector = None) -> Obs:
        pass

    def getInnovationObject(self
                            , observation: Obs
                            , state: State) -> Innovation:
        """To calculate inoovation

        Parameters
        ----------
        observation:Obs
            a vector of obs
        state: State
            Prior Estimated State

        Returns
        -------
        invVec
        """
        inv = Innovation(self.__observationMatrix, observation, state)
        return inv

    def getInnovation(self, zK: Obs, xKPrEst: State) -> Vector:
        return self.getInnovationObject().getInnovation()

    def getObservationMatrix(self) -> Matrix:
        return self.__observationMatrix

    def getObservationNoiseCov(self) -> Matrix:
        return self.__observationNoiseCov
