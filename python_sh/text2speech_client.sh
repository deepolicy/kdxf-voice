#!/bin/bash

source activate ROS-v2

cd ~/kdxf-voice/ros_work

source devel/setup.bash

cd workspace

rosrun topic_v5 text2speech_client.py 