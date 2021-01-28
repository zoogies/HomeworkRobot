# imports
from time import sleep
import datetime
import pytesseract as tess
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys


from tests import servertest

from ttgLib.TextToGcode import ttg

import matplotlib.pyplot as plt
from math import radians

# conscise TODO
# - print mount for pi on back of laser
# - cleanup repo files
# - throw exception if there is no text files for creds
# - pair down imports

# set offset for image rotation, should be fed from electron later (potentially)
offset = -90  # or just prompt at the beginning or as an optional arg
octoCreds = ""
waitTime = 25

# test server connection
def testConnection(ip, port):
    return servertest.tests().connectTest(ip, port)


def visualize(text):  # consider moving this into a test
    plotlist = []

    for item in ttg(text, 1, 0, "visualize", 2000).toGcode("Z10", "Z0", "G0", "G1"):
        if type(item) is tuple:
            plotlist.append(item)

    print("plotlist:", plotlist)
    pltx = []
    plty = []

    for tup in plotlist:
        pltx.append(tup[0])
        plty.append(tup[1])

    plt.scatter(pltx, plty)
    plt.show()


# parse the text from screenshot and calculate it as a multiplication problem
def calculateAnswer():
    # retrieve path on system to tesseract executable from file
    with open("tesseractPath.txt", "r") as tessPath:
        tess.pytesseract.tesseract_cmd = tessPath.read()

    # convert image text to a list of strings seperated by the multiplication operand
    text = tess.image_to_string(
        Image.open("images\\stream.png"),
        lang="eng",
        config="-c tessedit_char_whitelist=1234567890x",
    )

    # TODO check basic validity of answers before engraving

    print(datetime.datetime.now(), "- DETECTED TEXT -", text)
    if "x" in text:
        text = text.split("x")
        return int(text[0]) * int(text[1])
    elif "+" in text:
        text = text.split("+")
        return int(text[0]) + int(text[1])
    elif "-" in text:
        text = text.split("-")
        return int(text[0]) - int(text[1])
    elif "/" in text:
        text = text.split("/")
        return int(text[0]) / int(text[1])


# get octoprint login creds from file
with open("loginCreds.txt", "r") as loginCreds:
    octoCreds = loginCreds.read().split(" ")

# create headless webdriver
op = webdriver.ChromeOptions()
op.add_argument("headless")
path = "chromedriver.exe"
driver = webdriver.Chrome(path, options=op)

# send webdriver to local octoprint page and login
driver.get("http://octopi.local/?#control")  # redirect to webcam page
print(datetime.datetime.now(), "- driver started")
driver.find_element_by_id("login-user").send_keys(octoCreds[0])  # enter username
driver.find_element_by_id("login-password").send_keys(octoCreds[1])  # enter password
driver.find_element_by_id("login-button").click()  # login
print(datetime.datetime.now(), "- logged in")

# take screenshot of webcam as well as trim and rotate it by specified offset

# wait for stream to load
try:
    WebDriverWait(driver, waitTime).until(
        ec.visibility_of_element_located((By.ID, "webcam_image_framing"))
    )
except:
    print("ERROR - selenium timout after", waitTime, "seconds")
    exit()

driver.execute_script("window.scrollTo(1080, 0)")  # scroll to top right
driver.save_screenshot("images\\stream.png")  # take screenshot
print(datetime.datetime.now(), "- screenshot taken")
driver.quit()  # terminate driver
print(datetime.datetime.now(), "- driver quit")

# crop screenshot for parsing
im = Image.open("images\\stream.png")  # load the image
im = im.crop((160, 110, 745, 545))  # crop out corners of webpage
im = im.rotate(offset, expand=True)  # rotate image

im = im.convert("L")  # grayscale
im = im.filter(ImageFilter.MedianFilter())  # a little blur
im = im.point(lambda x: 0 if x < 80 else 255)  # threshold (binarize)
im = im.crop((216, 436, 434, 555))  # crop out corners of webpage
im = ImageOps.invert(im).save("images\\stream.png")

print(calculateAnswer())

# visualize(str(calculateAnswer()))

# MODEL:
# while we open webdriver and are issuing commands user can quit
# by control c or xing or whatever

# SECOND WEB DRIVER FOR COMMANDS

# create headless webdriver
op = webdriver.ChromeOptions()
op.add_argument("headless")
path = "chromedriver.exe"
# driver = webdriver.Chrome(path, options=op)
driver = webdriver.Chrome(path)

# send webdriver to local octoprint page and login
driver.get("http://octopi.local/#term")  # redirect to webcam page
print(datetime.datetime.now(), "- driver started")
driver.find_element_by_id("login-user").send_keys(octoCreds[0])  # enter username
driver.find_element_by_id("login-password").send_keys(octoCreds[1])  # enter password
driver.find_element_by_id("login-button").click()  # login
print(datetime.datetime.now(), "- logged in")

try:
    WebDriverWait(driver, waitTime).until(
        ec.visibility_of_element_located((By.ID, "term_link"))
    )
except:
    print("ERROR - selenium timout after", waitTime, "seconds")
    exit()

driver.find_element_by_id("term_link").click()  # focus terminal

try:
    WebDriverWait(driver, waitTime).until(
        ec.visibility_of_element_located((By.ID, "terminal-command"))
    )
except:
    print("ERROR - selenium timout after", waitTime, "seconds")
    exit()
sleep(5)
terminal = driver.find_element_by_id("terminal-command")
print(terminal)
terminal.sendKeys("G0X10")
terminal.send_keys(Keys.ENTER)

# TODO
# Traceback (most recent call last):
#   File "c:\Users\swoos\Documents\GitHub\HomeworkRobot\main.py", line 173, in <module>
#     terminal.sendKeys("G0X10")
# AttributeError: 'WebElement' object has no attribute 'sendKeys'