from array import array

from linearalgebra.Matrix import Matrix
from state.State import State
from state.filter.Filter import Filter
from state.obs import ObsSerie


class Particle(Filter):
    ''''''

    def __init__(self, initState:State,regionOfIntrest:Matrix, particlesNum:int):
        '''
        @todo ROI can be a distribution too

        Parameters
        -----------

        '''
        self.__currentParticleSet = None
        self.__particlesNum = particlesNum
        self.__regionOfInterest = regionOfIntrest

        super().__init__()


    def __sense(self, particle: State):
        '''z(x_t)~\sum f(x|\mu,\delta^2)
        x is the  measured distance between the particle and the given landmarke
        x_t is the particle
        \mu is the theoretical distance between the measured distance and the landmark
        '''
        pass
