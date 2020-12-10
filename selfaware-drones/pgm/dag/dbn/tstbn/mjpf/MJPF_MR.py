# Bring the MJPF to python

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

import networkx as net

import scipy.io as sio

import torchvision
from torchvision import datasets
from torchvision import transforms
from torchvision.utils import save_image

from IPython.display import Image
from numpy.core.records import fromarrays

import matplotlib.pyplot as plt

import cv2

import sklearn.metrics as metrics

import random
import mat4py

import os

from sklearn.preprocessing import normalize

from torch.autograd import Variable


import warnings
warnings.filterwarnings("ignore")

###############################################################################

# Color array for plotting
colors_array = np.array(['lightpink', 'grey', 'blue', 'cyan', 'lime', 'green', 'yellow', 'gold', 'red', 'maroon',
                   'rosybrown', 'salmon', 'sienna', 'palegreen', 'sandybrown', 'deepskyblue', 
                   'fuchsia', 'purple', 'crimson', 'cornflowerblue', 
                   'midnightblue', 'mediumturquoise', 'bisque', 'gainsboro', 'indigo',
                   'white'])


###############################################################################
# ----------------------- USER SETTINGS ---------------------------------------
###############################################################################

# this path
path = os.path.dirname(os.path.abspath(__file__)) 

# Where to save the results
outputFile = path + "/OUTPUT_odometry/"    

oldDistanceMethod = True
# Indicator for saving reconstruction, OF, interactive images
saveImages = True
# Indicator for plotting results
plotBool = True
# Indicator for writing the current time instant
printCounter = True

# some params of filter
active_node_threshold = 0.95
nParticles = 100
skewValue = 5

#--------------------------------------------------------------------------
# Settings to define
#--------------------------------------------------------------------------


# Do you want to use the training or testing data?
testing = 2; # 0=train, 1= AM, 2= UM

# offset between images
offset = 1;

# From which time instant to which one do we want to pick the data?
begin = 1;
ending = -1; #negative value to go to end of latent states vector

winningMetric = 1


# DATA   ------------------------------------------------------------------

# This all has to be done on the training data, so first download the training data

def loadData(dataFile): 
    
    data = mat4py.loadmat(dataFile)
    data = [ v for v in data.values() ]
    data = data[0]
    data = np.asarray(data)
    
    return data

dataFile = path + "/" + "CL_data_train_odometry.mat"
GS = loadData(dataFile)
variances = np.ones((GS.shape[0], GS.shape[1]))*1e-100

# mean values of the clusters 
meanNodes = mat4py.loadmat(path + "/" + "CL_clusterMeans_odometry.mat")
meanNodes = [ v for v in meanNodes.values() ]
meanNodes = meanNodes[0]
meanNodes = np.asarray(meanNodes)
    
dataColorNode = mat4py.loadmat(path + "/" + "CL_dataColorNode_odometry.mat")
dataColorNode = [ v for v in dataColorNode.values() ]
dataColorNode = dataColorNode[0]
dataColorNode = np.asarray(dataColorNode).astype(int) -1 # make sure it is an int array
    
lengthOfData = GS.shape[0]
numberLatentStates = int(GS.shape[1]/2)
z_dim = numberLatentStates

minData = np.min(GS, axis = 0)
minDataTrain = minData
maxData = np.max(GS, axis = 0)

data = GS

dataNorm = data - np.tile(minData, (data.shape[0] , 1)) # tile(a, (m, n)) = repmat(a, m, n)
maxDataNorm = np.max(dataNorm, axis = 0)
maxDataNormTrain = maxDataNorm
dataNorm = dataNorm/np.tile(maxDataNorm, (data.shape[0] , 1))

# Number of clusters
nClusters = meanNodes.shape[0]

# mean and covariance

# Define one array for each cluster:
datanodes = []
for i in range(nClusters):
    cluster_i = []
    datanodes.append(cluster_i)
    
# Insert the data of each cluster in the corresponding array
for i in range(lengthOfData):
    superstate_i = int(dataColorNode[i])
    state_i = data[i, :]
    datanodes[superstate_i].append(state_i)

datanodesNorm = []
for i in range(nClusters):
    cluster_i_norm = []
    datanodesNorm.append(cluster_i_norm)
    
for i in range(lengthOfData):
    superstate_i_norm = int(dataColorNode[i])
    state_i_norm = dataNorm[i, :]
    datanodesNorm[superstate_i_norm].append(state_i_norm)

    
summing = 0
for i in range(len(datanodes)):
    summing += len(datanodes[i])

# Calculate the covariance for each array
covSuperstates = np.zeros((nClusters, numberLatentStates*2, numberLatentStates*2))
mean_confirm = np.zeros((nClusters, numberLatentStates*2))
for i in range(nClusters):
    # if the cluster is not empty, calculate mean and covariance
    if len(datanodes[i]) != 0: 
        mean_confirm[i, :] = np.mean(datanodes[i], axis = 0)
        
        
#--------------------------------------------------------------------------
# Radius of acceptance and covariance

nodesCov = []
nodesCovNorm = []
for i in range(nClusters):
    nodesCov_i = []
    nodesCov.append(nodesCov_i)
    #nodesCovNorm.append(nodesCov_i)
