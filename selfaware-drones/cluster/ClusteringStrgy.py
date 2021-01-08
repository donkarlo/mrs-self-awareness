import abc
import array
class ClusteringStrgy():
    """
    An abstaract class that inforces all childs to have an strtegy to cluster the given data
    """
    def __init__(self, data: array):
        self._data = data
        self._clusters = None

    def getClusters(self)->array:
        """Returns the clusters

        Parameters
        ---------
        Returns
        ---------
        _clusters: array
            array of clusters
        """
        if self._clusters==None:
            return self._clusters

    @abc.abstractmethod
    def doSetClusters(self):
        """Abstract method that children should implement.

        All child should set self._clusters in this implemented method

        Parameters
        ----------
        Returns
        -------
        """
        pass
