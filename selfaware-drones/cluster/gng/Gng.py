import numpy as np
import matplotlib.pyplot as plt
import sklearn.metrics as metrics

class Gng:
    ''''''
    def __init__(self,
                 inputData,
                 maxNodeNum:int=100,
                 maxAge:int=100,
                 maxNumOfIterations:int=300,
                 alpha:float=0.5,
                 beta:float=0.0005,
                 eW:float=0.05,
                 eN:float=0.0006):
        '''
        Parameters
        ----------
        inputData:np.array
        maxNumOfIterations:int
        maxAge:int
        maxNodeNum:int
        alpha:
            local error decay rate.
        beta:
            global error decay rate.
        eW:
            winner node movement rate. normal valu =e is 0.05 and values greater than 0.3 are small and nodes in
            unstable graph.(e is abbr for epsilon)
        eN:
            neigbours of winner node movement rate, it must be much smaller than eW. should be one to tow orders of
            magnitude smaller than 0.0006
        '''
        self.__inputNpMatrix = self.__convertInputDataToNpMatrix(inputData)
        self.__normalizedInputNpMatrix = None
        self.__nodes = np.array
        self.__edges = np.array

    def getClustersNum(self):
        return len(self.__nodes)

    def getNormalizedNpMatrix(self) -> np.array:
        '''Normalization of the input data'''
        if(type(self.__normalizedInputNpMatrix) is not None):
            # Extract minimum of each row
            minOfRowsArr = np.min(self.__inputNpMatrix, axis=0)
            # Construct an array by repeating A the number of times given by reps.
            # shape[0] gives the number of rows
            # tile: repeat array of minimums of each row one time along columns (axe1) and number of rows times of minOfRowsArr along rows(axe0)
            dataNorm = self.__inputNpMatrix - np.tile(minOfRowsArr, (self.__inputNpMatrix.shape[0], 1))
            maxDataNorm = np.max(dataNorm, axis=0)
            self.__normalizedInputNpMatrix = dataNorm / np.tile(maxDataNorm, (self.__inputNpMatrix.shape[0], 1))
        return self.__normalizedInputNpMatrix

    def initialization(self):
        '''Two random nodes'''
        pass

    def selfOranizationPhase(self):
        '''Right after initialization'''
        pass

    def growingPhase(self):
        '''Right after selfOrganizationPhase'''
        pass

    def _doSetClusters(self):
        ''''''
        pass
    def __convertInputDataToNpMatrix(self,inputData)->np.array:
        self.__inputNpMatrix = inputData
        return self.__inputNpMatrix

    def getDataRowsNum(self):
        ''''''
        return self.__inputNpMatrix.shape[0]

    def getDataColsNum(self):
        '''Dimentions of data'''
        return self.__inputNpMatrix.shape[1]

    def plot(self, nodeRefVecs):
        # Clusters of input, assigning node colors to input data
        dataColorNode = np.zeros(self.getDataRowsNum())
        for counter in range(self.getDataRowsNum()):
            firstInputVectorFromPermutedInputs = self.getNormalizedNpMatrix()[counter, :]
            X = np.expand_dims(firstInputVectorFromPermutedInputs, axis=0)
            d = metrics.pairwise_distances(X=X, Y=nodeRefVecs, metric='euclidean')[0][:]
            minNode = np.argmin(d)
            dataColorNode[counter] = minNode

        # Positional case
        colors = {0: 'black',
                  1: 'grey',
                  2: 'blue',
                  3: 'cyan',
                  4: 'lime',
                  5: 'green',
                  6: 'yellow',
                  7: 'gold',
                  8: 'red',
                  9: 'maroon'}

        plt.ion()
        plt.show()

        figure, axesSubplot = plt.subplots(1, 1, figsize=(10, 10))
        fiveDVar = self.getNormalizedNpMatrix()[:, 0:5]

        for colorIndex, color in colors.items():
            axesSubplot.scatter(x=fiveDVar[dataColorNode == colorIndex, 0],
                                y=fiveDVar[dataColorNode == colorIndex, 1],
                                color=color,
                                label=str(colorIndex))
            axesSubplot.legend()

        axesSubplot.grid()
        plt.draw()
        figure.suptitle("Plotting clustering", fontsize=20)
