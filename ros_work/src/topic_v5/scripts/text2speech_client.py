#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
author: zhouxin, inksci@qq.com

Jan. 1, 2019

listen the topic "/inkvoice/text2speech" from ROS, and send the text with TCP.

"""
from __future__ import print_function

import rospy

from std_msgs.msg import String

import numpy as np

import base64

import socket

def callback_function(data):
    
    data_2 = base64.b64decode( str(data.data) )
    print( "data_2: ", data_2 )

    tcp_port = 15001

    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    s.connect(('127.0.0.1',tcp_port))

    print( "received through TCP: ", s.recv(1024).decode())

    s.send( data_2 )

    s.close()        


if __name__=='__main__':

    rospy.init_node('ink_control', anonymous=True)

    rospy.Subscriber('/inkvoice/text2speech', String, callback_function)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
