#!/usr/bin/env python3

import sys
import rospy
from sauavs.srv import *
from std_msgs.msg import String
from nav_msgs.msg import Odometry
import random
import time
import itertools
from leaderFollower.InnerSquares import InnerSquares
from leaderFollower.InnerSquaresTurnLeft4Inside import InnerSquaresTurnLeft4Inside
from leaderFollower.InnerSquaresTurnInside2P7 import InnerSquaresTurnInside2P7
from leaderFollower.InnerSquaresTurnInside5 import InnerSquaresTurnInside5


class Follower:
    counter = 0

    def __init__(self, followType):
        self._followType = followType
        self.__id = "uav2"

    def followLeaderCallBack(self, leaderOdometryNavMsg: Odometry) -> None:
        Follower.counter += 1

        leaderPos = leaderOdometryNavMsg.pose.pose.position

        followerPosX = None
        followerPosY = None
        followerPosZ = None

        ### Add the logic of new shapes herer
        if self._followType == "circle":
            followerPosX = leaderPos.x * 0.5
            followerPosY = leaderPos.y * 0.5
            followerPosZ = leaderPos.z
            followerHeading = 11
        elif self._followType == "lineNextTo":
            followerPosX = leaderPos.x
            followerPosY = leaderPos.y + 10
            followerPosZ = leaderPos.z
            followerHeading = 11
        elif self._followType == "lineFollow":
            followerPosX = leaderPos.x - 3
            followerPosY = leaderPos.y
            followerPosZ = leaderPos.z
            followerHeading = 11
        elif self._followType == "innerRectangles":
            innerRectangles = InnerSquares()
            followerPosX, followerPosY, followerPosZ, followerHeading = innerRectangles.getXyz(leaderOdometryNavMsg)
        elif self._followType == "innerRectanglesTurn4Inside":
            innerSquaresTurnLeft4Inside = InnerSquaresTurnLeft4Inside()
            followerPosX, followerPosY, followerPosZ, followerHeading = innerSquaresTurnLeft4Inside.getXyz(leaderOdometryNavMsg)
        elif self._followType == "innerSquaresTurnInside2P7":
            innerSquaresTurnInside2P7 = InnerSquaresTurnInside2P7()
            followerPosX, followerPosY, followerPosZ, followerHeading = innerSquaresTurnInside2P7.getXyz(leaderOdometryNavMsg)
        elif self._followType == "innerSquaresTurnInside5":
            innerSquaresTurnInside5 = InnerSquaresTurnInside5()
            followerPosX, followerPosY, followerPosZ, followerHeading = innerSquaresTurnInside5.getXyz(leaderOdometryNavMsg)
        if followerPosX is not None and followerPosY is not None and followerPosZ is not None:
            print("Leader: follow me to ({},{},{})".format(followerPosX, followerPosY, followerPosZ))
            # Change this line top change the frequency of the messages from the leader
            if Follower.counter % 10 == 0:
                rospy.wait_for_service('/{}/control_manager/goto'.format(self.__id))
                try:
                    # Vec4 is self defined in srv dir. I found the definition here: https://ctu-mrs.github.io/mrs_msgs/srv/Vec4.html
                    uav2GotoService = rospy.ServiceProxy('/{}/control_manager/goto'.format(self.__id), Vec4)
                    uav2GotoServiceResponse = uav2GotoService(
                        [followerPosX, followerPosY, followerPosZ, followerHeading])
                    if uav2GotoServiceResponse.success == True:
                        print(
                            "Follower: I started to go to ({},{},{})".format(followerPosX, followerPosY, followerPosZ))
                    return uav2GotoServiceResponse.success
                except rospy.ServiceException as e:
                    print("Service call failed: %s" % e)