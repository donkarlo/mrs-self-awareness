from pgm.dag.dbn import Dbn
from pgm.dag.dbn.tstbn.mjpf.abnormality import Strgy as AbnStrgy
from state import  ObservationCompositTimeSerie
from cluster import ClusteringStrgy

'''
Markov Jump Particle Filters
'''
class Mjpf(Dbn):
    '''
    
    '''
    def __init__(self, z:ObservationCompositTimeSerie, cStrgy: ClusteringStrgy, deltaT:int, abnormalityMeasurementStrgy:AbnStrgy):
        self._clusters = None
        self._z = z
        pass
    '''
    Z_k = (z_{k},(z_{k+1}-z_{k}))/deltaT
    '''
    def _getProcessedObservation(self):
        pass

    def _getClusters(self):
        pass

