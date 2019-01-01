#!/usr/bin/env python
"""
author: zhouxin, inksci@qq.com

talker
v1: just publish the topic
v2: publish the text received from TCP connection.
"""


import rospy
from std_msgs.msg import String

import numpy as np

import socket
import threading

import json

def tcplink(sock,addr, pub):
    print('Accept new connection from %s:%s...' % addr)
    sock.send( ('Welcome!').encode() )
    while True:
        data=sock.recv(1024).decode()
        print("data: ", data)

        data_json = json.loads( data )
        print('data_json["type"]: ', data_json["type"])

        if data_json["type"] == "text":
        	pub.publish( data_json["text"] )

        	data = { 'text': 'success publish the topic' }

        elif data_json["type"] == "close":
            break
        else:
        	data = { 'text': 'else' }
            
        str_json = json.dumps(data)
        sock.send( str_json.encode() )
    sock.close()
    print('Connection from %s:%s closed.'%addr)

if __name__=='__main__':

    rospy.init_node('ink_control', anonymous=True)

    pub = rospy.Publisher('/voice/speech2text', String, queue_size=10)

    TCP_PORT = 13002
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


