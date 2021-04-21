import unittest
from unittest import TestCase

from mmath.data.cluster.gng.graph.PlotBuilder import PlotBuilder


class TestPlot(TestCase):
    def test_visual(self):
        myPltTest = PlotBuilder()
        myPltTest.add2DNodes()
        myPltTest.add2DEdges()
        myPltTest.show()
if __name__ == '__main__':
    unittest.main()