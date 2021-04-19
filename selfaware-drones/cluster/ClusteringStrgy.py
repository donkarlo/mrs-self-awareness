import abc
from typing import List


class ClusteringStrgy(metaclass=abc.ABCMeta):
    """
    An abstaract class that inforces all childs to have an strtegy to cluster the given data
    """

    def __init__(self, inpData):
        self._inpData = inpData
        self._clusters = None

    def getClusters(self) -> List:
        """Returns the clusters

        Parameters
        ---------
        Returns
        ---------
        _clusters: array
            array of clusters
        """
        if self._clusters is None:
            print("Please wait ...")
            self._doSetClusters()
        return self._clusters

    @abc.abstractmethod
    def _doSetClusters(self):
        """

        Parameters
        ----------
        Returns
        -------
        """
        pass

    def getClustersNum(self) -> int:
        if self._clusters is not None:
            return len(self._clusters)
        else:
            return 0
