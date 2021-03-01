from pgm.dag.dbn.tstbn import Slice as TsDbnSlice
from state import State
from state.obs import Obs
from pgm.dag.dbn.tstbn.mjpf import Cluster
from pgm.dag.dbn.tstbn.mjpf import Likelihood
'''
Causal - likelihood - lanada in Carlo slides
'''
class Slice(TsDbnSlice):
    def __init__(self, timeInstance:int, obs: Obs, state: State, cluster: Cluster, likelihood:Likelihood):
        pass