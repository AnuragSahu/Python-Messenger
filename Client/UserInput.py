from MessageSender import messageSender


class UserInput(object):

    def takeUserInput(self, socket):
        message = str(input())
        messageSender.send(socket, message)

userInput = UserInput()