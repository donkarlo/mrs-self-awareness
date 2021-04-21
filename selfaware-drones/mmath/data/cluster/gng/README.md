#Growing Neural Gas
* Growing Neural Gas(GNG) is an incremental clustering algorithm called Growing Neural Gas (GNG) by Bernd Fritzke. See Refernces[[1]](#1).
* GNG works by forming a cometion between the two following phases:
  * After initialization, which
places two randomly generated nodes into a network, two
main phases are alternating until a selected stopping crite-
rion is met. The first phase (“self-organizing”) is adapta-
tion, which is performed in λ steps. In each step, random
input signal is generated and the neural network adapts
itself to it: a connection between two nodes nearest to the
input signal is strengthened (or created if it does not ex-
ist), then the nearest node and all its topological neighbors
(nodes connected directly to the node by an edge) move
towards the input signal and the nearest node’s error is
increased. This helps to identify areas where nodes are
not sufficiently adapted to input signals. After that, the
aging mechanism of edges is triggered – those edges that
were not strengthened for a long time (the age of the edge
is higher than A max ) are removed from the network. In
the last step of the adaptation, an error of each node is
decreased. Using this mechanism the neural network “for-
gets” old errors and thus it can focus on the most recent
ones.
  * In the second phase (“growing”), a new node is created
and connected into the network. The node’s error is used
for an identification of the area where the adaptation was
least successful – the node with the largest error and its
neighbor with the largest error are found. A new node is
created at the halfway between them. The errors of those
nodes are decreased.

### Quick start
* Stars represent nodes reference vectors and colored edges represent the edges
* Example with 2D plot.
  * Find and run this example in mmath/data/cluster/gng/examples/FiveUniformShapes/Cluster.py
  ```
  from mmath.data.cluster.gng.Gng import Gng
  from mmath.data.cluster.gng.PlotBuilder import PlotBuilder
  from mmath.data.cluster.gng.examples.FiveUniformShapes.Builder import Builder
  from mmath.linearalgebra.Matrix import Matrix
  
  # A class to generate cloud data points for 5 shapes
  shapeBuilder:Builder = Builder()
  allPoints:np.ndarray = shapeBuilder.getAllPoints()
  
  # allPoints is of type np.ndarray, convert it to Matrix
  inpRowsMatrix:Matrix = Matrix(allPoints)
  #For the settings see GNG.__init__() parameters
  gng:Gng = Gng(inpRowsMatrix,maxNodesNum=150)
  nodes:List[Node] = gng.getClusters()
  gng.getGraph().report()
  plotter = PlotBuilder(gng.getInpRowsMatrix(),gng.getGraph())
  plotter.showAll2D()
![2D presentation of 2D data](https://raw.githubusercontent.com/donkarlo/mrs-self-awareness/master/docs/assets/gng-samples/five-random-unified-shapes.png)

* Example with 3D Plot
* Find and run this example in mmath/data/cluster/gng/examples/FiveUniformShapes/Trajectory.py
* Download and replace fileDataBank value with the file in https://www.dropbox.com/s/8i9gwm4ku4pcyu7/pos-vel-obs-from-gps.txt?dl=0 or create a similar file with same entries and then set inputNpMatrix with a Matrix which recieves np.ndarrays of 6 dimentional rows  
  ```
  from mmath.data.cluster.gng.Gng import Gng
  from mmath.data.cluster.gng.PlotBuilder import PlotBuilder
  from ctumrs.topics.ThreeDPosVelFile import ThreeDPosVelFile
  from mmath.linearalgebra.Matrix import Matrix
  
  class TrajectoryExample:
      def run(self):
          # Positional data
          fileDataBank = "/path/to/data"
          t3dposVel = ThreeDPosVelFile(fileDataBank)
          inputNpMatrix = Matrix(t3dposVel.getNpArr(5000))
  
          gng = Gng(inputNpMatrix, maxNodesNum=33)
          gng.getClusters()
          gng.getGraph().report()
  
          plotBuilder = PlotBuilder(gng.getInpRowsMatrix(), gng.getGraph())
          plotBuilder.showAll3D()
  
  te = TrajectoryExample()
  te.run()
![3D presentation of 6D data](https://raw.githubusercontent.com/donkarlo/mrs-self-awareness/master/docs/assets/gng-samples/drone-two-step-5000-points-100-nodes.png)


### Interface (Only most important methods. For details see the classes themselves)

* Gng class
  ```
  # rawData can be a list or an np.ndarray
  dataMatrix:Matrix = Matrix(rawData)
  #For other settings see __init__ of Gng 
  gng:Gng = Gng(dataMatrix)
  # Finds and returns back a list of nodes. Always call first
  nodes:List[Node] = gng.getClusters()
  # Returns the the formed Graph
  graph:Graph = gng.getGraph()
  
* Graph class
  ```
  #To get the list of found nodes
  nodes:List[Node] = graph.getNodes()
  # Get final number of nodes
  nodesNum:int = graph.getNodesNum()
  
  #Get list of formed edges between nodes
  edges:List[Edge] = graph.getEdges()
  #Get final number of edges
  edgesNum:int = graph.getEdgesNum()
  
  #Print nodes with their reference vectors and number of found nodes and existing edges
  graph.report()
  
  #get two random nodes
  node:Node = graph.getRandomNode()
  anotherNode:Node = graph.getRandomNode()
  
  #get the edge between two given nodes, FROM HERE, LETS HOPE THERE IS AN EDGE BETWEEN THESE TWO RANDOM NODES :)
  if(graph.edgeExists(node,anotherNode)):
    edge:Edge = graph.getEdgeBetweenTwoNodes(node,anotherNode)
  
  # get all nodes which are connected to given node by an edge
  neigbourNodes:List[Node] = graph.getNeighbouringNodes(node)
  
  nodeEdges:List[Node] = graph.getNodeEdges(node)
  
* Most usefull Node class methods
  ```
  # get the vector which represents the class
  node.getRefVec()
  node.getError()
  
* Most usefull Edge class methods
  ```
  
  #Each edge is formed of two nodes and an age
  edge.getAge()
  edge.getNode1()
  edge.getNode2()
  
* PlotBuilder
  ```
  pltBld = PlotBuilder(dataMatrix,graph)
  # 2D

### Code methodology
mmath.data.cluster.gng.GNG class inherits mmath.data.cluster.gng.ClusteringStrgy class which enforces it to implement _doSetClusters method which will be used by its getClusters method  to either to compute and return back the found clusters if its the first run or just return back without re-execution of the process.
* Calling GNG.getClusters() results in calling GNG._runPhases which first intializes the GNG's graph object with two nodes and an edge between them (by calling gng.__initializeTheFirstTwoNodes) and then calls AdaptationPhase.run or GrowingPhase.run. It is the competition between the later two methods which gradually forms the graph.

### Extension 
* As mentioned in Code methodology section it would be nice if any extension inherits class GNG and overrides GNG._initializeTheFirstTwoNodes, GNG.__runPhases, AdaptationPhase.run or GrowingPhase.run methods.
* Please don't hesitate to extend the code or distribute it. It would be nice if you follow these rules in your extenstions 
  * Please see todo section to have some ideas on what is yet planned to be developed
  * All class attributes and methods starting with __ are considered 
  private and better not to be accessed outside the class.
  * All class attributes and methods starting with _ should be considered 
  protected members and better not be accessed outside the class hierarchy.
  * Any extention of Gng class should inherit from Gng class and override ClusteringStrgy._doSetClusters method
  * Please, develop the unit test simultaneously in test directory 
  * Please use numpydoc to for documenting the code


### Unit testing
* Please, please! develop the unit test simultaneously.
* Please use unittest
* All unit tests are in /test
* run the following to check all automated test
  > python -m unittest

###Benchmarks
See 

###Todo
* GNG:
  * GNG-U implementation
  * Supervised GNG implemetation
  * Developing a solution to find optimized configuration values for Gng parameters
* Graph related:
  * Implementing number of disconnected areas
* Plotting:
  * Adding more configurationsuch as color 
  * Animated plotting
  * Selective components for Graph.PlotBuilder
  * Color data points closest to a node's reference vector with the same color
* Performance:
  * It seems that Graph's methods related to searching for nodes and edges can be improved
* Test:
  * Writing more tests and modify differnt classes such that they are more test friendly
* Documentation: 
  * Developping numpydoc style documentation for all the code
  
###References
<a id="1">[1]</a> 
Bernd Fritzke. 1994. A growing neural gas network learns topologies. In Proceedings of the 7th International Conference on Neural Information Processing Systems (NIPS'94). MIT Press, Cambridge, MA, USA, 625–632.

