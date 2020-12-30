from mmath.linearalgebra.Matrix import Matrix
from state.State import State


class ProcessModel():
    '''
    x_k=Fx_{k-1}+Bu_{k-1}+w_k
    '''
    def __init__(self, f: Matrix, b: Matrix):
        pass
    def getNextState(self,previousState:State,)->State:
        pass
