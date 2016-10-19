#!/usr/bin/python

import rospy
from std_msgs.msg import String
import sys
import time
import numpy

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


        while(True):

            print "# 1 CHECK IF BOARD IS EMPTY"
            boardNotEmpty = True

            print "Checking Board"
            while boardNotEmpty:
                self.publishVisionBoard("getBoard")
                self.waitResponse()
                time.sleep(1)
                boardNotEmpty = False
                for boardSpot in self.board:
                    # 2 IF NOT EMPTY PRINT ERROR MESSAGE, GO TO 1
                    if boardSpot == '1' or boardSpot == '2':
                        boardNotEmpty = True
                        print "Error: Please remove bricks from board:\n" + str(self.board)


            print "# 2.1 LOOP WHILE BOARD CONTAINS NO 0's AND NO WINNER"
            gameFinished = False
            while not gameFinished:
                gameCheck = self.checkForWin(self.board)
                if gameCheck == "C":
                    print "# 2.2 FIND BEST MOVE"
                    move = self.getRobotMove(self.board, "2", "1")

                    print "# 2.3 ROBOT GET RED BRICK"
                    self.publishVisionBrick("red")
                    self.waitResponse()

                    print "# 2.4 PLACE BRICK"
                    print self.currentBrick
                    self.publishArmController(self.currentBrick + "," + str(move))
                    self.waitResponse()

                    print "# 2.4.1 IF WINNING, GO TO 3"
                    self.publishVisionBoard("getBoard")
                    self.waitResponse()
                    gameCheck = self.checkForWin(self.board)

                    if gameCheck == "C":
                        print "# 2.5 WAIT FOR PLAYER TO MAKE MOVE - WAIT FOR BOARD TO UPDATE TO CONTAIN AS MANY BLUES AS REDS"
                        playerTurn = True

                        while playerTurn:

                            blue = 0
                            red = 0

                            for boardSpot in self.board:
                                if boardSpot == "1":
                                    blue += 1

                                elif boardSpot == "2":
                                    red += 1
                            print "Blue: " + str(blue) + " - Red: " + str(red)

                            if red == blue:
                                playerTurn = False

                            else:
                                time.sleep(2)
                                self.publishVisionBoard("getBoard")
                                self.waitResponse()

                        print "# 2.6 GO TO STEP 2.1"


                else:
                    print "#3 PRINT WINNER MESSAGE, GO TO 1"
                    gameFinished = True

                    if gameCheck == "1":
                        print "Player WINZ! cheating bastard!"
                    elif gameCheck == "2":
                        print "Robot WINS! I am here to steal your ressources!"
                    else:
                        print "It's a TIE! Fuck you..."

                    raw_input("Press enter to play again")



        #self.publishVisionBrick("red")
        #self.waitResponse()


    def waitResponse(self):
        print "waitResponse"
        while self.waitForResponse:
            time.sleep(1)

    def callbackVisionBoard(self,data):
        print 'callbackVisionBoard'
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        self.board = data.data.split(",", 9)
        self.board = numpy.delete(self.board, 9)
        self.waitForResponse = False

    def callbackVisionBrick(self,data):
        print 'callbackVisionBrick'
        print "red brick given: " + data.data
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

    def checkForWin(self, board):
        WIN_OPTIONS = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                       (0, 3, 6), (1, 4, 7), (2, 5, 8),
                       (2, 5, 8), (0, 4, 8), (2, 4, 6))
        for row in WIN_OPTIONS:
            if board[row[0]] == board[row[1]] == board[row[2]] != "0":
                return board[row[0]]
        if "0" not in board:
            return "T"
        return "C"


    def possibleMoves(self,board):
        moves = []
        for square in range(8):
            if board[square] == "0":
                moves.append(square)
        return moves


    def getRobotMove(self, board, brickRobot,brickPlayer):
        board = board[:]
        BEST_MOVES = (4, 8, 6, 0, 2, 1, 3, 5, 7)

        #can I win this turn
        for move in self.possibleMoves(board):
            board[move] = brickRobot
            if self.checkForWin(board) == brickRobot:
                print "found a possible win"
                return move
            board[move] = "0"

        #can player win next turn
        for move in self.possibleMoves(board):
            board[move] = brickPlayer
            if self.checkForWin(board) == brickPlayer:
                print "found a way player can win, blocking this move"
                return move
            board[move] = "0"

        #make the best move
        for move in BEST_MOVES:
            if move in self.possibleMoves(board):
                return move

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
