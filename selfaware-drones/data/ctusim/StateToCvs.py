'''
This class is to read dumped filed from CTRU-MRS ROS bags record service and put it togethre  in CSV file in the
following format
px1,py1,pz1,vx1,vy1,vz1,px1,py2,pz3,vx1,vy2,vz3;....
Of course angular velocity and accelerations are also included the above presentation is just for presenting a sample
'''
class StateToCvs():
    def __init__(self, srcFilePathStr1, srcFilePathStr2, destFilePathStr):
        self.srcRowStr = ''
        pass
    '''
    Extract a row from one of the srcFiles
    '''
    def getNextSrcRow(self,srcFile):
        return
    '''
    Save a given STU-MRS row in a CSV row
    '''
    def saveCVSRow(self, srcRowStr):
        timeInstance = self.extractTimeInstance()
        px = self.__getPxFromRowStr()
        py = self.__getPyFromRowStr()
        pz = self.__getPzFromRowStr()
        vx = self.__getVxFromRowStr()
        vy = self.__getVxFromRowStr()
        vz = self.__getVxFromRowStr()
        str = px+","+py+","+pz+","+ vx+","+vy+","+vz+","
        #@todo save str to destFilePathStr
    '''
    '''
    def __getTimeInstanceFromRowStr(self,srcRowStr):
        pass

    def __getPxFromRowStr(self,srcRowStr):
        pass

    def __getPyFromRowStr(self,srcRowStr):
        pass

    def __getPzFromRowStr(self,srcRowStr):
        pass

    def __extractVxFromRowStr(self,srcRowStr):
        pass

    def __extractVyFromRowStr(self,srcRowStr):
        pass

    def __extractVzFromRowStr(self,srcRowStr):
        pass
