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


- move in direction, when limit switch close then stop & wait 1 sec, move opposite direction same distance


today:
program function
inputs: current possition (0 or 8), position on board to move to (1-7)
-moves to possition 1-7
outputs: new current possition (0 or 8)
(will only move over a few inches for safety)

once we have limit switches:
move over the entire board and tune positions to high accuracy on board



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

# Setup pin layout on PI
###GPIO.setmode(GPIO.BOARD)

# Establish Pins in software
GPIO.setup(button, GPIO.IN)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)

# Set the first direction you want it to spin
GPIO.output(DIR, CW)

sleeptime = 0.0003 # fastest step time ### 0.00025 MINIMUM!!!  power supply must be over 24V for fast speeds (0.0003), over 29V for 0.00028. # 0.003 = 0.83 in/sec
sleeptimeMax = 0.001 # slowest step time ### 0.001 MAXIMUM!!!
steps = 1000 # 8000 steps = 7.9 in
inches = steps * 0.0009875
timeinbetween = 2
acclerationFactor = 0.7 * 1142858 # 1 is default. increasing increases accel time/steps, decreasing decreases accel time/steps
accelSteps = int((sleeptimeMax - sleeptime) * acclerationFactor)#800 # num of steps to accel/decel for
print(accelSteps)

if (steps < (1 + accelSteps * 2)):
		sleeptime = sleeptimeMax - steps / (2 * acclerationFactor)
		if (sleeptime < 0.0003):
			print('you did something wrong')
			raise SystemExit(0)
		accelSteps = int((sleeptimeMax - sleeptime) * acclerationFactor)
		print(accelSteps)

sleepTimeChange = []
for i in range(accelSteps): # slowly decrease the step size to accelerate the motor
	sleepTimeChange.append(sleeptimeMax - (i * (sleeptimeMax - sleeptime) / accelSteps))

for i in range(steps - (2 * accelSteps)): # keep the step size constant for max speed
	sleepTimeChange.append(sleeptime)

for i in range(accelSteps): # slowly increase step size to decellerate motor
	sleepTimeChange.append(sleeptime + (i * (sleeptimeMax - sleeptime) / accelSteps))
print(sleepTimeChange)

#while True:
	#sleep(1)

try:
	# Run forever.
	while True:

		"""Change Direction: Changing direction requires time to switch. The
		time is dictated by the stepper motor and controller. """
		sleep(timeinbetween)
		# Esablish the direction you want to go
		GPIO.output(DIR,CW)
		print("CW")
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
				print('limit reached')
				sleep(1)
				GPIO.output(DIR,CCW)
				for x in range(50): # backwards
					GPIO.output(STEP,GPIO.HIGH)
					sleep(sleeptimeMax)
					GPIO.output(STEP,GPIO.LOW)
					sleep(sleeptimeMax)
				#raise SystemExit(0)
				break
				

		"""Change Direction: Changing direction requires time to switch. The
		time is dictated by the stepper motor and controller. """
		sleep(timeinbetween)
		GPIO.output(DIR,CCW)
		print("CCW")
		for x in range(steps): # backwards
			GPIO.output(STEP,GPIO.HIGH)
			sleep(sleepTimeChange[x])
			GPIO.output(STEP,GPIO.LOW)
			sleep(sleepTimeChange[x])

# Once finished clean everything up
except KeyboardInterrupt:
	print("\ncleanup")
	GPIO.output(STEP,GPIO.LOW)
	GPIO.output(DIR,GPIO.LOW)
	GPIO.cleanup()
