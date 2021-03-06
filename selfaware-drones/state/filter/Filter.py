import abc
from array import array

from distaware.State import State
from pgm.dag.dbn.hmm.Hmm import Hmm
from state.obs import ObsSerie
from state.obs.Obs import Obs


class Filter(Hmm):
    ''' In each filter, first we predict then we observe
    What is the PDF of state with a given set of obs
    if the variables are normally distributed and the transitions are linear, the Bayes filter becomes equal to the Kalman filter.
    It is an HMM
    '''

    def __init__(self, obsSerie: ObsSerie):
        self._obsSerie = obsSerie
        self._states = array(State)

    def addObservation(self, obs: Obs) -> None:
        self.__obsSerie.push(obs)

    @abc.abstractmethod
    def predict(self) -> State:
        pass

    @abc.abstractmethod
    def update(self, obs: Obs) -> State:
        pass
