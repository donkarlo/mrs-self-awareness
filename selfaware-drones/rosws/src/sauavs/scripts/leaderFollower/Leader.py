#!/usr/bin/env python3

import sys
import rospy
from sauavs.srv import *
from std_msgs.msg import String
from nav_msgs.msg import Odometry
import random
import time
import itertools
from leaderFollower.Follower import Follower
import sys

class Leader:
    '''
    '''

    def __init__(self, followType, pathToTrjectoryPoints, trajectoryPointsSeparator=' '):
        self._followType = followType
        self._pathToTrjectoryPoints = pathToTrjectoryPoints
        self._trajectoryPointsSeparator = trajectoryPointsSeparator
        self.__id = "uav1"

    def publishGPSOdometryTopic(self):
        '''
        Asking the leader to publish its GPS odometry topic
        '''
        f = Follower(self._followType)
        return rospy.Subscriber("/{}/odometry/odom_gps".format(self.__id), Odometry, f.followLeaderCallBack, queue_size=10)

    def getTrajectoryPoints(self):
        # Load trajectory file into an trajectoryArray

        file1 = open(self._pathToTrjectoryPoints, 'r')
        Lines = file1.readlines()
        trajectoryPoints = []
        for line in Lines:
            splitted = line.split(self._trajectoryPointsSeparator)
            splittedFloats = [float(splitted[0])
                , float(splitted[1])
                , float(splitted[2])
                , float(splitted[3])]
            trajectoryPoints.append(splittedFloats)
        return trajectoryPoints

    def gotoFromFileAndWaitFollowerToCome(self):

        self.publishGPSOdometryTopic()
        trajectoryPoints = self.getTrajectoryPoints()
        for trajectoryPoint in itertools.cycle(trajectoryPoints):
            try:
                rospy.wait_for_service('/{}/control_manager/goto'.format(self.__id))
                uav1GotoService = rospy.ServiceProxy('/{}/control_manager/goto'.format(self.__id), Vec4)
                gotoServiceResponse = uav1GotoService([trajectoryPoint[0]
                                                          , trajectoryPoint[1]
                                                          , trajectoryPoint[2]
                                                          , trajectoryPoint[3]])
                print("Leader: My MPC takes me to ({},{},{})".format(trajectoryPoint[0], trajectoryPoint[1],
                                                                     trajectoryPoint[2]))
                # change this to change how quick the leader moves from one point to the other
                rospy.sleep(1)
            except rospy.ServiceException as e:
                print("Service call failed: %s" % e)