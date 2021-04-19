from cluster.gng.Gng import Gng
from cluster.gng.PlotBuilder import PlotBuilder
from ctumrs.topics.ThreeDPosVelFile import ThreeDPosVelFile


class TrajectoryExample:
    def run(self):
        # Positional data
        fileDataBank = "/home/donkarlo/Dropbox/projs/research/data/self-aware-drones/ctumrs/two-step/manip/pos-vel-obs-from-gps.txt"
        t3dposVel = ThreeDPosVelFile(fileDataBank)
        inputNpMatrix = t3dposVel.getNpArr(5000)

        gng = Gng(inputNpMatrix, maxNodesNum=20)
        gng.getClusters()
        gng.getGraph().report()

        plotBuilder = PlotBuilder(gng.getMatrixInpVecs(), gng.getGraph())
        plotBuilder.showAll3D()

te = TrajectoryExample()
te.run()