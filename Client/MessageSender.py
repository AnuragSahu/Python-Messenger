class MessageSender(object):
    def send(self, client, data):
        client.send(bytes(data, "utf8"))

messageSender = MessageSender()