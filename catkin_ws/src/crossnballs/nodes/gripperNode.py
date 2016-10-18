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
        print 'callbackGrip'
        if data.data == "GRIP":
            self.grip(0.6)
        elif data.data == "RELEASE":
            self.grip(0.3)
        else:
            print "Wrong command given"

        self.pubGripper.publish("done")


    def grip(self, value):
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", value)
        time.sleep(1)
        self.joint_cmd_pub.publish(float(value))
        # TODO Maybe pause here?
        time.sleep(1)

if __name__ == "__main__":
    execfile('/home/ubuntu/ITROB1-04-project/catkin_ws/src/crossnballs/nodes/crossNballsLib.py')
    rospy.init_node("gripper_node_test")
    node = gripper_node()
    time.sleep(1)
    node.grip(0.3)
    rospy.spin()