#!/usr/bin/python

import rospy
from std_msgs.msg import String
import cv2
import cv2.cv as cv
import numpy as np
import sys
import urllib
import math


class visionNode:
    def __init__(self):
        self.subVisionBoard = rospy.Subscriber('requestBoard', String, self.callbackVisionBoard)
        self.pubVisionBoard = rospy.Publisher('respondBoard', String)

        self.subVisionMove = rospy.Subscriber(REQUEST_WAIT_FOR_MOVE_KEY, String, self.callbackVisionMove)
        self.pubVisionMove = rospy.Publisher(RESPOND_WAIT_FOR_MOVE_KEY, String)

        self.subVisionBrick = rospy.Subscriber('requestFreeBrick', String, self.callbackVisionBrick)
        self.pubVisionBrick = rospy.Publisher('respondFreeBrick', String)

    def callbackVisionBoard(self, data):
        print 'callbackVisionBoard'
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        # TODO return correct board status as an array
        self.pubVisionBoard.publish(str(data.data))

    def callbackVisionMove(self, data):
        print 'callbackVisionMove'
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        self.pubVisionMove.publish(data.data)

    # def publishVisionBoard(self,data):
    #    self.pub.publish(data)

    # def publishVisionMove(self, data):
    #    self.pub.publish(data)

    def callbackVisionBrick(self, data):
        print 'callbackVisionBrick'
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", str(data.data))
        blueBricks, redBricks = self.brickDectetor()

        # TODO check that the bricks are free

        if data.data == "red":
            self.pubVisionBrick.publish( str(redBricks[0][0]) + ", "  + str(redBricks[0][1]) )

        if data.data == "blue":
            self.pubVisionBrick.publish(blueBricks[0])

    def brickDectetor(self):
        print "brickDectetor"
        # img = self.get_from_webcam()
        # cv2.imwrite()
        imgOrginal = cv2.imread("image.jpg")
        imgcircle = imgOrginal

        imgcircle = cv2.medianBlur(imgcircle, 7)
        # cv2.imshow('merp',img)

        imgGRAY = cv2.cvtColor(imgcircle, cv2.COLOR_BGR2GRAY)
        # cv2.imshow(" imgGRAY ",imgGRAY)

        circles = cv2.HoughCircles(imgGRAY, cv.CV_HOUGH_GRADIENT, 1, 25, param1=35, param2=15, minRadius=13,
                                   maxRadius=20)

        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # draw the outer circle
            cv2.circle(imgcircle, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(imgcircle, (i[0], i[1]), 2, (0, 0, 255), 3)
        # cv2.imshow('detected circles', img)
        # cv2.waitKey(0)

        # img = cv2.imread("colortest.png")

        BlueBricks = []
        RedBricks = []

        for circle in circles[0]:
            print "x" + str(circle[0]) + "y" + str(circle[1])
            print imgOrginal[circle[1], circle[0]]
            # imgOrginal[circle[1],circle[0]]=[255,255,255]

            if (imgOrginal[circle[1], circle[0]][0] > 160):
                BlueBricks.append([circle[0], circle[1]])

            if (imgOrginal[circle[1], circle[0]][2] > 160):
                RedBricks.append([circle[0], circle[1]])

        # cv2.imshow('detected circles', imgOrginal)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # TODO Look in a region for colors and define better colorRange

        return BlueBricks, RedBricks

    def get_from_webcam(self):
        print "try fetch from webcam..."
        stream = urllib.urlopen('http://192.168.0.20/image/jpeg.cgi')

        bytes = ''
        bytes += stream.read(64500)
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')

        if a != -1 and b != -1:
            jpg = bytes[a:b + 2]
            bytes = bytes[b + 2:]
            i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_COLOR)
            return i
        else:
            print "did not receive image, try increasing the buffer size in line 13:"


if __name__ == '__main__':
    # Always load crossNballsLib first
    execfile('/home/ubuntu/ITROB1-04-project/catkin_ws/src/crossnballs/nodes/crossNballsLib.py')
    visionNode = visionNode()
    rospy.init_node('visionNode', anonymous=False)
    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
