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

        self.subVisionBoard = rospy.Subscriber(RESPOND_BOARD_KEY,String,self.callbackVisionBoard)
        self.pubVisionBoard = rospy.Publisher(REQUEST_BOARD_KEY,String)

        self.subVisionMove = rospy.Subscriber(RESPOND_WAIT_FOR_MOVE_KEY,String,self.callbackVisionMove)
        self.pubVisionMove = rospy.Publisher(REQUEST_WAIT_FOR_MOVE_KEY,String)

        self.subArmController = rospy.Subscriber(RESPOND_BRICKPLACMENT_KEY, String, self.callbackArmController)
        self.pubArmController = rospy.Publisher(REQUEST_BRICKPLACEMENT_KEY,  String)

        self.subVisionBrick = rospy.Subscriber(RESPOND_FREEBRICK_KEY,String,self.callbackVisionBrick)
        self.pubVisionBrick = rospy.Publisher(REQUEST_FREEBRICK_KEY, String)

    def gameloop(self):
        print "gameloop running"

        self.publishArmController("DEFAULT_POS")
        self.waitResponse()

        self.publishVisionBoard("getBoard")
        self.waitResponse()

        #TODO check if board is empty

        self.publishVisionBrick("red")
        self.waitResponse()

        self.publishArmController(self.currentBrick + ",7") #TODO correct this ,4
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
        print "publishVisionBoard"
        self.waitForResponse = True
        self.pubVisionBoard.publish(data)

    def publishVisionMove(self, data):
        print "publishVisionMove"
        self.waitForResponse = True
        self.pubVisionMove.publish(data)

    def publishVisionBrick(self, data):
        print "publishVisionBrick"
        self.waitForResponse = True
        self.pubVisionBrick.publish(data)

    def publishArmController(self, data):
        print "publishArmController"
        self.waitForResponse = True
        self.pubArmController.publish(data)
    
if __name__ == '__main__':
    # Always load crossNballsLib first
    execfile('/home/ubuntu/ITROB1-04-project/catkin_ws/src/crossnballs/nodes/crossNballsLib.py')
    gameLogic = gameLogic()
    rospy.init_node('gameLogic', anonymous=False)
    time.sleep(1)
    gameLogic.gameloop()
    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
