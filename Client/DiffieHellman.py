class DiffieHellman(object):
    def __init__(self):
        self.partialKeys = {}
        self.fullKeys = {}

    def calculatePartialKey(self, privateKey, publicKeys, userName, rUserName):
        myPublicKey = publicKeys[userName]
        partialKey = myPublicKey ** privateKey
        partialKey = partialKey % publicKeys[rUserName]
        self.partialKeys[rUserName] = partialKey
        print("Partial keys: ", self.partialKeys)

    def updatePartialKey(self, privateKey, publicKeys, userName, sUserName):
        sPublicKey = publicKeys[sUserName]
        partialKey = sPublicKey ** privateKey
        partialKey = partialKey % publicKeys[userName]
        self.partialKeys[sUserName] = partialKey
        print("Partial keys: ", self.partialKeys)

    def addFullKey(self, sUserName, sPartialKey, sPublicKey, privateKey):
        fullKey = int(sPartialKey) ** privateKey
        fullKey = fullKey % sPublicKey
        self.fullKeys[sUserName] = fullKey
        print("Full keys: ", self.fullKeys)


diffieHellman = DiffieHellman()
