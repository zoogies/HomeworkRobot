class test:
    def __init__(self):
        self.text = "done"
        self.readyforreturn = False

    def secondFunction(self):
        print("second function ran")
        self.readyforreturn = True
        return test.main(self)

    def main(self):
        if not self.readyforreturn:
            return test.secondFunction(self)
        else:
            return self.text