nodesRadAccepts_state = []    
nodesRadAcceptNorms_state = []
nodesRadAccepts_deriv = []  
nodesRadAcceptNorms_deriv = []

    
for i in range(nClusters):
    
    if len(datanodes[i]) == 0:
        nodesCov[i].append(np.zeros((numberLatentStates, numberLatentStates)))
        
    else:        
        datanode_of_cluster = np.asarray(datanodes[i])
        datanode_of_cluster_norm = np.asarray(datanodesNorm[i])
        
        nodesCov[i] = np.cov(np.transpose(datanode_of_cluster)) # calculation of covariance values
        #nodesCovNorm[i] = np.cov(np.transpose(datanode_of_cluster))  
        
    # Calculation of radius of acceptance
    nodeRadAccept_state = np.sqrt(np.sum(np.power((3*np.std(datanode_of_cluster[:,0:z_dim], axis = 0)),2)))
    nodeRadAcceptNorm_state = np.sqrt(np.mean(np.power((3*np.std(datanode_of_cluster[:,0:z_dim], axis = 0)),2)))
    
    
    nodeRadAccept_state = np.sqrt(np.sum(np.power((3*np.std(datanode_of_cluster[:, 0:z_dim], axis = 0)),2)))
    nodeRadAcceptNorm_state = np.sqrt(np.mean(np.power((3*np.std(datanode_of_cluster_norm[:, 0:z_dim], axis = 0)),2)))
    
    nodeRadAccept_deriv = np.sqrt(np.mean(np.power((3*np.std(datanode_of_cluster[:,z_dim:z_dim*2] , axis = 0)),2)))
    nodeRadAcceptNorm_deriv = np.sqrt(np.mean(np.power((3*np.std(datanode_of_cluster_norm[:,z_dim:z_dim*2], axis = 0)),2)))
    
    nodesRadAccepts_state.append(nodeRadAccept_state)
    nodesRadAcceptNorms_state.append(nodeRadAcceptNorm_state)
    
    nodesRadAccepts_deriv.append(nodeRadAccept_deriv)
    nodesRadAcceptNorms_deriv.append(nodeRadAcceptNorm_deriv)
    

covSuperstates = nodesCov
radiusState = nodesRadAccepts_state
radiusStateNorm = nodesRadAcceptNorms_state

radiusDeriv = nodesRadAccepts_deriv
radiusDerivNorm = nodesRadAcceptNorms_deriv

# Function to create the graph structure 
def FindGraphStructure (idx, offset):
    
    # Number of clusters
    N = int(max(idx)+1)
    
    # Length of the data
    data_length =  len(idx)
    
    # Create the index list: it just gives a correspondence key-index
    index = dict()
    for i in range (0, N):
        index[i] = i
   
    # list with all the interactions from a node i to a node j, with i != j
    interactions = []
    for i in range (0, data_length - offset):
        # If we have a movement from a cluster to another one
        #if idx[i + 1] != idx[i]:
        # Add the interaction to the list
        pair = [idx[i + offset], idx[i]]
        interactions.append(pair)
    # Sort the list in ascending order of numbers
    interactions.sort() 
    
    return index, interactions

def FindTransitionMat (index, interactions, result_folder, plotting):
    
    interactionMat = np.zeros((len(index), len(index)))
    for item in interactions:
        interactionMat[item[0], item[1]] += 1
        
    if plotting == True:
        plt.imshow(interactionMat)
        plt.savefig(result_folder)
        plt.close('all')
            
    interactionMat = normalize(interactionMat, axis=1, norm='l1')
        
    return interactionMat

index, interactions = FindGraphStructure (dataColorNode, offset)
transitionMat = FindTransitionMat(index, interactions, " ", plotting = False)


# --------------------------------------------------------------------------

# Variance of the observation
# This is used only as an observation covariance at the first time step.
varObs = np.mean(variances, axis = 0);

covObservation = np.zeros((numberLatentStates, numberLatentStates))
for i in range(numberLatentStates):
    covObservation[i, i] = varObs[i]
    
    
#--------------------------------------------------------------------------
# Folders where to pick data, images, code, NNs
#--------------------------------------------------------------------------

# DATA   ------------------------------------------------------------------

if testing == 0:
    
    dummy = 0
        
elif testing == 1:
    
    dataFile = path + "/" + "data_test_odometry.mat"
    GS = loadData(dataFile)
    variances = np.ones((GS.shape[0], GS.shape[1]))*1e-10
    
    begin = 1417;
    ending = 2198; 
    
else:
    
    dataFile = path + "/" + "test_data_UM_original.mat"
    GS = loadData(dataFile)
    variances = np.ones((GS.shape[0], GS.shape[1]))*1e-10
    
    begin = 1;
    ending = -1; #negative value to go to end of latent states vector
    

data = GS

lengthOfData = GS.shape[0]
numberLatentStates = int(GS.shape[1]/2)

#--------------------------------------------------------------------------
# Loading images
#--------------------------------------------------------------------------

# Cutting the data from begin and ending
if ending < 0:
    ending = GS.shape[0]
    
if ending > GS.shape[0]:
    ending = GS.shape[0]
    
if ending > 10000:
    ending = 10000

pickedIndices = np.arange(begin, ending-offset, offset)

data = data[pickedIndices, :]
lengthOfData = len(data)



###############################################################################

###############################################################################

###############################################################################

#########                MARKOV JUMP PARTICLE FILTER                 ##########

###############################################################################

###############################################################################

###############################################################################
    
    

    
'''
results, lambdas, predictionMuMin, activeNodes, innovationImgRealPredictedMin, innovationOFRealPredictedMin, onlyErrorAnomalyMin, onlyStateAnomalyMin, KLD_winners, KLDabn_all, MSE_Real_OFs = MJPF_NN.MJPF(variances, data, meanNodes, 
         numberLatentStates, nParticles, covObservation, minDataTrain, maxDataNormTrain,
         dataloaders, version, covSuperstates, skewValue, active_node_threshold, winningMetric, 
         calculateImageErrorsAnyway, vae, showWinningReconstruction, path, transitionMat, z_dim, NNs, 
         oldDistanceMethod,radiusStateNorm, saveImages, plotBool, printCounter)
'''



