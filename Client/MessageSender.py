class MessageSender(object):
    def send(self, client, data):
        print("Sending : "+data)
        client.send(bytes(data, "utf8"))

messageSender = MessageSender()