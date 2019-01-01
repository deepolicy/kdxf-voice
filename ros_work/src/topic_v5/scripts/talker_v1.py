#!/usr/bin/env python
"""
author: zhouxin, inksci@qq.com

talker
v1: just publish the topic

"""


import rospy
from std_msgs.msg import String



if __name__=='__main__':

    rospy.init_node('ink_control', anonymous=True)

    pub = rospy.Publisher('/voice/speech2text', String, queue_size=10)

    rate = rospy.Rate(1)

    while not rospy.is_shutdown():

        pub.publish( "123" )

        rate.sleep()
