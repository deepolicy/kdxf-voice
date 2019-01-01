#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
author: zhouxin, inksci@qq.com

Jan. 1, 2019

listen the topic "/inkvoice/text2speech" from ROS, and send the text with TCP.

"""
from __future__ import print_function

import sys
reload(sys)
sys.setdefaultencoding('utf8')
# https://www.cnblogs.com/QuLory/p/3615584.html

import rospy

from std_msgs.msg import String

import numpy as np

import base64


from socket import *


def callback_function(data):
    
    data_2 = base64.b64decode( str(data.data) )
    print( "data_2: ", data_2 )

    HOST ='127.0.0.1'

    PORT = 15001

    BUFFSIZE=1024

    ADDR = (HOST,PORT)

    # connect receive send close

    tctimeClient = socket(AF_INET,SOCK_STREAM)

    tctimeClient.connect(ADDR)

    # print( "received through TCP: ", tctimeClient.recv(BUFFSIZE).decode() )

    tctimeClient.send(data_2.encode())

    tctimeClient.close()


if __name__=='__main__':

    rospy.init_node('ink_control', anonymous=True)

    rospy.Subscriber('/inkvoice/text2speech', String, callback_function)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
