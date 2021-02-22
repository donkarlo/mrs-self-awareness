from trajectory.gen.ParamShapePointGeneratorComposit import *
from trajectory.gen.ParamLinePointGenerator import *

class SlopedTriangleParamShapePointGenerator(ParamShapePointGeneratorComposit):
    def __init__(self,distanceInterval):
        super(SlopedTriangleParamShapePointGenerator, self).__init__()
        print("new points")

        l1 = ParamShapeLine([1, 0, 0], [0, 0, 10])
        l1pg = ParamLinePointGenerator(l1, distanceInterval, 0, 10)
        l1pg.echoPoints()

        print("new points")

        l2 = ParamShapeLine([-0.5, 1, -0.5], [10, 0, 10])
        l2pg = ParamLinePointGenerator(l2, distanceInterval, 0, 10)
        l2pg.echoPoints()

        print("new points")

        l3 = ParamShapeLine([-0.5, -1, 0.5], [5, 10, 5])
        l3pg = ParamLinePointGenerator(l3, distanceInterval, 0, 10)
        l3pg.echoPoints()

        self\
            .add(l1pg)\
            .add(l2pg)\
            .add(l3pg)\

tspsg = SlopedTriangleParamShapePointGenerator(0.5)
tspsg.plot3DPoints()

tspsg.getPoints().addDim(0)
tspsg.getPoints().echoFile("/home/donkarlo/Desktop/my-sloped-triangle-05.txt", " ")