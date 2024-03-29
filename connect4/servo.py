"""
--------------------------------------------------------------------------
Servo Test
--------------------------------------------------------------------------
License:   
Copyright 2021 Erik Welsh

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

Test SG90 Servo

Modified by Samuel Sarver in 2022

"""
import time

import Adafruit_BBIO.PWM as PWM

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

SG90_FREQ   = 50#50                  # 20ms period (50Hz)
SG90_POL    = 0                   # Rising Edge polarity
SG90_OFF    = 0#5                   # 0ms pulse -- Servo is inactive
SG90_RIGHT  = 5#5                   # 1ms pulse (5% duty cycle)  -- All the way right 0.18 seconds for 60 degrees. 500 microseconds . 1.08 seconds
SG90_LEFT   = 10#10                  # 2ms pulse (10% duty cycle) -- All the way Left


# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

# None

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class Servo():
    """ CombinationLock """
    servo      = None
    
    def __init__(self, servo="P1_36"):
        """ Initialize variables and set up display """
        self.servo      = servo
        
        self._setup()
    
    # End def
    
    
    def _setup(self):
        """Setup the hardware components."""
        # Initialize Servo; Servo should be "off"
        PWM.start(self.servo, SG90_OFF, SG90_FREQ, SG90_POL)

    # End def


    def left(self):
        """Turn Servo to the left (counterclockwise)"""
        # Set servo
        PWM.set_duty_cycle(self.servo, SG90_LEFT)

    # End def


    def right(self):
        """Turn Servo to the right (clockwise)"""
        # Set servo
        PWM.set_duty_cycle(self.servo, SG90_RIGHT)

    # End def


    def cleanup(self):
        """Cleanup the hardware components."""
        
        # Stop servo
        PWM.stop(self.servo)
        PWM.cleanup()
    
    def stop(self):
        PWM.set_duty_cycle(self.servo, SG90_OFF)
        
    # End def

# End class

def setup():
    servo = Servo()

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':

    print("Servo Test")

    # Create instantiation of the servo
    servo = Servo()

    try:
        #time.sleep(1)
        print("Turn left (counterclockwise)")
        for i in range(15):
            servo.right()
            time.sleep(0.47)
            servo.cleanup()
            
            time.sleep(1)
            servo = Servo()
        
    except KeyboardInterrupt:
        pass

    # Clean up hardware when exiting
    servo.cleanup()

    print("Test Complete")

def drop1():
    servo = Servo()
    servo.right()
    time.sleep(0.47) ## adjusted to the time it takes to rotate 180 degrees
    #servo.stop()
    servo.cleanup()
    time.sleep(0.5)