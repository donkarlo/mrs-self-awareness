from typing import List

from mmath.data.cluster.gng.Runable import Runable
from mmath.data.cluster.gng.graph.Edge import Edge
from mmath.data.cluster.gng.graph.Graph import Graph
from mmath.data.cluster.gng.graph.Node import Node
from mmath.linearalgebra.Vector import Vector


class GrowingPhase(Runable):
    def __init__(self
                 , graph: Graph
                 , localErrorDecayRate
                 , globalErrorDecayRate):
        ''''''
        self.__graph = graph
        self.__globalErrorDecayRate = globalErrorDecayRate
        self.__localErrorDecayRate = localErrorDecayRate
        self.__runCounter = 0

    def run(self) -> None:
        ''''''
        self.__runCounter += 1
        self.__addNewNode()

    def getRunCounter(self) -> int:
        ''''''
        return self.__runCounter

    def __addNewNode(self) -> Node:
        # insert r betweeen u(node with largest error) and v(neighbor node with largest error), this should happen after one iteration
        # r
        nodeWithLargestError: Node = self.__graph.getNodeWithLargestError()

        # u, find the node with largest error
        nodeWithLargestErrorNeigbours: List[Node] = self.__graph.getNeighbouringNodes(nodeWithLargestError)
        neigbouringNodeWithLargestError: Node = self.__graph.getNodeWithLargestErrorAmongGivenNodes(
            nodeWithLargestErrorNeigbours)

        # Generating a new node
        newNodeRefVec: Vector = (nodeWithLargestError.getRefVec() + neigbouringNodeWithLargestError.getRefVec()) * 0.5
        newInsertedNodeBetween: Node = Node(newNodeRefVec, 0)
        self.__graph.addNode(newInsertedNodeBetween)

        # Mange edges between the new node and nodes with largest errors
        self.__graph.removeEdgeBetweenTwoNodes(nodeWithLargestError, neigbouringNodeWithLargestError)
        self.__graph.addEdge(Edge(newInsertedNodeBetween, nodeWithLargestError))
        self.__graph.addEdge(Edge(newInsertedNodeBetween, neigbouringNodeWithLargestError))

        # decrease the error variables of u and v
        nodeWithLargestError.updateError(self.__localErrorDecayRate * nodeWithLargestError.getError())
        neigbouringNodeWithLargestError.updateError(
            self.__localErrorDecayRate * neigbouringNodeWithLargestError.getError())

        # update r error with u
        newInsertedNodeBetween.updateError(nodeWithLargestError.getError())

        self.__decreaseErrorsGlobally()

    def __decreaseErrorsGlobally(self) -> None:
        ''''''
        for node in self.__graph.getNodes():
            node.updateError(node.getError() - self.__globalErrorDecayRate * node.getError())
