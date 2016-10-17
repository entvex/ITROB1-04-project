#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64
import time

class single_motor_node:
    def __init__(self):
        self.sub = rospy.Subscriber('requestGrip',Float64,self.callbackGrip)
        self.pub = rospy.Publisher('respondGrip',String)
        self.joint_cmd_pub = rospy.Publisher("/gripper/command", Float64)

    def callbackGrip(self, data):
        print 'callbackGrip'
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        self.joint_cmd_pub.publish(data)
        # TODO Maybe pause here?
        time.sleep(2)
        self.pub.publish("done")

if __name__ == "__main__":
    rospy.init_node("gripper_node_test")
    node = single_motor_node()
    rospy.spin()