# Distance of a point from the center of the clusters
def find_distances_from_clusters(currState, averageNodes):
    
    nDim = currState.shape[0]
    X = np.expand_dims(currState, axis=0)

    X_state = X[:,0: int(nDim/2)]
    X_deriv = X[:,int(nDim/2):nDim]
    wNorm_state = averageNodes[:, 0: int(nDim/2)]
    wNorm_deriv = averageNodes[:, int(nDim/2):nDim]
    d_state = metrics.pairwise_distances(X=X_state, Y=wNorm_state, metric='euclidean')[0][:]
    d_deriv = metrics.pairwise_distances(X=X_deriv, Y=wNorm_deriv, metric='euclidean')[0][:]
        
    value_state = d_state/np.sum(d_state)
    value_deriv = d_deriv/np.sum(d_deriv)
        
    return value_state, value_deriv, d_state, d_deriv

def find_distances_from_clusters_overall(currState, averageNodes):
    
    overall_state = np.expand_dims(currState, axis=0)
    
    distance = metrics.pairwise_distances(X=overall_state, Y=averageNodes, metric='euclidean')[0][:]
        
    return distance

def nodesProb(currState, averageNodesNorm, radiusStateNorm):
    
    #If the probability of being in a superstate is 'inThreshProb', it 
    # is considered to be imposible to be outside the model 
    inThreshProb = 0.8;                                                         
    outThreshProb = 1 - inThreshProb;
            
    # Total of neurons  
    nodesNumber = averageNodesNorm.shape[0]
    # Calculation of norm 1 distance from current positions to each neuron
    #value_state, value_deriv, d_state, d_deriv = find_distances_from_clusters(currState, averageNodesNorm)        
    #distances = d_state + d_deriv
    
    distances = find_distances_from_clusters_overall(currState, averageNodesNorm)    
            
    distFinal = distances/np.mean(np.asarray(radiusStateNorm))
            
    superStateProb = np.zeros(nodesNumber+1)
            
    superStateProb[0:nodesNumber] = 1 - distFinal
            
    # Sum elements
    superStateProb[0:nodesNumber] = superStateProb[0:nodesNumber]*(distFinal<1)
    
    if sum(superStateProb) == 0:
        print('empty node selected')
        superStateProb[nodesNumber] = 1
            
    # Calculation of maximum probability                
    #prob = np.max(superStateProb)                                                 
            
    # Probability of empty neuron is 1-probability of most likely neuron
    #probEmptyNeuron = np.max([1-(prob+outThreshProb), 0])
    #superStateProb[nodesNumber] = probEmptyNeuron
            
    #superStateProb = superStateProb/np.sum(superStateProb)
    
    '''
    distances = find_distances_from_clusters_overall(currState, averageNodesNorm)    
            
    distFinal = distances/np.mean(np.asarray(radiusStateNorm))
            
    superStateProb = np.zeros(nodesNumber+1)
            
    superStateProb[0:nodesNumber] = 1 - distFinal
            
    # Sum elements
    superStateProb[0:nodesNumber] = superStateProb[0:nodesNumber]*(distFinal<1)
            
    # Calculation of maximum probability                
    prob = np.max(superStateProb)                                                 
            
    # Probability of empty neuron is 1-probability of most likely neuron
    probEmptyNeuron = np.max([1-(prob+outThreshProb), 0])
    superStateProb[nodesNumber] = probEmptyNeuron
            
    superStateProb = superStateProb/np.sum(superStateProb)
    '''
    
            
    return superStateProb, distFinal


def CalculateBhattacharyyaDistance(pm, pv, qm, qv):
    
    # Copyright (c) 2008 Carnegie Mellon University
    #
    # You may copy and modify this freely under the same terms as
    # Sphinx-III
    
    #__author__ = "David Huggins-Daines <dhuggins@cs.cmu.edu>"
    #__version__ = "$Revision$"

    """
    Classification-based Bhattacharyya distance between two Gaussians
    with diagonal covariance.  Also computes Bhattacharyya distance
    between a single Gaussian pm,pv and a set of Gaussians qm,qv.
    """
    
    if (len(qm.shape) == 2):
        axis = 1
    else:
        axis = 0
    # Difference between means pm, qm
    diff = qm - pm
    # Interpolated variances
    pqv = (pv + qv) / 2.
    # Log-determinants of pv, qv
    ldpv = np.log(pv).sum()
    ldqv = np.log(qv).sum(axis)
    # Log-determinant of pqv
    ldpqv = np.log(pqv).sum(axis)
    # "Shape" component (based on covariances only)
    # 0.5 log(|\Sigma_{pq}| / sqrt(\Sigma_p * \Sigma_q)
    norm = 0.5 * (ldpqv - 0.5 * (ldpv + ldqv))
    # "Divergence" component (actually just scaled Mahalanobis distance)
    # 0.125 (\mu_q - \mu_p)^T \Sigma_{pq}^{-1} (\mu_q - \mu_p)
    dist = 0.125 * (diff * (1./pqv) * diff).sum(axis)
    
    return dist + norm


## Input:
# totNumOfSuperstates: total number of Superstates
# measurement: the current observation
# meanOfSuperstates: matrix consisting of the mean value of each Superstate
# covarianceOfSuperstates: cell consisting of the covariance matrix of each Superstate  
## Output:
# outputArg1 = probability_lamdaS;
def calculateLamdaS(nSuperStates, measurement, meanOfSuperstates, R, covarianceOfSuperstates, skewValue):
    
    lamdaS = np.zeros(nSuperStates)
    # Calculate lambda in terms of battacharyya distance b/w observation & each superstate:
    for index_s in range(nSuperStates):
        
        varianceOfMeasurement_s = np.diagonal(R)
        varianceOfSuperstate_s = np.diagonal(covarianceOfSuperstates[index_s])
        
        #varianceOfMeasurement_s = R
        #varianceOfSuperstate_s = covarianceOfSuperstates[index_s]
        
        lamdaS[index_s] = CalculateBhattacharyyaDistance(measurement,varianceOfMeasurement_s,meanOfSuperstates[index_s, :],varianceOfSuperstate_s)
              
    #Convert lamda to a discrete probability distribution:
    # using skewValue can help to make the probability distribution more skewed (for example if n=1 give you [0.6 0.4], n=2 will give you [0.1 0.9])
    probability_lamdaS = (1/(np.power(lamdaS, skewValue)))/np.sum(1/(np.power(lamdaS, skewValue)))
    
    return probability_lamdaS


