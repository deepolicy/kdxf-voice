
# "bash ./" rather than "sh ./"
# https://blog.csdn.net/weishuxiao1/article/details/38386611


gnome-terminal -x bash -c "bash ./roscore.sh;exec bash;"

gnome-terminal -x bash -c "bash ./speech2text_server.sh;exec bash;"

gnome-terminal -x bash -c "bash ./text2speech_client.sh;exec bash;"

gnome-terminal -x bash -c "bash ./text2speech.sh;exec bash;"

gnome-terminal -x bash -c "bash ./chat_robot_v2.sh;exec bash;"

