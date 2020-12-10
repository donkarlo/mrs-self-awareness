from pgm.dag.dbn import Coupled as CoupledDBN
from pgm.dag.dbn.tstbn.mjpf import Mjpf
class Coupled(CoupledDBN):
    def __init__(self, dbn1:Mjpf, dbn2:Mjpf):
        pass