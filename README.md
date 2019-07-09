# kdxf-voice

博智创新工作室

![inksci](https://github.com/inksci/xy_move_dqn/blob/master/assets/inksci-logo.png)

![inksci](https://github.com/inksci/kdxf-voice/blob/master/assets/ubuntu.png)
![inksci](https://github.com/inksci/kdxf-voice/blob/master/assets/kdxf.png)
![inksci](https://github.com/inksci/kdxf-voice/blob/master/assets/ros.png)


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
