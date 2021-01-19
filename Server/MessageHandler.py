from MessageSender import messageSender
from UserManager import userMannager

class MessageHandler(object):
    def handle_message(self, client, message):
        splittedMessage = message.split(maxsplit=1)
        command = splittedMessage[0]
        if(command == 'SIGNUP'):
            self.processSignUpCommand(client, splittedMessage[1])
        elif(command == 'SIGNIN'):
            self.processSignInCommand(client, splittedMessage[1])
        # elif(command == "SEND"):
        #     self.processSendCommand(client, splittedMessage[1])
        else:
            self.sendErrorMessage(client, "Invalid Command : " + command)

    def processSignUpCommand(self, client, argsString):
        from ClientManager import clientManager
        args = argsString.split()
        if(len(args) < 2):
            self.sendErrorMessage(client, "SignUp:: please provide user name and password")
        elif(len(args) > 2):
            self.sendErrorMessage(client, "SignUp:: user name and password should not contain spaces")
        else:
            getInfo = userMannager.addUser(args[0], args[1])
            if(getInfo == "UserAlreadyExist"):
                self.sendErrorMessage(client, "SignUp:: Username already Exists, Try another Username")
            elif(getInfo == "UserAdded"):
                clientManager.addClient(client, args[0])
                self.sendLoggedInMessage(client, args[0])

    def processSignInCommand(self, client, argsString):
        from ClientManager import clientManager
        args = argsString.split()
        if(len(args) < 2):
            self.sendErrorMessage(client, "SignIn:: please provide user name and password")
        elif(len(args) > 2):
            self.sendErrorMessage(client, "SignIn:: user name and password should not contain spaces")
        else:
            getInfo = userMannager.authUser(args[0], args[1])
            if(getInfo == "WrongPassword"):
                self.sendErrorMessage(client, "SignIn:: Password Incorrect")
            elif(getInfo == "UserNotFound"):
                self.sendErrorMessage(client, "SignIn :: User not found")
            elif( getInfo == "LogIn"):
                clientManager.addClient(client, args[0])
                self.sendLoggedInMessage(client, args[0])

    # def processSendCommand(self, client, argsString):
    #     from ClientManager import clientManager
    #     args = argsString.split()
    #     if(len(args) < 2):
    #         self.sendErrorMessage(client, "Send:: Please provide client name and Message")
    #     else:
    #         getInfo = userMannager.authUser(args[0], args[1])
            
    def sendErrorMessage(self, client, errorMessage):
        messageSender.sendError(client, errorMessage)

    def sendLoggedInMessage(self, client, userName):
      messageSender.send(client, "LOGIN_SUCCESS", "LoggedIn successfully:: " + userName)

messageHandler = MessageHandler()