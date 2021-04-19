from trajectory.ParamShapeLine import *
from trajectory.Point import *
from trajectory.gen.ParamShapePointGeneratorComposit import ParamShapePointGeneratorLeaf


class ParamLinePointGenerator(ParamShapePointGeneratorLeaf):
    """
	Generating points for lines
	The direction of normal vector (paramLine._nVec) shows toward which direction the points
	must be generated, that is normal vector [1,0,0] is different than [-1,0,0]
	in the sense of the order by which the points are generated
	additionally paramLine._cVec can be interpreted as the starting point from which the
	points should be generated along the normal vector (ParamLine._nVec)
	@:param paramLine
	@:param distanceInterval denote the amount by which
	"""

    def __init__(self, paramLine: ParamShapeLine, distanceInterval: float, lowerBand: float, upperband: float):
        self._paramLine = paramLine
        paramShape = ParamShape(self._paramLine.getName())
        super(ParamLinePointGenerator, self).__init__(paramShape, distanceInterval, lowerBand, upperband)

    def getDim(self) -> int:
        return len(self._paramLine.getNVec())

    def _generatePoints(self) -> None:
        t = self._lowerBand
        while (t <= self._upperBand):
            cords = []
            for dimCtr in range(self.getDim()):
                cords.append(self._paramLine._nVec[dimCtr] * t + self._paramLine._cVec[dimCtr])
            self._points.add(Point(cords))
            t += self._distanceInterval
