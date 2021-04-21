import matplotlib.pyplot as plt

from mmath.data.cluster.gng.graph.Graph import Graph
from mmath.test.GraphBuilder import GraphBuilder


class PlotBuilder:
    def __init__(self, graph: Graph = None)->None:
        if graph is None:
            self.__graph = GraphBuilder().getGraph()
        else:
            self.__graph = graph


    def add2DNodes(self)->None:
        xNodes = self.__graph.getNpNodesComponentsByIndex(0)
        yNodes = self.__graph.getNpNodesComponentsByIndex(1)
        plt.scatter(xNodes, yNodes, marker='*')

    def add2DEdges(self)->None:
        ''''''
        for edge in self.__graph.getEdges():
            edgeNode1 = edge.getNode1()
            edgeNode2 = edge.getNode2()
            xVals = [edgeNode1.getRefVec().getComponentByIndex(0), edgeNode2.getRefVec().getComponentByIndex(0)]
            yVals = [edgeNode1.getRefVec().getComponentByIndex(1), edgeNode2.getRefVec().getComponentByIndex(1)]
            plt.plot(xVals, yVals)

    def show(self)->None:
        ''''''
        plt.show()

    def getPlot(self)->plt:
        ''''''
        return plt
