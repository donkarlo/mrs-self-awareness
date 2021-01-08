import array
from cluster import ClusteringStrgy


class Gng(ClusteringStrgy):
    def __init__(self, data: array):
        super().__init__(data)

    def doSetClusters(self):
        pass