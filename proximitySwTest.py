import RPi.GPIO as GPIO
import time

# Use GPIO numbers, not pin numbers (alt=BOARD for the numbers on the GPIO header pins)
GPIO.setmode(GPIO.BCM)

#set up the GPIO BCM channel 17 for input
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

lv=True;
cvA=True;
cvB=True;

while (True):
	limiter_val = GPIO.input(17)
	cam_valA = GPIO.input(27)
	cam_valB = GPIO.input(22)

#End stop switch
	if limiter_val and not lv:
		print("Limiter switch closed")
	if not limiter_val and lv:
		print("Limiter switch opened")
	lv = limiter_val

#Limit pan right from camera's POV
	if cam_valA and not cvA:
		print("Cam switch A closed")
	if not cam_valA and cvA:
		print("Cam switch A opened")
	cvA = cam_valA
	
#Limit pan left from camera's POV
	if cam_valB and not cvB:
		print("Cam switch B closed")
	if not cam_valB and cvB:
		print("Cam switch B opened")
	cvB = cam_valB

	time.sleep(0.1)
