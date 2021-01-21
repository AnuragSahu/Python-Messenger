from threading import Thread
from Constants import BUFFERSIZE
from MessageReceiver import messageReceiver
from MessageSender import messageSender


class ClientManager(object):
    def __init__(self):
        self.clients = {}
        self.addresses = {}

    def handle_client_connection(self, client, client_address):
        messageSender.send(client, "GREETING", "Greetings from Server!!")
        self.addresses[client] = client_address
        self.init_message_receiver(client)

    def init_message_receiver(self, client):
        messageReceiver.read_incoming_messages(client)

    def addClient(self, client, userName):
        self.clients[userName] = client

    def getClient(self, userName):
        return self.clients[userName]

    def getAllClients(self):
        return self.clients.values()

    def getClientName(self, client):
        userNameList = list(self.clients.keys())
        clientsList = list(self.clients.values())

        position = clientsList.index(client)
        userName = userNameList[position]

        return userName


clientManager = ClientManager()
