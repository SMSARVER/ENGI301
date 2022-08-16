import Adafruit_BBIO.GPIO as GPIO
import time

button="P1_34"
GPIO.setup(button, GPIO.IN)

while True:
    print(GPIO.input(button))
    #print('test')
    time.sleep(0.25)
    