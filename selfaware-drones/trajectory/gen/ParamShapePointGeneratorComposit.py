from trajectory.Point import *
from trajectory.ParamShape import *
from trajectory.ParamShapeLine import *


class ParamShapePointGeneratorComponent:
    '''
    Shared between the composit and leaf PointGenerators
    '''
    def _generatePoints(self) -> None:
        pass

    def __init__(self):
        self._points = None

    def getPoints(self)->Points:
        if (self._points is None):
            self._points = Points()
            self._generatePoints()
        return self._points

    def echoPoints(self):
        for point in self.getPoints().getPointsList():
            point.echo()

    def _addPoint(self, point: Point):
        self._points.add(point)

    def getDim(self) -> int:
        return len(self.getPoints().getDim())

    def plot3DPoints(self):
        self.getPoints().plot3DPoints()

class ParamShapePointGeneratorLeaf(ParamShapePointGeneratorComponent):
    """
    A leaf generatotr
    """
    def __init__(self, paramShape: ParamShape, distanceInterval: float, lowerBand: float, upperBand: float):
        super(ParamShapePointGeneratorLeaf, self).__init__()
        self._paramShape = paramShape
        self._distanceInterval = distanceInterval
        self._lowerBand = lowerBand
        self._upperBand = upperBand

    def getParamShape(self) -> ParamShape:
        return self._paramShape



class ParamShapePointGeneratorComposit(ParamShapePointGeneratorComponent):
    """
    The composit of ParamShapePointGenerator
    """
    def __init__(self, paramShapePointGeneratorsList=[]):
        super(ParamShapePointGeneratorComposit, self).__init__()
        self._paramShapePointGeneratorsList = paramShapePointGeneratorsList

    def getPoints(self) -> Points:
        if (self._points is None):
            self._points = Points()
            for paramShapePointGenerator in self._paramShapePointGeneratorsList:
                self._points.getPointsList().extend(paramShapePointGenerator.getPoints().getPointsList())
        return self._points

    def add(self, paramShapeGeneratorLeaf: ParamShapePointGeneratorLeaf):
        self._paramShapePointGeneratorsList.append(paramShapeGeneratorLeaf)
        return self

    def getParamShapePointGeneratorsListLen(self):
        return len(self._paramShapePointGeneratorsList)