class MessageSender(object):
    def sendError(self, client, errorMessage):
        self.send(client, 'ERROR', errorMessage)

    def send(self, client, command, data):
        client.send(bytes(command + " " + data, "utf8"))

    def broadCast(self, clients, command, data):
        for client in clients:
            self.send(client, command, data)

messageSender = MessageSender()