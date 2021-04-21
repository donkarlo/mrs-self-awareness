from random import sample
from typing import List

from mmath.data.cluster.gng.RunableInterface import RunableInterface
from mmath.data.cluster.gng.graph.Edge import Edge
from mmath.data.cluster.gng.graph.Graph import Graph
from mmath.data.cluster.gng.graph.Node import Node
from mmath.linearalgebra.Matrix import Matrix
from mmath.linearalgebra.Vector import Vector


class AdaptationPhase(RunableInterface):
    def __init__(self
                 , inpVecs: Matrix
                 , graph: Graph
                 , closestNodeMovementRateTowardCurInpVec: float
                 , connectedNodesToClosestNodeMovementRateTowardCurInpVec: float
                 , maxAge: int):
        # setting Vars
        self.__maxAge: int = maxAge
        self.__closestNodeMovementRateTowardCurInpVec: float = closestNodeMovementRateTowardCurInpVec
        self.__neighborNodesOfClosestNodeMovementRateTowardCurInpVec: float = connectedNodesToClosestNodeMovementRateTowardCurInpVec

        # Gloabal vars
        self.__graph: Graph = graph
        self.__inpVecs: Matrix = inpVecs
        self.__closestNodeToCurInpVec: Node = None
        self.__secondClosestNodeToCurInpVec: Node = None
        self.__curInpVecIndex: int = None
        self.__curInpVec: Vector = None
        self.__selectedCurInptVecIndexes: List[int] = None
        self.__runCounter = 0

    def run(self) -> None:
        self.__runCounter += 1
        self.__setCurInpVec()
        self.__setTwoNearestNodesToCurInpVec()
        self.__updateCurClosestNodeLocalError()
        self.__moveClosestNodeTowardCurInpVec()
        self.__moveNeigboursOfClosestNodeTowardCurInpVec()
        self.__incrementAgesOfNeigboursOfCurClosestNode()
        self.__manageEdgeBetweenTheTwoNearestNodes()
        self.__removeOldEdges()
        self.__graph.removeEdgelessNodes()

    def getRunCounter(self):
        return self.__runCounter

    def __setCurInpVec(self) -> None:
        ''' bar(x)
        '''
        if self.__selectedCurInptVecIndexes is None:
            self.__selectedCurInptVecIndexes = []

        allIndexesSet = set(list(range(1, self.__inpVecs.getRowsNum())))
        self.__curInpVecIndex = sample(allIndexesSet, 1)[0]
        self.__curInpVec: Vector = Vector(self.__inpVecs.getNpRowByIndex(self.__curInpVecIndex))
        self.__selectedCurInptVecIndexes.append(self.__curInpVecIndex)

    def __setTwoNearestNodesToCurInpVec(self) -> None:
        ''''''
        self.__graph.getNodes().sort(key=lambda node: self.__curInpVec.getDistanceFrom(node.getRefVec()))
        self.__closestNodeToCurInpVec = self.__graph.getNodeByIndex(0)
        self.__secondClosestNodeToCurInpVec = self.__graph.getNodeByIndex(1)

    def __updateCurClosestNodeLocalError(self) -> None:
        ''''''
        newError = self.__closestNodeToCurInpVec.getError() + \
                   self.__curInpVec.getDistanceFrom(self.__getClosestNodeToCurInpVec().getRefVec())
        self.__getClosestNodeToCurInpVec().updateError(newError)

    def __getClosestNodeToCurInpVec(self) -> Node:
        ''''''
        if self.__closestNodeToCurInpVec is None:
            self.__setTwoNearestNodesToCurInpVec()
        return self.__closestNodeToCurInpVec

    def __getSecondClosestNodeToCurInpVec(self) -> Node:
        ''''''
        if self.__secondClosestNodeToCurInpVec is None:
            self.__setTwoNearestNodesToCurInpVec()
        return self.__secondClosestNodeToCurInpVec

    def __moveClosestNodeTowardCurInpVec(self) -> None:
        ''''''
        self.__moveNodeTowardCurInpVec(self.__getClosestNodeToCurInpVec()
                                       , self.__closestNodeMovementRateTowardCurInpVec)

    def __moveNeigboursOfClosestNodeTowardCurInpVec(self) -> None:
        ''''''
        if self.__graph.getNeighbouringNodes(self.__getClosestNodeToCurInpVec()) is not None:
            for neigbourNode in self.__graph.getNeighbouringNodes(self.__getClosestNodeToCurInpVec()):
                self.__moveNodeTowardCurInpVec(neigbourNode,
                                               self.__neighborNodesOfClosestNodeMovementRateTowardCurInpVec)

    def __moveNodeTowardCurInpVec(self, node: Node, rate: float) -> None:
        ''''''
        newVec:Vector = node.getRefVec() + (self.__curInpVec - node.getRefVec())*rate
        node.updateRefVec(newVec)

    def __incrementAgesOfNeigboursOfCurClosestNode(self) -> None:
        ''''''
        if self.__graph.getNodeEdges(self.__getClosestNodeToCurInpVec()) is not None:
            for edge in self.__graph.getNodeEdges(self.__getClosestNodeToCurInpVec()):
                newAge = edge.getAge() + 1
                edge.updateAge(newAge)

    def __manageEdgeBetweenTheTwoNearestNodes(self) -> None:
        ''''''
        edge: Edge = self.__graph.getEdgeBetweenTwoNodes(self.__getClosestNodeToCurInpVec(),
                                                         self.__getSecondClosestNodeToCurInpVec())
        if edge is not None:
            edge.updateAge(0)
        elif edge is None:
            edge = Edge(self.__getClosestNodeToCurInpVec(), self.__getSecondClosestNodeToCurInpVec(), 0)
            self.__graph.addEdge(edge)

    def __removeOldEdges(self) -> None:
        ''''''
        for edge in self.__graph.getEdges():
            if edge.getAge() > self.__maxAge:
                self.__graph.removeEdge(edge)
