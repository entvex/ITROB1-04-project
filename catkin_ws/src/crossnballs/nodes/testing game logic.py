

class gamelogic:
    def __init__(self):
        self.board = self.makeCleanBoard()
        self.turn = "X"
        self.player = "X"
        self.robot = "O"
    def game(self):
        gameBoard = self.makeCleanBoard()
        gameTurn = self.turn
        while not self.checkForWin(gameBoard):

            if gameTurn == self.player:
                move = self.getPlayerMove(gameBoard)
                gameBoard[move] = self.player
            else:
                move = self.getRobotMove(gameBoard,self.robot,self.player)
                gameBoard[move] = self.robot
            turn = self.nextTurn(turn)

        gameWinner =self.checkForWin(gameBoard)
        print gameWinner + " WON the game"


    def makeCleanBoard(self):
        board = []
        for square in range(9):
            board.append(" ")
        return board

    def checkForWin(self,board):
        WIN_OPTIONS = ((0,1,2),(3,4,5),(6,7,8),
                       (0,3,6),(1,4,7),(2,5,8),
                       (2,5,8),(0,4,8),(2,4,6))
        for row in WIN_OPTIONS:
            if board[row[0]] == board[row[1]] == board[row[2]] != " ":
                return board[row[0]]
        if " " not in board:
            return "T"
        return None

    def getPlayerMove(self,board):
        #testing use only




    def possibleMoves(self,board):
        moves = []
        for square in range(8):
            if board[square] == " ":
                moves.append(square)
        return moves


    def getRobotMove(self, board, brickRobot,brickPlayer):
        board = board[:]
        BEST_MOVES = (4, 8, 6, 0, 2, 1, 3, 5, 7);

        #can I win this turn
        for move in self.possibleMoves(board):
            board[move] = brickRobot
            if self.checkForWin(board) == brickRobot:
                print "found a possible win"
                return move
            board[move] = " "

        #can player win next turn
        for move in self.possibleMoves(board):
            board[move] = brickPlayer
            if self.checkForWin(board) == brickPlayer:
                print "found a way player can win, blocking this move"
                return move
            board[move] = " "

        #make the best move
        for move in BEST_MOVES:
            if move in self.possibleMoves(board):
                return move

    def nextTurn(self,turn):
        if turn == "X":
            return "O"
        else:
            return "X"

if __name__ == "__main__":
