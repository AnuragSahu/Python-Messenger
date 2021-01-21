from MessageSender import messageSender
from SessionInfo import sessionInfo
import random


class UserInput(object):

    def takeUserInput(self, socket):
        message = str(input())
        command = message.split(maxsplit=1)[0]
        if(command == "SIGNUP"):
            publicKey, privateKey = self.generateKeys()
            sessionInfo.setKeys(publicKey, privateKey)
            #print(publicKey, privateKey)
            messageSender.send(socket, message + " " +str(publicKey))

        else:
            messageSender.send(socket, message)

    def generateKeys(self):
        #TODO
        publicKeys = [197, 151]
        privateKeys = [199, 157]
        publicKey = random.choice(publicKeys)
        privateKey = random.choice(privateKeys)
        return publicKey, privateKey



userInput = UserInput()