from cluster.gng.Gng import Gng
from cluster.gng.PlotBuilder import PlotBuilder
from ctumrs.topics.ThreeDPosVelFile import ThreeDPosVelFile

# LOADING THE DATA TO CLUSTER #################################################


# Positional data
fileDataBank = "/home/donkarlo/Dropbox/projs/research/data/self-aware-drones/ctumrs/two-step/manip/pos-vel-obs-from-gps.txt"
t3dposVel = ThreeDPosVelFile(fileDataBank)
inputNpMatrix = t3dposVel.getNpArr(5000)

gng = Gng(inputNpMatrix, maxNodesNum=33)
gng.getClusters()
plotBuilder = PlotBuilder(gng.getMatrixInpVecs(), gng.getGraph())
plotBuilder.plot2d()