#!/usr/bin/env python
import os
import time

print "starting base.launch"

os.spawnl(os.P_DETACH, 'roslaunch au_crustcrawler_base base.launch')
time.sleep(3)

print "starting meta.launch"
os.spawnl(os.P_DETACH, 'roslaunch au_crustcrawler_base meta.launch')
time.sleep(3)

print "starting vision"
execfile('/home/ubuntu/ITROB1-04-project/catkin_ws/src/crossnballs/nodes/visionNode.py')

print "gripping"
execfile('/home/ubuntu/ITROB1-04-project/catkin_ws/src/crossnballs/nodes/gripperNode.py')

print "start armcontroller"
execfile('/home/ubuntu/ITROB1-04-project/catkin_ws/src/crossnballs/nodes/armControllerNode.py')

print "start gamelogic"
execfile('/home/ubuntu/ITROB1-04-project/catkin_ws/src/crossnballs/nodes/armControllerNode.py')

#http://stackoverflow.com/questions/19479504/how-can-i-open-two-consoles-from-a-single-script


#!/usr/bin/env python3
import sys
import time
from subprocess import Popen, PIPE, CREATE_NEW_CONSOLE

messages = 'This is Console1', 'This is Console2'

# open new consoles
processes = [Popen([sys.executable, "-c", """import sys
for line in sys.stdin: # poor man's `cat`
    sys.stdout.write(line)
    sys.stdout.flush()
"""],
    stdin=PIPE, bufsize=1, universal_newlines=True,
    # assume the parent script is started from a console itself e.g.,
    # this code is _not_ run as a *.pyw file
    creationflags=CREATE_NEW_CONSOLE)
             for _ in range(len(messages))]

# display messages
for proc, msg in zip(processes, messages):
    proc.stdin.write(msg + "\n")
    proc.stdin.flush()

time.sleep(10) # keep the windows open for a while

# close windows
for proc in processes:
    proc.communicate("bye\n")

#!/usr/bin/env python
"""Show messages in two new console windows simultaneously."""
import sys
import platform
from subprocess import Popen

messages = 'This is Console1', 'This is Console2'

# define a command that starts new terminal
if platform.system() == "Windows":
    new_window_command = "cmd.exe /c start".split()
else:  #XXX this can be made more portable
    new_window_command = "x-terminal-emulator -e".split()

# open new consoles, display messages
echo = [sys.executable, "-c",
        "import sys; print(sys.argv[1]); input('Press Enter..')"]
processes = [Popen(new_window_command + echo + [msg])  for msg in messages]

# wait for the windows to be closed
for proc in processes:
    proc.wait()

