class Request:
    def __init__(self, string):
        self.string = string
        self.elements = []
        self.status = ""
    def parse(self):
        self.string = self.string[:-4] # Chop off the \r\n\r\n
        self.string = self.string.replace("\r", "") # Chop out all carriage returns
        self.elements = []
        lines = self.string.split("\n")
        self.request = lines[0]
        lines = lines[1:]

        for l in lines:
            element = l.split(": ")
            print(element)
            self.elements.append(element)
    
    def create(self):
        string = self.status + "\r\n"
        for e in self.elements:
            string += (": ".join(e)) + "\r\n"
        string += "\r\n"
        print(string)
        self.string = string