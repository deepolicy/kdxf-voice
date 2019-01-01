#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
author: zhouxin, inksci@qq.com

Support: http://inksci.com/inkvoice

"""
from __future__ import print_function

import sys

# if sys.getdefaultencoding() != 'utf-8':
#     reload(sys)
#     sys.setdefaultencoding('utf-8')
# # https://blog.csdn.net/jewelsu/article/details/78683024

from multiprocessing import Process, Queue
import os, time, random

import rospy
from std_msgs.msg import String

from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint

import threading
import time

import numpy as np

# url get 
import urllib
import urllib2

import base64

import json




mutex = threading.Lock()


def chat( query ):

    print( "query: ", query )

    url = "http://www.tuling123.com/openapi/api?key=c3cd6d5a754d47bd86a0db70b9324e12&info=" + query

    req = urllib2.Request(url)
    print( "req: ", req )

    res_data = urllib2.urlopen(req)
    res = res_data.read()
    print( "res: ", res )
    # res:  {"code":100000,"text":"呵呵，苹果维生素含量很高哦！"}



    answer = json.loads( res )["text"]
    print( "answer: ", answer )

    return answer

def talker_4():

    try:

        pub = rospy.Publisher('/inkvoice/text2speech', String, queue_size=10)

        # rate = rospy.Rate(10)

        # qvel = [0, 0, 0, 0, 0, 0]

        global speech2text, mutex

        while not rospy.is_shutdown():

            publish_text = ""

            if mutex.acquire():

                publish_text = speech2text

                mutex.release()

            if not (publish_text == ""):
                print( "publish_text: ", publish_text )
                answer = chat( base64.b64decode( str(publish_text) ) )
                pub.publish( base64.b64encode( answer.encode("utf-8") ) )
                speech2text = ""


            # rate.sleep()

    except rospy.ROSInterruptException:
        pass








speech2text = ""

def callback_joint_states(data):

    data_2 = base64.b64decode( str(data.data) )
    print( "data_2: ", data_2 )

    global speech2text, mutex
    if mutex.acquire():    
        speech2text = data.data

        mutex.release()

    rospy.loginfo(rospy.get_caller_id() + 'I heard:  %s', data.data)

def listener_joint_states():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.

    rospy.Subscriber('/inkvoice/speech2text', String, callback_joint_states)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()









if __name__=='__main__':

    rospy.init_node('ink_control', anonymous=True)

    listener_thread = threading.Thread( target = listener_joint_states )
    listener_thread.setDaemon(True)
    listener_thread.start()






    pub_speed_thread = threading.Thread( target = talker_4 )
    pub_speed_thread.setDaemon(True)
    pub_speed_thread.start()

    # rate = rospy.Rate(10)

    # qvel = [0]*6
    # v_lmt = 0.2

    while 1:

        if not ( listener_thread.isAlive() or pub_speed_thread.isAlive() ):
            break;

    #     for i in range(6):

    #         qvel[i] += ( np.random.rand()*2-1 )* action_ampl*0.1

    #         qvel[i] = np.clip( qvel[i], -v_lmt, v_lmt )

    #     if mutex.acquire():
    #         qvel_global = qvel
    #         mutex.release()

    #     rate.sleep()