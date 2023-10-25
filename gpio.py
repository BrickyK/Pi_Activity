import RPi.GPIO as GPIO
from time import sleep 

GPIO.setmode(GPIO.BCM)      #set the pin mode
GPIO.setup(22, GPIO.OUT)    #set gpio pin 22 as output
GPIO.output(22, HIGH)       #turns on servo
GPIO.output(22, LOW)        #turns off servo

#######################################################################################################################################
# This portion of the code controls the servo. Servo should be able to switch and return tracks based on input
# from other parts of the code to be implimented later
#
#######################################################################################################################################
switched = False
def switch():
    while switched == False:
        GPIO.output(22, LOW)            # Train remains as normal
        print("Train continues")
    if switched == True:
        GPIO.output(22, HIGH)           # Switches the track(sends servo into active state)
        print("Switching Tracks")
        sleep(4)                        # Gives train time to pass through track switcher(varaible innacurate)
        GPIO.output(22, LOW)            # Returns track to normal(servo returns to inactive state)
        print("Returning Tracks")
        switched = False

for i in range(1, 6):
    switched = True

