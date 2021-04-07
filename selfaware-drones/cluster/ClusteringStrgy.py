import abc
class ClusteringStrgy(metaclass=abc.ABCMeta):
    """
    An abstaract class that inforces all childs to have an strtegy to cluster the given data
    """
    def __init__(self, inpData):
        self._inpData = inpData
        self._clusters = None

    @abc.abstractmethod
    def getClusters(self):
        """Returns the clusters

        Parameters
        ---------
        Returns
        ---------
        _clusters: array
            array of clusters
        """
        if self._clusters is None:
            self._doSetClusters()
        return self._clusters

    @abc.abstractmethod
    def _doSetClusters(self):
        """Abstract method that children should implement.

        All child should set self._clusters in this implemented method

        Parameters
        ----------
        Returns
        -------
        """

    def getClustersNum(self):
        return len(self.getClusters())