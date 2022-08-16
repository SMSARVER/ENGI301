# drops one piece in a specified location
import movetopos
from time import sleep
import servo

def dropPieceIn(position,col):
    newpos = int(float(col))
    newpos = movetopos.goto(position, newpos)
    servo.drop1()
    position = 4 # return to center of board
    position = movetopos.goto(newpos, position)
    return position