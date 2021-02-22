from trajectory.gen.ParamShapePointGeneratorComposit import *
from trajectory.gen.ParamLinePointGenerator import *

class TwoStepsParamShapePointGenerator(ParamShapePointGeneratorComposit):
    def __init__(self,distanceInterval):
        super(TwoStepsParamShapePointGenerator, self).__init__()
        print("new points")

        l1 = ParamShapeLine([1, 0, 0], [0, 0, 10])
        l1pg = ParamLinePointGenerator(l1, distanceInterval, 0, 5)
        l1pg.echoPoints()

        print("new points")

        l2 = ParamShapeLine([0, 0, -1], [5, 0, 10])
        l2pg = ParamLinePointGenerator(l2, distanceInterval, 0, 5)
        l2pg.echoPoints()

        print("new points")

        l3 = ParamShapeLine([1, 0, 0], [5, 0, 5])
        l3pg = ParamLinePointGenerator(l3, distanceInterval, 0, 5)
        l3pg.echoPoints()

        print("new points")

        l4 = ParamShapeLine([0, 1, 0], [10, 0, 5])
        l4pg = ParamLinePointGenerator(l4, distanceInterval, 0, 10)
        l4pg.echoPoints()

        print("new points")

        l5 = ParamShapeLine([-1, 0, 0], [10, 10, 5])
        l5pg = ParamLinePointGenerator(l5, distanceInterval, 0, 5)
        l5pg.echoPoints()

        print("new points")

        l6 = ParamShapeLine([0, 0, 1], [5, 10, 5])
        l6pg = ParamLinePointGenerator(l6, distanceInterval, 0, 5)
        l6pg.echoPoints()

        print("new points")

        l7 = ParamShapeLine([-1, 0, 0], [5, 10, 10])
        l7pg = ParamLinePointGenerator(l7, distanceInterval, 0, 5)
        l7pg.echoPoints()

        print("new points")
        l8 = ParamShapeLine([0, -1, 0], [0, 10, 10])
        l8pg = ParamLinePointGenerator(l8, distanceInterval, 0, 10)
        l8pg.echoPoints()

        self\
            .add(l1pg)\
            .add(l2pg)\
            .add(l3pg)\
            .add(l4pg)\
            .add(l5pg)\
            .add(l6pg)\
            .add(l7pg)\
            .add(l8pg)

tspsg = TwoStepsParamShapePointGenerator(0.5)
tspsg.plot3DPoints()
tspsg.getPoints().addDim(0)
tspsg.getPoints().echoFile("/home/donkarlo/Desktop/my-two-steps-05.txt", " ")