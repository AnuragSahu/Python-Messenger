from MessageSender import messageSender
from SessionInfo import sessionInfo
import random
from DiffieHellman import diffieHellman
from KeyboardThread import KeyboardThread
import pyDes
import time
import binascii

import Constants
import socket



class UserInput(object):

    def takeUserInput(self, socket):
        KeyboardThread(self.processInput)
        
    def processInput(self, argsString):
        socket = sessionInfo.socket
        command = argsString.split(maxsplit=1)[0]
        if(command == "SIGNUP"):
            publicKey, privateKey = self.generateKeys()
            sessionInfo.setKeys(publicKey, privateKey)
            messageSender.send(socket, argsString + " " + str(publicKey))
        elif(command == "SEND"):
            self.sharePartialKey(socket, argsString.split()[1])
            time.sleep(2) # 2 sec
            encryptedMessage =  self.encryptMessage(argsString.split(maxsplit=2)[1:])
            messageSender.send(socket, "SEND " + argsString.split()[1] + " " + encryptedMessage)
        elif(command == "SEND_FILE"):
            args = argsString.split(maxsplit = 2)
            rUserName = args[1]
            filePath = args[2]
            fileName = filePath.split("/")[-1]
            self.sharePartialKey(socket, rUserName)
            time.sleep(2) # 2 sec
            messageSender.send(socket, "SEND_FILE_PATH " + rUserName + " " + fileName)
            time.sleep(1) # 1s
            self.sendFile(socket, rUserName, filePath)
        elif(command == "GROUP_SEND"):
            groupName, message =  argsString.split(maxsplit=2)[1:]
            encryptedMessage = self.encryptGroupMessage(groupName, message)
            messageSender.send(socket, "GROUP_SEND " + groupName + " " + encryptedMessage)
        elif(command == "GROUP_SEND_FILE"):
            groupName, filePath =  argsString.split(maxsplit=2)[1:]
            fileName = filePath.split("/")[-1]
            messageSender.send(socket, "GROUP_SEND_FILE_PATH " + groupName + " " + fileName)
            time.sleep(1)
            self.groupSendFile(socket, groupName, filePath)
        else:
            messageSender.send(socket, argsString)

    def sendFile(self, client, rUserName, filePath):
        f = open(filePath,'rb')
        l = f.read(Constants.FILE_BUFFER)
        while(l):
            l = binascii.b2a_hex(l).decode(encoding='utf-8')
            l = self.encryptMessage([rUserName,l])
            messageSender.send(client, "FILEBUFFER " + rUserName + " " + l)
            l = f.read(Constants.FILE_BUFFER)
            time.sleep(0.1) #1s
        f.close()
        messageSender.send(client, "FILEBUFFER "+rUserName+" EOF")

    def groupSendFile(self, client, groupName, filePath):
        f = open(filePath,'rb')
        l = f.read(Constants.FILE_BUFFER)
        while(l):
            l = binascii.b2a_hex(l).decode(encoding='utf-8')
            l = self.encryptGroupMessage(groupName, l)
            messageSender.send(client, "GROUP_FILEBUFFER " + groupName + " " + l)
            l = f.read(Constants.FILE_BUFFER)
            time.sleep(0.1) #1s
        f.close()
        messageSender.send(client, "GROUP_FILEBUFFER "+groupName+" EOF")

    def generateKeys(self):
        # TODO
        publicKeys = [900900900900900900900900900900990990990990990990990990990991,
                      828287284895488684685288685423848464725278828768876456783237,
                      258623241511168180642964355153611979969197632389119917410067,
                      231969487719072553476532687103891221170830716283757301763621,
                      149147145143141139137135133131129127125123121119117115113111,
                      111111111111111112222333333333334445556677777777777889999999]

        privateKeys = [131, 137, 139, 149, 151, 157, 163]
        publicKey = random.choice(publicKeys)
        privateKey = random.choice(privateKeys)
        return publicKey, privateKey

    def sharePartialKey(self, socket, rUserName):
        if(rUserName not in diffieHellman.fullKeys.keys()):
            diffieHellman.calculatePartialKey(sessionInfo.privateKey, sessionInfo.publicKeys, sessionInfo.userName, rUserName)
            messageSender.send(socket, "SENDER_PARTIAL_KEY" + " " + rUserName + " " + str(diffieHellman.partialKeys[rUserName]))

    def encryptMessage(self, argsString):
        rUserName = argsString[0]
        message = argsString[1]
        fullkey = diffieHellman.fullKeys[rUserName]
        encryptObject = pyDes.triple_des(fullkey, padmode = pyDes.PAD_PKCS5)
        encryptedMessage = encryptObject.encrypt(message, padmode = pyDes.PAD_PKCS5)
        return binascii.b2a_hex(encryptedMessage).decode(encoding='utf-8') 
        #return encryptedMessage 

    def encryptGroupMessage(self, groupName, message):
        key = sessionInfo.groupKeys[groupName]
        encryptObject = pyDes.triple_des(key, padmode = pyDes.PAD_PKCS5)
        encryptedMessage = encryptObject.encrypt(message, padmode = pyDes.PAD_PKCS5)
        return binascii.b2a_hex(encryptedMessage).decode(encoding='utf-8') 

        




userInput = UserInput()
