"""
--------------------------------------------------------------------------
Position Reset with Limit Switches
--------------------------------------------------------------------------
License:   
Copyright 2022 Samuel Sarver

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------


About:
- Captures picture of connect 4 board
- returns 6x7 numpy array of 0's (green), 1's (blue), and 2's (red)

"""
from movetopos import *

sleeptimeRun = 0.0006 #should be smaller probbably but not too small
sleeptimeRetreat = 0.001 # as large (slow) as possible

LSright="P1_4"
LSleft="P1_2"

GPIO.setup(LSright, GPIO.IN)
GPIO.setup(LSleft, GPIO.IN)

def reset(pos): #1-7
    if pos > 4:
        direction = 1 #right is 1, 0 is left
        limswitch = LSright
    else:
        direction = 0
        limswitch = LSleft
    GPIO.output(DIR,direction)
    print("finding limit switch")
    #find limit switch
    while GPIO.input(limswitch)==0: # forwards
        if GPIO.input(button)==0:
            GPIO.output(STEP,GPIO.HIGH)
            sleep(sleeptimeRun)
            GPIO.output(STEP,GPIO.LOW)
            sleep(sleeptimeRun)
        else: # safety limit switch activated
            print('limit reached - position not accurate')
            raise SystemExit(0)
            break
    print("finding release")
    #find point where switch is released
    GPIO.output(DIR, not direction)
    while GPIO.input(limswitch)==1:
        GPIO.output(STEP,GPIO.HIGH)
        sleep(sleeptimeRetreat)
        GPIO.output(STEP,GPIO.LOW)
        sleep(sleeptimeRetreat)
    print("moving to possition 1 or 7")
    if limswitch == LSright:
        #MOVE TO POSITION 7 - a certian amount of steps 
        for i in range(1350):
            GPIO.output(STEP,GPIO.HIGH)
            sleep(sleeptimeRun)
            GPIO.output(STEP,GPIO.LOW)
            sleep(sleeptimeRun)
        return(7)
    else:
        #MOVE TO POSITION 1 - a certain amount of steps
        for i in range(2850):
            GPIO.output(STEP,GPIO.HIGH)
            sleep(sleeptimeRun)
            GPIO.output(STEP,GPIO.LOW)
            sleep(sleeptimeRun)
        return(1)

if __name__ == '__main__':
    reset(1)