class FileLoader:
    def __init__(self, file):
        self.file = file
        self.contents = b''
        self.mime_type = "text/html"

    def load(self):
        fp = open(self.file, "rb")
        self.contents = fp.read()
        fp.close()