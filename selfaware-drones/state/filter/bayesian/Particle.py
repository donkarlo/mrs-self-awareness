from array import array

from state.obs import ObsSerie
from state.State import State
from state.filter.bayesian import Filter


class Particle(Filter):
    ''''''
    def __init__(self, observationSerie: ObsSerie, landMarks:array(State)):
        '''

        Parameters
        -----------
        landMarks:array(State)
            States that are known to us. Such as centroids of clusters
        '''
        super(Particle, self).__init__(observationSerie)
        self.__particles = array(State)


    def getCurrentPosteriorState(self):
        pass

    def __action(self):
        '''Accuracy reduction'''
        pass

    def __sense(self, particle: State):
        pass

    def __sense(self,particle:State,landMark:State):
        '''z(x_t)~\sum f(x|\mu,\delta^2)
        x is the  measured distance between the particle and the given landmarke
        x_t is the particle
        \mu is the theoretical distance between the measured distance and the landmark
        '''
        pass

    def getLandMarkNumber(self):
        '''
        if the state is formed of [position,velocity] in 3d then the numebr of landmarks is 6.
        It can also be the distance from
        '''
        pass

    def generateParticles(self,number):
        pass

    def __moveParticles(self, deltaState):
        ''''''
        return

    def getCurrentEstimatedState(self):
        '''Return posterior state according to current obs'''
        return



