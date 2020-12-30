from mmath.linearalgebra.Matrix import Matrix

'''
z_k=Hx_{k}+v_{k}
'''
class MeasurementModel():
    def __init__(self, h:Matrix):
        self._h=h
        pass
    def getStateByObservation(self,):
        pass