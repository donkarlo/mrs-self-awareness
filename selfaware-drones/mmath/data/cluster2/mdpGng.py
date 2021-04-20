# -*- coding: utf-8 -*-
# Generated by codesnippet sphinx extension on 2016-03-08

import matplotlib.pyplot as plt
import mdp
import numpy as np

from mmath.data.cluster.gng.Gng import Gng
from ctumrs.topics.ThreeDPosVelFile import ThreeDPosVelFile

np.random.seed(0)
mdp.numx_rand.seed(1266090063)

##########################
fileDataBank = "/home/donkarlo/Dropbox/projs/research/data/self-aware-drones/ctumrs/two-step/manip/pos-vel-obs-from-gps.txt"
t3dposVel = ThreeDPosVelFile(fileDataBank)
inputData = t3dposVel.getNpArr()
gng = Gng(inputData)
inputData = gng.getNormalizedNpMatrix()

gng = mdp.nodes.GrowingNeuralGasNode(max_nodes=75)

forStep = 500
for i in range(0, inputData.shape[0], forStep):
    gng.train(inputData[i:i + forStep])
    # [...] plotting instructions
gng.stop_training()
print(gng.graph.connected_components())
nObj = len(gng.graph.connected_components())
print(nObj)


def plotXYZ(data, nodes=None):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(data[:, 0], data[:, 1], data[:, 2])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()


plotXYZ(inputData)
