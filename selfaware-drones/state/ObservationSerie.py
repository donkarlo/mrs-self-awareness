from array import *

from state import Observation

class ObservationSerie():
    """A time serie of observation vectors
    """
    def __init__(self, observations=array(Observation)):
        self.__observations = observations

    def push(self,observation:Observation)->None:
        self.__observations.append(observation)