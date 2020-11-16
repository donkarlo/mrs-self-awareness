from trajectory.ParamShapeLine import *
from trajectory.ParamShapePointGeneratorComposit import *
from trajectory.ParamLinePointGenerator  import *

class TwoStepsParamShapePointGenerator(ParamShapePointGeneratorComposit):
    def __init__(self,distanceInterval):
        super(TwoStepsParamShapePointGenerator, self).__init__()
        print("new points")

        l1 = ParamShapeLine([1, 0, 0], [0, 0, 10])
        l1pg = ParamLinePointGenerator(l1, distanceInterval, 0, 10)
        l1pg.echoPoints()

        print("new points")

        l2 = ParamShapeLine([0, 1, 0], [10, 0, 10])
        l2pg = ParamLinePointGenerator(l2, distanceInterval, 0, 10)
        l2pg.echoPoints()

        print("new points")

        l3 = ParamShapeLine([-1, 0, 0], [10, 10, 10])
        l3pg = ParamLinePointGenerator(l3, distanceInterval, 0, 10)
        l3pg.echoPoints()

        print("new points")

        l4 = ParamShapeLine([0, -1, 0], [0, 10, 10])
        l4pg = ParamLinePointGenerator(l4, distanceInterval, 0, 10)
        l4pg.echoPoints()

        self\
            .add(l1pg)\
            .add(l2pg)\
            .add(l3pg)\
            .add(l4pg)\

tspsg = TwoStepsParamShapePointGenerator(0.5)
tspsg.plot3DPoints()
tspsg.getPoints().addDim(0)
tspsg.getPoints().echoFile("/home/donkarlo/Desktop/my-rect-05.txt", " ")