###############################################################################
# Bring the MJPF to python

###############################################################################
# Import of all necessary functions

import os
import random
import warnings

import matplotlib.pyplot as plt
import numpy as np
from IPython import get_ipython

import Config
###############################################################################
# Custom codes
import DefineColors
import DistanceCalculations as DC
import KF
import LoadData as LD

###############################################################################
# This is to say if you want the plots inline or on a separate window

# get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('matplotlib', 'qt')

###############################################################################

warnings.filterwarnings("ignore")

###############################################################################
# Colors for clustering plotting
colors_array = DefineColors.DefineColors()

###############################################################################
# ---------------------------- USER SETTINGS ----------------------------------
###############################################################################

path = os.path.dirname(os.path.abspath(__file__))

# Configuring the settings
config = Config.ConfigureSettings()  # Insert your settings in this file

###############################################################################
# ---------------------------- DATA LOADING  ----------------------------------
###############################################################################

# Loading the VOCABULARY

nClusters, nodesMean, nodesCov, dataColorNode, transitionMat, temporalTransitionMatrix, maxClustersTime = LD.loadVocabulary(
    path,
    config['inputFolder'],
    config['Vocabulary'])
###############################################################################
# Loading the testing data
if config['testing'] == 0:
    dataFile = path + "/" + config['inputFolder'] + "/" + "DataPM.mat"
    pos = LD.loadFile(dataFile)
    pos = np.transpose(pos)
elif config['testing'] == 1:
    dataFile = path + "/" + config['inputFolder'] + "/" + "DataOA.mat"
    pos = LD.loadFile(dataFile)
    pos = np.transpose(pos)
elif config['testing'] == 2:
    dataFile = path + "/" + config['inputFolder'] + "/" + "DataUturn.mat"
    pos = LD.loadFile(dataFile)
    pos = np.transpose(pos)

vel = np.zeros((pos.shape[0], pos.shape[1]))
for i in range(1, pos.shape[0]):
    vel[i, :] = pos[i, :] - pos[i - 1, :]

GS = np.concatenate((pos, vel), axis=1)
data = GS

###############################################################################
# Parameters Used in the Filtering Process

# Length of testing data
dataLength = data.shape[0]
# Number of latent states
GSVDimension = data.shape[1]
# Number of clusters
nSuperStates = nClusters

# Number of particles 
N = config['nParticles'];

skewValue = config['skewValue']

###############################################################################
# Transition matrix
A = np.eye(GSVDimension, GSVDimension)
# Measurement matrix
H = np.eye(GSVDimension, GSVDimension)
# Control input
B = np.zeros((GSVDimension, int(GSVDimension / 2)))
B[0, 0] = 1
B[1, 1] = 1
B[2, 0] = 1
B[3, 1] = 1

###############################################################################
# Generate Observation Noise (Observation Noise): 
# v ~ N(0,R) meaning v is gaussian noise with covariance R
Var_ONoise = 1e-2  # Observation Noise variance % it was = 2
Mu_ONoise = 0  # Observation Noise mean
Std_ONoise = np.sqrt(Var_ONoise)  # Standard deviation of the obs noise

###############################################################################
# Empty values to fill
predicted_superstate = np.zeros((N, dataLength));
predicted_state = np.zeros((GSVDimension, dataLength, N));
predicted_cov_state = np.zeros((GSVDimension, GSVDimension, dataLength, N));
updated_state = np.zeros((GSVDimension, dataLength, N));
updated_cov_state = np.zeros((GSVDimension, GSVDimension, dataLength, N));

predicted_state_resampled = np.zeros((GSVDimension, dataLength, N))
predicted_superstate_resampled = np.zeros((N, dataLength))
updated_state_resampled = np.zeros((GSVDimension, dataLength, N))
updated_cov_state_resampled = np.zeros((GSVDimension, GSVDimension, dataLength, N))
CLA_resampled = np.zeros((N, dataLength))
CLB_resampled = np.zeros((N, dataLength))

w = np.zeros((N, 1))
weightscoeff = np.zeros((N, dataLength))
t = np.zeros((N, 1))

probability_lamdaS = np.zeros((dataLength, nSuperStates))
predicted_superstates = np.zeros((N, dataLength))

# Anomalies
CLA = np.zeros((N, dataLength))
CLB = np.zeros((N, dataLength))
KLDabn_all = np.zeros((dataLength, 1))

histogram_before_update = np.zeros((nSuperStates, dataLength))
histogram_after_update = np.zeros((nSuperStates, dataLength))

discreteEvents_basedOn_LamdaS = np.zeros((dataLength, 1))

