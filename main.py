# imports
import time
from PIL import Image
from selenium import webdriver

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
    driver.get('http://octopi.local/?#control')                             #redirect to webcam page
    driver.find_element_by_id("login-user").send_keys(octoCreds[0])         #enter username
    driver.find_element_by_id("login-password").send_keys(octoCreds[1])     #enter password
    driver.find_element_by_id("login-button").click()                       #login
    time.sleep(3)                                                           #wait for redirect
    driver.get('http://octopi.local/?#control')                             #send to webcam stream
    time.sleep(3)                                                           #wait for redirect
    driver.execute_script("window.scrollTo(1080, 0)")                       #scroll to top right
    driver.save_screenshot("HomeworkRobot\\images\\stream.png")             #take screenshot
    driver.quit()                                                           #terminate driver

    #crop screenshot for parsing
    im = Image.open("HomeworkRobot\\images\\stream.png")
    im.crop((233, 108, 675, 439)).save("HomeworkRobot\\images\\stream_crop.png", quality=100)

#70D10AE2AB3048B8AEA90CD1F4B74C3D api key

#def sendCommand():
    #maybe connect by importing or shell
    #might even be able to send the completed gcode file over tbh

# TODO maybe move driver and other stuff organize filesystem
# TODO put this all in an electron application readout progress on web driver? stream to panel on electron app?
# https://github.com/dragondgold/octo-control easy clap