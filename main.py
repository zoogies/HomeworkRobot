# imports
from time import sleep
import datetime
import pytesseract as tess
from PIL import Image
from selenium import webdriver
from tests import servertest

from gcodeLib.rewrite import ttg

import matplotlib.pyplot as plt
from math import radians  # TODO pair down imports

# TODO throw exception if there is no text files for creds

# set offset for image rotation, should be fed from electron later (potentially)
offset = 0  # or just prompt at the beginning or as an optional arg
octoCreds = ""
waitTime = 30

# test server connection
def testConnection(ip, port):
    return servertest.tests().connectTest(ip, port)


def createDriver(octoCreds):
    # get octoprint login creds from file
    if octoCreds == "":
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
    driver.find_element_by_id("login-password").send_keys(
        octoCreds[1]
    )  # enter password
    driver.find_element_by_id("login-button").click()  # login

    print(datetime.datetime.now(), "- logged in")

    return driver


# take screenshot of webcam as well as trim and rotate it by specified offset
def getWebcamFrame(waitTime):

    driver = createDriver(octoCreds)  # create a new driver

    sleep(waitTime)  # wait for stream to load
    driver.execute_script("window.scrollTo(1080, 0)")  # scroll to top right
    driver.save_screenshot("images\\stream.png")  # take screenshot

    print(datetime.datetime.now(), "- screenshot taken")

    driver.quit()  # terminate driver

    print(datetime.datetime.now(), "- driver quit")

    # crop screenshot for parsing
    im = Image.open("images\\stream.png")  # load the image
    im = im.crop((160, 180, 745, 545))  # crop out corners
    im = im.rotate(offset, expand=True).save("images\\stream.png")  # rotate and save


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

    # TODO look for key operators and split by that depending on whats shown, then you can do every operation
    # maybe find library that solves from string so that you can do anything
    # check basic validity of answers before engraving
    text = text.split("x")
    return int(text[0]) * int(text[1])


def visualize():  # consider moving this into a test
    plotlist = []

    for item in ttg("poggers", 1, radians(offset), "visualize", 500).toGcode(
        "ON", "OFF", "FAST", "SLOW"
    ):
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


def sendCommands():
    createDriver(octoCreds)


# getWebcamFrame(waitTime)
# calculateAnswer()
"""
print(
    ttg("a b c d  abcd", 1, radians(offset), "file", 2000).toGcode(
        "M03 S500", "M05 S0", "G0", "G1"
    )
)
"""
# on off format is
# M05 S0, M03 S500

# text size is mm
visualize()
# conscise TODO
# - pipeline to send commands to printer
# - print mount for pi on back of laser
# - extra cable management
# - cleanup repo files