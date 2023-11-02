#import dependencies
import numpy as np

import RPi.GPIO as GPIO


from tkinter import *

import os

import time
from time import sleep

#import opencv for computer vision stuff

import cv2

#import matplotlip so we can visualize an image

from matplotlib import pyplot as plt

#########################################################################
# GPIO Setup
#########################################################################
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(13, GPIO.OUT)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT)

###########################################################################
###########################################################################
###########################################################################

endme = 0


#initialize a variable to track last messages
last_detection_time = {'Blue': 0, 'Pink': 0, 'Yellow': 0, 'Purple': 0}

#define a time interval to display the printed message
time_for_message = .62

content_detection_timer = time.time()

#create a dictionary for contents
cargo = {'Blue': 'Coal', 'Pink': 'Molten Phenol', 'Yellow': 'Chicken'}

#dictionary for cargo to contamination level
contamination = {'Coal': 1, 'Molten Phenol': 10, 'Chicken': 0}

#variable to track the contamination level
contamination_level = 0

cargolist = []

switching = 'No'

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

def reset_vari():
    global contamination_level
    global cargolist
    global switching
    global led_timer
    contamination_level = 0
    cargolist = []
    switching = 'No'
    led_timer = 0

#define function to print detected color
def print_detected_color(value, color):
    current_time = time.time()
    if value == '1' and (current_time - last_detection_time[color] >= time_for_message):
        if color == 'Purple':
            global endme
            endme += 1
        else:
            print(f'{color} Detected')
            last_detection_time[color] = current_time

def update_labels():
    contamination_label.config(text="Risk Level:   {}".format(contamination_level))
    contents_label.config(text="Contents:   {}".format(cargolist))
    switching_label.config(text="Switching:   {}".format(switching))

def blink():
    led_timer = 0
    while led_timer <= 4:
        if switching == "Yes":
            for i in range(0, 2):
                GPIO.output(13, GPIO.HIGH)
                sleep(0.5)
                GPIO.output(13, GPIO.LOW)
                sleep(0.5)
            led_timer += 1
        elif switching == "No":
            GPIO.output(12, GPIO.HIGH)
            sleep(0.5)
            GPIO.output(12, GPIO.LOW)
            sleep(0.5)
            led_timer += 1

def startcode():
    global cap
    global last_detection_time
    global time_for_message
    global content_detection_timer
    global cargo
    global contamination
    global contamination_level
    global cargolist
    global switching
    global endme
    cap = cv2.VideoCapture(00000000)
    
    reset_vari()
    

    while True:
        # get a frame from the camera
        ret, frame = cap.read()
        width = int(cap.get(3))
        height = int(cap.get(4))

        #calculate the coordinates of the center pixel
        center_x = width // 2
        center_y = height // 2

        #convert the center pixel to HSV color
        center_pixel_hsv = cv2.cvtColor(frame[center_y, center_x].reshape(1, 1, 3), cv2.COLOR_BGR2HSV)

        #define your color ranges
        lower_blue = create_color(75, 70, 100)
        upper_blue = create_color(120, 255, 255)

        lower_pink = create_color(158, 50, 100)
        upper_pink = create_color(175, 255, 255)

        lower_yellow = create_color(30, 2, 100)
        upper_yellow = create_color(60, 255, 255)

        lower_purple = create_color(121, 30, 100)
        upper_purple = create_color(149, 255, 225)

        #check if the center pixel matches any of the color ranges
        is_center_pixel_blue = cv2.inRange(center_pixel_hsv, lower_blue, upper_blue) > 0
        is_center_pixel_pink = cv2.inRange(center_pixel_hsv, lower_pink, upper_pink) > 0
        is_center_pixel_yellow = cv2.inRange(center_pixel_hsv, lower_yellow, upper_yellow) > 0
        is_center_pixel_purple = cv2.inRange(center_pixel_hsv, lower_purple, upper_purple) > 0

        #process the center pixel results through detecting_colors and print_detected_color functions
        detect_blue = detecting_colors(is_center_pixel_blue)
        print_detected_color(detect_blue, 'Blue')
        
        detect_pink = detecting_colors(is_center_pixel_pink)
        print_detected_color(detect_pink, 'Pink')

        detect_yellow = detecting_colors(is_center_pixel_yellow)
        print_detected_color(detect_yellow, 'Yellow')

        detect_purple = detecting_colors(is_center_pixel_purple)
        print_detected_color(detect_purple, 'Purple')

        #display the center pixel with a circle
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
        elif detected_color == '1':
            detected_color = 'Purple'
            

        current_time = time.time()  # Get the current time
        if detected_color and (current_time - content_detection_timer >= time_for_message):
            #determine cargo based off color
            content = cargo.get(detected_color)
            
            #append cargo to the list
            if content not in cargolist:
                cargolist.append(content)

            #add to the contamination level based off cargo
            contamination_level += contamination.get(content, 0)
            content_detection_timer = current_time  # Reset the timer

        if content:
            print(f'Content: {content}, Contamination Level: {contamination_level}')
        # Create a way to kill the program and reset the contamination level
        if cv2.waitKey(1) == ord('q') or endme == 1:
            break

        if contamination_level >= 10:
            switching = 'Yes'

    endme = 0
    cap.release()
    cv2.destroyAllWindows()
    update_labels()
    window.update_idletasks()

def combine():
    startcode()
    blink()



        


window = Tk()
window.title("Freshman Expo")
window.minsize(1600, 1200)
window.config(bg="#211AC6")

window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

######################################################################
# Top Frame
######################################################################
topFrame = Frame(window, width=1200, height=100, bg='white')
topFrame.grid(row=0, column=0,columnspan=3, sticky = N, padx=10, pady=1)

Label(topFrame, text="Railway Contamination Reduction System", font=("Impact", 70), bg="white", fg="blue").grid(row=1, column=1, columnspan=2, padx=40)

######################################################################
# Info Display
######################################################################
statusFrame = Frame(window, width=800, height=200, bg='white')
statusFrame.grid(row=0, column=0, sticky = W, padx = 10, pady=1)

contamination_label = Label(statusFrame, text="", font=("Times", 64), bg="white",  fg="blue")
contamination_label.grid(row=1, column=0, sticky=W, padx=10)

contents_label = Label(statusFrame, text="", font=("Times", 64), bg="white",  fg="blue")
contents_label.grid(row=2, column=0, sticky=W, padx=10)

switchingFrame = Frame(window, width=200, height=100, bg='white')
switchingFrame.grid(row=0, column=2, sticky = E, padx = 10, pady=1)

Label(switchingFrame, text="            Notice:            ", font=('Times 64 underline'), bg="white", fg="blue").grid(row=0, column=0, columnspan=2, padx=4)                                                                                       

switching_label = Label(switchingFrame, text="", font=("Times", 64), bg="white",  fg="blue")
switching_label.grid(row=1, column=0, sticky=W, padx=10)

######################################################################
# Track Image Display
trackFrame = Frame(window, bg='skyblue')
trackFrame.grid(row=2, column=0, columnspan=3, padx = 10, pady=1)

image = PhotoImage(file=os.path.join("gojo.gif"))               #Insert an image(same folder)
img = Label(trackFrame, image=image)
img.image = image
img.pack()

######################################################################
# Button to start Bricky's Code

# hello
update_labels()

scanCargo = Button(window, text="Scan Cargo", font=("Times", 32), command=combine).grid(row=3, column=0, columnspan=4)
    
window.mainloop()

