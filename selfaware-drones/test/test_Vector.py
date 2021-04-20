import unittest

import numpy as np

from mmath.linearalgebra.Vector import Vector


class TestVector(unittest.TestCase):
    def test_get_distance_from(self):
        vec1: Vector = Vector([1, 1, 1])
        vec2: Vector = Vector([2, 2, 2])
        self.assertTrue(vec1.getDistanceFrom(vec2) - np.sqrt(3) < 0.001)

    def test__sum__(self):
        vec1: Vector = Vector([1, 1, 1])
        vec2: Vector = Vector([2, 2, 2])
        sumVec = vec1 + vec2
        self.assertTrue(sumVec[0] == [3])

    def test__mul__(self):
        vec1: Vector = Vector([1, 2, 4])
        mulVec = vec1 * 0.5
        self.assertTrue(mulVec[2] == [2])

    def test_moveTowardVecByDistance(self):
        startVec:Vector = Vector([2,2])
        endVec:Vector = Vector([1,1])
        mvRate = 0.1
        startVec.moveTowardVecByRate(endVec, mvRate)
        print(startVec.getNpRows()[0][0])
        self.assertTrue(startVec.getNpRows()[0][0] == 2.1)



if __name__ == '__main__':
    unittest.main()