def KLDiv(p, q):
    """Kullback-Liebler divergence from multinomial p to multinomial q,
    expressed in nats."""
    if (len(q.shape) == 2):
        axis = 1
    else:
        axis = 0
    # Clip before taking logarithm to avoid NaNs (but still exclude
    # zero-probability mixtures from the calculation)
    return (p * (np.log(p.clip(1e-10,1))
                 - np.log(q.clip(1e-10,1)))).sum(axis)   # - N
    
def single_KLD_Abnormality(PP, QQ, KLDAbnMax, histogramProb, N):
    
    if np.sum(np.isinf(QQ)) >= 1:
        KLD_simmetrica = KLDAbnMax 
    elif np.sum(np.isnan(QQ)) >= 1:
        KLD_simmetrica = KLDAbnMax
    elif np.sum(np.isnan(PP)) >= 1:
        KLD_simmetrica = KLDAbnMax
    else:
        KLD_simmetrica = (histogramProb/N)*KLDiv(PP,QQ) + (histogramProb/N)*KLDiv(QQ,PP) #to achieve symmerty
    
    if np.sum(np.isinf(KLD_simmetrica)) >= 1:
        KLD_simmetrica = KLDAbnMax;
    
    return KLD_simmetrica

## Input:
# totNumOfSuperstates: total number of Superstates
# N: total number of Particles
# histogram: histogram at time t-1 (after PF resampling)
# transitionMat: the transition matrix learned from previous experience
# probability_lamdaS: probability vector representing a discrete probability disctribution         
def KLD_Abnormality(nSuperstates, N, histogram, transitionMat, probability_lamdaS, KLDAbnMax):
    
    ##Procedure:
    sommaKLD_simmetrica = 0
    
    for indKLD in range(nSuperstates):
        particella = histogram[indKLD]
        
        if particella > 0:
            
            PP = transitionMat[indKLD,:] +1e-20 # add 1e-100 since KLD doesnt allow zero values
            QQ = probability_lamdaS
            
            KLD_simmetrica = single_KLD_Abnormality(PP, QQ, KLDAbnMax, particella, N)
            
            sommaKLD_simmetrica = sommaKLD_simmetrica + KLD_simmetrica
        
    return sommaKLD_simmetrica


###############################################################################

###############################################################################

###############################################################################

#########                MARKOV JUMP PARTICLE FILTER                 ##########

###############################################################################

###############################################################################

###############################################################################

'''
def MJPF(variances, data, meanNodes, numberLatentStates, nParticles, covObservation, minDataTrain, 
         maxDataNormTrain,dataloaders, version, covSuperstates, skewValue, active_node_threshold, winningMetric, 
         calculateImageErrorsAnyway, vae, showWinningReconstruction, path, transitionMat, z_dim, NNs, 
         oldDistanceMethod,radiusStateNorm, saveImages, plotBool, printCounter):
'''
    
variances = variances

dataLength = data.shape[0]

averageNodes = meanNodes
averageState = meanNodes[:,0:numberLatentStates]
averageDiv = meanNodes[:,numberLatentStates: 2*numberLatentStates]

# Definition of the parameters

# Number of considered Superstates (clusters)
nSuperStates = averageState.shape[0]

# Number of latent states
numState = averageState.shape[1]
# Number of particles (discrete and continuous levels)
N = nParticles;

predictionMuMin = np.zeros((numState*2, dataLength));

# Transition matrix for the continous-time system.
#A = [eye(numState),zeros(numState);zeros(numState),zeros(numState)];
# Measurement model.
H = np.zeros((numState, numState*2))
H[0:numState, 0:numState] = np.eye(numState)
# Control input
#B = [eye(numState);eye(numState)];

# Initial variance in the measurements.
R = covObservation

# Innovation measurements preallocations

# 0 : full state (mus + err)
fullStateAnomaly = np.zeros((N, dataLength))
# 1 : state (mus)
onlyStateAnomaly = np.zeros((N, dataLength))
# 2 : error/velocity (err)
onlyErrorAnomaly = np.zeros((N, dataLength))
# 3 : error/velocity, based on actual data (err)
innovationErr = np.zeros((N, dataLength))
# 4 : MSE between updated and predicted image
innovationImgUpdatedPredicted = np.zeros((N, dataLength))
# 5 : MSE between real and predicted image
innovationImgRealPredicted = np.zeros((N, dataLength))
innovationOFRealPredicted = np.zeros((N, dataLength))
innovationImgOFRealPredicted = np.zeros((N, dataLength))

MSE_Real_OFs = np.zeros(dataLength);

# For discrete-level anomaly
KLD_winners = np.zeros(dataLength)
KLDabn_all = np.zeros(dataLength)

# Where to save the value for the winning node at each time instant
innovation_min = np.zeros(dataLength)
innovationErrMin = np.zeros(dataLength)
fullStateAnomalyMin = np.zeros(dataLength)
onlyStateAnomalyMin = np.zeros(dataLength)
onlyErrorAnomalyMin = np.zeros(dataLength)
innovationErrMin = np.zeros(dataLength)
innovationImgUpdatedPredictedMin = np.zeros(dataLength)
innovationImgRealPredictedMin = np.zeros(dataLength)
innovationOFRealPredictedMin = np.zeros(dataLength)

indexes_innov_min = np.zeros(dataLength)


db1s = np.zeros((N, dataLength))
db2s = np.zeros((N, dataLength))
db1sMin = np.zeros(dataLength)
db2sMin = np.zeros(dataLength)

# Winning superstate at each time instant
superstateMinInnov = np.zeros(dataLength);


