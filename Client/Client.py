from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from MessageReceiver import messageReceiver
from Constants import *

ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

if __name__ == "__main__":
    messageReceiver.read_incoming_messages(client_socket)
