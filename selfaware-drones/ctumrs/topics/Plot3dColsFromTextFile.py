import matplotlib.pyplot as plt


class PlotFromCtuMrsTopicTextFile:
    def __init__(self, filePath: str, askingFields=[]):
        self.__filePath = filePath
        self.__askingFields = askingFields

    def getAllCollumnNamesSpilited(self) -> list:
        # todo lazy loading
        f = open(self.__filePath, "r")
        l1 = f.readline();
        allCollumnNames = l1.split(",")
        return allCollumnNames

    def getCollumnIndexByAskingFieldName(self, askingFieldName: str) -> int:
        allColNames = self.getAllCollumnNamesSpilited()
        colCounter = 0;
        for collName in allColNames:
            if (collName == askingFieldName):
                return colCounter
            colCounter += 1
        return -1
        # todo throw an exception for askingFieldName which didnt exist in allColNames

    '''
    '''

    def getXyzIndexes(self) -> list:
        # assuming that asking fields are oreder to match x,y,z
        askingFiledCounter = 0
        for askingField in self.__askingFields:
            index = self.getCollumnIndexByAskingFieldName(askingField)
            if (index != -1 and askingFiledCounter == 0):
                xIndex = index
            if (index != -1 and askingFiledCounter == 1):
                yIndex = index
            if (index != -1 and askingFiledCounter == 2):
                zIndex = index
            askingFiledCounter += 1
        return [xIndex, yIndex, zIndex]

    def plot(self):
        file = open(self.__filePath, "r")
        fileLineCounter = 0
        x = []
        y = []
        z = []
        xIndex, yIndex, zIndex = self.getXyzIndexes()
        for line in file:
            if (fileLineCounter < 220000):
                if (fileLineCounter > 1):
                    lsplt = line.split(",")
                    x.append(float(lsplt[xIndex]))
                    y.append(float(lsplt[yIndex]))
                    z.append(float(lsplt[zIndex]))
                fileLineCounter += 1
            else:
                break
        file.close()

        # Plot from here
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x, y, z, c='r', marker='o', s=0.1)
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        plt.show()

    def plotGradually(self):
        pass
