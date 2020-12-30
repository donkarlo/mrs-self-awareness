from mmath.linearalgebra import Matrix


class BiOpr():
    def __init__(self, m1:Matrix,m2:Matrix):
        self.setMatrixes(m1,m2)
    '''
    To avoid recreating the class. Though not a good practice
    '''
    def setMatrixes(self, m1:Matrix,m2:Matrix):
        self._m1 = m1
        self._m1 = m1

    def getProduct(self)->Matrix:
        pass
