# About Growing Neural Gas

* GNG is an unsupervised application

# Dependencies, compilation and running (Debian-based OS)
* Python 3.5+
   ```
   $ sudo add-apt-repository ppa:deadsnakes/ppa
   $ sudo apt update
   $ sudo apt install python3.5
* numpy version 1.19.2
  
# Installation
* clone the project from the git repository or simply copy it to a directory such as /path/to/project
   ```
   $ git clone https://github.com/donkarlo/mrs-self-awareness

#Quick start
* Sample 
  ```
  shapeBuilder = Builder()
  allPoints = shapeBuilder.getAllPoints()
  inpRowsMatrix = Matrix(allPoints)
  gng = Gng(inpRowsMatrix,maxNodesNum=150)
  gng.getClusters()
  gng.getGraph().report()
  plotter = PlotBuilder(gng.getInpRowsMatrix(),gng.getGraph())
  plotter.showAll2D()

#interface
  $ gng.getClusters()->List[Node]
  $ https://github.com/donkarlo/mrs-self-awareness/tree/master/selfaware-drones/cluster

# Samples
Format: ![3D presentation of 6D data](https://www.dropbox.com/s/xapyq58jtdfbuge/drone-two-step-5000-points-100-nodes.png?dl=0)
Format: ![2D presentation of 2D data](https://www.dropbox.com/s/u3830gzooc7ednf/five-random-unified-shapes.png?dl=0)
# Todo
* Implementing number of disconnected areas
* CGNG implementation
* Supervised GNG