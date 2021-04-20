import unittest
from unittest import TestCase

from mmath.data.cluster.gng.Gng import Gng
from ctumrs.topics.ThreeDPosVelFile import ThreeDPosVelFile


class TestGng(TestCase):
    # shared with all TestGng
    fileDataBank = "/home/donkarlo/Dropbox/projs/research/data/self-aware-drones/ctumrs/two-step/manip/pos-vel-obs-from-gps.txt"
    t3dposVel = ThreeDPosVelFile(fileDataBank)
    inputNpMatrix = t3dposVel.getNpArr(1000)
    gng = Gng(inputNpMatrix, maxNodesNum=30)
    gng.getClusters()
    graph = gng.getGraph()

    # def test_noEdglessNodesLeft(self):
    #     ''''''
    #     self.assertTrue(self.gng.getGraph().getEdgelessNodes() is None)
    #
    # def test_nodelessEdges(self):
    #     ''''''
    #     for edge in self.graph.getEdges():
    #         self.assertTrue(edge.getNode1() is not None and edge.getNode2() is not None)


if __name__ == '__main__':
    unittest.main()
