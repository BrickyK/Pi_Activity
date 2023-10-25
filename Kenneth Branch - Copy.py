#import dependencies
import numpy as np


import time

#import opencv for computer vision stuff

import cv2

#import matplotlip so we can visualize an image

from matplotlib import pyplot as plt

###########################################################################
###########################################################################
###########################################################################


#connect to camera
cap = cv2.VideoCapture(0)

#initialize a variable to track last messages
last_detection_time = {'Blue': 0, 'Red': 0, 'Yellow': 0}

#define a time interval to display the printed message
time_for_message = 0

#define a function to create colors
def create_color(value1, value2, value3):
    color_value = np.array([value1, value2, value3])
    return color_value

#create function to make masks
def create_mask(lowerValue, upperValue):
    mask = cv2.inRange(hsv, lowerValue, upperValue)
    return mask

#create function to combine masks
def combine_masks(value1, value2, value3):
    mask = value1 + value2 + value3
    return mask

#create function to detect if the computer sees these colors
def detecting_colors(value):
    current_time = time.time()
    hasColor = np.sum(value)
    if hasColor > 0:
        return '1'
    else:
        return '0'

#define function to print detected color
def print_detected_color(value, color):
    current_time = time.time()
    if value == '1' and (current_time - last_detection_time[color] >= time_for_message):
        print(f'{color} Detected')
        last_detection_time[color] = current_time
    
while True:
    #get a frame from the capture device
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))

    #convert image to hsv color
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #create colors using create_color function
    lower_blue = create_color(110, 50, 50)
    upper_blue = create_color(130, 255, 255)

    lower_red = create_color(0, 100, 20)
    upper_red = create_color(10, 255, 255)

    lower_yellow = create_color(20, 100, 100)
    upper_yellow = create_color(30, 255, 255)

    #create masks using create_masks function
    blue_mask = create_mask(lower_blue, upper_blue)

    red_mask = create_mask(lower_red, upper_red)

    yellow_mask = create_mask(lower_yellow, upper_yellow)

    #combine masks using combine_masks function to scan multiple colors at once
    mask = combine_masks(blue_mask, red_mask, yellow_mask)

    #keep only pixles with these colors
    result = cv2.bitwise_and(frame, frame, mask=mask)

    #create a visual window to see what the computer sees
    cv2.imshow('frame', result)

    #detect colors in the frames and print them
    detect_blue = detecting_colors(blue_mask)
    print_detected_color(detect_blue, 'Blue')
    
    detect_red = detecting_colors(red_mask)
    print_detected_color(detect_red, 'Red')

    detect_yellow = detecting_colors(yellow_mask)
    print_detected_color(detect_yellow, 'Yellow')
    
    
    #create a way to kill the program
    if cv2.waitKey(1) == ord('q'):
               break
cap.release()
cv2.destroyAllWindows()
############################################################################
#TEST CAMERA#
# Display the frame using Matplotlib
###plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))  # Convert the frame to RGB color format
###plt.show()  # Show the image

# Release the camera when you're done
###cap.release()
############################################################################
def take_photo():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cv2.imwrite('webcamphoto.jpg', frame)
    cap.release()
    
