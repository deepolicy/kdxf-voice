from __future__ import print_function
import os
import threading

# os.system("ls > ink-8362.txt")
# os.system("./roscore.sh")

def listener_joint_states():

	pass
	# os.system("./roscore.sh")

listener_thread = threading.Thread( target = listener_joint_states )
listener_thread.setDaemon(True)
listener_thread.start()






def thread_02_fun():
	pass
	# os.system("./speech2text_server.sh")

thread_02 = threading.Thread( target = thread_02_fun )
thread_02.setDaemon(True)
thread_02.start()




print( "\n", "-"*5, "inksci.com", "-"*5, "\n" )

os.system("./speech2text_server.sh")


while 1:

    if not ( listener_thread.isAlive() or thread_02.isAlive() ):
        break;