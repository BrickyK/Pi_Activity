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
cap = cv2.VideoCapture(00000000)

#initialize a variable to track last messages
last_detection_time = {'Blue': 0, 'Pink': 0, 'Yellow': 0}

#define a time interval to display the printed message
time_for_message = .62

content_detection_timer = time.time()

#create a dictionary for contents
cargo = {'Blue': 'Coal', 'Pink': 'Molten Phenol', 'Yellow': 'Chicken'}

contamination = {'Coal': 1, 'Molten Phenol': 10, 'Chicken': 0}

contamination_level = 0

#define a function to create colors
def create_color(value1, value2, value3):
    color_value = np.array([value1, value2, value3])
    return color_value

#create function to make masks
def create_mask(lowerValue, upperValue):
    mask = cv2.inRange(center_pixel_hsv, lowerValue, upperValue)
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


# ... (your previous code)

while True:
    # Get a frame from the capture device
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))

    # Calculate the coordinates of the center pixel
    center_x = width // 2
    center_y = height // 2

    # Convert the center pixel to HSV color
    center_pixel_hsv = cv2.cvtColor(frame[center_y, center_x].reshape(1, 1, 3), cv2.COLOR_BGR2HSV)

    # Define your color ranges
    lower_blue = create_color(75, 80, 100)
    upper_blue = create_color(100, 255, 255)

    lower_pink = create_color(140, 50, 50)
    upper_pink = create_color(170, 255, 255)

    lower_yellow = create_color(32, 100, 100)
    upper_yellow = create_color(60, 255, 255)

    # Check if the center pixel matches any of the color ranges
    is_center_pixel_blue = cv2.inRange(center_pixel_hsv, lower_blue, upper_blue) > 0
    is_center_pixel_pink = cv2.inRange(center_pixel_hsv, lower_pink, upper_pink) > 0
    is_center_pixel_yellow = cv2.inRange(center_pixel_hsv, lower_yellow, upper_yellow) > 0

    # Process the center pixel results through detecting_colors and print_detected_color functions
    detect_blue = detecting_colors(is_center_pixel_blue)
    print_detected_color(detect_blue, 'Blue')
    
    detect_pink = detecting_colors(is_center_pixel_pink)
    print_detected_color(detect_pink, 'Pink')

    detect_yellow = detecting_colors(is_center_pixel_yellow)
    print_detected_color(detect_yellow, 'Yellow')

    # Display the center pixel with a circle
    frame_with_center = cv2.circle(frame.copy(), (center_x, center_y), 5, (0, 0, 255), -1)  # Draw a red circle on the center pixel
    cv2.imshow('frame', frame_with_center)

    detected_color = None
    content = None
    if detect_blue == '1':
        detected_color = 'Blue'
    elif detect_pink == '1':
        detected_color = 'Pink'
    elif detect_yellow == '1':
        detected_color = 'Yellow'

    current_time = time.time()  # Get the current time
    if detected_color and (current_time - content_detection_timer >= time_for_message):
        content = cargo.get(detected_color)
        contamination_level += contamination.get(content, 0)
        content_detection_timer = current_time  # Reset the timer

    if content:
        print(f'Content: {content}, Contamination Level: {contamination_level}')
    # Create a way to kill the program
    if cv2.waitKey(1) == ord('q'):
        break
    elif cv2.waitKey(1) == ord('e'):
        contamination_level == 0


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
    
