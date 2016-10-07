#!/usr/bin/python

REQUESTBRINKPLACEMENT_KEY = 'requestBrinkplacement'
RESPONDBRICKPLACMENT_KEY  = 'respondBrickplacement'

DEFAULT_POS = [0.23, 0.0, 0.339]

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