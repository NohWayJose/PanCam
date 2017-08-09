from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
import sys, argparse, subprocess, time, atexit, threading
import RPi.GPIO as GPIO


parser = argparse.ArgumentParser()


parser.add_argument("-s", "--start_dist",
                    required=True,
                    help="mm from zeroth position to start position for camera",
                    type=int)

parser.add_argument("-f", "--finish_dist",
                    required=True,
                    help="mm from zeroth position to finish position for camera",
                    type=int)

#panMode = parser.add_mutually_exclusive_group()

#panMode.add_argument_group('panGroup')
#panMode.add_argument_group('noPanGroup')

parser.add_argument("-p", "--pan",
                    required = True,
                    choices = ['focus','fixed'],
                    default = 'focus',
                    help="--pan is optional but if present requires --target_dist, --target_offset & --target_width. If --pan is not present, --camera_angle is required")

parser.add_argument("-x","--target_dist",
                    default =  100,
                    help="mm along axis of travel from the camera's starting point to the nearest point of the target object",
                    type=int)

parser.add_argument("-y","--target_offset",
                    default = 100,
                    help="mm from the camera to the line through the target object that's parallel to the axis of travel",
                    type=int)

parser.add_argument("-w","--target_width",
                    default = 20,
                    help="mm width of the target object, measured parallel to the axis of travel",
                    type=int)

parser.add_argument("-a", "--camera_angle",
                    default = 90,
                    help="degrees either side of 90deg from axis of travel (aspiration to use a captured image to set angle)",
                    type=int)

parser.add_argument("-t", "--movie_length",
                    #default =  60,
                    help="time elapsed for finished movie, in seconds",
                    type=int)

parser.add_argument("-n", "--frames",
                    #default =  1500,
                    nargs = '?',
                    help="number of frames",
                    type=int)

parser.add_argument("-e", "--shoot_time",
                    #default = 3600,
                    help="elapsed time for all shots, in seconds",
                    type=int)

parser.add_argument("-i", "--intershot_pause",
                    #default = 2.4,
                    help="intershot pause, in seconds",
                    type=float)

parser.add_argument("-r", "--image_size",
                    choices=['l','L','m','M','s','S'],
                    default = 'm',
                    help="L=1080p, M=720p, S=360p",
                    type=str)

args = parser.parse_args()

print '\n\nEverything: ' + str(args)

# key constants (may require calibration)
_anglePerPulse_ = 3.6
_threadPitch_ = 1.5
_framesPerSecond_ = 25



#---------------------------------------------------------------------------------------
#convert linear distance to a pulse count for the stepper for linear motion
def dist2pulses(len):
    numberOfPulses = len * 360 / _anglePerPulse_ * _threadPitch_
    return int(numberOfPulses)
#---------------------------------------------------------------------------------------
    
#---------------------------------------------------------------------------------------
#convert 
#dist2pulses(args.finish_dist - args.start_dist)
def time2frames(_time):
    numberOfFrames = _time * _framesPerSecond_
    _frameCount = int(numberOfFrames)
    return _frameCount
#---------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------
def shootTime2pauseTime(shootTime, frames):
    timePerFrame = shootTime / frames
    return timePerFrame
#---------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------
#Command argument validation logic
    
print '\nDistance from home to start point is ' + str(args.start_dist) + 'mm and will take ' + str(dist2pulses(args.start_dist)) + ' pulses!'
#_start2endPulses = dist2pulses(args.finish_dist - args.start_dist)
print '\nDistance from start to finish point is ' + str(args.finish_dist - args.start_dist) + 'mm and will take ' + str(_start2endPulses) + ' pulses!'

if args.pan == 'focus':
    if  args.target_dist == 100 and args.target_offset == 100 and args.target_width == 20:
        print "\nUsing default values for --target_dist <100 mm>, --target_offset <100 mm> & --target_width <20 mm>."
    else:
        print '\ntarget_dist = ' + str(args.target_dist)  + '\n\ntarget_offset = ' + str(args.target_offset) + '\n\ntarget_width = ' + str(args.target_width)
             
if args.pan == 'fixed':
    if args.camera_angle == 90:
        print "\nUsing default camera_angle = " + str(args.camera_angle)
    else:
        print "\ncamera_angle = " + str(args.camera_angle)
    if args.target_dist != 100 and args.target_offset != 100 and args.target_width != 20:
        print "\nIf --pan = 'fixed', sequence just requires a --camera_angle, but not --target_dist, --target_offset & --target_width, which will be ignored!"
            
