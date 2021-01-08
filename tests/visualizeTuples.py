from gcodelibtest.textToGcode import textToGcode

# https://stackoverflow.com/questions/18458734/how-do-i-plot-list-of-tuples-in-python

# TODO wtf is this

class tests:
    def fetchTuples(self):
        #collect tuples
        tuples = textToGcode("a",1,0).toGcode()
        print(tuples)

        #drop all non tuples from returned gcode command list
        i = 0 #im small brain so i cant use enumerate TODO
        for item in tuples:
            if not isinstance(item, tuple):
                tuples.remove(i)
            i+=1 # TODO why is this here, what did i just do
        return(tuples)