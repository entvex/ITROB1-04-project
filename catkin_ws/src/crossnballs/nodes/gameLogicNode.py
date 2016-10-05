#!/usr/bin/python

import rospy
from std_msgs.msg import String
import sys

class gameLogic:

    def __init__(self):
        self.subVisionBoard = rospy.Subscriber('respondBoard',String,self.callbackVisionBoard)
        self.pubVisionBoard = rospy.Publisher('requestBoard',String)

        self.subVisionMove = rospy.Subscriber('moveMade',String,self.callbackVisionMove)
        self.pubVisionMove = rospy.Publisher('waitForMove',String)

        self.subArmController = rospy.Subscriber('respondBrickPlacement', String, self.callbackArmController)
        self.pubArmController = rospy.Publisher('requestBrinkPlacement',  String)

    def callbackVisionBoard(self,data):
        print 'callbackVisionBoard'
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        self.pubVisionBoard(data.data)

    def callbackVisionMove(self,data):
        print 'callbackVisionMove'
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        self.pubVisionMove(data.data)

    def callbackArmController(self,data):
        print 'callbackArmController'
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        self.pubArmController(data.data)

    def publishVisionBoard(self,data):
        self.pub.publish(data)

    def publishVisionMove(self, data):
        self.pub.publish(data)

    def publishBrickPlacement(self, data):
        self.pub.publish(data)
    
if __name__ == '__main__':
    gameLogic = gameLogic()
    rospy.init_node('gameLogic', anonymous=False)
    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