# Initialization Filtering steps.
# Initial guesses for the state mean and covariance.
#Q = [covPrediction , zeros(numState) ; zeros(numState), covPrediction] ;

# Weight of particles 
weightsPar = np.zeros(N);


# Definition of parameters
statepred3 = np.zeros((numState*2,dataLength,N))     
#statepred4 = zeros(numState*2,dataLength,N,M);                                    
Ppred = np.zeros((numState*2,numState*2,dataLength,N))                                    
stateUpdated = np.zeros((numState*2,dataLength,N))
updatedP1 = np.zeros((numState*2,numState*2,dataLength,N))
weightscoeff_n = np.zeros((N,dataLength))

activeNodes = np.zeros((N,dataLength))

# Saving the lambda for the discrete level anomaly
lambdas = np.zeros((nSuperStates, dataLength))
lambdas_after_state =  np.zeros((nSuperStates, dataLength))

firstIt = 0

activeNodesPrev = np.zeros((N, 1))


averageNodesNorm = averageNodes - np.tile(minDataTrain, (averageNodes.shape[0] , 1)) # tile(a, (m, n)) = repmat(a, m, n)
maxDataNorm = np.max(maxDataNormTrain, axis = 0)
averageNodesNorm = averageNodesNorm/np.tile(maxDataNorm, (averageNodes.shape[0] , 1))

obsCovariance = covObservation
    

###########################################################################
###########################################################################

i = -1

