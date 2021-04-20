from mmath.data.cluster.gng.Gng import Gng
from mmath.data.cluster.gng.PlotBuilder import PlotBuilder
from ctumrs.topics.ThreeDPosVelFile import ThreeDPosVelFile
from mmath.linearalgebra.Matrix import Matrix


class TrajectoryExample:
    def run(self):
        # Positional data
        fileDataBank = "/home/donkarlo/Dropbox/projs/research/data/self-aware-drones/ctumrs/two-step/manip/pos-vel-obs-from-gps.txt"
        t3dposVel = ThreeDPosVelFile(fileDataBank)
        inputNpMatrix = Matrix(t3dposVel.getNpArr(5000))

        gng = Gng(inputNpMatrix, maxNodesNum=33)
        gng.getClusters()
        gng.getGraph().report()

        plotBuilder = PlotBuilder(gng.getInpRowsMatrix(), gng.getGraph())
        plotBuilder.showAll3D()

te = TrajectoryExample()
te.run()