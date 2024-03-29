from MessageSender import messageSender
from UserManager import userMannager
from Command import Commands
import json
import time


class MessageHandler(object):

    def handle_message(self, client, message):
        #print("Recieved : " + message)
        splittedMessage = message.split(maxsplit=1)
        command = splittedMessage[0]
        if(len(splittedMessage) < Commands[command].value + 1):
            self.sendErrorMessage(client, "Incomplete Command")
        if(command == 'SIGNUP'):
            self.processSignUpCommand(client, splittedMessage[1].strip())
        elif(command == 'SIGNIN'):
            self.processSignInCommand(client, splittedMessage[1].strip())
        elif(command == 'SEND'):
            self.processSendCommand(client, splittedMessage[1].strip())
        elif(command == 'CREATE'):
            self.processCreateCommand(client, splittedMessage[1].strip())
        elif(command == 'LIST'):
            self.processListCommand(client)
        elif(command == 'JOIN'):
            self.processJoinCommand(client, splittedMessage[1].strip())
        elif(command == 'GROUP_SEND'):
            self.processGroupSendCommand(client, splittedMessage[1].strip())
        elif(command == 'SENDER_PARTIAL_KEY'):
            self.processSenderPartialKeyCommand(client, splittedMessage[1].strip())
        elif(command == 'RECEIVER_PARTIAL_KEY'):
            self.processReceiverPartialKeyCommand(client, splittedMessage[1].strip())
        elif(command == 'SEND_FILE_PATH'):
            self.processSendFilePathCommand(client, splittedMessage[1].strip())
        elif(command == 'GROUP_SEND_FILE_PATH'):
            self.processGroupSendFilePathCommand(client, splittedMessage[1].strip())
        elif(command == 'FILEBUFFER'):
            self.processFileBufferCommand(client, splittedMessage[1].strip())
        elif(command == 'GROUP_FILEBUFFER'):
            self.processGroupFileBufferCommand(client, splittedMessage[1].strip())
        else:
            self.sendErrorMessage(client, "Invalid Command : " + command)

    def processSignUpCommand(self, client, argsString):
        from ClientManager import clientManager
        args = argsString.split()
        if(len(args) < 3):
            self.sendErrorMessage(client, "SignUp:: please provide user name and password")
        elif(len(args) > 3):
            self.sendErrorMessage(client, "SignUp:: user name and password should not contain spaces")
        else:
            getInfo = userMannager.addUser(args[0], args[1], args[2])
            if(getInfo == "UserAlreadyExist"):
                self.sendErrorMessage(client, "SignUp:: Username already Exists, Try another Username")
            elif(getInfo == "UserAdded"):
                clientManager.addClient(client, args[0])
                self.sendLoggedInMessage(client, args[0])
                allClients = clientManager.getAllClients()
                publicKeys = userMannager.getPublicKeys()
                time.sleep(1) # wait for 1 sec
                messageSender.broadCast(allClients, "PUBLIC_KEYS", json.dumps(publicKeys))

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

    def processSendCommand(self, client, argsString):
        from ClientManager import clientManager
        args = argsString.split()
        if(len(args) < 2):
            self.sendErrorMessage(client, "Send:: Please provide client name and Message")
        else:
            getInfo = userMannager.getUserInfo(args[0])
            if(getInfo == "NoSuchUser"):
                self.sendErrorMessage(client, "Send:: User with name : " + args[0])
            else:
                senderName = clientManager.getClientName(client)
                message = args[1]
                reciever_client = clientManager.getClient(args[0])
                self.sendMessage(reciever_client, senderName, message)

    def processCreateCommand(self, client, argsString):
        from GroupManager import groupManager
        from ClientManager import clientManager
        groupName = argsString
        senderName = clientManager.getClientName(client)
        groupKey = groupManager.createGroup(senderName, groupName)
        self.sendGroupJoinMessage(client, groupName, groupKey)

    def processListCommand(self, client):
        from GroupManager import groupManager
        groupsList = groupManager.listGroup()
        group_list = "groupName  Number of Participants \n"
        for i in groupsList:
            row = str(i) + " " + str(groupsList[i]) + "\n"
            group_list += row
        self.sendGroupList(client, group_list)

    def processJoinCommand(self, client, argsString):
        from GroupManager import groupManager
        from ClientManager import clientManager
        groupName = argsString
        userName = clientManager.getClientName(client)
        groupKey = groupManager.joinGroup(userName, groupName)
        self.sendGroupJoinMessage(client, groupName, groupKey)
            
    def processSenderPartialKeyCommand(self, sClient, argsString):
        from ClientManager import clientManager
        rUserName, key = argsString.split()
        sUserName = clientManager.getClientName(sClient)
        rClient = clientManager.getClient(rUserName)
        messageSender.send(rClient, "SENDER_PARTIAL_KEY", sUserName + " " + key)

    def processReceiverPartialKeyCommand(self, sClient, argsString):
        from ClientManager import clientManager
        rUserName, key = argsString.split()
        sUserName = clientManager.getClientName(sClient)
        rClient = clientManager.getClient(rUserName)
        messageSender.send(rClient, "RECEIVER_PARTIAL_KEY", sUserName + " " + key)

    def processGroupSendCommand(self, client, argsString):
        from GroupManager import groupManager
        from ClientManager import clientManager
        args = argsString.split(maxsplit = 1)
        groupName = args[0]
        sUserName = clientManager.getClientName(client)
        listOfParticipants = groupManager.getParticipants(groupName)
        socketOfParticipants = clientManager.getClients(listOfParticipants)
        socketOfParticipants.remove(client)
        messageSender.broadCast(
            socketOfParticipants,"GROUP_MESSAGE", groupName + " " + sUserName + " " + args[1])

    def processSendFilePathCommand(self, client, argsString):
        from ClientManager import clientManager
        args = argsString.split(maxsplit=1)
        sUserName = clientManager.getClientName(client)
        rUserName = args[0]
        rSocket = clientManager.getClient(rUserName)
        messageSender.send(rSocket, "SEND_FILE_PATH", sUserName+" "+ args[1])

    def processFileBufferCommand(self, client, argsString):
        from ClientManager import clientManager
        args = argsString.split(maxsplit = 1)
        rUserName = args[0]
        buffer = args[1]
        rClient = clientManager.getClient(rUserName)
        messageSender.send(rClient, "FILEBUFFER", buffer)
    
    def processGroupSendFilePathCommand(self, client, argsString):
        from ClientManager import clientManager
        from GroupManager import groupManager
        args = argsString.split(maxsplit = 1)
        groupName = args[0]
        fileName = args[1]

        sUserName = clientManager.getClientName(client)
        listOfParticipants = groupManager.getParticipants(groupName)
        socketOfParticipants = clientManager.getClients(listOfParticipants)
        socketOfParticipants.remove(client)
        messageSender.broadCast(
            socketOfParticipants,"GROUP_SEND_FILE_PATH", groupName + " " + sUserName + " " + fileName)

    def processGroupFileBufferCommand(self, client, argsString):
        from ClientManager import clientManager
        from GroupManager import groupManager
        args = argsString.split(maxsplit = 1)
        groupName = args[0]
        buffer = args[1]
        sUserName = clientManager.getClientName(client)
        listOfParticipants = groupManager.getParticipants(groupName)
        socketOfParticipants = clientManager.getClients(listOfParticipants)
        socketOfParticipants.remove(client)
        messageSender.broadCast(
            socketOfParticipants,"GROUP_FILEBUFFER", groupName + " " + sUserName + " " + buffer)



    def sendErrorMessage(self, client, errorMessage):
        messageSender.sendError(client, errorMessage)

    def sendLoggedInMessage(self, client, userName):
      messageSender.send(client, "LOGIN_SUCCESS", "LoggedIn successfully:: " + userName)

    def sendMessage(self, client, senderName, message):
        messageSender.send(client, "MESSAGE", senderName + " " + message)

    def sendGroupList(self, client, group_list):
        messageSender.send(client, "GROUP_LIST", group_list)

    def sendGroupJoinMessage(self, client, groupName, groupKey):
        messageSender.send(client, "GROUP_JOIN", groupName+" "+groupKey)

messageHandler = MessageHandler()