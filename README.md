# Homework Robot

[![time tracker](https://wakatime.com/badge/github/Yoyolick/HomeworkRobot.svg)](https://wakatime.com/badge/github/Yoyolick/HomeworkRobot) [![Maintainability](https://api.codeclimate.com/v1/badges/d02830cae1461df36a87/maintainability)](https://codeclimate.com/github/Yoyolick/HomeworkRobot/maintainability)

A WIP codebase to solve math problems and laser engrave them onto the worksheet.

## Dependancies

Homework robot makes the assumption that you are running a setup very similar to the following:

- Raspberry pi octoprint server connected to laser engraver main board
- raspberry pi camera connected and mounted on the side of the laser toolhead
- repository cloned to laptop or desktop windows computer

## Setup

To run the project successfully you need to do the following:

1. [download chromedriver](https://chromedriver.chromium.org/downloads) to root of the directory

2. run the `dependancies.bat` file

3. replace the text in `tesseractPath.txt` with the path to your tesseract install. ex: `C:\Users\USERNAME\AppData\Local\Programs\Tesseract-OCR\tesseract.exe`

4. create the file `loginCreds.txt` in the root of the `HomeworkRobot` directory and type your octoprint username and password **seperated by one space on line 1**

5. [install ttg lib](https://github.com/Yoyolick/TextToGcode) as a library through pip

## Usage

- run `main.py`
