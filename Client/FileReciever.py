class FileReciever(object):
    def __init__(self):
        self.fileName = None
        self.file = None
        self.sUserName = None

    def createFile(self, sUsername, fileName):
        self.fileName = fileName
        self.sUserName = sUsername
        self.file = open(self.fileName, 'wb')

    def writeFile(self, buffer):
        self.file.write(buffer)

    def closeFile(self):
        self.file.close()
        self.fileName = None
        self.file = None

fileReciever = FileReciever()