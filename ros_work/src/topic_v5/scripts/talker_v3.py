#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author: zhouxin, inksci@qq.com

talker
v1: just publish the topic
v2: publish the text received from TCP connection.
v3: without json, pure string
"""

import sys
reload(sys)
sys.setdefaultencoding('utf8')
# https://www.cnblogs.com/QuLory/p/3615584.html

import rospy
from std_msgs.msg import String

import numpy as np

import socket
import threading


def tcplink(sock,addr, pub):
    print('Accept new connection from %s:%s...' % addr)
    sock.send( ('Welcome! 创造').encode() )
    while True:




        data = sock.recv(1024)
        # print("data: ", data)

        data = data.decode( "utf-8" )
        data_str = str( data )
        # data = str( data )

        # # # mys='\xe4\xbd\xa0\xe5\x9c\xa8\xe5\x81'
        mys = data
         
        # sl = list(mys)
        # # print(sl)
        # i=0 
        # while i<len(sl):
        #     s=sl[i]
        #     try:
        #         s=s.encode('raw_unicode_escape').decode('utf-8')
        #         i+=1
        #     except:
        #         #删掉它 
        #         sl.remove(s)
        mys=''.join(mys)

        print( "mys" )

        print(mys)
        # print mys

        # data = mys


        print("data: ", data)
        print("data_str: ", data_str)

        print( ("----").join( str( data ).split("\\u") ) )

        if data == "close":
            break
        else:
            pub.publish( data_str )

            data_send = 'success publish the topic'

        sock.send( data_send.encode() )
    sock.close()
    print('Connection from %s:%s closed.'%addr)

if __name__=='__main__':

    rospy.init_node('ink_control', anonymous=True)

    pub = rospy.Publisher('/voice/speech2text', String, queue_size=10)

    TCP_PORT = 13001
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


