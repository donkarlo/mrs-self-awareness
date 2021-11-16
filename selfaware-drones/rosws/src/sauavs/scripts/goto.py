#!/usr/bin/env python

from __future__ import print_function

import sys
import rospy
from beginner_tutorials.srv import *
import random

def goto(x, y , z, h):
    rospy.wait_for_service('/uav1/control_manager/goto')
    try:
        gotoService = rospy.ServiceProxy('/uav1/control_manager/goto', Vec4)
        gotoResponse = gotoService([x, y , z, h])
        return gotoResponse
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

def usage():
    return "%s [x y]"%sys.argv[0]

if __name__ == "__main__":
    x = random.randint(1, 20)
    y = random.randint(1, 20)
    print(x)
    print( " " )
    print(y)
    gotoResponse = goto(x, y,10,11)
    print("")
