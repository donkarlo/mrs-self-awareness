class DumpedTextFile():
    '''A topic file created by ...

    '''

    def __init__(self, filePath: str):
        self.__filePath = filePath

    def getColumnIndexByName(self, targetColName: str) -> int:
        '''
        '''
        colIndexCounter = 0;
        for colName in self.getColumnNamesList():
            if colName == targetColName:
                return colIndexCounter
            colIndexCounter += 1

    def getColumnNamesList(self) -> list:
        ''''''
        file = open(self.__filePath, 'r')
        lineList = file.readline().split(",")
        file.close()
        return lineList

    def getFilePath(self) -> str:
        ''''''
        return self.__filePath