# neither/one/other/both of movie_length and frames
if not args.movie_length and not args.frames:  
    print "\n--movie_length in seconds or --frames is required!"
elif args.movie_length and not args.frames:
    print "\nmovie_length = " + str(args.movie_length) + "s. This will require " + str(time2frames(args.movie_length)) + "frames"
    _frameCount = time2frames(args.movie_length)
elif args.frames and not args.movie_length:
    print "\nmovie will be " + str(args.frames) + " frames long. This will take " + str(args.frames / _framesPerSecond_) + "seconds"
    _frameCount = args.frames
elif args.frames and args.movie_length:
    print "\nmovie_length = " + str(args.movie_length) + "s. This will require " + str(time2frames(args.movie_length)) + "frames (--frames will be ignored)" 
    _frameCount = time2frames(args.movie_length)
else:
    print "\nError parsing --movie_length or --frames"
   
    
# neither/one/other/both of shoot_time and intershot_pause   
if not args.shoot_time and not args.intershot_pause:  
    print "\n--shoot_time in seconds or --intershot_pause in seconds is required!"
elif args.shoot_time and not args.intershot_pause:
   print "\nshoot_time will be " + str(args.shoot_time) + "s. \nThe pause between each frame will be " +  str(shootTime2pauseTime(args.shoot_time, _frameCount))
   _intershotPause = shootTime2pauseTime(args.shoot_time, _frameCount)
elif args.intershot_pause and not args.shoot_time:
    print "\nmnshoot_time will be about " + str(args.intershot_pause * _frameCount) + " seconds long."
    _intershotPause = args.intershot_pause
elif args.intershot_pause and args.shoot_time:
    print "\nshoot_time will be " + str(args.shoot_time) + "s. \nThe pause between each frame will be " +  str(shootTime2pauseTime(args.shoot_time, _frameCount))
    _intershotPause = shootTime2pauseTime(args.shoot_time, _frameCount)
else:
    print "\nError parsing --shoot_time or --intershot_pause"
    
_pulsesPerFrame = dist2pulses(args.finish_dist - args.start_dist) / _frameCount
print "\n" + str(_pulsesPerFrame) + " pulses will precede each frame"
#---------------------------------------------------------------------------------------





#---------------------------------------------------------------------------------------
# global variables/defaults
_frameCount = 1500
_pulses2start = 0
_start2endPulses = dist2pulses(args.finish_dist - args.start_dist)
_intershotPause = 2
_pulsesPerFrame = dist2pulses(args.finish_dist - args.start_dist) / _frameCount
_pulseTally = 0
#---------------------------------------------------------------------------------------

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


#setting up for return to home

S1_spr = 160 #Stepper1 steps/rev
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
    
    
print("Stepper 1 returning home")

while (limiter_val == True):
	limiter_val = GPIO.input(17)
	if not st1.isAlive():
		dir = Adafruit_MotorHAT.FORWARD
		#steps = 33333 #about 0.5m worth at a pitch of 1.5mm/rev
		steps = 160 #one revolution is 100 x 3.6deg/rev = 1.5mm travel
		st1 = threading.Thread(target=stepper_worker, args=(myStepper1, steps, dir, stepstyles[1],))
		st1.start()
	time.sleep(0.2)  # Small delay to stop from constantly polling threads (see: https://forums.adafruit.com/viewtopic.php?f=50&t=104354&p=562733#p562733)
print("Beginning postion reached. Sequence now starting.")

#

#Setting up for pulse to position, pause, shoot, record total pulses - rinse & repeat


S1_spr = 160 #Stepper1 steps/rev
S2_spr = 450 #Stepper2 steps/rev
limiter_val = True

while (_pulseTally <= _start2endPulses ): # Below here needs more work
	limiter_val = GPIO.input(17)
	if not st1.isAlive():
		dir = Adafruit_MotorHAT.FORWARD
		#steps = 33333 #about 0.5m worth at a pitch of 1.5mm/rev
		steps = 160 #one revolution is 100 x 3.6deg/rev = 1.5mm travel
		st1 = threading.Thread(target=stepper_worker, args=(myStepper1, steps, dir, stepstyles[1],))
		st1.start()
	time.sleep(0.2)  # Small delay to stop from constantly polling threads (see: https://forums.adafruit.com/viewtopic.php?f=50&t=104354&p=562733#p562733)
print("Beginning postion reached. Sequence now starting.")

turnOffMotors()




