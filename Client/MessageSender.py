class MessageSender(object):
    def send(self, client, data):
        print("Sending : "+str(data))
        client.send(bytes(data, "utf8"))

    def sendBytesData(self, client, data):
        client.send(data)

messageSender = MessageSender()