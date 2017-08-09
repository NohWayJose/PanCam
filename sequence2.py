from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
import sys, argparse

parser = argparse.ArgumentParser()

parser.add_argument("-s", "--start_dist", help="mm from zeroth position to start position for camera", type=int)

parser.add_argument("-f", "--finish_dist", help="mm from zeroth position to finish position for camera", type=int)

parser.add_argument("-p", "--pan", help="--pan requires --target_dist, --target_offset & --target_width. If pan is not present, --camera_angle is required")

parser.add_argument("-x","--target_dist", help="mm along axis of travel from the camera's starting point to the nearest point of the target object", type=int)

parser.add_argument("-y","--target_offset", help="mm from the camera to the line through the target object that's parallel to the axis of travel", type=int)

parser.add_argument("-w","--target_width", help="mm width of the target object, measured parallel to the axis of travel",type=int)

parser.add_argument("-a", "--camera_angle", help="degrees either side of 90deg from axis of travel (aspiration to use a captured image to set angle", type=int)

parser.add_argument("-t", "--movie_length", help="time elapsed for finished movie", type=int)

parser.add_argument("-n", "--frames", help="number of frames", type=int)

parser.add_argument("-i", "--intershot_pause", help="intershot pause", type=int)

parser.add_argument("-e", "--shoot_time", help="elapsed time for all shots", type=int)

args = parser.parse_args()

_anglePerPulse_ = 3.6
_threadPitch_ = 1.5


def dist2pulses(len):
    numberOfPulses = len * 360 / _anglePerPulse_ * _threadPitch_
    return int(numberOfPulses)
    
    
print 'Distance from home to start point is ' + str(args.start_dist) + 'mm and will take ' + str(dist2pulses(args.start_dist)) + ' pulses!'
print 'Distance from start to finish point is ' + str(args.finish_dist - args.start_dist) + 'mm and will take ' + str(dist2pulses(args.finish_dist - args.start_dist)) + ' pulses!'


if args.pan:
    if not args.target_dist or not args.target_offset or not args.target_width:
        print "--pan requires --target_dist, --target_offset & --target_width."
    else:
        print 'target_dist = ' + str(args.target_dist)  + '\ntarget_offset = ' + str(args.target_offset) + '\ntarget_width = ' + str(args.target_width)
        if args.camera_angle:
            print "\n--camera_angle is not needed for --pan and will be ignored!"
        
if not args.pan:
    if not args.camera_angle:
        print "Omitting --pan requires --camera_angle"
    else:
        print 'camera_angle = ' + str(args.camera_angle)
        if args.target_dist or args.target_offset or args.target_width:
            print "\nIf --pan is omitted, flyby just requires a --camera_angle, but not --target_dist, --target_offset & --target_width, which will be ignored!"
 
