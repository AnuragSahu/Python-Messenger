from MessageSender import messageSender
from UserManager import userMannager

class MessageHandler(object):
    def handle_message(self, client, message):
        splittedMessage = message.split(maxsplit=1)
        command = splittedMessage[0]
        if(command == 'SIGNUP'):
            self.processSignUpCommand(client, splittedMessage[1])

    def processSignUpCommand(self, client, argsString):
        from ClientManager import clientManager
        args = argsString.split()
        if(len(args) < 2):
            self.sendErrorMessage(client, "SignUp:: please provide user name and password")
        elif(len(args) > 2):
            self.sendErrorMessage(client, "SignUp:: user name and password should not contain spaces")
        else:
            userMannager.addUser(args[0], args[1])
            clientManager.addClient(client, args[0])
            self.sendLoggedInMessage(client, args[0])

    def sendErrorMessage(self, client, errorMessage):
        messageSender.sendError(client, errorMessage)

    def sendLoggedInMessage(self, client, userName):
      messageSender.send(client, "LOGIN_SUCCESS", "LoggedIn successfully:: " + userName)

messageHandler = MessageHandler()