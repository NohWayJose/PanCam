import RPi.GPIO as GPIO
import time

# Use GPIO numbers, not pin numbers (alt=BOARD for the numbers on the GPIO header pins)
GPIO.setmode(GPIO.BCM)

#set up the GPIO BCM channel 17 for input
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

lv=True;
cv=True;

while (True):
	limiter_val = GPIO.input(17)
	cam_val = GPIO.input(22)

	if limiter_val and not lv:
		print("Limiter switch closed")
	if not limiter_val and lv:
		print("Limiter switch opened")
	lv = limiter_val

	if cam_val and not cv:
		print("Cam switch closed")
	if not cam_val and cv:
		print("Cam switch opened")
	cv = cam_val
	
	time.sleep(0.1)
