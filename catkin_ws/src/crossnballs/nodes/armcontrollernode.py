#!/usr/bin/python

import rospy
from std_msgs.msg import String
import sys

class ArmControllerNode:

    def __init__(self):
        self.sub = rospy.Subscriber('requestBrinkPlacement',String,self.callback)
        self.pub = rospy.Publisher('respondBrickPlacment',String)
        print 'Hey from init'


    def callback(self,data):
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        print data.data
        print 'Hey from callback'
        self.publish("merp")

    def publish(self,data):
        self.pub.publish(data)

    #pub = rospy.Publisher('brink', String, queue_size=10)
    #rospy.init_node('talker', anonymous=True)
    #rate = rospy.Rate(10) # 10hz
    
if __name__ == '__main__':
    ArmController = ArmControllerNode()
    rospy.init_node('ArmControllerNode', anonymous=False)
    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
