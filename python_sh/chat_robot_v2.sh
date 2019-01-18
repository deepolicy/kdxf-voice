#!/bin/bash

source activate ROS-v2

cd ~/kdxf-voice/ros_work

source devel/setup.bash

cd workspace

rosrun topic_v5 chat_robot_v2.py 