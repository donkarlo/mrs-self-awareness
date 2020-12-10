from pgm import State

'''
Generalised states
'''
class Gs(State):
    def __init__(self,derivativesVec=[]):
        self.__derivativesVec = derivativesVec
        pass