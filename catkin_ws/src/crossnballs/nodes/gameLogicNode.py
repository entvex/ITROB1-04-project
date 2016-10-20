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
        self.gameOver = False

        self.subVisionBoard = rospy.Subscriber(RESPOND_BOARD_KEY,String,self.callbackVisionBoard)
        self.pubVisionBoard = rospy.Publisher(REQUEST_BOARD_KEY,String)

        self.subArmController = rospy.Subscriber(RESPOND_BRICKPLACMENT_KEY, String, self.callbackArmController)
        self.pubArmController = rospy.Publisher(REQUEST_BRICKPLACEMENT_KEY,  String)

        self.subVisionBrick = rospy.Subscriber(RESPOND_FREEBRICK_KEY,String,self.callbackVisionBrick)
        self.pubVisionBrick = rospy.Publisher(REQUEST_FREEBRICK_KEY, String)

        self.pubArduino = rospy.Publisher("requestArduino",String)
        self.subArduino = rospy.Subscriber("respondArduino",String,self.callbackArduino)

    def gameloop(self):
        print "gameloop running"


        self.publishArmController("DEFAULT_POS")
        self.waitResponse()


        while(True):



            print "# 1 CHECK IF BOARD IS EMPTY"
            boardNotEmpty = True

            print "Checking Board"
            while boardNotEmpty:
                self.publishVisionBoard(GET_BOARD)
                self.waitResponse()
                time.sleep(1)
                boardNotEmpty = False
                print "2 IF NOT EMPTY PRINT ERROR MESSAGE, GO TO 1"
                for boardSpot in self.board:
                    if boardSpot == BLUE_SLOT or boardSpot == RED_SLOT:
                        boardNotEmpty = True
                        print "Error: Please remove bricks from board:\n" + str(self.board)


            print "# 2.1 LOOP WHILE BOARD CONTAINS NO 0's AND NO WINNER"
            gameFinished = False
            while not gameFinished:
                self.pubArduino.publish("red")
                gameCheck = self.checkForWin(self.board)
                if gameCheck == CONTINUE_GAME:
                    print "# 2.2 FIND BEST MOVE"
                    move = self.getRobotMove(self.board, RED_SLOT, BLUE_SLOT)

                    print "# 2.3 ROBOT GET RED BRICK"
                    self.publishVisionBrick(BRICK_RED)
                    self.waitResponse()

                    print "# 2.4 PLACE BRICK"
                    print self.currentBrick
                    self.publishArmController(self.currentBrick + "," + str(move))
                    self.waitResponse()

                    print "# 2.4.1 IF WINNING, GO TO 3"
                    self.publishVisionBoard(GET_BOARD)
                    self.waitResponse()
                    gameCheck = self.checkForWin(self.board)

                    if gameCheck == CONTINUE_GAME:
                        print "# 2.5 WAIT FOR PLAYER TO MAKE MOVE - WAIT FOR BOARD TO UPDATE TO CONTAIN AS MANY BLUES AS REDS"
                        self.pubArduino.publish("green")
                        playerTurn = True

                        while playerTurn:

                            blue = 0
                            red = 0

                            for boardSpot in self.board:
                                if boardSpot == BLUE_SLOT:
                                    blue += 1

                                elif boardSpot == RED_SLOT:
                                    red += 1
                            print "Blue: " + str(blue) + " - Red: " + str(red)

                            if red == blue:
                                playerTurn = False

                            else:
                                time.sleep(2)
                                self.publishVisionBoard(GET_BOARD)
                                self.waitResponse()

                        print "# 2.6 GO TO STEP 2.1"


                else:
                    print "#3 PRINT WINNER MESSAGE, GO TO 1"
                    gameFinished = True

                    if gameCheck == BLUE_SLOT:
                        print "Player WINZ! You cheated!"
                    elif gameCheck == RED_SLOT:
                        print "Robot WINS! Like i always do!"
                    else:
                        print "It's a tie"

                    self.gameOver = True
                    print "Game over please press your arduino to start a new game"
                    while (self.gameOver):
                        time.sleep(1)


    def waitResponse(self):
        while self.waitForResponse:
            time.sleep(1)

    def callbackVisionBoard(self,data):
        self.board = data.data.split(",", 9)
        self.board = numpy.delete(self.board, 9)
        self.waitForResponse = False

    def callbackVisionBrick(self,data):
        self.currentBrick = data.data
        self.waitForResponse = False

    def callbackArmController(self,data):
        self.waitForResponse = False

    def callbackArduino(self,data):
        print "Arduino: " + str(data.data)
        self.gameOver = False

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
        self.pubArmController.publish(data)

    def pubArduino(self,data):
        self.pubArduino.publish(data)

    def checkForWin(self, board):
        WIN_OPTIONS = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                       (0, 3, 6), (1, 4, 7), (2, 5, 8),
                       (2, 5, 8), (0, 4, 8), (2, 4, 6))
        for row in WIN_OPTIONS:
            if board[row[0]] == board[row[1]] == board[row[2]] != EMPTY_SLOT:
                return board[row[0]]
        if EMPTY_SLOT not in board:
            return TIE
        return CONTINUE_GAME


    def possibleMoves(self,board):
        moves = []
        for square in range(9):
            if board[square] == EMPTY_SLOT:
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
            board[move] = EMPTY_SLOT

        #can player win next turn
        for move in self.possibleMoves(board):
            board[move] = brickPlayer
            if self.checkForWin(board) == brickPlayer:
                print "found a way player can win, blocking this move"
                return move
            board[move] = EMPTY_SLOT
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