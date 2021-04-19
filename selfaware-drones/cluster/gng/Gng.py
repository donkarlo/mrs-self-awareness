import numpy as np

from cluster.ClusteringStrgy import ClusteringStrgy
from cluster.gng.AdaptationPhase import AdaptationPhase
from cluster.gng.graph.Edge import Edge
from cluster.gng.graph.Graph import Graph
from cluster.gng.GrowingPhase import GrowingPhase
from cluster.gng.graph.Node import Node
from mmath.linearalgebra.Matrix import Matrix
from mmath.linearalgebra.Vector import Vector


class Gng(ClusteringStrgy):
    '''Find how GNG works in AdaptationPhase and GrowingPhase'''

    def __init__(self,
                 rawInputData,
                 maxNodesNum: int = 100,
                 maxAge: int = 100,
                 maxIterationsNum: int = 300,  # landa
                 localErrorDecayRate: float = 0.5,  # alpha
                 globalErrorDecayRate: float = 0.0005,  # beta
                 closestNodeMovementRateTowardCurInpVec: float = 0.05,  # eW
                 connectedNodesToClosestNodeMovementRateTowardCurInpVec: float = 0.0006  # eN
                 ):
        '''
        Parameters
        ----------
        rawInputData:np.array
        maxIterationsNum:int
        maxAge:int
        maxNodesNum:int
        alpha:
            local error decay rate.
        beta:
            global error decay rate.
        eW:
            winner node movement rate. normal valu =e is 0.05 and values greater than 0.3 are small and nodes in
            unstable graph.(e is abbr for epsilon)
        eN:
            neigbours of winner node movement rate, it must be much smaller than eW. should be one to tow orders of
            magnitude smaller than 0.0006
        '''
        # super().__init__(rawInputData)
        self.__inpVecs: Matrix = rawInputData
        self.__closestNodeMovementRateTowardCurInpVec: float = closestNodeMovementRateTowardCurInpVec
        self.__neighborNodesOfClosestNodeMovementRateTowardCurInpVec: float = connectedNodesToClosestNodeMovementRateTowardCurInpVec
        self.__maxAge: int = maxAge
        self.__maxIterationsNum: int = maxIterationsNum
        self.__maxNodesStepNum: int = maxNodesNum
        self.__iterationCounter: int = 0
        self.__localErrorDecayRate: float = localErrorDecayRate
        self.__globalErrorDecayRate: float = globalErrorDecayRate
        self._clusters = None
        self.__graph: Graph = Graph()
        self.__adaptationPhase = None
        self.__growingPhase = None

    def _doSetClusters(self) -> None:
        ''''''
        self.__prepareData()
        self.__initializePhases()
        self.__initializeTheFirstTwoNodes()
        self.__runPhases()
        self.__report()

    def __prepareData(self)->None:
        ''''''
        self.__convertInputDataToNpMatrix()
        np.random.shuffle(self.__inpVecs)
        self.__normalizeInpVecs()
        self.__convertInpVecsToMatrix()

    def __initializePhases(self)->None:
        ''''''
        self.__adaptationPhase: AdaptationPhase = AdaptationPhase(self.__inpVecs
                                                                  , self.__graph
                                                                  , self.__closestNodeMovementRateTowardCurInpVec
                                                                  ,self.__neighborNodesOfClosestNodeMovementRateTowardCurInpVec
                                                                  , self.__maxAge)
        self.__growingPhase: GrowingPhase = GrowingPhase(self.__graph
                                                         , self.__localErrorDecayRate
                                                         , self.__globalErrorDecayRate)
    def __initializeTheFirstTwoNodes(self) -> None:
        '''Create two randomly positioned nodes, name them s(the winner node which is closer to bar(x)) and r '''
        node1RefVec: Vector = Vector(np.random.rand(self.__inpVecs.getColsNum(), 1))
        node1 = Node(node1RefVec, 0)
        self.__graph.addNode(node1)

        node2RefVec: Vector = Vector(np.random.rand(self.__inpVecs.getColsNum(), 1))
        node2 = Node(node2RefVec, 0)
        self.__graph.addNode(node2)

        edgeNode1Node2: Edge = Edge(node1, node2, 0)
        self.__graph.addEdge(edgeNode1Node2)

    def __runPhases(self)->None:
        # stop condition
        # todo make it a function can be based on performance
        while self.__graph.getNodesNum() < self.__maxNodesStepNum:
            print("Nodes num so far: " + str(self.__graph.getNodesNum()))
            self.__adaptationPhase.run()
            if (self.__iterationCounter / self.__maxIterationsNum) == 1:
                self.__growingPhase.run()
                print("Growing counter so far: " + str(self.__growingPhase.getRunCounter()))
                self.__iterationCounter = 0
            self.__iterationCounter += 1
        self._clusters = self.__graph.getNodes()



    def __report(self)->None:
        ''''''
        print("Ran with success")
        print("Nodes num " + str(self.__graph.getNodesNum()))
        print("Edge num " + str(self.__graph.getEdgesNum()))
        print ("Adaptation run num "+str(self.__graph.getEdgesNum()))

    def __convertInpVecsToMatrix(self) -> None:
        ''''''
        self.__inpVecs = Matrix(self.__inpVecs)

    def __convertInputDataToNpMatrix(self) -> np.array:
        ''''''
        self.__inpVecs = np.asarray(self.__inpVecs)

    def __normalizeInpVecs(self) -> None:
        '''Normalization of the input data'''
        # Extract minimum of each row
        minOfRowsArr = np.min(self.__inpVecs, axis=0)
        # Construct an array by repeating A the number of times given by reps.
        # shape[0] gives the number of rows
        # tile: repeat array of minimums of each row one time along columns (axe1) and number of rows times of minOfRowsArr along rows(axe0)
        dataNorm = self.__inpVecs - np.tile(minOfRowsArr, (self.__inpVecs.shape[0], 1))
        maxDataNorm = np.max(dataNorm, axis=0)
        self.__inpVecs = dataNorm / np.tile(maxDataNorm, (self.__inpVecs.shape[0], 1))

    def getMatrixInpVecs(self) -> Matrix:
        ''''''
        return self.__inpVecs

    def getGraph(self) -> Graph:
        ''''''
        return self.__graph
