from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D

from mmath.data.cluster.gng.graph.Graph import Graph
from mmath.data.cluster.gng.graph.PlotBuilder import PlotBuilder as GraphPlotBuilder
from mmath.linearalgebra.Matrix import Matrix


class PlotBuilder(GraphPlotBuilder):
    def __init__(self, inpRowsMatrix: Matrix, graph: Graph):
        ''''''
        super().__init__(graph)
        self.__inpRowsMatrix: Matrix = inpRowsMatrix

    def add2DInpRowsMatrixScatter(self):
        ''''''
        xInpVecs = self.__inpRowsMatrix.getNpColByIndex(0)
        yInpVecs = self.__inpRowsMatrix.getNpColByIndex(1)
        self.getPlot().scatter(xInpVecs, yInpVecs, marker='.', c='lightblue')

    def showAll2D(self):
        ''''''
        self.add2DInpRowsMatrixScatter()
        self.add2DNodes()
        self.add2DEdges()
        self.getPlot().show()

    def showAll3D(self):
        ''''''
        fig = pyplot.figure()
        ax = Axes3D(fig)

        # Raw Data
        xInpVecs = self.__inpRowsMatrix.getNpColByIndex(0)
        yInpVecs = self.__inpRowsMatrix.getNpColByIndex(1)
        zInpVecs = self.__inpRowsMatrix.getNpColByIndex(2)
        ax.scatter(xInpVecs, yInpVecs, zInpVecs, c='lightblue', marker='.', alpha=0.04, linewidth=5)

        #nodes
        xNodes = self.__graph.getNpNodesComponentsByIndex(0)
        yNodes = self.__graph.getNpNodesComponentsByIndex(1)
        zNodes = self.__graph.getNpNodesComponentsByIndex(2)
        ax.scatter(xNodes, yNodes, zNodes, marker='*', s=200,c='red')

        #Edges
        for edge in self.__graph.getEdges():
            edgeNode1 = edge.getNode1()
            edgeNode2 = edge.getNode2()
            xVals = [edgeNode1.getRefVec().getComponentByIndex(0), edgeNode2.getRefVec().getComponentByIndex(0)]
            yVals = [edgeNode1.getRefVec().getComponentByIndex(1), edgeNode2.getRefVec().getComponentByIndex(1)]
            zVals = [edgeNode1.getRefVec().getComponentByIndex(2), edgeNode2.getRefVec().getComponentByIndex(2)]
            ax.plot(xVals, yVals,zVals, linewidth=7)


        pyplot.show()