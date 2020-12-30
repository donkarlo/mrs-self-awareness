from mmath.linearalgebra import Matrix
from mmath.linearalgebra.BiOpr import BiOpr
from pgm.dag.dbn.tstbn.mjpf.abnormality import Strgy as AbnormalityStrgy
from state.ObservationComposit import ObservationComposit
from state.State import State

'''
y^{~}_{k} = z_k-Hx^{^-}_{k}
'''
class Innovation(AbnormalityStrgy):
    '''

    '''
    def __init__(self,z:ObservationComposit,h:Matrix,priorEstimatedState:State):
        self._z = z
        self._h = h
        self._pES = priorEstimatedState

    '''
    '''
    def getInnovation(self)->Matrix:
        mbOpr = BiOpr()
        mbOpr.setMatrixes(self._h,self._pES)
        yK = self.getLastObservation() * mbOpr.getProduct(self._h,self._pES)
        return yK