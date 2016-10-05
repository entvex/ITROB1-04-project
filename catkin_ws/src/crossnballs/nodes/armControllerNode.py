#!/usr/bin/python

import rospy
from std_msgs.msg import String
import sys

class ArmControllerNode:

    def __init__(self):
        self.subBrinkPlacement = rospy.Subscriber('requestBrinkPlacement',String,self.callbackBrickPlacment)
        self.pubBrinkPlacement = rospy.Publisher('respondBrickPlacment',String)

    def callbackBrickPlacment(self,data):
        print 'callbackBrickPlacment'
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        self.publish(data.data)

    def publishBrickPlacment(self,data):
        print 'publishBrickPlacment'
        self.pubBrinkPlacement.publish(data)
    
if __name__ == '__main__':
    ArmController = ArmControllerNode()
    rospy.init_node('ArmControllerNode', anonymous=False)
    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
