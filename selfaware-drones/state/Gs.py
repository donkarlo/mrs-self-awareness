from state import State

class Gs(State):
    '''Generalised states
    '''
    def __init__(self,derivativesVec=[]):
        self.__derivativesVec = derivativesVec
        pass