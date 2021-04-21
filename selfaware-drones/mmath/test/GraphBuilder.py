from mmath.data.cluster.gng.graph.Edge import Edge
from mmath.data.cluster.gng.graph.Graph import Graph
from mmath.data.cluster.gng.graph.Node import Node
from mmath.linearalgebra.Vector import Vector


class GraphBuilder:

    def __init__(self):
        ''''''
        self.graph = Graph()
        self.node1: Node = Node(Vector([1, 4, 5]), 0)
        self.node2: Node = Node(Vector([5, 3, 1]), 0)
        self.node3: Node = Node(Vector([3, 6, 2]), 0)
        self.node4: Node = Node(Vector([6, 4, -1]), 0)
        self.graph.addNode(self.node1)
        self.graph.addNode(self.node2)
        self.graph.addNode(self.node3)
        self.graph.addNode(self.node4)

        self.edgeN1N2: Edge = Edge(self.node1, self.node2, 0)
        self.edgeN1N3: Edge = Edge(self.node1, self.node3, 0)
        self.edgeN2N3: Edge = Edge(self.node2, self.node3, 0)
        self.edgeN4N3: Edge = Edge(self.node4, self.node3, 0)

        self.graph.addEdge(self.edgeN1N2)
        self.graph.addEdge(self.edgeN1N3)
        self.graph.addEdge(self.edgeN2N3)
        self.graph.addEdge(self.edgeN4N3)

    def getGraph(self):
        return self.graph
