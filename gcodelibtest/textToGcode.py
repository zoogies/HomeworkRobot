import math #for rotate later on

class textToGcode:
    def __init__(self,text,size,rotation):
        self.text = text
        self.size = size
        self.rotation = rotation
        self.charList = []

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

        for point in points:
            return([
                points[point] - points[point + 1]
            ])

    def toGcode(self):
        textToGcode.split(self)
        for char in self.charList:
            if(char == "a" or "A"):
                return(textToGcode.a(self))