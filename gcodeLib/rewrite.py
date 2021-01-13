# TODO naming convention of basically everything
# double check globals, can prob abstract away many things
# add if switch for returns only if method is return

import math


class ttg:
    def __init__(self, text, size, rotation):
        # set basic passed args
        self.text = text
        self.size = size
        self.rotation = rotation

        # set global class vars
        self.rotationNeeded = False
        self.readyForReturn = False

        # set defualts commands, TODO have function thats toGcode with custom commands
        self.offCmd = "M5"
        self.onCmd = "M3"
        self.fastCmd = "G0"
        self.slowCmd = "G1"

        # check if the user has specified a positive or negative rotation
        if self.rotation != 0:
            self.rotationNeeded = True

    def finalize(self, operations):
        """
        for operation in operations:
            gcodeCmdList.append[self.fastCmd + "x"]
            break  # placeholder for condensing to single lines
        """
        # gcodeCmdList = []
        # gcodeCmdList.append("pog")

        return gcodeCmdList

    # LETTER FUNCTIONS

    def a(self):
        points = [
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (1, 5),
            (2, 5),
            (3, 5),
            (4, 4),
            (4, 3),
            (4, 2),
            (3, 2),
            (2, 2),
            (1, 2),
            (0, 2),
            "off",
            "fast",
            (4, 2),
            "on",
            "slow",
            (4, 1),
            (4, 0),
        ]

        operations = []

        if self.rotationNeeded:
            for point in points:
                if type(point) is tuple:
                    originX = 0  # TODO let this be specified?
                    originY = 0  # decide if even needed

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

                    operations.append(newpoint)

                elif isinstance(point, str):
                    operations.append(point)

        else:
            for point in points:
                operations.append(point)

        # replace string commands with their specified gcode commands
        for count, command in enumerate(operations):
            if command == "off":
                operations[count] = self.offCmd
            elif command == "on":
                operations[count] = self.onCmd
            elif command == "fast":
                operations[count] = self.fastCmd
            elif command == "slow":
                operations[count] = self.slowCmd

        # return ttg.finalize(self, operations)
        return operations  # debug

    # FOOTER

    # get and call functions for letter in given text and append them to queue
    def collectCharacters(self):
        charList = []

        for char in self.text:
            charList.append(char)

        for char in charList:
            if char == "a" or "A":
                return ttg.a(self)

    def toGcode(self, method):
        if self.readyForReturn and method == "return":
            return "TODO placeholder"
        elif not self.readyForReturn:
            return ttg.collectCharacters(self)

    def toGcodeCustom(self, method, on, off, fast, slow):
        self.onCmd = on
        self.offCmd = off
        self.fastCmd = fast
        self.slowCmd = slow

        if method == "return":  # make this have parity
            return ttg.toGcode(self, method)
