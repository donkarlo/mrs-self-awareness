import unittest
from typing import List

from mmath.data.cluster.gng.graph.Node import Node
from mmath.linearalgebra.Vector import Vector
from test.GraphBuilder import GraphBuilder


class TestGraph(unittest.TestCase):
    def test_getNewNodeUniqueId(self):
        ''''''
        graphMaker = GraphBuilder()
        newNode = Node(Vector([1,4,8]),0)
        graphMaker.graph.addNode(newNode)
        otherNodIds = [graphMaker.node1.getId(),graphMaker.node2.getId(),graphMaker.node3.getId()]
        self.assertFalse(newNode.getId() in otherNodIds)

    def test_getNeighbouringNodes(self):
        ''''''
        graphMaker = GraphBuilder()
        neiboursOfNode1:List[Node] = graphMaker.graph.getNeighbouringNodes(graphMaker.node1)
        self.assertTrue(len(neiboursOfNode1)==2)
        self.assertTrue(graphMaker.graph.isNodeInNodes(graphMaker.node2,neiboursOfNode1) and graphMaker.graph.isNodeInNodes(graphMaker.node3,neiboursOfNode1))
        self.assertFalse(graphMaker.graph.isNodeInNodes(graphMaker.node1,neiboursOfNode1))

    def test_getEdges(self):
        ''''''
        graphBuilder = GraphBuilder()
        edgesOfNode1 = graphBuilder.graph.getNodeEdges(graphBuilder.node3)

        edgeCounter = 0
        for edge in edgesOfNode1:
            edgeCounter += 1
        self.assertTrue(edgeCounter == 3)


if __name__ == '__main__':
    unittest.main()
