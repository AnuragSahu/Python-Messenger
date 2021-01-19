class MessageSender(object):
    def sendError(self, client, errorMessage):
        send(client, 'ERROR', errorMessage)

    def send(self, client, command, data):
        client.send(bytes(command + " " + data, "utf8"))

messageSender = MessageSender()