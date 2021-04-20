from mmath.data.cluster import ClusteringStrgy
from pgm.dag.dbn import Dbn
from pgm.dag.dbn.tstbn.mjpf.abnormality import StrategyInterface as AbnStrgy
from state.State import State
from state.filter.bayesian.kalman import Kalman
from state.obs import ObsSerie


class Mjpf(Dbn):
    '''Markov Jump Particle Filters
    Practically, it tries to cluster behaviorally (Behavaior embodies in changes of velocity such that the agent changes its super state. for example the agent changes from a stright path to a to curved path)
    Particle filter works like we have behaviorial map (the map we need for any PF) presented in the form of clusters of SOM or GNG with a weigthing startegy which prefers
    velocity from input data which is formd of x=[\vec{position},\vec{velocity}]
    '''

    def __init__(self, ObservationSerie: ObsSerie, clusteringStrategy: ClusteringStrgy, timeInterval: int,
                 abnormalityMeasurementStrgy: AbnStrgy):
        '''

        Parameters
        ----------
        _ObeservationSeri: ObsSerie
        '''
        self._ObeservationSeri = ObservationSerie  # Similar to Particle filtering at least two conscutive observations are needed
        self._currentEstimatedSuperState = None  # will be estimated
        self._currentEstimatedContinousState = None  # if None, then use self.__getCurrentEstimatedSuperState
        self._clusteringStrategy = clusteringStrategy  # Each cluster should form a state where velocity is constant
        pass

    def _getProcessedObservation(self):
        '''Z_k = (z_{k},(z_{k+1}-z_{k}))/timeInterval
        '''
        pass

    def __getSuperStates(self):
        '''By the clustering startegy'''
        pass

    def __getCurrentEstimatedSuperState(self, observation: ObsSerie) -> State:
        '''The activated region in which the velocity is quasi static, by particle filter

        todo
        ----
        The return value can be an array of training data forming that cluster

        Return
        ------
        State
            Since every cluster defines a super state and so far the superstates where presented by a state like the cetroids
            or the neuron of an SOM then the return value is a State
        '''
        pass

    def __getCurrentEstimatedSuperStateKalmanFilter(self) -> Kalman:
        pass

    def __getCurrentEstimatedContinousState(self) -> State:
        pass

    def __getUncertaintyBoundry(self) -> float:
        '''How much '''
