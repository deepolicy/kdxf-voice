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

 


if __name__=='__main__':

    data = "inksci client with Python"

    data_2 = base64.b64decode( "data" )
    print( "data_2: ", data_2 )

    tcp_port = 12704

    tcp_ip = "192.168.43.33"

    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    s.connect(( tcp_ip ,tcp_port))

    print( "received through TCP: ", s.recv(1024).decode("utf-8"))

    # send and receive.
    s.send( data_2 )
    s.recv(1024).decode("utf-8")

    # send and close.
    s.send( "close" )
    s.close()     
