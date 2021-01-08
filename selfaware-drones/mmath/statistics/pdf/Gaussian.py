import math
class Gaussian():
    def __init__(self, mean:float, standardDeviation:float):
        self.__mean = mean
        self.__standardDeviation = standardDeviation
        pass

    def getValue(self,x:float):
        y = (1/(self.__standardDeviation*math.sqrt(2*math.pi)))*math.e**(-(x-self.__mean)**2/(2*self.__standardDeviation**2))
        return y