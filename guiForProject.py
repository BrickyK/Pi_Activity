from tkinter import *
import os
from final_detect import *

window = Tk()
window.title("Test")
window.config(bg="grey")

risk_level = 40
contents = "Chicken, Molten Phentenol, Coal"
switching = "Yes"

def resetContam():
    contamination_level = 0
    return contamination_level

def resetCont():
    contents = "Null"
    return contents
######################################################################
# Top Frame
######################################################################
topFrame = Frame(window, width=600, height=50, bg='white')
topFrame.grid(row=0, column=0,columnspan=2, padx=10, pady=10)

Label(topFrame, text="Title of Project why is it blue", font=("Impact", 14), bg="white", fg="blue").grid(row=1, column=0, columnspan=2, padx=40)

######################################################################
# Info Display
######################################################################
statusFrame = Frame(window, width=400, height=100, bg='white')
statusFrame.grid(row=1, column=0,sticky = W, padx = 10, pady=10)

Label(statusFrame, text="Risk Level:   {}".format(risk_level), font=("Times", 14), bg="white",  fg="blue").grid(row=1, column=0, sticky = W, padx=10)
Label(statusFrame, text="Contents:   {}".format(contents), font=("Impact", 14), bg="white",  fg="blue").grid(row=2, column=0, sticky = W, padx=10)

switchingFrame = Frame(window, width=200, height=100, bg='white')
switchingFrame.grid(row=1, column=2,sticky = E, padx = 10, pady=10)

Label(switchingFrame, text="            Notice:            ", font=('Impact 14 underline'), bg="white", fg="blue").grid(row=0, column=0, columnspan=2, padx=4)                                                                                       
Label(switchingFrame, text="Switching:   {}".format(switching), font=("Impact", 14), bg="white",  fg="blue").grid(row=1, column=0, sticky = W, padx=10)

######################################################################
# Track Image Display
trackFrame = Frame(window, width=650, height=400, bg='skyblue')
trackFrame.grid(row=2, column=0, padx = 10, pady=10)

image = PhotoImage(file=os.path.join("gojo.gif"))               #Insert an image(same folder)
smallerimg = image.subsample(2, 2)
img = Label(trackFrame, image=smallerimg)
img.image = image
img.pack()

######################################################################
# Button to start Bricky's Code

scanCargo = Button(window, text="Scan Cargo", command=start)
scanCargo.pack()