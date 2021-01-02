"""
OLD SERIAL TESTS

import serial
import time

ser = serial.Serial()
ser.baudrate = 115200
ser.port = "COM3"
ser.open()

ser.write(b"M3 S50")
#ser.write(b"$J=G91X10.0F1000")
#print("G0 X10 Y10\r\n")

#G0 X10 Y10
#M3 S0

ser.close()
"""

#figure out how to send commands to rpi to send the image back and forth on web server
#LaserGRBL must be half split in top left of the screen

#imports
import time
import subprocess
from subprocess import Popen
from os import path
from pymouse import PyMouse
from pykeyboard import PyKeyboard

#setup mouse and keyboard
m = PyMouse()
k = PyKeyboard()

#create the path .txt and auto assume the path
if(not path.exists("HomeworkRobot\path.txt")):
    grblPath = open("HomeworkRobot\path.txt", "x")
    grblPath.write('"C:\Program Files (x86)\LaserGRBL"')

#open laserGRBL using the path specified in path.txt
grblPath = open("HomeworkRobot\path.txt", "r").read()
subprocess.Popen(grblPath)

#laserGRBL initialization
time.sleep(3) #await laserGRBL open
m.click(564, 68, 1) #connect to serial
m.click(11, 139, 1) #select gcode entrybox

#this is where the connect to write probems code goes

#test gcode
k.type_string('G0 X10 Y10')
k.tap_key(k.enter_key)