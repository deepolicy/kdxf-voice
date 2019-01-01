#!/usr/bin/env python
"""
author: zhouxin, inksci@qq.com

with speedj():
rostopic pub /ur_driver/URScript std_msgs/String -r 125 -- 'speedj([0, 0, 0, 0, 0, 0.5], *acc: double, t: 0.008 )'

Move the robot randomly.

"""

from multiprocessing import Process, Queue
import os, time, random

import rospy
from std_msgs.msg import String

from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint

import threading
import time

import numpy as np




from sensor_msgs.msg import JointState

ur_position = [0]*6
ur_velocity = [0]*6

def callback_joint_states(data):

    global ur_position, ur_velocity, mutex
    if mutex.acquire():    

        ur_position = data.position
        ur_velocity = data.velocity

        mutex.release()

    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data)









if __name__=='__main__':

    rospy.init_node('ink_control', anonymous=True)

    rospy.Subscriber('/joint_states', JointState, callback_joint_states)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
