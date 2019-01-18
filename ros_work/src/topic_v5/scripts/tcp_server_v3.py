#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author: zhouxin, inksci@qq.com

Jan. 1, 2019

"""

from __future__ import print_function

import sys
reload(sys)
sys.setdefaultencoding('utf8')
# https://www.cnblogs.com/QuLory/p/3615584.html

import rospy
from std_msgs.msg import String

import numpy as np

import socket
import threading

import base64

def tcplink(sock, addr, pub):
    print('Accept new connection from %s:%s...' % addr)
    sock.send( ('Welcome! 欢迎使用！').encode() )
    while True:

        data = sock.recv(1024)

        data = data.decode( "utf-8" )
        print("data: ", data)

        data_b64 = base64.b64encode( data )

        print( "data_b64: ", data_b64 )
        # print( base64.b64decode( data_b64 ) )

        if data == "close":
            sock.close()
            print('Connection from %s:%s closed.'%addr)
            break
        else:

            pub.publish( str( data_b64 ) )
            # data: "6Iu55p6c5aW95ZCD5ZCX77yf"

            data_send = 'successfully publish the topic!'

            sock.send( data_send )

if __name__=='__main__':

    rospy.init_node('ink_control', anonymous=True)

    pub = rospy.Publisher('/inkvoice/speech2text', String, queue_size=10)

    TCP_PORT = 12601
    #Create The Socket
    my_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    #Listen The Port
    my_sock.bind(('',TCP_PORT))
    my_sock.listen(5)
    print( 'TCP_PORT: ', TCP_PORT, " , ", 'Waiting for connection...')
        
    while True:
        # Accept A New Connection
        sock,addr = my_sock.accept()
        
        # Create A New Thread to Deal with The TCP Connection
        threading.Thread(target=tcplink(sock,addr, pub)).start()


