import numpy as np
import sklearn.metrics as metrics
from cluster.gng.Gng import Gng
from ctumrs.topics.ThreeDPosVelFile import ThreeDPosVelFile

# LOADING THE DATA TO CLUSTER #################################################


# Positional data
fileDataBank = "/home/donkarlo/Dropbox/projs/research/data/self-aware-drones/ctumrs/two-step/manip/pos-vel-obs-from-gps.txt"
t3dposVel = ThreeDPosVelFile(fileDataBank)
inputNpMatrix = t3dposVel.getNpArr()

# PARAMETERS DEFINITION #######################################################

# Number of nodes
maxNodesNumbers = 10

# Iteration (repetition of input data)
iterationMax = 100

#It is after how many datapoints to check if it is necessary to add or delete a node
#Base GNG should have L_Growing (maybe also implemented in some other way), whereas I think L_Decay is related to the GNG-U only
# Growing rate
lGrowing = 1000
# Decay rate should be faster than the growing then it will remove extra nodes
lDecay = 1000

# Movement of winner node
eW = 0.05

# Movement of all other nodes except winner, must be a lot smaller than epsilonB
eN = 0.0006

# Decaying local error and utility: alpha*error
alpha = 0.5

# Decaying local error and utility
delta = 0.9995

# It could be a function of params.lGrowing, e.g., params.LDecay = 2*params.lGrowing
maxAge = 100

# k is used to define when to remove nodes
k = 1.5

plotFlag = True

# CLUSTERING PROCEDURE ########################################################
gng = Gng(inputNpMatrix)
clusterVector = gng.getNormalizedNpMatrix()
normedInputNpMatrix = clusterVector

# Permutation of the rows of the input data vector
permutationValues = np.random.RandomState(seed=2).permutation(gng.getDataRowsNum())
clusterVector = clusterVector[permutationValues, :]

clusterVectorMin = np.min(clusterVector, axis=0)
clusterVectorMax = np.max(clusterVector, axis=0)

# Initialization ##############################################################
# Initial 2 nodes for training the algorithm: The fist two node in GNG initialiazation phase
numOfInitialNodes = 2

# create a matrix with the Ni rows and dimention of data
nodeRefVecs = np.zeros((numOfInitialNodes, gng.getDataColsNum()))
# It returns an array of random numbers generated from the continuous uniform 
# distributions with lower and upper endpoints specified by 'CVmin' and 'CVmax'.
for i in range(numOfInitialNodes):
    nodeRefVecs[i, :] = np.random.uniform(low=clusterVectorMin, high=clusterVectorMax, size=None)

# error
error = np.zeros(numOfInitialNodes)
# utility
utility = np.ones(numOfInitialNodes)
# Connections between nodes
nodeConnections = np.zeros((numOfInitialNodes, numOfInitialNodes))
# Ages of the edges
edgeAges = np.zeros((numOfInitialNodes, numOfInitialNodes))

# Loop ########################################################################
# Counter of cycles inside the algorithm
cycleCountersInsideAlgorithm = 0

