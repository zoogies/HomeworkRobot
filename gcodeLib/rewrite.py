# TODO naming convention of basically everything
# double check globals, can prob abstract away many things
# TODO consider putting all the letters in their own class/file/seperate files
# TODO rewrite space as not just offset -- Why did i say this?

import math
import time
from os import rename, remove


class ttg:
    def __init__(self, text, size, rotation, method):
        # set basic passed args
        self.text = text
        self.size = size
        self.rotation = rotation
        self.method = method

        # set global class vars
        self.rotationNeeded = False
        self.readyForReturn = False
        self.operations = []
        self.currentXOffset = 0
        self.parsed = False
        self.verts = []

        # set defualts commands, TODO have function thats toGcode with custom commands
        self.offCmd = "M5"
        self.onCmd = "M3"
        self.fastCmd = "G0"
        self.slowCmd = "G1"

        # check if the user has specified a positive or negative rotation
        if self.rotation != 0:
            self.rotationNeeded = True

    def finalize(self):
        finalOperations = []

        for point in self.operations:
            if type(point) is tuple:
                originX = 0
                originY = 0
                newpointX = (
                    originX
                    + math.cos(self.rotation) * (point[0] - originX)
                    - math.sin(self.rotation) * (point[1] - originY)
                )
                newpointY = (
                    originY
                    + math.sin(self.rotation) * (point[0] - originX)
                    + math.cos(self.rotation) * (point[1] - originY)
                )
                newpoint = (newpointX, newpointY)
                finalOperations.append(newpoint)
            elif isinstance(point, str):
                finalOperations.append(point)

        # replace placeholder string commands with GCODE commands
        for count, command in enumerate(finalOperations):
            if command == "off":
                finalOperations[count] = self.offPowerCmd
            elif command == "on":
                finalOperations[count] = self.onPowerCmd
            elif command == "fast":
                finalOperations[count] = self.fastCmd
            elif command == "slow":
                finalOperations[count] = self.slowCmd

        if self.method == "visualize":
            return finalOperations

        elif self.method == "return" or self.method == "file":
            if self.method == "file":
                try:
                    remove("output.txt")
                except:
                    pass
                gFile = open("output.txt", "a")

            returnList = []
            lastMoveType = ""

            for command in finalOperations:
                currentCommand = ""

                if command == self.onPowerCmd:
                    currentCommand = self.onPowerCmd
                elif command == self.offPowerCmd:
                    currentCommand = self.offPowerCmd

                if command == self.slowCmd:
                    lastMoveType = "slow"
                    pass
                elif command == self.fastCmd:
                    lastMoveType = "slow"
                    pass

                if type(command) == tuple:
                    if lastMoveType == "slow":
                        currentCommand += self.slowCmd
                    elif lastMoveType == "fast":
                        currentCommand += self.fastCmd
                    # TODO text size
                    currentCommand += " X" + str(command[0])
                    currentCommand += " Y" + str(command[1])

                # TODO modify if statement for write to file
                if currentCommand != "":
                    returnList.append(currentCommand)

            if self.method == "return":
                return returnList

            elif self.method == "file":
                for line in returnList:
                    gFile.write(line + "\n")

                gFile.close()

                try:
                    remove("output.gcode")
                except:
                    pass

                rename(r"output.txt", r"output.gcode")

                return "output.gcode file generated successfully"

    def appendPoints(self, points):
        for point in points:
            self.operations.append(point)

    # LETTER FUNCTIONS

    def whiteSpace(self):
        self.currentXOffset += 4  # TODO check if this is right for character spaces

    #           .   .
    #       .           .
    #   .                   .
    #   .                   .
    #   .                   .
    #   .   .   .   .   .   .
    #   .                   .
    #   .                   .
    #   .                   .
    #   .                   .

    def a(self):  # TODO rewrite
        xOff = self.currentXOffset

        points = [
            "on",
            "slow",
            (0 + xOff, 0),
            (0 + xOff, 7),
            (1 + xOff, 8),
            (2 + xOff, 9),
            (3 + xOff, 9),
            (4 + xOff, 8),
            (5 + xOff, 7),
            (5 + xOff, 0),
            "off",
            "fast",
            (5 + xOff, 4),
            "on",
            "slow",
            (0 + xOff, 4),
            "off",
            "fast",
            (0 + xOff, 0),
        ]

        ttg.appendPoints(self, points)

    # TODO alright heres the requirements for letter verts
    # - every point has a tuple
    # - off on fast slow
    # - every list starts with on and ends with off

    #   .   .   .   .
    #   .               .
    #   .                   .
    #   .                   .
    #   .               .
    #   .   .   .   .
    #   .               .
    #   .                   .
    #   .                   .
    #   .   .   .   .   .

    def b(self):
        xOff = self.currentXOffset

        points = [
            "on",
            "slow",
            (0 + xOff, 0),
            (0 + xOff, 9),
            (3 + xOff, 9),
            (4 + xOff, 8),
            (5 + xOff, 7),
            (5 + xOff, 6),
            (4 + xOff, 5),
            (3 + xOff, 4),
            (0 + xOff, 4),
            "off",
            "fast",
            (3 + xOff, 4),
            "on",
            "slow",
            (4 + xOff, 3),
            (5 + xOff, 2),
            (5 + xOff, 1),
            (4 + xOff, 0),
            (0 + xOff, 0),
            "off",
        ]

        ttg.appendPoints(self, points)

    #       .   .   .   .
    #   .                   .
    #   .
    #   .
    #   .
    #   .
    #   .
    #   .
    #   .                   .
    #       .   .   .   .

    def c(self):
        xOff = self.currentXOffset

        points = [
            "off",
            "fast",
            (5 + xOff, 1),
            "on",
            "slow",
            (4 + xOff, 0),
            (1 + xOff, 0),
            (0 + xOff, 1),
            (0 + xOff, 8),
            (1 + xOff, 9),
            (4 + xOff, 9),
            (5 + xOff, 8),
            "off",
            "fast",
            (0 + xOff, 0),
        ]

        ttg.appendPoints(self, points)

    # FOOTER

    # get and call functions for letter in given text and append them to queue
    def collectCharacters(self):
        for char in self.text:
            if char == " ":
                ttg.whiteSpace(self)
                self.currentXOffset += 8

            if char == "a" or char == "A":
                ttg.a(self)
                self.currentXOffset += 8

            if char == "b" or char == "B":
                ttg.b(self)
                self.currentXOffset += 8

            if char == "c" or char == "C":
                ttg.c(self)
                self.currentXOffset += 8

        return ttg.finalize(self)

    def encode(self):
        if self.readyForReturn and self.method == "visualize":
            return self.verts

        elif not self.readyForReturn:
            return ttg.collectCharacters(self)

    def toGcode(self, onPower, offPower, fast, slow):
        self.onPowerCmd = onPower
        self.offPowerCmd = offPower
        self.fastCmd = fast
        self.slowCmd = slow

        return ttg.encode(self)