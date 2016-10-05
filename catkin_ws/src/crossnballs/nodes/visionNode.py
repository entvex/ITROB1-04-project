#!/usr/bin/python

import rospy
from std_msgs.msg import String
import sys

class visionNode:

    def __init__(self):
        self.subVisionBoard = rospy.Subscriber('requestBoard',String,self.callbackVisionBoard)
        self.pubVisionBoard = rospy.Publisher('respondBoard',String)

        self.subVisionMove = rospy.Subscriber('waitForMove',String,self.callbackVisionMove)
        self.pubVisionMove = rospy.Publisher('moveMade',String)

    def callbackVisionBoard(self,data):
        print 'callbackVisionBoard'
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        self.pubVisionBoard(data.data)

    def callbackVisionMove(self,data):
        print 'callbackVisionMove'
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        self.pubVisionMove(data.data)

    def publishVisionBoard(self,data):
        self.pub.publish(data)

    def publishVisionMove(self, data):
        self.pub.publish(data)
    
if __name__ == '__main__':
    visionNode = visionNode()
    rospy.init_node('visionNode', anonymous=False)
    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
