# imports
import time
import datetime
import cv2
import re
import pytesseract as tess
from PIL import Image
from selenium import webdriver

#set offset for image rotation, should be fed from electron later (potentially)
offset = -90

def getWebcamFrame():
    #get octoprint login creds from file
    with open("HomeworkRobot\loginCreds.txt", "r") as loginCreds:
        octoCreds = loginCreds.read().split(" ")

    #create headless webdriver
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    path = "HomeworkRobot\\chromedriver.exe"
    driver = webdriver.Chrome(path, options=op)

    #send webdriver to local octoprint page and login
    driver.get('http://octopi.local/?#control')                                         #redirect to webcam page

    print(datetime.datetime.now(), "- driver started")

    driver.find_element_by_id("login-user").send_keys(octoCreds[0])                     #enter username
    driver.find_element_by_id("login-password").send_keys(octoCreds[1])                 #enter password
    driver.find_element_by_id("login-button").click()                                   #login

    print(datetime.datetime.now(), "- logged in")

    time.sleep(6)                                                                       #wait for stream to load
    driver.execute_script("window.scrollTo(1080, 0)")                                   #scroll to top right
    driver.save_screenshot("HomeworkRobot\\images\\stream.png")                         #take screenshot

    print(datetime.datetime.now(), "- screenshot taken")

    driver.quit()                                                                       #terminate driver

    print(datetime.datetime.now(), "- driver quit")

    #crop screenshot for parsing
    im = Image.open("HomeworkRobot\\images\\stream.png")                                #load the image
    im = im.crop((160, 180, 745, 545))                                                  #crop out corners
    im = im.rotate(offset, expand = True).save("HomeworkRobot\\images\\stream.png")     #rotate and save
    
#tess shit
def tessShit():
    with open("HomeworkRobot\\tesseractPath.txt", "r") as tessPath:
        tess.pytesseract.tesseract_cmd = tessPath.read()

    text = tess.image_to_string("HomeworkRobot\\images\\stream.png")
    print("."+text+".")

getWebcamFrame()
tessShit()

#conscise TODO
# - pipeline to send commands to printer
# - process image and calculate it
# - take calculated answer and transfer number points to gcode commands for printer
# - print mount for pi on back of laser
# - extra cable management





#other shit:
#70D10AE2AB3048B8AEA90CD1F4B74C3D api key
#def sendCommand():
    #maybe connect by importing or shell
    #might even be able to send the completed gcode file over tbh
# TODO maybe move driver and other stuff organize filesystem
# TODO put this all in an electron application readout progress on web driver? stream to panel on electron app?
# https://github.com/dragondgold/octo-control easy clap