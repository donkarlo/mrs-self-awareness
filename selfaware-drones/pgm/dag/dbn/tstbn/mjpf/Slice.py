from pgm.dag.dbn.tstbn import Slice as TsDbnSlice
from state import ObservationComposit, State
from pgm.dag.dbn.tstbn.mjpf import Cluster
from pgm.dag.dbn.tstbn.mjpf import Likelihood
'''
Causal - likelihood - lanada in Carlo slides
'''
class Slice(TsDbnSlice):
    def __init__(self, timeInstance:int, obs: ObservationComposit, state: State, cluster: Cluster, likelihood:Likelihood):
        pass