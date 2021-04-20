import uuid
from random import choice
from typing import List

import numpy as np

from mmath.data.cluster.gng.graph.Edge import Edge
from mmath.data.cluster.gng.graph.Node import Node


class Graph:
    ''''''

    def __init__(self
                 , nodes: List[Node] = None
                 , edges: List[Edge] = None):
        ''''''
        self.__nodes = nodes if nodes is not None else []
        self.__edges = edges if edges is not None else []

    def addNode(self, node: Node) -> None:
        ''''''
        nodeId = self.__getNewNodeUniqueId()
        node.updateId(nodeId)
        self.__nodes.append(node)

    def __getNewNodeUniqueId(self) -> uuid.UUID:
        return uuid.uuid1()

    def addEdge(self, edge: Edge) -> None:
        if edge.getNode1().getId() == edge.getNode2().getId():
            raise Exception("edge has same nodes on both sides")

        if not self.edgeExists(edge.getNode1(), edge.getNode2()):
            self.__edges.append(edge)

    def edgeExists(self, node1, node2) -> bool:
        if self.getEdgeBetweenTwoNodes(node1, node2) is None:
            return False
        else:
            return True

    def removeEdge(self, edge: Edge) -> None:
        ''''''
        edgeCounter = 0
        for loopingEdge in self.__edges:
            if edge.getNode1().getId() == loopingEdge.getNode1().getId() and edge.getNode2().getId() == loopingEdge.getNode2().getId():
                del self.__edges[edgeCounter]
            elif edge.getNode2().getId() == loopingEdge.getNode1().getId() and edge.getNode1().getId() == loopingEdge.getNode2().getId():
                del self.__edges[edgeCounter]
            edgeCounter += 1

    def removeEdgeBetweenTwoNodes(self, node1: Node, node2: Node):
        edge: Edge = self.getEdgeBetweenTwoNodes(node1, node2)
        self.removeEdge(edge)

    def removeNode(self, node: Node) -> None:
        ''''''
        # first remove edges from that node
        self.removeEdgeByNode(node)

        nodeCounter = 0
        for loopingNode in self.__nodes:
            if node.getId() == loopingNode.getId():
                del self.__nodes[nodeCounter]
            nodeCounter += 1

    def removeEdgeByNode(self, node: Node) -> None:
        ''''''
        edgeCounter = 0
        for loopingEdge in self.__edges:
            if loopingEdge.getNode1().getId() == node.getId() or loopingEdge.getNode2().getId() == node.getId():
                del self.__edges[edgeCounter]
            edgeCounter += 1

    def getNeighbouringNodes(self, node: Node) -> List[Node]:
        ''''''
        neighborNodes = []
        for edge in self.__edges:
            if node.getId() == edge.getNode1().getId():  # if given node's id matches one side of the edge's node
                if not self.isNodeInNodes(edge.getNode2(), neighborNodes):  # to make sure it is unique
                    neighborNodes.append(edge.getNode2())  # put the other side's node in neigbouring nodes list
            elif node.getId() == edge.getNode2().getId():  # if given node's id matches one side of the edge's node
                if not self.isNodeInNodes(edge.getNode1(), neighborNodes):  # to make sure it is unique
                    neighborNodes.append(edge.getNode1())  # put the other side's node in neigbouring nodes list
        if (len(neighborNodes) > 0):
            return neighborNodes
        return None

    def isNodeInNodes(self, node: Node, givenNodes: List[Node]) -> bool:
        ''''''
        for givenNode in givenNodes:
            if (givenNode.getId() == node.getId()):
                return True
        return False

    def getNodeEdges(self, node: Node) -> List[Edge]:
        foundEdges = []
        for edge in self.__edges:
            if edge.hasNode(node):
                foundEdges.append(edge)
        if len(foundEdges) == 0:
            return None
        else:
            return foundEdges

    def getEdgeBetweenTwoNodes(self, node1: Node, node2: Node) -> Edge:
        ''''''
        for edge in self.__edges:
            if edge.getNode1().getId() == node1.getId() and edge.getNode2().getId() == node2.getId():
                return edge
            elif edge.getNode1().getId() == node2.getId() and edge.getNode2().getId() == node1.getId():
                return edge
        return None

    def getEdges(self) -> List[Edge]:
        return self.__edges

    def getNodes(self) -> List[Node]:
        return self.__nodes

    def getNodeByIndex(self, index) -> Node:
        ''''''
        return self.__nodes[index]

    def getNodeById(self, id: int) -> Node:
        if self.__nodes is not None:
            for node in self.__nodes:
                if node.getId() == id:
                    return node
        return None

    def getRandomNode(self):
        ''''''
        return choice(self.__nodes)

    def getNodeWithLargestError(self) -> Node:
        ''''''
        return self.getNodeWithLargestErrorAmongGivenNodes(self.__nodes)

    def getNeighbouringNodeWithLargestError(self, node: Node) -> Node:
        ''''''
        neihbours = self.getNeighbouringNodes(node)
        return self.getNodeWithLargestErrorAmongGivenNodes(neihbours)

    def getNodeWithLargestErrorAmongGivenNodes(self, givenNodes: List[Node]) -> Node:
        ''''''
        nodeWithLargestError: Node = None
        if givenNodes is not None:
            for node in givenNodes:
                if nodeWithLargestError is None or node.getError() > nodeWithLargestError.getError():
                    nodeWithLargestError = node
        return nodeWithLargestError

    def removeEdgelessNodes(self) -> None:
        ''''''
        for node in self.getNodes():
            edges = self.getNodeEdges(node)
            if edges is None:
                self.removeNode(node)

    def getEdgelessNodes(self):
        ''''''
        edglessNodes: List[Node] = None
        allNodeIds = [node.getId() for node in self.__nodes]
        for node in self.__nodes:
            for edge in self.__edges:
                if edge.getNode1().getId() == node.getId() or edge.getNode2().getId() == node.getId():
                    if not node.getId() in allNodeIds:
                        edglessNodes.append(node)
        return edglessNodes

    def getNodesNum(self) -> int:
        ''''''
        if self.__nodes is not None:
            return len(self.__nodes)
        else:
            return 0

    def getEdgesNum(self):
        ''''''
        if self.__edges is not None:
            return len(self.__edges)
        else:
            return 0

    def getNpNodesComponentsByIndex(self, componentIndex: int):
        ''''''
        colData = []
        for node in self.getNodes():
            colData.append(node.getRefVec().getComponentByIndex(componentIndex))
        npCol = np.asarray(colData)
        return npCol

    def printNodes(self):
        print("Nodes reference vectors are as follows:")
        for node in self.__nodes:
            print(node.getRefVec().getNpRows())

    def report(self):
        self.printNodes()
        print("Number of clusters/nodes: " + str(self.getNodesNum()))
        print("Number of edges: " + str(self.getEdgesNum()))