#!/usr/bin/python

# Interface keys
REQUEST_BOARD_KEY = 'requestBoard'
RESPOND_BOARD_KEY = 'respondBoard'

REQUEST_WAIT_FOR_MOVE_KEY = 'moveMade'
RESPOND_WAIT_FOR_MOVE_KEY = 'waitForMove'

REQUEST_BRICKPLACEMENT_KEY = 'requestBrinkPlacement'
RESPOND_BRICKPLACMENT_KEY = 'respondBrickPlacement'

ARM_DEFAULT_POS = [0.0, 0.0, 0.569]

def coordinateconverter(x,y):
    convertConstant = 0.001154

    xOffset = 304
    yOffset = 382

    newX = -(y-yOffset)*convertConstant
    newY = -(x-xOffset)*convertConstant

    return newX, newY

if __name__ == '__main__':
    x,y = coordinateconverter(253,113)
    print str(x) + " " + str(y)
    x, y = coordinateconverter(360, 219)
    print str(x) + " " + str(y)
    x, y = coordinateconverter(304, 167)
    print str(x) + " " + str(y)