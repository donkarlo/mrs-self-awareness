from mmath.data.cluster.gng.Gng import Gng
from mmath.data.cluster.gng.PlotBuilder import PlotBuilder
from mmath.data.cluster.gng.examples.FiveUniformShapes.Builder import Builder
from mmath.linearalgebra.Matrix import Matrix

#All points can be
shapeBuilder = Builder()
allPoints = shapeBuilder.getAllPoints()
inpRowsMatrix = Matrix(allPoints)
gng = Gng(inpRowsMatrix,maxNodesNum=50)
gng.getClusters()
gng.getGraph().report()
plotter = PlotBuilder(gng.getInpRowsMatrix(),gng.getGraph())
plotter.showAll2D()
