#!/usr/bin/env python
"""
author: zhouxin, inksci@qq.com

with speedj():
rostopic pub /ur_driver/URScript std_msgs/String -r 125 -- 'speedj([0, 0, 0, 0, 0, 0.5], *acc: double )'

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

qvel_global = [0, 0, 0, 0, 0, 0]
mutex = threading.Lock()

action_ampl = 0.2 # rad/s^2

def talker_4():

    try:
        acc_max = action_ampl*0.008

        pub = rospy.Publisher('/ur_driver/URScript', String, queue_size=10)

        rate = rospy.Rate(125)

        qvel = [0, 0, 0, 0, 0, 0]

        global qvel_global, mutex

        while not rospy.is_shutdown():

            if mutex.acquire():

                for i in range(6):
                    if ( qvel_global[i] - qvel[i] ) > acc_max:
                        qvel[i] += acc_max
                    elif ( qvel_global[i] - qvel[i] ) < -acc_max:
                        qvel[i] -= acc_max
                    else:
                        qvel[i] = qvel_global[i]

                mutex.release()

            pub.publish( "speedj( "+ str( qvel ) +" , "+ str( 0.008 ) +" )" )

            rate.sleep()

    except rospy.ROSInterruptException:
        pass

def talker_4_process(q):

    global qvel_global, mutex

    rospy.init_node('talker_4_process', anonymous=True)
    pub_speed_thread = threading.Thread( target = talker_4 )

    pub_speed_thread.setDaemon(True)

    pub_speed_thread.start()

    try:
        
        rate = rospy.Rate(20)

        while not rospy.is_shutdown():

            if not pub_speed_thread.isAlive():
                break;

            qvel_data = q.get(True)

            if mutex.acquire():
                qvel_global = qvel_data
                mutex.release()

            rate.sleep()

    except rospy.ROSInterruptException:
        pass










from sensor_msgs.msg import JointState

ur_position = [0]*6
ur_velocity = [0]*6

def callback_joint_states(data):

    global ur_position, ur_velocity
    if mutex.acquire():    

        ur_position = data.position
        ur_velocity = data.velocity

        mutex.release()

    # rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data)

def listener_joint_states():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.

    rospy.Subscriber('/joint_states', JointState, callback_joint_states)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()









if __name__=='__main__':
    q = Queue()
    p_talker_4 = Process(target=talker_4_process, args=(q,))
    p_talker_4.start()

    rospy.init_node('ink_control', anonymous=True)

    listener_thread = threading.Thread( target = listener_joint_states )
    listener_thread.setDaemon(True)

    listener_thread.start()

    rate = rospy.Rate(10)

    qvel = [0]*6
    v_lmt = 0.2

    while 1:

        if not listener_thread.isAlive():
            break;

        for i in range(6):

            qvel[i] += ( np.random.rand()*2-1 )* action_ampl*0.1

            qvel[i] = np.clip( qvel[i], -v_lmt, v_lmt )

        q.put( qvel )

        rate.sleep()