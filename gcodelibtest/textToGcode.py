import math #for rotate later on

class textToGcode:
    def __init__(self,text,size,rotation):
        self.text = text
        self.size = size
        self.rotation = rotation
        self.charList = []
        self.origin = 0,0
        #the off on fast slow commands might be something 
        #you want to have them specify with args
        self.offCmd = "M5"
        self.onCmd = "M3"
        self.fastCmd = "G0"
        self.slowCmd = "G1"

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

        #there has to be a way to do this with only one loop
        for point in points:
            operations.append(point)

        #maybe replace this with enumerate bc your code is dogshit
        i = 0
        for command in operations: #this shit needs moved out of a letter function bc im not writing this a million times,
            #letter functions should just be a list of points and commands that referance the rotate and parse functions
            #tbh the rotate should just be a check before trying to parse any letters and then if its not 0 we can just run it before output
            #detect basic commands and set them to the basic user value
            if command == "off":
                operations[i] = self.offCmd
            elif command == "on":
                operations[i] = self.onCmd
            elif command == "fast":
                operations[i] = self.fastCmd
            elif command == "slow":
                operations[i] = self.slowCmd

            if self.rotation != 0:
                #https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python
                break

            i+=1
        print(operations)

        #https://stackoverflow.com/questions/15884527/how-can-i-prevent-the-typeerror-list-indices-must-be-integers-not-tuple-when-c
        #my head hurts
        """ 
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
         """
    
    def toGcode(self):
        textToGcode.split(self)
        for char in self.charList:
            if(char == "a" or "A"):
                return(textToGcode.a(self))



# just to keep in mind if youre gonna publish this you should have 
# multiple ways to return the values including an actual gcode file 
# itself and not a list of commands