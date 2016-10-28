# ITROB1-04-project

Disclaimer:

These were hacks made for / during the lesson and are not gold standard / best practise, nicely documented or in any way production ready code to be used for anything else but my own learning in this class. The code will not be updated for ROS versions.

Please see Collaborators/members to see the people who worked on this project.

Launching the nodes robot
-----------
	roslaunch au_crustcrawler_base base.launch

in another terminal after the base has been successfully brought up

	roslaunch au_crustcrawler_base meta.launch

The meta has launched and exited again start rosserial if you have an arduino with two LEDS and a button run

	rosrun rosserial_python serial_node.py /dev/ttyUSB1
  
 Then change folder to 
 
 	cd catkin_ws/src/crossnballs/nodes/
 
 and run the nodes by using
 
  	./startall.sh
  
