from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
import time
import atexit
import threading
import random

import requests
import json

import RPi.GPIO as GPIO

# Use GPIO numbers, not pin numbers (alt=BOARD for the numbers on the GPIO header pins)
GPIO.setmode(GPIO.BCM)

#set up the GPIO BCM channel 17 for input
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT()

# create empty threads (these will hold the stepper 1 and 2 threads)
st1 = threading.Thread()
st2 = threading.Thread()


# recommended for auto-disabling DC motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

S1_spr = 100 #Stepper1 steps/rev
S2_spr = 450 #Stepper2 steps/rev
limiter_val = True

myStepper1 = mh.getStepper(S1_spr, 1)      # 200 steps/rev, motor port #1
myStepper2 = mh.getStepper(S2_spr, 2)      # 200 steps/rev, motor port #1
myStepper1.setSpeed(60)          # 60 RPM
myStepper2.setSpeed(60)          # 60 RPM


stepstyles = [Adafruit_MotorHAT.SINGLE, Adafruit_MotorHAT.DOUBLE, Adafruit_MotorHAT.INTERLEAVE, Adafruit_MotorHAT.MICROSTEP]

def stepper_worker(stepper, numsteps, direction, style):
    #print("Steppin!")
	stepper.step(numsteps, direction, style)
    #print("Done")

while (limiter_val == True):
	limiter_val = GPIO.input(17)
	if not st1.isAlive():
		print("Stepper 1 returning home")
		dir = Adafruit_MotorHAT.FORWARD
		#steps = 33333 #about 0.5m worth at a pitch of 1.5mm/rev
		steps = 160 #one revolution is 100 x 3.6deg/rev = 1.5mm travel
		st1 = threading.Thread(target=stepper_worker, args=(myStepper1, steps, dir, stepstyles[1],))
		st1.start()
	time.sleep(0.2)  # Small delay to stop from constantly polling threads (see: https://forums.adafruit.com/viewtopic.php?f=50&t=104354&p=562733#p562733)
print("Beginning postion reached. Turning off motor.")
turnOffMotors()
