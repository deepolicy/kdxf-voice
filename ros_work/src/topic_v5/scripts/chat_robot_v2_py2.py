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

import os, time, random

import rospy
from std_msgs.msg import String

import time

# lib for the url connect with get method. 
import urllib2

import base64

import json


def chat( query ):

    print( "query: ", query )

    url = "http://www.tuling123.com/openapi/api?key=c3cd6d5a754d47bd86a0db70b9324e12&info=" + query

    req = urllib2.Request(url)

    url_result = urllib2.urlopen(req).read()
    print( "url_result: ", url_result )
    # url_result:  {"code":100000,"text":"呵呵，苹果维生素含量很高哦！"}

    answer = json.loads( url_result )["text"]
    print( "answer: ", answer )

    return answer



def callback_function(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard:  %s', data.data)

    data_2 = base64.b64decode( str(data.data) )
    print( "data_2: ", data_2 )

    answer = chat( data_2 )
    pub.publish( base64.b64encode( answer.encode("utf-8") ) )




if __name__=='__main__':

    rospy.init_node('ink_control', anonymous=True)

    pub = rospy.Publisher('/inkvoice/text2speech', String, queue_size=10)

    rospy.Subscriber('/inkvoice/speech2text', String, callback_function)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

