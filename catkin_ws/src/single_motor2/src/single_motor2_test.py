#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64

class MyCommander():
	def __init__(self):
		self.count = 0.0
		self.pub = rospy.Publisher("joint1/command",Float64)
		self.timer = rospy.Timer(rospy.Duration(1), self.runner)
	def runner(self, event):
		self.count = (self.count+1) % 2
		self.pub.publish(self.count)


if __name__ == "__main__": 
	rospy.init_node('single_motor_commander')
	node = MyCommander() 
	rospy.spin()
