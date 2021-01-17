# Homework Robot - CURRENTLY A WORK IN PROGRESS

[![time tracker](https://wakatime.com/badge/github/Yoyolick/HomeworkRobot.svg)](https://wakatime.com/badge/github/Yoyolick/HomeworkRobot)

A WIP codebase to solve math problems and laser engrave them onto the worksheet.

## Dependancies

Homework robot makes the assumption that you are running a setup very similar to the following:

- Raspberry pi octoprint server connected to laser engraver main board
- raspberry pi camera connected and mounted on the side of the laser toolhead
- repository cloned to laptop or desktop windows computer

## Setup

To run the project successfully you need to have the following done:

1. [chromedriver downloaded](https://chromedriver.chromium.org/downloads) to root of the directory

2. run the `dependancies.bat` file

3. replace the text in `tesseractPath.txt` with the path to your tesseract install. ex: `C:\Users\USERNAME\AppData\Local\Programs\Tesseract-OCR\tesseract.exe`

4. create `loginCreds.txt` in the root of the directory and type your octoprint username and password **seperated by one space on line 1**

5. install ttg lib (TODO this isnt published)

## Usage

- run `main.py`