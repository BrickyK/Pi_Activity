from tkinter import *
import os

window = Tk()
window.title("Test")
window.config(bg="grey")

contamination_level = 40
contents = "Something Stupid"
switching = "Yes"
######################################################################
# Top Frame
######################################################################
topFrame = Frame(window, width=600, height=50, bg='white')
topFrame.grid(row=0, column=0,columnspan=2, padx=10, pady=10)

Label(topFrame, text="Title of Project why is it blue", bg="white", fg="blue").grid(row=1, column=0, columnspan=2, padx=40)

######################################################################
# Info Display
######################################################################
statusFrame = Frame(window, width=200, height=100, bg='white')
statusFrame.grid(row=1, column=0, pady=10)

Label(statusFrame, text="Contamination Level: {}".format(contamination_level), bg="white",  fg="blue").grid(row=1, column=0, padx=10)
Label(statusFrame, text="Contents: {}".format(contents), bg="white",  fg="blue").grid(row=2, column=0)
Label(statusFrame, text="Switching: {}".format(switching), bg="white",  fg="blue").grid(row=3, column=0)

######################################################################
# Track Image Display
trackFrame = Frame(window, width=650, height=400, bg='skyblue')
trackFrame.grid(row=2, column=0, pady=10)
