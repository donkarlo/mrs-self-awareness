from typing import List, Tuple
import numpy as np

class Builder:
    def __init__(self):
        pass

    def uniform(self, min, max, samplesNum)->List[float]:
        """Return a random number between min_ and max_ ."""
        return np.random.uniform(min,max,samplesNum)


    def zipTolist(self,zipData)->List:
        return [list(a) for a in zipData]

    def circumferenceDistribution(self,center:List[float], radius:float, samplesNum:int):
        """Return n random points uniformly distributed on a circumference."""
        phi = self.uniform(0, 2 * np.math.pi, samplesNum)
        x = [radius * np.math.cos(point)+ center[0] for point in phi]
        y = [radius * np.math.sin(point)+ center[1] for point in phi]
        return self.zipTolist(zip(x,y))


    def circleDistribution(self,center:List[float], radius:float, nSamples:int):
        """Return n random points uniformly distributed on a circle."""
        phi = self.uniform(0, 2 * np.math.pi, nSamples)
        sqrt_r = [np.math.sqrt(point) for point in self.uniform(0, radius * radius, nSamples)]
        x = [sqPoint* np.math.cos(phiPoint)+center[0] for sqPoint,phiPoint in zip(sqrt_r,phi)]
        y = [sqPoint* np.math.sin(phiPoint)+center[1] for sqPoint,phiPoint in zip(sqrt_r,phi)]
        return self.zipTolist(zip(x, y))


    def rectangleDistribution(self,center, w, h, n):
        """Return n random points uniformly distributed on a rectangle."""
        x = [point[0] + center[0] for point in self.uniform(-w / 2., w / 2., (n, 1))]
        y = [point[0] + center[1] for point in self.uniform(-h / 2., h / 2., (n, 1))]
        return self.zipTolist(zip(x, y))

    def getAllPoints(self):

        samplesNum = 2000

        cf1 = self.circumferenceDistribution([6, -0.5], 2, samplesNum)
        cf2 = self.circumferenceDistribution([3, -2], 0.3, samplesNum)

        cl1 = self.circleDistribution([-5, 3], 0.5, int(samplesNum / 2))
        cl2 = self.circleDistribution([3.5, 2.5], 0.7, samplesNum)
        #
        # #four sides of a rectangle
        r1 = self.rectangleDistribution([-1.5, 0], 1, 4, samplesNum)
        r2 = self.rectangleDistribution([+1.5, 0], 1, 4, samplesNum)
        r3 = self.rectangleDistribution([0, +1.5], 2, 1, int(samplesNum / 2))
        r4 = self.rectangleDistribution([0, -1.5], 2, 1, int(samplesNum / 2))


        allPoints = np.asarray(cf1+cf2+cl1+cl2+r1+r2+r3+r4)

        return allPoints