import math #for rotate later on

class textToGcode:
    def __init__(self,text,size,rotation):
        self.text = text
        self.size = size
        self.rotation = rotation
        self.rotationNeeded = False
        self.charList = []
        self.origin = 0,0
        #TODO:
        #the off on fast slow commands might be something 
        #you want to have them specify with args
        self.offCmd = "M5"
        self.onCmd = "M3"
        self.fastCmd = "G0"
        self.slowCmd = "G1"

        if self.rotation != 0:
            self.rotationNeeded = True

    def split(self):
        for char in self.text:
            self.charList.append(char)

    def parse(self,operations):
        #TODO maybe replace this with enumerate bc your code is dogshit
        i = 0
        for command in operations:
            #detect basic commands and set them to the basic user value
            if command == "off":
                operations[i] = self.offCmd
            elif command == "on":
                operations[i] = self.onCmd
            elif command == "fast":
                operations[i] = self.fastCmd
            elif command == "slow":
                operations[i] = self.slowCmd

            if self.rotationNeeded: #here is where i rotate every point in operations before drawqueue
                #https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python
                break

            i+=1
        print(operations)
        #TODO here is where i would pass to the drawqueue which would queue it based on whitespace between characters
        #or maybe handle the whitespace in each parse idk ill have to see

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
            #"fast",
            (4,2),
            "on",
            "slow",
            (4,1),
            (4,0)
        ]

        operations = []

        #TODO there has to be a way to do this with only one loop
        for point in points:
            operations.append(point)

        #parse this letters points before sending to the draw queue
        textToGcode.parse(self,operations)

    def toGcode(self):
        textToGcode.split(self)
        for char in self.charList:
            if(char == "a" or "A"):
                return(textToGcode.a(self))



# just to keep in mind if youre gonna publish this you should have 
# multiple ways to return the values including an actual gcode file 
# itself and not a list of commands
#could add lowercase letters as well if you have time