"""
--------------------------------------------------------------------------
Connect 4 Stepper Motor Control
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

TODO:
- sperate "buttons" for each switch
- when switch hit, move very slowly in opposite direction until button no longer pressed (this is the accurate possition)
- knowledge of its current possition. left limit switch is possition zero and right limit switch is how every many steps it takes to get there (test to find out)
- if on the right side of the board but the left limit switch disconnects, then stop program altogether since something weird happened
- start game by homing
- remove possitions 0 and 8 and always have funnel over the board
- find out how long it takes to rotate 180 degrees

"""
import Adafruit_BBIO.GPIO as GPIO
from time import sleep

button="P1_34"  #limit switch
# Direction pin from controller
DIR = "P2_24"
# Step pin from controller
STEP = "P2_22"
# 0/1 used to signify clockwise or counterclockwise.
CW = 1
CCW = 0

# Establish Pins in software
GPIO.setup(button, GPIO.IN)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)

# Set the first direction you want it to spin
GPIO.output(DIR, CW)
	
def goto(position, newpos):
	travelX = (position - newpos)*-1
	if (travelX == 0):
		return newpos

	stepsTo1Pos = 1740 # the number of steps between game board columns
	steps = abs(int(travelX * stepsTo1Pos))
	direction = int((travelX > 0))
	sleeptime = 0.0004 # fastest step time ### 0.00025 MINIMUM!!!  power supply must be over 24V for fast speeds (0.0003), over 29V for 0.00028. # 0.003 = 0.83 in/sec
	sleeptimeMax = 0.001 # slowest step time ### 0.001 MAXIMUM!!!
	#steps = 1000 # 8000 steps = 7.9 in
	#inches = steps * 0.0009875
	acclerationFactor = 0.7 * 1142858 # 1 is default. increasing increases accel time and # of steps, decreasing decreases accel time and # of steps. arbitrary number
	accelSteps = int((sleeptimeMax - sleeptime) * acclerationFactor)#800 # num of steps to accel/decel for
	
	if (steps < (1 + accelSteps * 2)): # if distance is small enough to where reaching max speed would cause an acceleration to great, we set a new max speed that is lower
		sleeptime = sleeptimeMax - steps / (2 * acclerationFactor)
		if (sleeptime < 0.0003):
			print('you did something wrong')
			raise SystemExit(0)
		accelSteps = int((sleeptimeMax - sleeptime) * acclerationFactor)
	
	sleepTimeChange = []
	for i in range(accelSteps): # slowly decrease the step size to accelerate the motor
		sleepTimeChange.append(sleeptimeMax - (i * (sleeptimeMax - sleeptime) / accelSteps))
	
	for i in range(steps - (2 * accelSteps)): # keep the step size constant for max speed
		sleepTimeChange.append(sleeptime)
	
	for i in range(accelSteps): # slowly increase step size to decellerate motor
		sleepTimeChange.append(sleeptime + (i * (sleeptimeMax - sleeptime) / accelSteps))
	
	try:
		# Esablish the direction you want to go
		GPIO.output(DIR,direction)
		# Run for 200 steps. This will change based on how you set you controller
		for x in range(steps): # forwards
			if GPIO.input(button)==0:
				# Set one coil winding to high
				GPIO.output(STEP,GPIO.HIGH)
				# Allow it to get there.
				sleep(sleepTimeChange[x]) # Dictates how fast stepper motor will run ########## 0.0005 is nice 1"/s
				# Set coil winding to low
				GPIO.output(STEP,GPIO.LOW)
				sleep(sleepTimeChange[x]) # Dictates how fast stepper motor will run
			else: # limit switch activated
				print('limit reached - position not accurate')
				sleep(1)
				GPIO.output(DIR,(not direction))
				for x in range(50): # backwards
					GPIO.output(STEP,GPIO.HIGH)
					sleep(sleeptimeMax)
					GPIO.output(STEP,GPIO.LOW)
					sleep(sleeptimeMax)
				raise SystemExit(0)
				break
		sleep(0.5)	
		return newpos
	
	# Once finished clean everything up
	except KeyboardInterrupt:
		print("\ncleanup")
		GPIO.output(STEP,GPIO.LOW)
		GPIO.output(DIR,GPIO.LOW)
		GPIO.cleanup()
