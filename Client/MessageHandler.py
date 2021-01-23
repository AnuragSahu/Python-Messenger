from UserInput import userInput
from SessionInfo import sessionInfo
import json
from DiffieHellman import diffieHellman
from MessageSender import messageSender


class MessageHandler():
    def handle_message(self, socket, message):
        print("Recieved : " + message)
        splittedMessage = message.split(maxsplit=1)
        command = splittedMessage[0]
        if(command == 'GREETING'):
            self.processMessage(socket, splittedMessage[1])
        elif(command == 'LOGIN_SUCCESS'):
            self.processLogInSuccessResponse(socket, splittedMessage[1])
        elif(command == 'ERROR'):
            self.processMessage(socket, splittedMessage[1])
        elif(command == 'MESSAGE'):
            self.processMessage(socket, splittedMessage[1])
        elif(command == 'GROUP_CREATED'):
            self.processMessage(socket, splittedMessage[1])
        elif(command == 'GROUP_LIST'):
            self.processMessage(socket, splittedMessage[1])
        elif(command == 'GROUP_JOIN'):
            self.processGroupJoinSuccessResponse(socket, splittedMessage[1])
        elif(command == 'PUBLIC_KEYS'):
            self.processPublicKeysResponse(socket, splittedMessage[1])
        elif(command == 'SENDER_PARTIAL_KEY'):
            self.processSenderPartialKeyCommand(socket, splittedMessage[1])
        elif(command == 'RECEIVER_PARTIAL_KEY'):
            self.processReceiverPartialKeyCommand(socket, splittedMessage[1])
        else:
            self.processMessage(socket, "Unknown response")

    def processLogInSuccessResponse(self, socket, argsString):
        sessionInfo.updateLoggedInStatus(True, argsString.split()[-1])
        print(argsString)

    def processGroupJoinSuccessResponse(self, socket, argsString):
        self.processMessage(socket, argsString)

    def processMessage(self, socket, argsString):
        print(argsString)
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


messageHandler = MessageHandler()
