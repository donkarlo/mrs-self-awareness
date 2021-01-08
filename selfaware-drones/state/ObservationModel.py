from mmath.linearalgebra import Vector
from mmath.linearalgebra.Matrix import Matrix
from state import Observation, State
from state.filter.bayesian.kalman import Innovation

class ObservationModel():
    '''z_k=Hx_{k}+v_{k}, v_{k}~N(0,R)

    '''
    def __init__(self
                 , observationMatrix:Matrix
                 , observationNoiseCov:Matrix):
        self.__observationMatrix = observationMatrix
        self.__observationNoiseCov = observationNoiseCov

    def getStateByObservation(self
                              , observation:Observation
                              , onservationNoise:Vector=None)->State:
        pass

    def getObservationByState(self
                              ,state:State
                              , onservationNoise:Vector=None)->Observation:
        pass

    def getInnovationObject(self
                            , observation:Observation
                            , state:State)->Innovation:
        """To calculate inoovation

        Parameters
        ----------
        observation:Observation
            a vector of observation
        state: State
            Prior Estimated State

        Returns
        -------
        invVec
        """
        inv = Innovation(self.__observationMatrix, observation , state)
        return inv

    def getInnovation(self, zK:Observation, xKPrEst:State)->Vector:
        return self.getInnovationObject().getInnovation()

    def getObservationMatrix(self)->Matrix:
        return self.__observationMatrix

    def getObservationNoiseCov(self)->Matrix:
        return self.__observationNoiseCov