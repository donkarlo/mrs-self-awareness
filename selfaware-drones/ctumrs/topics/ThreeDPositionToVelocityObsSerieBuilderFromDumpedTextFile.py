from ctumrs.topics.DumpedTextFile import DumpedTextFile
from state.obs.ObsSerie import ObsSerie
from state.obs.ThreeDPosVelObs import ThreeDPosVelObs
from state.obs.ThreeDPosVelObsSerieBuilder import ThreeDPosVelObsSerieBuilder


class ThreeDPositionToVelocityObsSerieBuilderFromDumpedTextFile:
    '''This class is responsible for Building and observation serie from a topic dumped text file and save it
    '''

    def __init__(self, dumpedTextFile: DumpedTextFile, posColNames: list, linelimit: int):
        '''
        Parameters
        ----------
        posColNames: array
            XYZ must be in order
        '''
        self.__dumpedTextFile = dumpedTextFile
        self.__posColNames = posColNames
        self.__obsSerie = None
        self.__linelimit = linelimit

    def getObsSerie(self) -> ObsSerie:
        """
        """
        if (self.__obsSerie == None):
            fileToReadFrom = open(self.__dumpedTextFile.getFilePath(), "r")
            threeDPosVelObsSerieBuilder = ThreeDPosVelObsSerieBuilder()
            for lineCounter, curLine in enumerate(fileToReadFrom):
                if lineCounter > self.__linelimit:
                    break
                elif lineCounter == 0:
                    continue
                elif lineCounter == 1:
                    curTime, curXObs, curYObs, curZObs = self.getTimeXyzObsFromStrLine(curLine)
                    curThreeDPosVelObs = ThreeDPosVelObs(curTime, curXObs, curYObs, curZObs, "0", "0", "0")
                    threeDPosVelObsSerieBuilder.append(curThreeDPosVelObs)  # we are fixing index 0
                    continue
                prvObs = threeDPosVelObsSerieBuilder.getObsSerie().getByIdx(lineCounter - 2)
                prvTime, prvXObs, prvYObs, prvZObs = float(prvObs.getComponentByIdx(0)), float(
                    prvObs.getComponentByIdx(1)), float(prvObs.getComponentByIdx(2)), float(prvObs.getComponentByIdx(3))
                curTime, curXObs, curYObs, curZObs = self.getTimeXyzObsFromStrLine(curLine)

                # timeDiff = (curTime - prvTime) / 1000000000000
                timeDiff = curTime - prvTime
                curXVelObs, curYVelObs, curZVelObs = [(curXObs - prvXObs) / timeDiff
                    , (curYObs - prvYObs) / timeDiff
                    , (curZObs - prvZObs) / timeDiff]
                curThreeDPosVelObs = ThreeDPosVelObs(curTime
                                                     , curXObs
                                                     , curYObs
                                                     , curZObs
                                                     , curXVelObs
                                                     , curYVelObs
                                                     , curZVelObs)
                threeDPosVelObsSerieBuilder.append(curThreeDPosVelObs)
                # update the first row with the second row velocity
                if lineCounter == 2:
                    firstThreeDPosVelObs = threeDPosVelObsSerieBuilder.getObsSerie().getByIdx(0)
                    firstThreeDPosVelObs.updateByIndex(3, curXVelObs)
                    firstThreeDPosVelObs.updateByIndex(4, curYVelObs)
                    firstThreeDPosVelObs.updateByIndex(5, curZVelObs)
            self.__obsSerie = threeDPosVelObsSerieBuilder.getObsSerie()
        return self.__obsSerie

    def saveToFileWithTime(self, filePath: str, sep=","):
        ''''''
        # save to the file from here
        with open(filePath, 'w') as f:
            for obs in self.getObsSerie().getObsArr():
                f.write("{}{}{}{}{}{}{}{}{}{}{}{}{}\n".format(obs.getTime(), sep,
                                                              obs.getComponentByIdx(0), sep,
                                                              obs.getComponentByIdx(1), sep,
                                                              obs.getComponentByIdx(2), sep,
                                                              obs.getComponentByIdx(3), sep,
                                                              obs.getComponentByIdx(4), sep,
                                                              obs.getComponentByIdx(5)))

    def saveToFileWithoutTime(self, filePath: str, sep=","):
        ''''''
        # save to the file from here
        with open(filePath, 'w') as f:
            for obs in self.getObsSerie().getObsArr():
                f.write("{}{}{}{}{}{}{}{}{}{}{}\n".format(
                    obs.getComponentByIdx(0), sep,
                    obs.getComponentByIdx(1), sep,
                    obs.getComponentByIdx(2), sep,
                    obs.getComponentByIdx(3), sep,
                    obs.getComponentByIdx(4), sep,
                    obs.getComponentByIdx(5)))

    def getTimeXyzObsIndexes(self) -> list:
        '''
        '''
        timeIndex = 0
        xColIndex = self.__dumpedTextFile.getColumnIndexByName(self.__posColNames[0])
        yColIndex = self.__dumpedTextFile.getColumnIndexByName(self.__posColNames[1])
        zColIndex = self.__dumpedTextFile.getColumnIndexByName(self.__posColNames[2])
        return [timeIndex, xColIndex, yColIndex, zColIndex]

    def getTimeXyzObsFromStrLine(self, line: str) -> list:
        '''
        '''
        curLineList = line.split(",")
        timeIndex, xIndex, yIndex, zIndex = self.getTimeXyzObsIndexes()
        time = float(curLineList[timeIndex])
        curXObs = float(curLineList[xIndex])
        curYObs = float(curLineList[yIndex])
        curZObs = float(curLineList[zIndex])

        return [time, curXObs, curYObs, curZObs]
