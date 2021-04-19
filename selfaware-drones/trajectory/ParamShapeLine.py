from trajectory.ParamShape import ParamShape


class ParamShapeLine(ParamShape):
    def __init__(self, nVec=[], cVec=[]):
        # todo check the length of nVec is equal to length of cVec
        self._nVec = nVec
        self._cVec = cVec
        super().__init__("line")

    def getNVec(self):
        return self._nVec

    def getCVec(self):
        return self._cVec

    def getDim(self) -> int:
        return len(self._nVec)
