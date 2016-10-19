#!/usr/bin/python

import rospy
from std_msgs.msg import String
import cv2
import cv2.cv as cv
import numpy as np
import sys
import urllib
import time


class visionNode:
    def __init__(self):
        self.subVisionBoard = rospy.Subscriber(REQUEST_BOARD_KEY, String, self.callbackVisionBoard)
        self.pubVisionBoard = rospy.Publisher(RESPOND_BOARD_KEY, String)

        self.subVisionBrick = rospy.Subscriber(REQUEST_FREEBRICK_KEY, String, self.callbackVisionBrick)
        self.pubVisionBrick = rospy.Publisher(RESPOND_FREEBRICK_KEY, String)

    def callbackVisionBoard(self, data):
        print 'callbackVisionBoard'
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        boardList = self.getBoard()

        self.pubVisionBoard.publish(boardList)

    def callbackVisionBrick(self, data):
        print 'callbackVisionBrick'
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", str(data.data))

        redBricks = []
        blueBricks = []

        if data.data == "red":
            while (len(redBricks) == 0):
                blueBricks, redBricks = self.brickDectetor()
                time.sleep(1)
            print "red brick detected: " + str(redBricks[0][0]) + ", "  + str(redBricks[0][1])
            self.pubVisionBrick.publish( str(redBricks[0][0]) + ", "  + str(redBricks[0][1]) )

        if data.data == "blue":
            while (len(blueBricks) == 0):
                blueBricks, redBricks = self.brickDectetor()
                time.sleep(1)
            self.pubVisionBrick.publish(str(blueBricks[0][0]) + ", " + str(blueBricks[0][1]))

    def getBoard(self):
        print "getBoard"

        validData = False
        while ( not validData ):
            boardList = ["", "", ""]
            for list in range(3):
                board = [0,0,0,0,0,0,0,0,0]
                BlueBricks, RedBricks = self.brickDectetor(boardIncluded=True)

                xlower = [234,285,336,234,285,336,234,285,336]
                xupper = [271,322,379,271,322,379,271,322,379]
                ylower = [90,90,90,145,145,145,196,196,196]
                yupper = [130,130,130,183,183,183,238,238,238]
                i = 0

                for loop in xlower:
                    for RedBrick in RedBricks:
                        if( RedBrick[0] >= xlower[i] and RedBrick[0] <= xupper[i] and RedBrick[1] >= ylower[i] and RedBrick[1] <= yupper[i]):
                            board[i] = 2

                    for BlueBrick in BlueBricks:
                        if( BlueBrick[0] >= xlower[i] and BlueBrick[0] <= xupper[i] and BlueBrick[1] >= ylower[i] and BlueBrick[1] <= yupper[i]):
                            board[i] = 1
                    i = i+1
                for brick in board:
                    boardList[list] = boardList[list] + str(brick) + ","

            if ( boardList[0] == boardList[1] == boardList[2]):
                validData = True

        return boardList[0]

    def brickDectetor(self,boardIncluded=False):
        print "brickDectetor"

        imgOriginal = self.get_from_webcam()
        # cv2.imwrite()
        #imgOrginal = cv2.imread("image.jpg")
        imgcircle = imgOriginal

        imgcircle = cv2.medianBlur(imgcircle, 7)
        #cv2.imshow('medianBlur',imgcircle)
        #cv2.waitKey(100)

        imgGRAY = cv2.cvtColor(imgcircle, cv2.COLOR_BGR2GRAY)
        #cv2.imshow('cvtColor',imgGRAY)
        #cv2.waitKey(100)

        circles = cv2.HoughCircles(imgGRAY, cv.CV_HOUGH_GRADIENT, 1, 25, param1=35, param2=15, minRadius=13,maxRadius=20)

        print "circles: " + str(circles)
        if circles == None:
            return [],[]      # Makes caller try again

        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # draw the outer circle
            cv2.circle(imgcircle, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(imgcircle, (i[0], i[1]), 2, (0, 0, 255), 3)

        cv2.imshow('cvtColor',imgcircle)
        cv2.waitKey(100)

        BlueBricks = []
        RedBricks = []

        for circle in circles[0]:
            #print "x" + str(circle[0]) + "y" + str(circle[1])
            print imgOriginal[circle[1], circle[0]]
            # imgOrginal[circle[1],circle[0]]=[255,255,255]

            # Limits of board
            xMin = 234
            xMax = 379
            yMin = 90
            ymax = 238

            #Excludeds bricks from board if boardIncluded=False
            if (imgOriginal[circle[1], circle[0]][0] > 100):
                if (not boardIncluded and not ( circle[0] >= xMin and circle[0] <= xMax and circle[1] >= yMin and circle[1] <= ymax ) ):
                    BlueBricks.append([circle[0], circle[1]])
                elif (boardIncluded ):
                    BlueBricks.append([circle[0], circle[1]])

            if (imgOriginal[circle[1], circle[0]][2] > 140):
                if (not boardIncluded and not (circle[0] >= xMin and circle[0] <= xMax and circle[1] >= yMin and circle[1] <= ymax)):
                    RedBricks.append([circle[0], circle[1]])
                elif ( boardIncluded ):
                    RedBricks.append([circle[0], circle[1]])


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
            #cv2.imshow('RealImage from webcam',i)
            #cv2.waitKey(100)
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
