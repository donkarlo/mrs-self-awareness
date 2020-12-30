from array import *

from state import ObservationComposit


class ObservationTimeSerie():
    def __init__(self, obsCmp=array(ObservationComposit)):
        self.obsCmp = obsCmp