import os
class FileReciever(object):
    def __init__(self):
        self.fileName = None
        self.file = None
        self.sUserName = None

    def createFile(self, sUsername, fileName):
        self.fileName = fileName
        self.sUserName = sUsername
        try: 
            os.makedirs(self.sUserName)
        except OSError:
            pass
        self.file = open(self.sUserName+"/"+self.fileName, 'wb')

    def writeFile(self, buffer):
        self.file.write(buffer)

    def closeFile(self):
        self.file.close()
        filePath = self.sUserName+"/"+self.fileName
        self.fileName = None
        self.file = None
        return filePath 

fileReciever = FileReciever()