min_innovation = np.zeros((dataLength, 1))
minCLAs = np.zeros((dataLength, 1))
minCLBs = np.zeros((dataLength, 1))

###############################################################################
# MAIN LOOP


plt.ion()
# fig, axes = plt.subplots(1, 1, figsize=(10, 5))

fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1, figsize=(20, 10))
fig.suptitle('Positions and anomalies')

# min and max values of position for position plotting
max_pos_x = np.max(data[:, 0])
max_pos_y = np.max(data[:, 1])
min_pos_x = np.min(data[:, 0])
min_pos_y = np.min(data[:, 1])

for i in range(dataLength - 1):

    if config['printCounter'] == True:
        print(str(i) + " out of " + str(dataLength))

    # Gaussian Observation Noise
    ONoise = Std_ONoise * np.random.randn(GSVDimension, 1) + Mu_ONoise * np.ones((GSVDimension, 1))
    OVar = np.var(ONoise)
    R = np.eye(GSVDimension) * OVar

    # ------ INITIAL STEP ------ > #
    if i == 0:  # Initial step
        for n in range(N):

            predicted_state[:, i, n] = np.random.multivariate_normal(data[i, :], R)
            predicted_cov_state_initial = R;
            t[n] = 1
            weightscoeff[n, i] = 1 / N

            # Observe first Measurement Zt
            current_measurement = data[i, :]

            # Calculate Message Back-ward Propagated towards discrete-level (S)
            if n == 0:
                probability_lamdaS[i, :] = DC.calculateLamdaS(nSuperStates, current_measurement, nodesMean, R, nodesCov,
                                                              skewValue)

            predicted_superstate = random.choices(np.arange(nSuperStates), weights=probability_lamdaS[i, :], k=1)[0]
            predicted_superstates[n, i] = predicted_superstate

            ## ------------------------ UPDATE STEP ---------------------------
            # -- update states -- #
            ## during the update kalman computes the posterior p(x[k] | z[1:k]) = N(x[k] | m[k], P[k])
            updated_state[:, i, n], updated_cov_state[:, :, i, n] = KF.kf_update(predicted_state[:, i, n],
                                                                                 predicted_cov_state_initial,
                                                                                 current_measurement, H, R)

            ## ------------------------- ANOMALIES ----------------------------

            ## Calculate Abnormalities
            # -- continuous level -- #
            # measure bhattacharrya distance between p(xk/xk-1) and p(zk/xk)
            CLA[n, i] = DC.CalculateBhattacharyyaDistance(predicted_state[:, i, n],
                                                          np.diag(predicted_cov_state_initial),
                                                          current_measurement, np.diag(R))

            # measure bhattacharrya distance between p(xk/xk-1) and p(xk/sk)

            CLB[n, i] = DC.CalculateBhattacharyyaDistance(predicted_state[:, i, n],
                                                          np.diag(predicted_cov_state_initial),
                                                          nodesMean[predicted_superstate, :],
                                                          np.diag(nodesCov[predicted_superstate]))

            # -- update superstates -- #
            w[n] = weightscoeff[n, i] * probability_lamdaS[i, predicted_superstate]

        ## Calculate Histogram before update
        for ii in range(nSuperStates):
            elements = np.where(predicted_superstates[:, i] == ii)
            histogram_before_update[ii, i] = len(elements[0])

        ## ------------------------- PF Resampling ----------------------------
        w = w / np.sum(w);  # normalize weights
        # multinomial distribution to pick multiple likely particles
        swap_index = random.choices(np.arange(N), weights=w, k=N)
        for n in range(N):
            predicted_state_resampled[:, i, n] = predicted_state[:, i, swap_index[n]]
            predicted_superstate_resampled[n, i] = predicted_superstates[swap_index[n], i]
            updated_state_resampled[:, i, n] = updated_state[:, i, swap_index[n]]
            updated_cov_state_resampled[:, :, i, n] = updated_cov_state[:, :, i, swap_index[n]]
            CLA_resampled[n, i] = CLA[swap_index[n], i]
            CLB_resampled[n, i] = CLB[swap_index[n], i]
        predicted_state = predicted_state_resampled
        predicted_superstates = predicted_superstate_resampled
        updated_state = updated_state_resampled
        updated_cov_state = updated_cov_state_resampled
        CLA = CLA_resampled
        CLB = CLB_resampled
        ## Calculate Histogram after update
        for ii in range(nSuperStates):
            elements = np.where(predicted_superstates[:, i] == ii)
            histogram_after_update[ii, i] = len(elements[0])

        weightscoeff[:, i + 1] = 1 / N

        ## Calculate Abnormalities
        # -- discrete level -- #
        KLDA = DC.KLD_Abnormality(nSuperStates, N, histogram_after_update[:, i], transitionMat,
                                  probability_lamdaS[i, :], KLDAbnMax=10000)
        KLDabn_all[i] = KLDA

        ## Calculate Generalized Errors
        indexMaxLamdaS = np.argmax(probability_lamdaS[i, :])
        discreteEvents_basedOn_LamdaS[i] = indexMaxLamdaS

        # ------ INITIAL STEP ------ < #

    # ------ FOLLOWING STEPS ------ > #  
    if i > 0:

        for n in range(N):
            ## Discrete-Level prediction
            # Select row of transition matrix
            transitionMatRow = transitionMat[int(predicted_superstates[n, i - 1]), :]
            # Considering time matrices, if we have been in a cluster for
            # more than one time instant
            maxTimeCurrentCluster = maxClustersTime[int(predicted_superstates[n, i - 1])]

            if t[n][0] > 1 and t[n][0] < maxTimeCurrentCluster:
                # select the temporal transition matrix related to being
                # in the current cluster for t(n) instances
                curr_temporalTransitionMatrix = temporalTransitionMatrix[int(t[n]), :, :]
                temporalTransitionMatRow = curr_temporalTransitionMatrix[int(predicted_superstates[n, i - 1]), :]
                finalTransitionMatRow = (temporalTransitionMatRow + transitionMatRow) / 2
                finalTransitionMatRow = finalTransitionMatRow / np.sum(finalTransitionMatRow)

            elif t[n][0] > 1 and t[n] >= maxTimeCurrentCluster:
                # select the last temporal transition matrix
                curr_temporalTransitionMatrix = temporalTransitionMatrix[maxTimeCurrentCluster - 1, :, :]
                temporalTransitionMatRow = curr_temporalTransitionMatrix[int(predicted_superstates[n, i - 1]), :]

                # If we have spent more time in the cluster than usual, the
                # probability of all clusters becomes more equal
                # This is to avoid getting stuck in a cluster
                probability_passage_to_all = 1 * np.abs(maxTimeCurrentCluster - t[n][0]) / (N * maxTimeCurrentCluster)

                finalTransitionMatRow = (temporalTransitionMatRow + transitionMatRow) / 2 + probability_passage_to_all
                finalTransitionMatRow = finalTransitionMatRow / np.sum(finalTransitionMatRow)

            else:
                finalTransitionMatRow = transitionMatRow

            # I find probability of next superstate
            probability = random.choices(np.arange(nSuperStates), weights=finalTransitionMatRow, k=1)[0]
            predicted_superstates[n, i] = probability
            predicted_superstate = int(predicted_superstates[n, i])

            # Increasing the time we have spent in the cluster (if we stayed in same cluster)
            if (predicted_superstates[n, i - 1] == predicted_superstates[n, i]):
                t[n] = t[n] + 1  # If same superstate, add 1
            else:
                t[n] = 1  # Else rinizialize by 1

            ## Calculate Histogram before update
            for ii in range(nSuperStates):
                elements = np.where(predicted_superstates[:, i] == ii)
                histogram_before_update[ii, i] = len(elements[0])

            ## Continuous-Level prediction
            # Xt = AXt-1 + BUst-1 + wt
            currentState = updated_state[:, i - 1, n]
            currentCov = updated_cov_state[:, :, i - 1, n]

            U = nodesMean[int(predicted_superstates[n, i - 1]), int((GSVDimension / 2)):GSVDimension]
            Q2 = nodesCov[int(predicted_superstates[n, i - 1])]

            [predicted_state[:, i, n], predicted_cov_state[:, :, i, n]] = KF.kf_predict(currentState, currentCov, A, Q2,
                                                                                        B, U)

            ## Receive new Measurement Zt
            current_measurement = data[i, :]

            ## Calculate Message Back-ward Propagated towards discrete-level (S)
            if n == 0:
                probability_lamdaS[i, :] = DC.calculateLamdaS(nSuperStates, current_measurement, nodesMean, R, nodesCov,
                                                              skewValue)

            ## Calculate Abnormalities
            # -- discrete level -- #
            KLDA = DC.KLD_Abnormality(int(nSuperStates), N, histogram_after_update[:, i - 1], transitionMat,
                                      probability_lamdaS[i, :], KLDAbnMax=10000)
            KLDabn_all[i] = KLDA
            # -- continuous level -- #
            # measure bhattacharrya distance between p(xk/xk-1) and p(zk/xk)
            CLA[n, i] = DC.CalculateBhattacharyyaDistance(predicted_state[:, i, n],
                                                          np.diag(predicted_cov_state[:, :, i, n]),
                                                          current_measurement, np.diag(R))

            # measure bhattacharrya distance between p(xk/xk-1) and p(xk/sk)

            CLB[n, i] = DC.CalculateBhattacharyyaDistance(predicted_state[:, i, n],
                                                          np.diag(predicted_cov_state[:, :, i, n]),
                                                          nodesMean[int(predicted_superstates[n, i - 1]), :],
                                                          np.diag(nodesCov[int(predicted_superstates[n, i - 1])]))

            ## UPDATE STEP
            # -- update states -- #
            ## during the update kalman computes the posterior p(x[k] | z[1:k]) = N(x[k] | m[k], P[k])
            updated_state[:, i, n], updated_cov_state[:, :, i, n] = KF.kf_update(predicted_state[:, i, n],
                                                                                 predicted_cov_state[:, :, i, n],
                                                                                 current_measurement, H, R)

            # -- update superstates -- #
            w[n] = weightscoeff[n, i] * probability_lamdaS[i, predicted_superstate]

        ## ------------------------- PF Resampling ----------------------------
        w = w / np.sum(w);  # normalize weights
        # multinomial distribution to pick multiple likely particles
        swap_index = random.choices(np.arange(N), weights=w, k=N)
        for n in range(N):
            predicted_state_resampled[:, i, n] = predicted_state[:, i, swap_index[n]]
            # predicted_cov_state_resampled[:,:,i,n] = predicted_cov_state[:,:,i,swap_index[n]]
            predicted_superstate_resampled[n, i] = predicted_superstates[swap_index[n], i]
            updated_state_resampled[:, i, n] = updated_state[:, i, swap_index[n]]
            updated_cov_state_resampled[:, :, i, n] = updated_cov_state[:, :, i, swap_index[n]]
            CLA_resampled[n, i] = CLA[swap_index[n], i]
            CLB_resampled[n, i] = CLB[swap_index[n], i]
        predicted_state = predicted_state_resampled
        # predicted_cov_state   = predicted_cov_state_resampled
        predicted_superstates = predicted_superstate_resampled
        updated_state = updated_state_resampled
        updated_cov_state = updated_cov_state_resampled
        CLA = CLA_resampled
        CLB = CLB_resampled
        ## Calculate Histogram after update
        for ii in range(nSuperStates):
            elements = np.where(predicted_superstates[:, i] == ii)
            histogram_after_update[ii, i] = len(elements[0])

        weightscoeff[:, i + 1] = 1 / N

    innovations = predicted_state[:, i, :] - updated_state[:, i, :]
    min_innovation[i] = np.min(np.mean(np.abs(innovations[1:int(GSVDimension / 2), :])))
    minCLA = np.argmin(CLA[:, i])
    minCLAs[i] = CLA[minCLA, i]
    minCLB = np.argmin(CLB[:, i])
    minCLBs[i] = CLB[minCLB, i]

    #######################################################################
    ## PLOTTING

    if i % config['timeStepPlotting'] == 0:  # Plotting every tot seconds

        ax1.plot(KLDabn_all[2:i])
        ax1.set_xlabel('time (s)')
        ax1.set_ylabel('KLDA')

        ax2.plot(min_innovation[2:i])
        ax2.set_xlabel('time (s)')
        ax2.set_ylabel('inn')

        ax3.plot(minCLAs[2:i])
        ax3.set_xlabel('time (s)')
        ax3.set_ylabel('CLA')

        ax4.plot(minCLBs[2:i])
        ax4.set_xlabel('time (s)')
        ax4.set_ylabel('CLB')

        max_inWindow = np.max((0, i - 50))  # take last 50 time instants

        ax5.clear()
        ax5.scatter(data[max_inWindow:i, 0], data[max_inWindow:i, 1])
        ax5.set_xlim([min_pos_x, max_pos_x])
        ax5.set_ylim([min_pos_y, max_pos_y])
        ax5.set_xlabel('x')
        ax5.set_ylabel('y')

        plt.show()
        plt.pause(0.0001)

        # This is instead for single plots inline, in case separate window is
        # too slow

        '''
        fig, axes = plt.subplots(1, 1, figsize=(10, 5))
        axes.plot(KLDabn_all[2:i])        
        plt.show()
        
        fig, axes = plt.subplots(1, 1, figsize=(10, 5))
        axes.plot(min_innovation[2:i])        
        plt.show()
        
        fig, axes = plt.subplots(1, 1, figsize=(10, 5))
        axes.plot(minCLAs[2:i])        
        plt.show()
        
        fig, axes = plt.subplots(1, 1, figsize=(10, 5))
        axes.plot(minCLBs[2:i])        
        plt.show()
        '''
