from UserInput import userInput
from SessionInfo import sessionInfo
import json
from DiffieHellman import diffieHellman
from MessageSender import messageSender
from FileReciever import fileReciever
import binascii
import pyDes


class MessageHandler():
    def handle_message(self, socket, message):
        #print("Recieved : " + message)
        splittedMessage = message.split(maxsplit=1)
        command = splittedMessage[0]
        if(command == 'GREETING'):
            self.processMessage(socket, splittedMessage[1])
        elif(command == 'LOGIN_SUCCESS'):
            self.processLogInSuccessResponse(socket, splittedMessage[1])
        elif(command == 'ERROR'):
            self.processMessage(socket, splittedMessage[1])
        elif(command == 'MESSAGE'):
            self.processRecievedMessage(socket, splittedMessage[1])
        elif(command == 'GROUP_CREATED'):
            self.processGroupJoinSuccessResponse(socket, splittedMessage[1])
        elif(command == 'GROUP_LIST'):
            self.processMessage(socket, splittedMessage[1])
        elif(command == 'GROUP_JOIN'):
            self.processGroupJoinSuccessResponse(socket, splittedMessage[1])
        elif(command == 'GROUP_MESSAGE'):
            self.processGroupMessageResponse(socket, splittedMessage[1])
        elif(command == 'PUBLIC_KEYS'):
            self.processPublicKeysResponse(socket, splittedMessage[1])
        elif(command == 'SENDER_PARTIAL_KEY'):
            self.processSenderPartialKeyCommand(socket, splittedMessage[1])
        elif(command == 'RECEIVER_PARTIAL_KEY'):
            self.processReceiverPartialKeyCommand(socket, splittedMessage[1])
        elif(command == 'SEND_FILE_PATH'):
            self.processFilePathResponse(socket, splittedMessage[1])
        elif(command == 'FILEBUFFER'):
            self.processFileBufferResponse(socket, splittedMessage[1])
        elif(command == 'GROUP_SEND_FILE_PATH'):
            self.processGroupFilePathResponse(socket, splittedMessage[1])
        elif(command == 'GROUP_FILEBUFFER'):
            self.processGroupFileBufferResponse(socket, splittedMessage[1])
        
        else:
            self.processMessage(socket, "Unknown response")

    def processLogInSuccessResponse(self, socket, argsString):
        sessionInfo.updateLoggedInStatus(True, argsString.split()[-1])
        print(argsString)

    def processGroupJoinSuccessResponse(self, socket, argsString):
        args = argsString.split(maxsplit=1)
        groupKey = args[1]
        groupName = args[0]
        sessionInfo.joinGroup(groupName, groupKey)
        self.processMessage(socket, "Successfully Joined : "+groupName)

    def processMessage(self, socket, argsString):
        print(argsString)
        userInput.takeUserInput(socket)

    def processRecievedMessage(self, socket, argsString):
        args = argsString.split(maxsplit = 1)
        fullKey = diffieHellman.fullKeys[args[0]]
        encryptObject = pyDes.triple_des(fullKey, padmode = pyDes.PAD_PKCS5)
        decryptedMessage = encryptObject.decrypt(binascii.a2b_hex(args[1]), padmode = pyDes.PAD_PKCS5)
        message =  decryptedMessage.decode(encoding='utf-8') 
        print(args[0] + " : " + message)
        userInput.takeUserInput(socket)

    def processPublicKeysResponse(self, socket, argsString):
        publicKeys = json.loads(argsString)
        sessionInfo.setPublicKeys(publicKeys)
        userInput.takeUserInput(socket)

    def processSenderPartialKeyCommand(self, socket, argsString):
        sUserName, key = argsString.split()
        diffieHellman.updatePartialKey(
            sessionInfo.privateKey, sessionInfo.publicKeys, sessionInfo.userName, sUserName)
        diffieHellman.addFullKey(
            sUserName, key, sessionInfo.publicKeys[sessionInfo.userName], sessionInfo.privateKey)
        messageSender.send(socket, "RECEIVER_PARTIAL_KEY" + " " +
                           sUserName + " " + str(diffieHellman.partialKeys[sUserName]))

    def processReceiverPartialKeyCommand(self, socket, argsString):
        sUserName, key = argsString.split()
        diffieHellman.addFullKey(
            sUserName, key, sessionInfo.publicKeys[sUserName], sessionInfo.privateKey)

    def processGroupMessageResponse(self, socket, argsString):
        args = argsString.split(maxsplit = 2)
        groupName  = args[0]
        sUserName = args[1]
        message = args[2]
        groupKey = sessionInfo.groupKeys[groupName]
        encryptObject = pyDes.triple_des(groupKey, padmode = pyDes.PAD_PKCS5)
        decryptedMessage = encryptObject.decrypt(binascii.a2b_hex(message), padmode = pyDes.PAD_PKCS5)
        message =  decryptedMessage.decode(encoding='utf-8') 
        self.processMessage(socket, groupName+": "+sUserName+": "+message)

    def processFilePathResponse(self, socket, argsString):
        args = argsString.split(maxsplit=1)
        rUserName = sessionInfo.userName
        fileReciever.createFile(rUserName, args[1])
        print("Recieving file "+args[1]+" from "+args[0])

    def processFileBufferResponse(self, socket, argsString):
        buffer = argsString
        if(buffer != "EOF"):
            sUserName = fileReciever.sUserName
            fullKey = diffieHellman.fullKeys[sUserName]
            encryptObject = pyDes.triple_des(fullKey, padmode = pyDes.PAD_PKCS5)
            decryptedMessage = encryptObject.decrypt(binascii.a2b_hex(buffer), padmode = pyDes.PAD_PKCS5)
            buffer =  decryptedMessage.decode(encoding='utf-8')
            buffer = binascii.a2b_hex(buffer)
            fileReciever.writeFile(buffer)
        else:
            filePath = fileReciever.closeFile()
            self.processMessage(socket, "File Recived at "+filePath)

    def processGroupFileBufferResponse(self, socket, argsString):
        args = argsString.split(maxsplit=2)
        groupName = args[0]
        #sUserName = args[1]
        buffer = args[2]
        if(buffer != "EOF"):
            groupKey = sessionInfo.groupKeys[groupName]
            encryptObject = pyDes.triple_des(groupKey, padmode = pyDes.PAD_PKCS5)
            decryptedMessage = encryptObject.decrypt(binascii.a2b_hex(buffer), padmode = pyDes.PAD_PKCS5)
            buffer =  decryptedMessage.decode(encoding='utf-8')
            buffer = binascii.a2b_hex(buffer)
            fileReciever.writeFile(buffer)
        else:
            filePath = fileReciever.closeFile()
            self.processMessage(socket, "File Recived at "+filePath)
    
    def processGroupFilePathResponse(self, socket, argsString):
        args = argsString.split(maxsplit=2)
        groupName = args[0]
        sUserName = args[1]
        fileName = args[2]
        rUserName = sessionInfo.userName
        fileReciever.createFile(groupName+"/"+rUserName, fileName)
        print("Recieving file "+fileName+" from "+sUserName+" in "+groupName)

        


messageHandler = MessageHandler()
