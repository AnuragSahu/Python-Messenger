from threading import Thread
from Constants import BUFFERSIZE
from MessageHandler import messageHandler

class MessageReceiver(object):
  def read_incoming_messages(self, client):
    Thread(target=self.read_messages, args=(client,)).start()

  def read_messages(self, client):
    while True:
      msg = client.recv(BUFFERSIZE).decode("utf8")
      messageHandler.handle_message(client, msg)

messageReceiver = MessageReceiver()