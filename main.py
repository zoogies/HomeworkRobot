# imports
from selenium import webdriver
import time
import subprocess
import requests
from subprocess import Popen
from os import path
from pymouse import PyMouse
from pykeyboard import PyKeyboard
from bs4 import BeautifulSoup as bs
from PIL import Image

"""
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
"""

"""
cookies = open("HomeworkRobot\cookies.txt").read()
print(cookies)
headers = open("HomeworkRobot\headers.txt").read()
print(headers)
"""

#soup = bs(requests.get('http://octopi.local/webcam/?action=stream&1609656825275').content, "html.parser")
#soup = soup.find_all("img")
##soup = soup.getAttribute('src');
# print(soup) #limited because wont get webcam source due to being loaded after using js




def getWebcamFrame():
    #get octoprint login creds from file
    with open("HomeworkRobot\loginCreds.txt", "r") as loginCreds:
        octoCreds = loginCreds.read().split(" ")

    #create headless driver
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    path = "HomeworkRobot\\chromedriver.exe"
    driver = webdriver.Chrome(path, options=op)

    #send driver to local octoprint page and login
    driver.get('http://octopi.local/?#control')                             #redirect to webcam page
    driver.find_element_by_id("login-user").send_keys(octoCreds[0])         #enter username
    driver.find_element_by_id("login-password").send_keys(octoCreds[1])     #enter password
    driver.find_element_by_id("login-button").click()                       #login
    time.sleep(3)                                                           #wait for redirect
    driver.get('http://octopi.local/?#control')                             #send to webcam stream
    time.sleep(3)                                                           #wait for redirect
    driver.execute_script("window.scrollTo(1080, 0)")                       #scroll to top right
    driver.save_screenshot("HomeworkRobot\\stream.png")                     #take screenshot
    driver.quit()                                                           #terminate driver

    #crop screenshot for parsing
    im = Image.open("HomeworkRobot\\stream.png")
    im.crop((233, 108, 675, 439)).save("HomeworkRobot\\stream_crop.png", quality=100)

# TODO clean this shit please

# ok well its an action stream so i just need to download one frame
# TODO put this all in an electron application readout progress on web driver? stream to panel on electron app?
# TODO design and print mout for camera and pi that slot on

"""
from bs4 import BeautifulSoup
from selenium import webdriver

url = "http://octopi.local/"
browser = webdriver.PhantomJS()
browser.get(url)
html = browser.page_source
soup = BeautifulSoup(html, 'lxml')
a = soup.find_all("img").getAttribute("src")
print(a)
"""
# figure out how to send commands to rpi to send the image back and forth on web server
# LaserGRBL must be half split in top left of the screen
# maybe octoprint search for div to send gcode or retrieve image to parse on pc, local webserver

# wait thats actually so much easier just octoprint server the thing wtf
# https://github.com/dragondgold/octo-control easy clap
