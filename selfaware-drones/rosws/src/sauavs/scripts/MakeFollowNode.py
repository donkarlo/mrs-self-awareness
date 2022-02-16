#!/usr/bin/env python3
import rospy
from sauavs.srv import *
from leaderFollower.Leader import Leader



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

    # followType = "innerRectangles"
    # filePathToTrajectory = "/home/donkarlo/mrs_workspace/src/trajectory_loader/sample_trajectories/rectangle30.txt"
    # trajectorySepartor = " "

    # followType = "innerRectanglesTurn4Inside"
    # filePathToTrajectory = "/home/donkarlo/Dropbox/projs/research/data/self-aware-drones/trajectory-points/rectangle30TurnLeft4Pcs-0-5.txt"
    # trajectorySepartor = " "

    # followType = "innerSquaresTurnInside2P7"
    # filePathToTrajectory = "/home/donkarlo/Dropbox/projs/research/data/self-aware-drones/trajectory-points/square30TurnLeft2-7Pcs-0-5.txt"
    # trajectorySepartor = " "

    followType = "innerSquaresTurnInside5"
    filePathToTrajectory = "/home/donkarlo/Dropbox/projs/research/data/self-aware-drones/trajectory-points/square-30-turn-left-5-pcs-0-5.txt"
    trajectorySepartor = " "

    #Ask the leader to publish its GPS odometry
    leader = Leader(followType, filePathToTrajectory, trajectorySepartor)
    leader.gotoFromFileAndWaitFollowerToCome()
    
    #Keeps your node from exiting until the node has been shutdown
    rospy.spin()


