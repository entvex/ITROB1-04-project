#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64
import time

class gripper_node:
    def __init__(self):
        self.subGripper = rospy.Subscriber(REQUEST_GRIPPER_KEY,String,self.callbackGrip)
        self.pubGripper = rospy.Publisher(RESPOND_GRIPPER_KEY,String)
        self.joint_cmd_pub = rospy.Publisher("/gripper/command", Float64)

    def callbackGrip(self, data):
        if data.data == "GRIP":
            self.grip(0.6)
        elif data.data == "RELEASE":
            self.grip(0.0)
        else:
            print "Wrong command given"

        self.pubGripper.publish("done")


    def grip(self, value):
        time.sleep(1)
        self.joint_cmd_pub.publish(float(value))
        time.sleep(1)

if __name__ == "__main__":
    execfile('/home/ubuntu/ITROB1-04-project/catkin_ws/src/crossnballs/nodes/crossNballsLib.py')
    rospy.init_node("gripper_node")
    node = gripper_node()
    time.sleep(1)
    node.grip(0.0)
    rospy.spin()