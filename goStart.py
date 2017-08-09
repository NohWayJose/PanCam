from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
import sys, argparse, time, atexit, threading, random, requests, json
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

parser = argparse.ArgumentParser()

parser.add_argument("-s", "--start_dist",
                    required=True,
                    help="mm from zeroth position to start position for camera",
                    type=int)

args = parser.parse_args()

print '\n\nEverything: ' + str(args)

# key constants (may require calibration)
_anglePerPulse_ = 8.64
_threadPitch_ = 1.5
_framesPerSecond_ = 25
_frameCount = 1500
dist_travelled = 0

def dist2pulses(len):
    numberOfPulses = len * 360 / _anglePerPulse_ * _threadPitch_
    return int(numberOfPulses)

def stepper_worker(stepper, numsteps, direction, style):
    #print("Steppin!")
        stepper.step(numsteps, direction, style)
    #print("Done")


while (dist_travelled < args.start_dist):
        if not st1.isAlive():
                print("Stepper 1 moving to start position at " + str(args.start_dist) + "mm (" + str(dist2pulses(args.start_dist)) + "pulses)")
                dir = Adafruit_MotorHAT.BACKWARD
                #steps = 33333 #about 0.5m worth at a pitch of 1.5mm/rev
                #steps = int(360/_anglePerPulse_) 
                steps = dist2pulses(args.start_dist)/5 
                st1 = threading.Thread(target=stepper_worker, args=(myStepper1, steps, dir, stepstyles[1],))
                st1.start()
		dist_travelled = dist_travelled+args.start_dist/5
        time.sleep(0.1)  # Small delay to stop from constantly polling threads (see: https://forums.adafruit.com/viewtopic.php?f=50&t=104354&p=562733#p562733)
print("Start postion reached. Turning off motor.")
turnOffMotors()

