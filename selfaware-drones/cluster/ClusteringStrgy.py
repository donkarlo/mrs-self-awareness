import abc
import array
class ClusteringStrgy():
    def __init__(self, data: array):
        self._data = data
        self._clusters = None

    def getClusters(self)->array:
        return self._clusters

    @abc.abstractmethod
    def doGetClusters(self):
        pass
