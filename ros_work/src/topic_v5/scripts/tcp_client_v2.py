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

    data_2 = base64.b64decode( str("data.data") )
    print( "data_2: ", data_2 )

    tcp_port = 12701

    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    s.connect(('192.168.43.33',tcp_port))

    # print( "received through TCP: ", s.recv(1024).decode())
    print( "received through TCP: ", s.recv(1024).decode("utf-8"))
    

    s.send( data_2 )

    s.close()     
