# kdxf-voice

## 博智创新工作室

![inksci](https://github.com/inksci/xy_move_dqn/blob/master/assets/inksci-logo.png)

![inksci](https://github.com/inksci/kdxf-voice/blob/master/assets/ubuntu.png)
![inksci](https://github.com/inksci/kdxf-voice/blob/master/assets/kdxf.png)
![inksci](https://github.com/inksci/kdxf-voice/blob/master/assets/ros.png)


<<<<<<< HEAD
软件路径：
将kdxf-voice文件夹放在~/文件夹下，即：~/kdxf-voice

运行环境：

### 1(ROS)
Python 3.6
(conda.env: conda create -n kdxf-voice-v1 python=3.6)

roscore: 不需要特殊依赖。

speech2text_server.py: ros的python包。
pip install -U rosdep rosinstall_generator wstool rosinstall six vcstools

### 2(http socket)
pip install bottle_websocket


更多...
发音调用系统的软件。
=======
### 测试系统的录音功能
rec -c 1 -U -r 8000 -2 radio.wav trim 0 00:30

将会进行 30 秒的录音：

In:0.00% 00:00:***30***.72 [00:00:00.00] Out:240k  [      |      ]        Clip:0    
Done.

代码使用了 conda，相应的环境名为：Ros-v2

### 将 github 代码部署到 ~/kdxf-voice/ 文件夹下

则 ros 工作路径为：
~/kdxf-voice/ros_work

![inksci](https://github.com/inksci/kdxf-voice/blob/master/assets/kdxf-voice.png)

运行 ~/kdxf-voice/python_sh 文件夹下的 python 脚本：

bat_run.sh        roscore.sh             

- chat_robot_v2.sh 

机器人聊天系统，接收 ros 中发布的文本消息，得到相应的回答并发送到 ros 系统中。


sh_test                


- text2speech_client.sh




py_run.py         

- speech2text.sh

kdxf 语音识别模块。运行 kdxf 的 c 程序，将来自麦克风的语音转化成文本。


- speech2text_server.sh  

python 话题发布模块。将来自 ***kdxf 语音识别模块*** 提交的文本发布到 ros 话题中。


- text2speech_client.sh

python 话题监听模块。将从 ros 中监听到的文本发送给 ***kdxf 语音合成模块***。

- text2speech.sh

kdxf 语音合成模块。运行 kdxf 的 c 程序，将文本合成语音并播放。

>>>>>>> ed68052fa8e442f8a61c82741ae3a44c3bb1ef05