# Loop over the number of iterations parameter
for iterationCounter in range(iterationMax):
    print("Iteration " + str(iterationCounter) + " out of " + str(iterationMax))
    print("Number of nodes in current iteration: " + str(nodeRefVecs.shape[0]))
    # Loop over the number of data
    for counter in range(gng.getDataRowsNum()):
        # todo: this section is what I added tp prevent the NAN, bigger h=than float(64) or indefinite
        if counter == 0:
            counter = 1
        # Select Input

        cycleCountersInsideAlgorithm = cycleCountersInsideAlgorithm + 1
        # pick first input vector from permuted inputs
        firstInputVectorFromPermutedInputs = clusterVector[counter, :]

        # COMPETITION AND RANKING
        # pairwise distance between normalized input value and the normalized node means
        X = np.expand_dims(firstInputVectorFromPermutedInputs, axis=0)
        X_state = X[:, 0: int(gng.getDataColsNum() / 2)]
        X_deriv = X[:, int(gng.getDataColsNum() / 2):gng.getDataColsNum()]
        wNorm_state = nodeRefVecs[:, 0: int(gng.getDataColsNum() / 2)]
        # print(wNorm_state)
        wNorm_deriv = nodeRefVecs[:, int(gng.getDataColsNum() / 2):gng.getDataColsNum()]
        d_state = metrics.pairwise_distances(X=X_state, Y=wNorm_state, metric='euclidean')[0][:]
        d_deriv = metrics.pairwise_distances(X=X_deriv, Y=wNorm_deriv, metric='euclidean')[0][:]

        value_state = d_state / np.sum(d_state)
        value_deriv = d_deriv / np.sum(d_deriv)

        d = value_state + value_deriv

        # Organize distances between nodes and the first data point in an ascending order
        SortOrder = np.argsort(d)

        # Closest node index to the first data point
        s1 = SortOrder[0]
        # Second closest node index to the first data point                                              
        s2 = SortOrder[1]

        # Aging
        # Increment the age of all edges emanating from s1
        edgeAges[s1, :] = edgeAges[s1, :] + 1
        edgeAges[:, s1] = edgeAges[:, s1] + 1

        # Add Error
        dist0 = np.power(d[s1], 2)
        dist1 = np.power(d[s2], 2)
        error[s1] = error[s1] + dist0

        # Utility
        # Initial utility is zero in first case and dist is the error of first node
        deltaUtility = dist1 - dist0
        # Difference between error of two nodes
        utility[s1] = utility[s1] + deltaUtility

        # ADAPTATION
        # Move the nearest distance node and it's neibors towards the input signal 
        # by fractions Eb and En resp.
        # 1) move nearest node
        nodeRefVecs[s1, :] = nodeRefVecs[s1, :] + eW * (firstInputVectorFromPermutedInputs - nodeRefVecs[s1, :])

        # Take all the connections of the closest node to the data in question
        Ns1 = np.where(nodeConnections[s1, :] == 1)
        # 2) move neighbors
        # for j in Ns1[0]:
        #    wNorm[j,:] = wNorm[j,:] + epsilon_n*(x-wNorm[j,:])   
        nodeRefVecs[Ns1, :] = nodeRefVecs[Ns1, :] + eN * (firstInputVectorFromPermutedInputs - nodeRefVecs[Ns1, :])

        # Create link
        # If s1 and s2 are connected by an edge , set the age of this edge to 
        # zero , it such edge doesn't exist create it
        nodeConnections[s1, s2] = 1
        nodeConnections[s2, s1] = 1
        # Age of the edge
        edgeAges[s1, s2] = 0
        edgeAges[s2, s1] = 0

        # Remove old links
        # remove edges with an age larger than Amax(a threshold value)
        nodeConnections[edgeAges > maxAge] = 0

        # Number of connections of each node                                                
        nNeighbor = np.sum(nodeConnections, axis=1)
        # Eliminate alone nodes from the C and t matrix and 
        # from wNorm, E and utility vector
        indexAloneNodes = np.where(nNeighbor == 0)
        nodeConnections = np.delete(nodeConnections, (indexAloneNodes), axis=0)
        nodeConnections = np.delete(nodeConnections, (indexAloneNodes), axis=1)
        edgeAges = np.delete(edgeAges, (indexAloneNodes), axis=0)
        edgeAges = np.delete(edgeAges, (indexAloneNodes), axis=1)

        nodeRefVecs = np.delete(nodeRefVecs, (indexAloneNodes), axis=0)
        error = np.delete(error, (indexAloneNodes), axis=0)
        utility = np.delete(utility, (indexAloneNodes), axis=0)

        # ADD NEW NODES at every L_growing

        if ((np.remainder(cycleCountersInsideAlgorithm, lGrowing) == 0) and (nodeRefVecs.shape[0] < maxNodesNumbers)):
            # Determine the unit q with the maximum accumulated error
            q = np.argmax(error)
            # Maximum index related to the error related to a connected node
            figure = np.argmax(nodeConnections[:, q] * error)

            # Total number of nodes
            r = nodeRefVecs.shape[0] + 1
            index_r = r - 1  # to index the new node
            # Insert a new unit r halfway between q and it's neibor f with 
            # the largest error variable
            newNode = (nodeRefVecs[q, :] + nodeRefVecs[figure, :]) / 2
            nodeRefVecs = np.vstack([nodeRefVecs, newNode])

            # Adding one row and column to C and t
            C_temp = np.zeros((r, r))
            C_temp[0:r - 1, 0: r - 1] = nodeConnections
            nodeConnections = C_temp

            t_temp = np.zeros((r, r))
            t_temp[0:r - 1, 0: r - 1] = edgeAges
            edgeAges = t_temp

            # Remove old connections and introduce the presence of the
            # new created node
            nodeConnections[q, figure] = 0  # eliminating connections between the two former neighbors
            nodeConnections[figure, q] = 0
            nodeConnections[q, index_r] = 1  # Creating connections between old nodes and new one
            nodeConnections[index_r, q] = 1
            nodeConnections[index_r, figure] = 1
            nodeConnections[figure, index_r] = 1
            edgeAges[index_r, :] = 0
            edgeAges[:, index_r] = 0

            # Decrease the error variable of q and f by multiplying them with a constant 'alpha'
            error[q] = alpha * error[q]
            error[figure] = alpha * error[figure]
            # Initialize the error of the new node equal to error of the winner node
            newError = error[q]
            error = np.append(error, newError)
            # Decrease the error variable of q and f by multiplying them with a constand 'alpha'
            newUtility = 0.5 * (utility[q] + utility[figure])
            utility = np.append(utility, newUtility)

        # REMOVE NODES at every L_decay

        if (np.remainder(cycleCountersInsideAlgorithm, lDecay) == 0):

            # Maximum accumulated error
            max_E = np.max(error)
            # Node node_useless having minimum utility
            min_utility = np.min(utility)
            node_useless = np.argmin(utility)
            # Utility factor
            CONST = min_utility * k

            if (CONST < max_E):
                # Remove the connection having smaller utility factor
                nodeConnections = np.delete(nodeConnections, (node_useless), axis=0)
                nodeConnections = np.delete(nodeConnections, (node_useless), axis=1)
                # Remove the node having smaller utility factor
                nodeRefVecs = np.delete(nodeRefVecs, (node_useless), axis=0)
                # Remove the min utility value from the utility vector                                  
                utility = np.delete(utility, (node_useless), axis=0)
                # Remove error vector correspond to the node having min utility                              
                error = np.delete(error, (node_useless), axis=0)
                # Remove aging vector correspond to the node having min utility
                edgeAges = np.delete(edgeAges, (node_useless), axis=0)
                edgeAges = np.delete(edgeAges, (node_useless), axis=1)

            # E = alpha*E
            # utility = alpha*utility

        # Decrease errors
        # Decrease error variables by multiplying them with a constant delta
        error = delta * error
        # Decrease the utility by alpha_utility constant
        utility = delta * utility

    dataColorNode = np.zeros(gng.getDataRowsNum())
    for cl in range(gng.getDataRowsNum()):
        firstInputVectorFromPermutedInputs = normedInputNpMatrix[cl, :]
        X = np.expand_dims(firstInputVectorFromPermutedInputs, axis=0)
        d = metrics.pairwise_distances(X=X, Y=nodeRefVecs, metric='euclidean')[0][:]
        minNode = np.argmin(d)
        dataColorNode[cl] = minNode

    wReal = np.zeros((nodeRefVecs.shape[0], nodeRefVecs.shape[1]))
    countPerCluster = np.zeros(nodeRefVecs.shape[0])
    sumPerCluster = np.zeros((nodeRefVecs.shape[0], nodeRefVecs.shape[1]))

    for i in range(gng.getDataRowsNum()):
        currentState = clusterVector[counter, :]
        currentCluster = dataColorNode[i]
        sumPerCluster[int(currentCluster), :] += currentState
        countPerCluster[int(currentCluster)] += 1

    for i in range(nodeRefVecs.shape[0]):
        wReal[i, :] = sumPerCluster[i, :] / countPerCluster[i]

    # if there were no elements belonging to a particular node, we keep it 
    # as it is, but the utility of it is cut to 0
    if countPerCluster[i] == 0:
        wReal[i, :] = nodeRefVecs[i, :]
        utility[i] = 0

    nodeRefVecs = wReal

    if plotFlag == True:  # to ADD
        print("plotting...")

# print number of clusters
print(nodeRefVecs.shape[0])

# print cluster means
print(nodeRefVecs)

gng.plot(nodeRefVecs)
