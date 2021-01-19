import abc
from array import array

from distaware.State import State
from pgm.dag.dbn.hmm.Hmm import Hmm
from state import ObservationSerie
from state.Observation import Observation


class Filter(Hmm):
    ''' In each filter, first we predict then we observe
    What is the PDF of state with a given set of observation
    if the variables are normally distributed and the transitions are linear, the Bayes filter becomes equal to the Kalman filter.
    It is an HMM
    '''
    def __init__(self, observationSerie:ObservationSerie):
        self._observationSerie = observationSerie
        self._states =  array(State)

    def addObservation(self, observation:Observation)->None:
        self.__observationSerie.push(observation)

    @abc.abstractmethod
    def predict(self)->State:
        pass

    @abc.abstractmethod
    def update(self, obs:Observation)->State:
        pass
