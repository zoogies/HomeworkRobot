# imports
from time import sleep
from datetime import datetime
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


def waitForElement(elementName):
    try:
        WebDriverWait(driver, waitTime).until(
            ec.visibility_of_element_located((By.ID, elementName))
        )
    except:
        print(
            datetime.now(),
            "- ERROR - selenium timout after",
            waitTime,
            "seconds",
        )
        exit()


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
    # TODO make string parser

    print(datetime.now(), "- DETECTED TEXT -", text)
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
print(datetime.now(), "- driver started")
driver.find_element_by_id("login-user").send_keys(octoCreds[0])  # enter username
driver.find_element_by_id("login-password").send_keys(octoCreds[1])  # enter password
driver.find_element_by_id("login-button").click()  # login
print(datetime.now(), "- logged in")

# take screenshot of webcam as well as trim and rotate it by specified offset

# wait for stream to load
waitForElement("webcam_image_framing")

driver.execute_script("window.scrollTo(1080, 0)")  # scroll to top right
driver.save_screenshot("images\\stream.png")  # take screenshot
print(datetime.now(), "- screenshot taken")
driver.quit()  # terminate driver
print(datetime.now(), "- driver quit")

# crop screenshot for parsing
im = Image.open("images\\stream.png")  # load the image
im = im.crop((160, 110, 745, 545))  # crop out corners of webpage
im = im.rotate(offset, expand=True)  # rotate image

im = im.convert("L")  # grayscale
im = im.filter(ImageFilter.MedianFilter())  # a little blur
im = im.point(lambda x: 0 if x < 80 else 255)  # threshold (binarize)
im = im.crop((216, 436, 434, 555))  # crop out corners of webpage
im = ImageOps.invert(im).save("images\\stream.png")

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
print(datetime.now(), "- driver started")
driver.find_element_by_id("login-user").send_keys(octoCreds[0])  # enter username
driver.find_element_by_id("login-password").send_keys(octoCreds[1])  # enter password
driver.find_element_by_id("login-button").click()  # login
print(datetime.now(), "- logged in")

waitForElement("term_link")

driver.find_element_by_id("term_link").click()  # focus terminal

# using sleep here physically hurts my brain but literally
# nothing else works because selenium waiting for dynamic
# elements to become enabled is stupid and broken
sleep(5)
# TODO maybe try except select until it works

# visualize(str(calculateAnswer()))

try:
    # NOTES
    # - need to have the toolhead the highest it can go and zero it there
    # - touching the paper is Z-44
    # - for move ops it shoudld be -40

    # setup commands
    # zero at top
    driver.find_element_by_id("terminal-command").send_keys(
        "G92X0Y0Z0"
    )  # this might need to move to like the top left of page if do multiple in one process
    driver.find_element_by_id("terminal-command").send_keys(Keys.ENTER)
    print(datetime.now, "- zeroing x y and z axis")
    sleep(1)  # give a sec between startup commands

    # move down offset on y so we dont write ON the text
    driver.find_element_by_id("terminal-command").send_keys("G0Y-10")
    driver.find_element_by_id("terminal-command").send_keys(Keys.ENTER)
    print(datetime.now, "- moving below text")
    sleep(3)  # give toolhead a second to move

    # move down to hover position
    driver.find_element_by_id("terminal-command").send_keys("G0Z-40")
    driver.find_element_by_id("terminal-command").send_keys(Keys.ENTER)
    print(datetime.now, "- moving pen down to rest position")
    sleep(5)  # give toolhead a second to move

    for command in ttg((str(calculateAnswer())), 2, 0, "return", 2000).toGcode(
        "Z-44", "Z-40", "G0", "G1"
    ):
        print(command)
        sleep(1)
        driver.find_element_by_id("terminal-command").send_keys(command)
        driver.find_element_by_id("terminal-command").send_keys(Keys.ENTER)

except Exception as error:
    print(
        datetime.now(),
        "- ERROR - selenium is stupid, please modify main.py and make the sleep last longer",
    )
    print(error)
    driver.quit()  # terminate driver
    exit()

input("press any key to close ")
driver.quit()  # terminate driver
exit()
# TODO ttglib validate input data and return errors
# TODO ttglib missing a G0


# TODO
# - speed between points
# - lib optimizations not to return to zero, (understand whole context of text and move to next point)
# - make it not write on top of the text lmao, make offset under
# - auto calculate from string