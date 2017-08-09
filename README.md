# PanCam
Python (on a Pi) to control two stepper motors and a Pi camera for photographing small slow things (buds/bugs/etc)

The hardware consists of:
*   a 3-part telescopic track (a file drawer slider)
*   a Raspberry Pi, mounted on the inner slider
*   An Adafruit Pi Stepper/DC motor shield
*   A Raspberry Pi camera (Rev 1.3)
*   An 8deg/step stepper motor mounted on the outer slider. The spindle is attached to a 350mm threaded rod (studding), which passes through a nut attached to the inner slider. This controls the incremental linear movement of all the items attached to the inner slider.
*   A 3deg/step and gears, mounted on the inner slider. On the final gear is a 3D printed Pi Camera mount. This controls the incremental rotation of the camera.
*   A micro limit switch, mounted next to the motor. This is used to return the camera to a known start position

_resetCam.py_  
Loops until end stop reached - each loop calculates the number of pulses required to cover about 1/10th of the distance (so that the end stop can be detected) May convert this to the number of pulses required for one revolution = 1.5mm

_goStart.py_  
Takes a single parameter (-s | --start_dist) which calculates the number of pulses required to move the slider by the specified distance

_sequenceX.py_  
Takes the following parameters (the logic for usage is in the code)  
    "-s", "--start_dist"        = mm from zeroth position to start position for camera  
    "-f", "--finish_dist"       = mm from zeroth position to finish position for camera  
    "-p", "--pan"               = pan is optional but if present requires --target_dist, --target_offset & --target_width. If --pan is not present, --camera_angle is required  
    "-x","--target_dist"        = mm along axis of travel from the camera's starting point to the nearest point of the target object  
    "-y","--target_offset"      = mm from the camera to the line through the target object that's parallel to the axis of travel  
    "-w","--target_width"       = mm width of the target object, measured parallel to the axis of travel  
    "-a", "--camera_angle"      = degrees either side of 90deg from axis of travel (aspiration to use a captured image to set angle)  
    "-t", "--movie_length"      = time elapsed for finished movie, in seconds  
    "-n", "--frames"            = number of frames  
    "-e", "--shoot_time"        = elapsed time for all shots, in seconds  
    "-i", "--intershot_pause"   = intershot pause, in seconds  
    "-r", "--image_size"        = L=1080p, M=720p, S=360p  

The program uses the variables to calculate the position of a virtual pivot point behind the target and then calculates the number of frames required and the shoot time delay between each frame. Then it incrementally moves the camera between the start and finish positions, also incrementing the rotation of the camera so that it constantly points at the virtual pivot point.
