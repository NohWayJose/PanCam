from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
import sys, getopt

def main(argv):
	cam2targetX = ''
	cam2targetY = ''
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["-s=","-x=","-y=","-w=","-l=","-p=","-t=","-n=","-i=","-e=","-a="])
		
		# s = mm from zeroth position to start position for camera
		# x = mm along axis of travel from the camera's starting point to the nearest point of the target object
		# y = mm from the camera to the line through the target object that's parallel to the axis of travel
		# w = mm width of the target object, measured parallel to the axis of travel
		# p = pan boolean. yes | no
			# p=y then ask for x,y & w
			# p=n then ask for a, which is the camera angle (a constant)
		# t or n = time elapsed or number of frames
		# i or e = intershot pause or elapsed shopping =  
