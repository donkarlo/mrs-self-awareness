from state.obs.Obs import Obs as ObservationBase


class Observation(ObservationBase):
    '''Can come both by GPS or IMU'''
    def __init__(self):
        super(Observation, self).__init__()
