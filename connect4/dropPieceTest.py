import movetopos
from time import sleep

position = int(float(input("What is the current position? (0-8): ")))

while True:
    
    newpos = int(float(input("Select a position to move to (0-8): ")))
    print('moving to position',newpos,'...')
    #print(position,newpos)
    newpos = movetopos.goto(position, newpos)
    
    #print('current position:', position)
    print('dropping piece')
    sleep(3)
    
    if (newpos > 4):
        position = 8
        print('moving to position:',position)
        #print(position,newpos)
        position = movetopos.goto(newpos, position)
    else:
        position = 0
        print('moving to position:',position)
        #print(position,newpos)
        position = movetopos.goto(newpos, position)
            