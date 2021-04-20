from mmath.data.cluster.gng.graph.Node import Node


class Edge:
    def __init__(self, node1: Node, node2: Node, age: int = 0):
        ''''''
        self.__age = age
        self.__node1 = node1
        self.__node2 = node2

    def getNode1(self) -> Node:
        return self.__node1

    def getNode2(self) -> Node:
        return self.__node2

    def getAge(self) -> int:
        return self.__age

    def hasNode(self, node: Node) -> bool:
        '''if the edge has the given node'''
        if self.__node1.getId() == node.getId() or self.__node2.getId() == node.getId():
            return True
        return False

    def updateAge(self, updatedAge: int) -> None:
        self.__age = updatedAge
