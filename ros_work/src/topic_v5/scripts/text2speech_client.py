#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""



author: zhouxin, inksci@qq.com

listen the topic "/inkvoice/text2speech" from ROS, and send the text with TCP.

"""
from __future__ import print_function


import sys

# https://www.cnblogs.com/QuLory/p/3615584.html


# if sys.getdefaultencoding() != 'utf-8':
#     reload(sys)
#     sys.setdefaultencoding('utf-8')
# # https://blog.csdn.net/jewelsu/article/details/78683024


import rospy
from std_msgs.msg import String

import numpy as np

import threading

import base64

import socket





mutex = threading.Lock()

text2speech = ""

def callback_function(data):
    
    data_2 = base64.b64decode( str(data.data) )
    print( "data_2: ", data_2 )

    rospy.loginfo(rospy.get_caller_id() + 'I heard: %s', data.data)


    global text2speech, mutex
    if mutex.acquire():    
        text2speech = data.data



        mutex.release()





    tcp_port = 15001

    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    s.connect(('127.0.0.1',tcp_port))

    print( s.recv(1024).decode())

    s.send( data_2 )
    # s.send( "请问你想查询哪个城市".encode("utf-8") )


    # str_recv = s.recv(1024).decode()
    
    # data_json = json.loads( str_recv )
    
    # state_dim = data_json["state_dim"]
    # action_dim = data_json["action_dim"]
    # DoF = data_json["DoF"]
    # max_steps = data_json["max_steps"]
    # action_ampl = data_json["action_ampl"]
    # v_lmt = data_json["v_lmt"]
    # time_step = data_json["time_step"]

    # s.send('exit')
    s.close()        







def listener_thread():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.

    rospy.Subscriber('/inkvoice/text2speech', String, callback_function)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()









if __name__=='__main__':

    rospy.init_node('ink_control', anonymous=True)

    listener_thread = threading.Thread( target = listener_thread )
    listener_thread.setDaemon(True)
    listener_thread.start()


    while 1:

        if not ( listener_thread.isAlive() ):
            break;
