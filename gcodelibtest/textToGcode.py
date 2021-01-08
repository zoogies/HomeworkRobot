import math # for rotate later on

class textToGcode:
    def __init__(self,text,size,rotation):
        # set basic vars needed for processing text
        self.text = text
        self.size = size
        self.rotation = rotation
        self.rotationNeeded = False
        self.charList = []
        self.origin = 0,0
        self.readyForReturn = False
        self.points = []

        # set defualts commands, can be changed by calling changeCmds() first
        self.offCmd = "M5"
        self.onCmd = "M3"
        self.fastCmd = "G0"
        self.slowCmd = "G1"

        # check if the user has specified a positive or negative rotation
        if self.rotation != 0:
            self.rotationNeeded = True 

    def parse(self,operations):
        # TODO maybe replace this with enumerate bc your code is dogshit
        i = 0
        for command in operations:
            # detect basic commands and set them to the basic user value
            if command == "off":
                operations[i] = self.offCmd
            elif command == "on":
                operations[i] = self.onCmd
            elif command == "fast":
                operations[i] = self.fastCmd
            elif command == "slow":
                operations[i] = self.slowCmd

            self.rotationNeeded = True #testing

            #this might actually need to go into its own function later for self.points bc youll need it to calculate toolpath
            if self.rotationNeeded: # here is where i rotate every point in operations before drawqueue
                # https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python
                # clean up list to only contain tuples
                self.points = operations # create copy of list so we can remove all strings
                ii=0 # TODO enumerate
                for point in self.points:
                    if not isinstance(point, tuple):
                        del self.points[ii]
                    ii+=1

            i+=1

        self.readyForReturn = True
        textToGcode.toGcode(self)

        #print(operations)
        # TODO here is where i would pass to the drawqueue which would queue it based on whitespace between characters
        # or maybe handle the whitespace in each parse idk ill have to see

    # height to width is 10:6
    #
    #       .   .   .
    #   .               .
    #   .               .
    #   .   .   .   .   .
    #   .               .
    #   .               .

    def a(self):
        points = [
            (0,0),
            (0,1),
            (0,2),
            (0,3),
            (0,4),
            (1,5),
            (2,5),
            (3,5),
            (4,4),
            (4,3),
            (4,2),
            (3,2),
            (2,2),
            (1,2),
            (0,2),
            "off",
            "fast",
            (4,2),
            "on",
            "slow",
            (4,1),
            (4,0)
        ]

        operations = []

        # TODO there has to be a way to do this with only one loop
        for point in points:
            operations.append(point)

        # parse this letters points before sending to the draw queue
        textToGcode.parse(self,operations)

    # function to split text up into its characters, called on by toGcode()
    def split(self):
        for char in self.text:             # TODO check if it works with spaces and anomylous characters
            self.charList.append(char)

    # main function called upon by program, starts the flow of splitting parsing
    # and converting the text, then adding it to the draw queue and returning it
    def toGcode(self):
        if(self.readyForReturn == False):
            textToGcode.split(self)
            for char in self.charList:
                if(char == "a" or "A"):
                    textToGcode.a(self)
        elif(self.readyForReturn):
            x = self.points
            return x # this returns none WHY?!?!?!??!

    # same as to gcode, but allows user to pass args for custom commands
    def toGcodeWithArgs(self,offCode,onCode,fastCode,slowCode): # TODO maybe get better naming convention
        self.offCmd = offCode
        self.onCmd = onCode         # TODO revisit this passing args system, there has to be a 
        self.fastCmd = fastCode     # better way and to make it more accessible to people
        self.slowCmd = slowCode

        textToGcode.split(self)
        for char in self.charList: # TODO update and fix this shit
            if(char == "a" or "A"):
                textToGcode.a(self)

# just to keep in mind if youre gonna publish this you should have 
# multiple ways to return the values including an actual gcode file 
# itself and not a list of commands
# could add lowercase letters as well if you have time
# TODO rearange layout of functions in file https://salishsea-meopar-tools.readthedocs.io/en/latest/python_packaging/library_code.html