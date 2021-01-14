# TODO naming convention of basically everything
# double check globals, can prob abstract away many things
# add if switch for returns only if method is return
# check whitespace
# return all letters
# fix bug with adding extra A to front
# bug with repeating letters

import math
import time


class ttg:
    def __init__(self, text, size, rotation):
        # set basic passed args
        self.text = text
        self.size = size
        self.rotation = rotation

        # set global class vars
        self.rotationNeeded = False
        self.readyForReturn = False
        self.operations = []
        self.currentXOffset = 0
        self.parsed = False

        # set defualts commands, TODO have function thats toGcode with custom commands
        self.offCmd = "M5"
        self.onCmd = "M3"
        self.fastCmd = "G0"
        self.slowCmd = "G1"

        # check if the user has specified a positive or negative rotation
        if self.rotation != 0:
            self.rotationNeeded = True

    def rotate(self):
        newOps = []

        for point in self.operations:
            if type(point) is tuple:
                originX = 0  # TODO let this be specified?
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
                newOps.append(newpoint)
            elif isinstance(point, str):
                newOps.append(point)

        self.operations.clear()
        self.operations = newOps

        # replace all commands in one sweep
        for count, command in enumerate(self.operations):
            if command == "off":
                self.operations[count] = self.offCmd
            elif command == "on":
                self.operations[count] = self.onCmd
            elif command == "fast":
                self.operations[count] = self.fastCmd
            elif command == "slow":
                self.operations[count] = self.slowCmd

    def tempOpAdd(self, points):
        for point in points:
            self.operations.append(point)

    # LETTER FUNCTIONS

    def whiteSpace(self):
        self.currentXOffset += 4  # TODO check if this is right for character spaces

    def a(self):  # TODO rewrite
        xOff = self.currentXOffset

        points = [
            (0 + xOff, 0),
            (0 + xOff, 1),
            (0 + xOff, 2),
            (0 + xOff, 3),
            (0 + xOff, 4),
            (1 + xOff, 5),
            (2 + xOff, 5),
            (3 + xOff, 5),
            (4 + xOff, 4),
            (4 + xOff, 3),
            (4 + xOff, 2),
            (3 + xOff, 2),
            (2 + xOff, 2),
            (1 + xOff, 2),
            (0 + xOff, 2),
            "off",
            "fast",
            (4 + xOff, 2),
            "on",
            "slow",
            (4 + xOff, 1),
            (4 + xOff, 0),
        ]

        ttg.tempOpAdd(self, points)

    # TODO alright heres the requirements for letter verts
    # - every point has a tuple
    # - off on fast slow
    # - every list starts with on and ends with off
    # TODO rewrite space as not just offset

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

        ttg.tempOpAdd(self, points)

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

        ttg.tempOpAdd(self, points)

    # FOOTER

    # get and call functions for letter in given text and append them to queue
    def collectCharacters(self):
        charList = []

        for char in self.text:
            charList.append(char)

        for char in charList:
            if char == " ":
                ttg.whiteSpace(self)
                self.currentXOffset += 8

            elif char == "c" or "C":
                ttg.c(self)
                self.currentXOffset += 8

            elif char == "b" or "B":
                ttg.b(self)
                self.currentXOffset += 8

            elif char == "a" or "A":
                ttg.a(self)
                self.currentXOffset += 8

        ttg.rotate(self)

        return self.operations  # DEBUG

    def toGcode(self, method):
        if self.readyForReturn and method == "return":
            # TODO make method a self and decide between make file and return at end of parse
            return "TODO placeholder"

        elif not self.readyForReturn:
            return ttg.collectCharacters(self)

    def toGcodeCustom(self, method, on, off, fast, slow):
        self.onCmd = on
        self.offCmd = off
        self.fastCmd = fast
        self.slowCmd = slow

        if method == "return":  # TODO make this have parity
            return ttg.toGcode(self, method)
