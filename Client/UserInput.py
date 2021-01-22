from MessageSender import messageSender
from SessionInfo import sessionInfo
import random
from DiffieHellman import diffieHellman


class UserInput(object):

    def takeUserInput(self, socket):
        message = str(input())
        command = message.split(maxsplit=1)[0]
        if(command == "SIGNUP"):
            publicKey, privateKey = self.generateKeys()
            sessionInfo.setKeys(publicKey, privateKey)
            #print(publicKey, privateKey)
            messageSender.send(socket, message + " " + str(publicKey))
        elif(command == "SEND"):
            self.sharePartialKey(socket, message.split()[1])
            #self.encryptMessage(message.split(maxsplit=2)[2])
        else:
            messageSender.send(socket, message)

    def generateKeys(self):
        # TODO
        publicKeys = [167, 173, 179, 181, 191, 193, 197]
        privateKeys = [131, 137, 139, 149, 151, 157, 163]
        publicKey = random.choice(publicKeys)
        privateKey = random.choice(privateKeys)
        return publicKey, privateKey

    def sharePartialKey(self, socket, rUserName):
        if(rUserName not in diffieHellman.fullKeys.keys()):
            messageSender.send(socket, "SENDER_PARTIAL_KEY" + " " + rUserName + " " + str(diffieHellman.partialKeys[rUserName]))

userInput = UserInput()