for i in range(dataLength) :
    
    if printCounter == True:
        print (str(i) + " out of " + str(dataLength))
    elif i % 500 == 499:
        print (str(i) + " out of " + str(dataLength))
        
    currMeas = data[i, :]
    
    statesToPropagate = []
    
    for sp in range(nSuperStates):
        cluster_sp = []
        statesToPropagate.append(cluster_sp)
        
    # For EACH PARTICLE
    for n in range(N):
        
        if i == firstIt:
    
            currState = currMeas # it is already noisy
            currVar = variances[i, :]
            currP1 = np.zeros((numberLatentStates*2,numberLatentStates*2))
            currP1[0:numberLatentStates, 0:numberLatentStates] = R
            currP1[numberLatentStates:numberLatentStates*2, numberLatentStates:numberLatentStates*2]
            
            weightscoeff_n[n,i] = 1/N 
            
        else:
            
            # NEXT MEASUREMENT APPEARS
            # UPDATE
                       
            # new data
            currData = currMeas
            currVar = variances[i, :]
            
            # Covariance of observation, from the vars of the image
            currObsVar = variances[i,:]
            
            obsCovariance = currObsVar[0:numState]*np.eye(numState)
            
            predCovariance = Ppred[:, :, i - 1, n]
                    
            H = np.zeros((numState, numState*2))
            H[0:numState, 0:numState] = np.eye(numState)
            H_transpose = np.transpose(H)
                
            # Innovation
            innov_m = currData[0:numState] - np.dot(H,statepred3[:,i-1, n])
            
            # Covariance of the innovation:
            innovationCov = np.dot(H, np.dot(predCovariance,H_transpose)) + obsCovariance
            
            # KALMAN GAIN: it considers uncertainty in interactive and uncertainty in
            # the sensors and can thus be used to weight the final interactive through
            # the innovation.
            inverse_innovationCov = np.linalg.inv(innovationCov)
            kalmanGain = np.dot(predCovariance, np.dot(H_transpose, inverse_innovationCov))
            
            #print('KG ' + str(kalmanGain))
            
            # FINAL PREDICTION UPDATE AT THE CURRENT INSTANT:
            # State interactive: we update the interactive done in the PREDICTION stage
            # throught the new observation.
            # As weight we use the Kalman gain: if the Kalman gain is high and I am
            # very confident in the sensorial data I got, I will correct a lot,
            # otherwise little.
            stateUpdated[:, i, n] = statepred3[:,i-1, n] + np.dot(kalmanGain,innov_m)
            
            # We also update the covariance estimation:
            covEstimatedTemp = np.dot(kalmanGain, innovationCov)
            #covEstimatedTemp = np.dot(kalmanGain, predCovariance)
            covEstimatedTemp = np.dot(covEstimatedTemp, np.transpose(kalmanGain))
            covEstimated = predCovariance - covEstimatedTemp
            
        
            
    
            # FINAL PREDICTION UPDATE AT THE CURRENT INSTANT:
            
            # State interactive: we update the interactive done in the PREDICTION stage
            # throught the new observation.
            # As weight we use the Kalman gain: if the Kalman gain is high and I am
            # very confident in the encoded data I got, I will correct a lot,
            # otherwise little.
            stateUpdated[:, i, n] = statepred3[:,i-1, n] +  np.dot(kalmanGain,innov_m)
            stateUpdated[numState:numState*2, i, n] = currData[numState:numState*2]
            
            # Covariance update
            updatedP1[:,:,i,n] = covEstimated
            
            # Association of updated states to variables
            currP1 = updatedP1[:,:,i,n]
            # updated state of object
            currState = stateUpdated[:, i, n]
            updatedState = currState
            
        
        
        #----------------------------------------------------------------------
        ##   SECOND BLOCK (Calculation of current superstates)
        
        #   TRANSFORMATION OF STATES INTO SUPERSTATES
        
        # Normalizing the current state
        
        currStateNorm = currState - minDataTrain
        currStateNorm = currStateNorm/maxDataNormTrain
        
        # Probability of being in each node and distance
        
        # nodesProb function
        # Calculation of lambda for discrete-level anomaly:
        # In this way we obtain a value for each superstate that
        # defines a distance between the SUPERSTATE and the OBSERVATION
        covGeneralizedObservation = np.zeros((numState*2, numState*2))
                
        covGeneralizedObservation[0:numState, 0:numState] = obsCovariance
        covGeneralizedObservation[numState:2*numState, numState:2*numState] = 2*obsCovariance # approx
        
        lambda_after_state = calculateLamdaS(nSuperStates, currState, averageNodes, covGeneralizedObservation, covSuperstates, skewValue)
        
        lambdas_after_state[:,i] = lambda_after_state
        
        if oldDistanceMethod == False:
            probDist = lambda_after_state
            distance = 1/probDist
        else:
            
            radiusStateNorm
            
            currStatePos = currState[0:z_dim]
            currStateDeriv = currState[z_dim:2*z_dim]
            probDistPos, distancePos = nodesProb(currStatePos,averageState,radiusState*np.ones(len(radiusState)))  
            probDistDeriv, distanceDeriv = nodesProb(currStateDeriv,averageDiv,radiusDeriv*np.ones(len(radiusDeriv)))
            
            probDist = (probDistDeriv + probDistPos)/sum((probDistDeriv + probDistPos))
            distance = distancePos + distanceDeriv
        

        ind_node = np.argsort(-probDist) # rank in descending order (argsort does it in ascending by default)
        prob_node = probDist[ind_node]
        
        # cumulative sum
        prob_node_cum = np.cumsum(prob_node)
        # selecting the first possible active nodes based on a threshold on the active sum
        active_nodes = ind_node[prob_node_cum < active_node_threshold]
        active_prob = prob_node[prob_node_cum < active_node_threshold]
        if active_nodes.size == 0:
            active_nodes = ind_node[1]
            active_prob = prob_node[1]
            
        probDist = np.zeros(nSuperStates+1)
        probDist[active_nodes] = active_prob
        probDist = probDist/np.sum(probDist)
        
        # choose a node from the list of remaining nodes and save it in activeNodes
        activeNodes[n,i] = random.choices(np.arange(nSuperStates), weights = probDist[0:len(probDist)-1], k = 1)[0]
        
        # if chosen node is the empty one
        if activeNodes[n,i] >= nSuperStates:
            probDist = 1/distance
            probDist = probDist/np.sum(probDist)
            activeNodes[n,i] = random.choices(np.arange(nSuperStates), weights = probDist, k = 1)[0]   
            
        
        #######################################################################
        ## THIRD BLOCK (Abnormal measurements' calculation/particle weighting)
        if i > firstIt:
    
            
            # CALCULATION OF ABNORMALITY MEASUREMENTS
            
            # Values of the predicted and updated states.
            predictedState = statepred3[:,i-1,n]
            
            # Normalization
            # Predicted state
            normalizedPredictedState = predictedState - minDataTrain
            normalizedPredictedState = normalizedPredictedState/maxDataNormTrain
            # Updated state
            normalizedUpdatedState = updatedState - minDataTrain
            normalizedUpdatedState = normalizedUpdatedState/maxDataNormTrain
            
            
            ###############################################################
            ## DB1
            
            # measure bhattacharrya distance between p(xk/zk-1) and p(xk/sk) 
            predicted_state              = statepred3[:,i-1,n]
            predicted_variance           = Ppred[:,:,i-1,n]
            predicted_cluster_center     = averageNodes[int(activeNodes[n, i-1])]
            predicted_cluster_covariance = covSuperstates[int(activeNodes[n, i-1])]
            
            db1 = CalculateBhattacharyyaDistance(predicted_state, np.diag(predicted_variance), 
                                                 predicted_cluster_center, np.diag(predicted_cluster_covariance))
            
            db1_mean = np.mean(db1)
            
            db1s[n, i] = db1_mean
            
            ###############################################################
            ## DB2
            # measure bhattacharrya distance between p(xk/zk-1) and p(zk/xk) 
            
            db2 = CalculateBhattacharyyaDistance(predicted_state, np.diag(predicted_variance),
                                      currMeas, currVar)
            
            db2_mean = np.mean(db2)
            
            db2s[n, i] = db2_mean
            
            ###############################################################
            
            # Innovations at state level (always calculated anyway, as they are fast to compute)
            # INNOVATIONS AT STATE LEVEL:
            # 0 : full state (mus + err)
            fullStateAnomaly[n, i] = np.mean(np.abs(normalizedPredictedState - normalizedUpdatedState))
            if winningMetric == 0:
                weightsPar[n] = weightscoeff_n[n,i-1]/(fullStateAnomaly[n,i] + 1e-10)
                
            # 1 : state (mus)
            onlyStateAnomaly[n, i] = np.mean(np.abs(normalizedPredictedState[0:numState] - normalizedUpdatedState[0:numState]))
            if winningMetric == 1:
                weightsPar[n] = weightscoeff_n[n,i-1]/(onlyStateAnomaly[n,i] + 1e-10)
            
            # 2 : error/velocity (err)
            onlyErrorAnomaly[n, i] = np.mean(np.abs(normalizedPredictedState[numState:numState*2] - normalizedUpdatedState[numState:numState*2]))
            if winningMetric == 2:
                weightsPar[n] = weightscoeff_n[n,i-1]/(onlyErrorAnomaly[n,i] + 1e-10)
                
            if winningMetric == 6:
                weightsPar[n] = weightscoeff_n[n,i-1]/(db2s[n,i] + 1e-10)
 
            ###################################################################
            ## FOURTH BLOCK (wait for all particles, particle resampling)
            if n == N-1:
    
                # Winning neuron chosen, based on the selected metric
                if winningMetric == 0:
                    innovation_min[i] = np.min(fullStateAnomaly[:, i])
                    index_innov_min = np.argmin(fullStateAnomaly[:, i])
                elif winningMetric == 1:
                    innovation_min[i] = np.min(onlyStateAnomaly[:, i])
                    index_innov_min = np.argmin(onlyStateAnomaly[:, i])
                elif winningMetric == 2:
                    innovation_min[i] = np.min(onlyErrorAnomaly[:, i])
                    index_innov_min = np.argmin(onlyErrorAnomaly[:, i])
                elif winningMetric == 3:
                    innovation_min[i] = np.min(innovationErr[:, i])
                    index_innov_min = np.argmin(innovationErr[:, i])
                elif winningMetric == 6:
                    innovation_min[i] = np.min(db2s[:, i])
                    index_innov_min = np.argmin(db2s[:, i])
                    
                indexes_innov_min[i] = index_innov_min
                    
                # All the metrics, for the winning neuron
                fullStateAnomalyMin[i] = fullStateAnomaly[index_innov_min, i]
                onlyStateAnomalyMin[i] = onlyStateAnomaly[index_innov_min, i]
                onlyErrorAnomalyMin[i] = onlyErrorAnomaly[index_innov_min, i]
                
                db1sMin[i] = db1s[index_innov_min, i]
                db2sMin[i] = db2s[index_innov_min, i]
            
                predictionMuMin[:, i] = statepred3[:, i-1, index_innov_min]
                
                # Saving the cluster of the winning neuron.
                superstateMinInnov[i] = activeNodes[index_innov_min, i-1]
                                
                # Normalize weights in such a way that they all sum 1
                weightsPar = weightsPar/np.sum(weightsPar)  
                # Assign weights
                weightscoeff_n[:,i] = weightsPar  
                

                # Take N random numbers from the discrete distribution
                wRes = random.choices(np.arange(N), weights = weightsPar, k = N)
                
                
                ###############################################################
                ### DISCRETE LEVEL ANOMALY
                
                # Calculation of lambda for discrete-level anomaly:
                # In this way we obtain a value for each superstate that
                # defines a distance between the SUPERSTATE and the OBSERVATION
                covGeneralizedObservation = np.zeros((numState*2, numState*2))
                
                covGeneralizedObservation[0:numState, 0:numState] = obsCovariance
                covGeneralizedObservation[numState:2*numState, numState:2*numState] = 2*obsCovariance # approx
                
                # To fix the fact that covariance matrices could be
                # positive semi-definite, but in the following code, we
                # want them to be definite
                # https://www.mathworks.com/matlabcentral/answers/134774-error-using-chol-matrix-must-be-positive-definite
                
                KLDAbnMax = np.max(KLDabn_all)
                
                
                lambda_ = calculateLamdaS(nSuperStates, currMeas, averageNodes, covGeneralizedObservation, covSuperstates, skewValue)
    
                lambdas[:, i] = lambda_;
                
                
                # Building the histogram of the particles at the previous
                # time instant, i.e. which clusters were chosen
                
                histogram = np.zeros(nSuperStates)
                for h in range(nSuperStates):
                    # histogram(1, h) = sum(activeNodesPrev== h);
                    active_Node_sample = np.where(activeNodes[:, i-1] == h)[0]
                    if active_Node_sample.size != 0:
                        weight = weightsPar[active_Node_sample[0]]
                        histogram[h] = np.sum(activeNodes[:,i-1]== h)*weight
                
                histogram = histogram/(np.sum(histogram))
                
                # totNumOfSuperstates: total number of Superstates
                # N: total number of Particles
                # histogram: histogram at time t-1 (after PF resampling)
                # transitionMat: the transition matrix learned from previous experience
                # probability_lamdaS: probability vector representing a discrete probability disctribution
       
                KLDabn = KLD_Abnormality(nSuperStates, nParticles, histogram, transitionMat, lambda_, KLDAbnMax)
     
                KLDabn_all[i] = KLDabn
                
                # Now KLD abn calculation just for the winner node
                PPwinner = transitionMat[int(activeNodes[int(index_innov_min), i-1]),:] +1e-20 # add 1e-100 since KLD doesnt allow zero values
                QQ = lambda_;
                
                KLD_winner = single_KLD_Abnormality(PPwinner, QQ, KLDAbnMax, 1, 1)
                
                KLD_winners[i] = KLD_winner
    
                
                ###############################################################
                
                activeNodesPrev = activeNodes
                
                for ij in range(N):
                    # REPLACEMENT OF CORRECTED DATA DEPENDING ON
                    # SURVIVING NEURONS
                    
                    tempUpdated = stateUpdated
                    stateUpdated[:,i,ij] = tempUpdated[:,i,wRes[ij]]
                    updatedP1[:,:,i,ij] = updatedP1[:,:, i,wRes[ij]]
                    activeNodesPrev = activeNodes;
                    tempActiveNodes = activeNodes;
                    activeNodes[ij,i] = tempActiveNodes[wRes[ij],i]
                    
                    currState = stateUpdated[:,i,ij]
                              
                    #currP1 = updatedP1(:,:,i,ij);
                    
                    # Weight of particles
                    weightscoeff_n[ij,i] = 1/N                             
                    
                    ###########################################################
                    
                    ## FIFTH BLOCK (interactive of next discrete and continous levels)
                    
                    superstate = int(activeNodes[ij,i])
                    superstate_Mean = meanNodes[superstate, :]
                    
                    U = meanNodes[superstate,numState:numState*2]
                    Q = covSuperstates[superstate]
                    
                    A = np.zeros((numState*2, numState*2))
                    A[0:numState, 0:numState] = np.eye(numState)
                    B = np.zeros((numState*2, numState))
                    B[0:numState, 0:numState] = np.eye(numState)
                    B[numState:numState*2, 0:numState] = np.eye(numState)
                    
                    predMean = np.dot(A, currState) + np.dot(B,U)
                    predCovariance = np.dot(A, np.dot(currP1, np.transpose(A))) + Q
                    
                #Insert in interactive mean and covariance vectors
                statepred3[:, i, ij] = predMean;
                Ppred[:, :, i, ij] = predCovariance;
                    
    
        #######################################################################
        ## SIXTH BLOCK (interactive of next discrete and continous levels)
        if i == firstIt:
            
            superstate = int(activeNodes[n,i])
            
            #  PREDICTION DISCRETE PART (LABELS)
            
            U = meanNodes[superstate,numState:numState*2]
            Q = covSuperstates[superstate]
            
            #  PREDICTION CONTINUOUS PART (LABELS)
            
            A = np.zeros((numState*2, numState*2))
            A[0:numState, 0:numState] = np.eye(numState)
            B = np.zeros((numState*2, numState))
            B[0:numState, 0:numState] = np.eye(numState)
            B[numState:numState*2, 0:numState] = np.eye(numState)
            
            predMean = np.dot(A, currState) + np.dot(B,U)
            predCovariance = np.dot(A, np.dot(currP1, np.transpose(A))) + Q
            
        #Insert in interactive mean and covariance vectors
        statepred3[:, i, n] = predMean;
        Ppred[:, :, i, n] = predCovariance
    
    jump = 1
    if plotBool == True and i > firstIt and (i + 1)%jump == 0:
        
        if i % 100 == 0:
            plt.close('all')
            
            
            #get_ipython().run_line_magic('matplotlib', 'inline')
            
            if winningMetric == 0 :
                nameAnomaly = "full_state_pred"
                fig, axes = plt.subplots(1, 1, figsize=(10, 5))
                axes.plot(fullStateAnomalyMin[2:i])        
                plt.savefig(outputFile + "A_PLOT_" + nameAnomaly + ".png")
                #plt.show()
            
            nameAnomaly = "innovation"
            fig, axes = plt.subplots(1, 1, figsize=(10, 5))
            axes.plot(onlyStateAnomalyMin[2:i])        
            plt.savefig(outputFile + "A_PLOT_" + nameAnomaly + ".png")
            plt.show()
            
            nameAnomaly = "KLD_all_pred"
            fig, axes = plt.subplots(1, 1, figsize=(10, 5))
            axes.plot(KLDabn_all[2:i])        
            plt.savefig(outputFile + "A_PLOT_" + nameAnomaly + ".png")
            plt.show()
            
            nameAnomaly = "KLD_winner_pred"
            fig, axes = plt.subplots(1, 1, figsize=(10, 5))
            axes.plot(KLD_winners[2:i])        
            plt.savefig(outputFile + "A_PLOT_" + nameAnomaly + ".png")
            plt.show()
            
            nameAnomaly = "db1sMin"
            fig, axes = plt.subplots(1, 1, figsize=(10, 5))
            axes.plot(db1sMin[2:i])        
            plt.savefig(outputFile + "\A_PLOT_" + nameAnomaly + ".png")
            plt.show()
            
            for i in range(len(db2sMin)):
                if db2sMin[i] <=16:
                    db2sMin[i] =16
            
            
            nameAnomaly = "db2sMin"
            fig, axes = plt.subplots(1, 1, figsize=(10, 5))
            axes.plot(db2sMin[2:i])        
            plt.savefig(outputFile + "\A_PLOT_" + nameAnomaly + ".png")
            plt.show()
            
            #get_ipython().run_line_magic('matplotlib', 'qt')
            '''
            nameAnomaly = "odometry"
            fig, axes = plt.subplots(1, 1, figsize=(10, 5))
            plt.scatter(data[2:i-1, 0], data[2:i-1, 1], color = 'blue')
            plt.scatter(predictionMuMin[0, i], predictionMuMin[1, i], color = 'red')
            winnerSuperstate = superstateMinInnov[i]
            meanOfSuperstate = meanNodes[int(winnerSuperstate), 0:2]
            plt.scatter(meanNodes[:, 0], meanNodes[:, 1], color = 'yellow')
            plt.scatter(meanOfSuperstate[0], meanOfSuperstate[1], color = 'green')
            for i in range(meanNodes.shape[0]):
                axes.annotate(i, (meanNodes[i, 0], meanNodes[i, 1]))
            plt.title('Scatter plot pythonspot.com')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.savefig(outputFile + str(i) + "A_PLOT_" + nameAnomaly + ".png")
            plt.draw()
            '''
            
            #plt.pause(0.25)

        
        
    
    if (i % 50 == 0) or (i> 500):
        results = fromarrays([superstateMinInnov,
                    onlyErrorAnomalyMin, onlyStateAnomalyMin, fullStateAnomalyMin, KLDabn_all,
                    KLD_winners, db1sMin, db2sMin], 
                    names=['superstateMinInnov', 'onlyErrorAnomalyMin', 'onlyStateAnomalyMin',
                           'fullStateAnomalyMin', 'KLDabn_all', 'KLD_winners', 
                           'db1sMin', 'db2sMin'])
        
    
    '''
        estimationAbn = fromarrays([innovation_min,
                            activeNodes, 
                            predictionMuMin,
                            innovationImgRealPredictedMin, 
                            innovationOFRealPredictedMin, 
                            superstateMinInnov,
                            onlyErrorAnomalyMin, 
                            onlyStateAnomalyMin, 
                            fullStateAnomalyMin, 
                            KLDabn_all,
                            KLD_winners, 
                            MSE_Real_OFs,
                            lambdas], 
                    names=['innovation_min',
                           'activeNodes',
                           'predictionMuMin',
                           'innovationImgRealPredictedMin', 
                           'innovationOFRealPredictedMin',
                           'superstateMinInnov', 
                           'onlyErrorAnomalyMin', 
                           'onlyStateAnomalyMin',
                           'fullStateAnomalyMin', 
                           'KLDabn_all', 
                           'KLD_winners', 
                           'MSE_Real_OFs',
                           'lambdas'])
    '''
    
    nameFile = 'results_test_' + '_odometry_' + '_metric' + str(winningMetric) + '_particles' + str(nParticles) + '_skew' + str(skewValue) + '_thresh' + str(active_node_threshold) +'_testing' + str(testing)
            
    #sio.savemat(nameFile + '.mat', {'results': results})


        
#plt.show()


