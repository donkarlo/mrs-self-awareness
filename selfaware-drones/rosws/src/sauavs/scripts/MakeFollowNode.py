#!/usr/bin/env python3

import sys
import rospy
from sauavs.srv import *
from std_msgs.msg import String
from nav_msgs.msg import Odometry
import random
import time
import itertools

class Follower:
    counter = 0
    def __init__(self, followType):
        self._followType = followType

    def followLeaderCallBack(self,LeaderOdometryNavMsg:Odometry)->None:
        Follower.counter += 1

        uav1Position = LeaderOdometryNavMsg.pose.pose.position
        
        uav2X = None
        uav2Y = None 
        uav2Z = None

        ### Add the logic of new shapes herer
        if self._followType == "circle":
            uav2X = uav1Position.x * 0.5
            uav2Y = uav1Position.y * 0.5 
        elif self._followType == "lineNextTo":
            uav2X = uav1Position.x
            uav2Y = uav1Position.y + 10
        elif self._followType == "lineFollow":
            uav2X = uav1Position.x - 3
            uav2Y = uav1Position.y
        elif self._followType == "innerRectangles":
            tol=0.5
            if uav1Position.x<-5 and uav1Position.x>-15 and uav1Position.y>5 and uav1Position.y<15:
                # Region 1
                uav2X = -5
                uav2Y = 5
            elif uav1Position.x>-5 and uav1Position.x<5 and uav1Position.y<15+tol and uav1Position.y>15-tol:
                # Region 2
                uav2X = uav1Position.x
                uav2Y = uav1Position.y -10
            elif uav1Position.x>5 and uav1Position.x<15 and uav1Position.y>5 and uav1Position.y<15:
                # Region 3
                uav2X = 5
                uav2Y = 5
            elif uav1Position.x>15-tol and uav1Position.x<15+tol and uav1Position.y<5 and uav1Position.y>-5:
                # Region 4
                uav2X = uav1Position.x - 10
                uav2Y = uav1Position.y
            elif uav1Position.x>5 and uav1Position.x<15 and uav1Position.y<-5 and uav1Position.y>-15:
                # Region 5
                uav2X = 5
                uav2Y = -5
            elif uav1Position.x<5 and uav1Position.x>-5 and uav1Position.y>-15-tol and uav1Position.y<-15+tol:
                # Region 6
                uav2X = uav1Position.x
                uav2Y = uav1Position.y+10
            elif uav1Position.x<-5 and uav1Position.x>-15 and uav1Position.y<-5 and uav1Position.y>-15:
                # Region 7
                uav2X = -5
                uav2Y = -5
            elif uav1Position.x<-15+tol and uav1Position.x>-15-tol and uav1Position.y>-5 and uav1Position.y<5:
                # Region 8
                uav2X = uav1Position.x +10
                uav2Y = uav1Position.y
        
        uav2Z = uav1Position.z
        uav2H = 11

        if uav2X is not None and uav2Y is not None and uav2Z is not None:
            print ("Leader: follow me to ({},{},{})".format(uav2X,uav2Y,uav2Z))   
            # Change this line top change the frequency of the messages from the leader
            if Follower.counter%10 == 0:
                rospy.wait_for_service('/uav2/control_manager/goto')
                try:
                    #Vec4 is self defined in srv dir. I found the definition here: https://ctu-mrs.github.io/mrs_msgs/srv/Vec4.html
                    uav2GotoService = rospy.ServiceProxy('/uav2/control_manager/goto', Vec4)
                    uav2GotoServiceResponse = uav2GotoService([uav2X, uav2Y , uav2Z, uav2H])
                    if uav2GotoServiceResponse.success == True:
                        print ("Follower: I started to go to ({},{},{})".format(uav2X,uav2Y,uav2Z))
                    return uav2GotoServiceResponse.success
                except rospy.ServiceException as e:
                    print("Service call failed: %s"%e)

class Leader:
    '''
    '''
    def __init__(self,followType, pathToTrjectoryPoints,trajectoryPointsSeparator = ' '):
        self._followType = followType
        self._pathToTrjectoryPoints = pathToTrjectoryPoints
        self._trajectoryPointsSeparator = trajectoryPointsSeparator
    
    def publishGPSOdometryTopic(self):
        '''
        Asking the leader to publish its GPS odometry topic
        '''
        f = Follower(self._followType)
        return rospy.Subscriber("/uav1/odometry/odom_gps", Odometry, f.followLeaderCallBack, queue_size=10)

    def getTrajectoryPoints(self):
        #Load trajectory file into an trajectoryArray
        
        file1 = open(self._pathToTrjectoryPoints , 'r')
        Lines = file1.readlines()
        trajectoryPoints = []
        for line in Lines:
            splitted = line.split(self._trajectoryPointsSeparator )
            splittedFloats = [float(splitted[0])
                ,float(splitted[1])
                ,float(splitted[2])
                ,float(splitted[3])]
            trajectoryPoints.append(splittedFloats)
        return trajectoryPoints

    def gotoFromFileAndWaitFollowerToCome(self):

        self.publishGPSOdometryTopic()
        trajectoryPoints = self.getTrajectoryPoints()
        for trajectoryPoint in itertools.cycle(trajectoryPoints):
            try:
                rospy.wait_for_service('/uav1/control_manager/goto')
                uav1GotoService = rospy.ServiceProxy('/uav1/control_manager/goto', Vec4)
                gotoServiceResponse = uav1GotoService([trajectoryPoint[0]
                    , trajectoryPoint[1] 
                    , trajectoryPoint[2]
                    , trajectoryPoint[3]])
                print("Leader: My MPC takes me to ({},{},{})".format(trajectoryPoint[0],trajectoryPoint[1],trajectoryPoint[2]))
                #change this to change how quick the leader moves from one point to the other
                rospy.sleep(1)
            except rospy.ServiceException as e:
                print("Service call failed: %s"%e)


if __name__ == "__main__":
    #init the node
    rospy.init_node('MakeFollowNode', anonymous=True)

    ### comment and uncomment to change the trajectory 
    # followType = "lineNextTo"
    # filePathToTrajectory = "/home/donkarlo/mrs_workspace/src/trajectory_loader/sample_trajectories/LineFromX0ToStep05Return.txt"
    # trajectorySepartor = " "

    # followType = "lineFollow"
    # filePathToTrajectory = "/home/donkarlo/mrs_workspace/src/trajectory_loader/sample_trajectories/LineFromX0ToStep05Return.txt"
    # trajectorySepartor = " "
    
    # followType = "circle"
    # filePathToTrajectory = "/home/donkarlo/mrs_workspace/src/trajectory_loader/sample_trajectories/circle_10_5.txt"
    # trajectorySepartor = ","

    followType = "innerRectangles"
    filePathToTrajectory = "/home/donkarlo/mrs_workspace/src/trajectory_loader/sample_trajectories/rectangle30.txt"
    trajectorySepartor = " "
    
    #Ask the leader to publish its GPS odometry
    leader = Leader(followType, filePathToTrajectory, trajectorySepartor)
    leader.gotoFromFileAndWaitFollowerToCome()
    
    #Keeps your node from exiting until the node has been shutdown
    rospy.spin()