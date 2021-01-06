import math #for rotate later on

class textToGcode:
    def __init__(self,text,size,rotation):
        self.text = text
        self.size = size
        self.rotation = rotation
        self.charList = []
        self.offCmd = "off"
        self.onCmd = "on"
        self.fastCmd = "fast"
        self.slowCmd = "slow"

    def split(self):
        for char in self.text:
            self.charList.append(char)

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

        #https://stackoverflow.com/questions/15884527/how-can-i-prevent-the-typeerror-list-indices-must-be-integers-not-tuple-when-c
        #my head hurts

        for point in points:
            if point != str:
                operations.append(points[point] - points[point + 1])
            elif point == str:
                if point == "off":
                    operations.append(self.offCmd)
                elif point == "on":
                    operations.append(self.onCmd)
                elif point == "slow":
                    operations.append(self.slowCmd)
                elif point == "fast":
                    operations.append(self.fastCmd)

    def toGcode(self):
        textToGcode.split(self)
        for char in self.charList:
            if(char == "a" or "A"):
                return(textToGcode.a(self))