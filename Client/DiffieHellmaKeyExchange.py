class DiffeHellmanKeyExchange(object):
    def __init__(self):
        self.myPublicKey = 0
        self.myPrivateKey = 0
        self.publicKeys = None
        self.fullKey = None
        
    def setKeys(self, publicKey, privateKey):
        self.myPublicKey = publicKey
        self.myPrivateKey = privateKey

    def generatePartialKey(self, recieverPublicKey):
        partialKey = self.myPublicKey**self.myPrivateKey
        partialKey = partialKey % recieverPublicKey
        return partialKey

    def generateFullKey(self, partialKey, senderPublicKey):
        fullKey = partialKey ** self.myPrivateKey
        fullKey = fullKey % senderPublicKey
        self.fullKey = fullKey
        return fullKey

    def encryptMessage(self, message):
        encryptedMessage = ""
        key = self.fullKey
        for c in message:
            encryptedMessage += chr(ord(c) + key)
        return encryptedMessage

    def decryptMessage(self, encryptedMessage):
        decryptedMessage = ""
        key = self.fullKey
        for c in encryptedMessage:
            decryptedMessage += chr(ord(c) - key)
        return decryptedMessage