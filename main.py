#imports
import time
import subprocess
import requests
from subprocess import Popen
from os import path
from pymouse import PyMouse
from pykeyboard import PyKeyboard
from bs4 import BeautifulSoup as bs

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
#print(soup) #limited because wont get webcam source due to being loaded after using js

from selenium import webdriver
from time import sleep

path="HomeworkRobot\\chromedriver.exe"
driver=webdriver.Chrome(path)
driver.get('http://octopi.local/webcam/?action=stream&1609656825275') #TODO make webdriver headless its annoying
driver.get_screenshot_as_file("screenshot.png") #TODO ss doesent work
driver.quit()
print("end...")

#TODO clean this shit please

#ok well its an action stream so i just need to download one frame



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
#figure out how to send commands to rpi to send the image back and forth on web server
#LaserGRBL must be half split in top left of the screen
#maybe octoprint search for div to send gcode or retrieve image to parse on pc, local webserver

#wait thats actually so much easier just octoprint server the thing wtf
#https://github.com/dragondgold/octo-control easy clap