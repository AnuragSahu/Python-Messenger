from UserInput import userInput
from SessionInfo import sessionInfo


class MessageHandler():
    def handle_message(self, socket, message):
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
        else:
            self.processMessage(socket, "Unknown response")

    def processLogInSuccessResponse(self, socket, argsString):
        sessionInfo.updateLoggedInStatus(True)
        self.processMessage(socket, argsString)

    def processMessage(self, socket, argsString):
        print(argsString)
        userInput.takeUserInput(socket)


messageHandler = MessageHandler()
