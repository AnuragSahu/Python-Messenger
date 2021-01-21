from UserInput import userInput
from SessionInfo import sessionInfo
import json


class MessageHandler():
    def handle_message(self, socket, message):
        print("Recieved : "+ message)
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
            self.processgoupJoinSuccessResponse(socket, splittedMessage[1])
        elif(command == 'PUBLIC_KEYS'):
            self.processPublicKeysResponse(socket, splittedMessage[1])
        else:
            self.processMessage(socket, "Unknown response")

    def processLogInSuccessResponse(self, socket, argsString):
        sessionInfo.updateLoggedInStatus(True)
        print(argsString)

    def processgoupJoinSuccessResponse(self, socket, argsString):
        self.processMessage(socket, argsString)

    def processMessage(self, socket, argsString):
        print(argsString)
        userInput.takeUserInput(socket)

    def processPublicKeysResponse(self, socket, argsString):
        publicKeys = json.loads(argsString)
        sessionInfo.setPublicKeys(publicKeys)
        userInput.takeUserInput(socket)


messageHandler = MessageHandler()
