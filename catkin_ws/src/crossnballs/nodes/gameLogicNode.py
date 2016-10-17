#!/usr/bin/python

import rospy
from std_msgs.msg import String
import sys
import time

class gameLogic:

    def __init__(self):
        self.board = []
        self.currentBrick = None
        self.waitForResponse = False

        self.subVisionBoard = rospy.Subscriber('respondBoard',String,self.callbackVisionBoard)
        self.pubVisionBoard = rospy.Publisher('requestBoard',String)

        self.subVisionMove = rospy.Subscriber(RESPOND_WAIT_FOR_MOVE_KEY,String,self.callbackVisionMove)
        self.pubVisionMove = rospy.Publisher(REQUEST_WAIT_FOR_MOVE_KEY,String)

        self.subArmController = rospy.Subscriber(RESPOND_BRICKPLACMENT_KEY, String, self.callbackArmController)
        self.pubArmController = rospy.Publisher(REQUEST_BRICKPLACEMENT_KEY,  String)

        self.subVisionBrick = rospy.Subscriber('respondFreeBrick',String,self.callbackVisionBrick)
        self.pubVisionBrick = rospy.Publisher('requestFreeBrick', String)

    def gameloop(self):
        print "gameloop running"

        self.publishVisionBoard("getBoard")
        self.waitResponse()

        #TODO check if board is empty

        self.publishVisionBrick("red")
        self.waitResponse()

        self.publishArmController(self.currentBrick)
        self.waitResponse()




    def waitResponse(self):
        print "waitResponse"
        while self.waitForResponse:
            time.sleep(1)

    def callbackVisionBoard(self,data):
        print 'callbackVisionBoard'
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        self.board = data.data
        self.waitForResponse = False

    def callbackVisionBrick(self,data):
        print 'callbackVisionBrick'
        self.currentBrick = data.data
        self.waitForResponse = False

    def callbackVisionMove(self, data):
        print 'callbackVisionMove'
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        #self.pubVisionMove(data.data)
        self.waitForResponse = False

    def callbackArmController(self,data):
        print 'callbackArmController'
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        #self.pubArmController(data.data)
        self.waitForResponse = False

    def publishVisionBoard(self,data):
        self.waitForResponse = True
        self.pubVisionBoard.publish(data)

    def publishVisionMove(self, data):
        self.waitForResponse = True
        self.pubVisionMove.publish(data)

    def publishVisionBrick(self, data):
        self.waitForResponse = True
        self.pubVisionBrick.publish(data)

    def publishArmController(self, data):
        self.waitForResponse = True
        self.pubVisionBrick.publish(data)
    
if __name__ == '__main__':
    # Always load crossNballsLib first
    execfile('/home/ubuntu/ITROB1-04-project/catkin_ws/src/crossnballs/nodes/crossNballsLib.py')
    gameLogic = gameLogic()
    rospy.init_node('gameLogic', anonymous=False)
    gameLogic.gameloop()
    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
