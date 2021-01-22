class DiffieHellman(object):
    def __init__(self):
        self.partialKeys = {}
        self.fullKeys = {}

    def updatePartialKeys(self, privateKey, publicKeys, userName):
        myPublicKey = publicKeys[userName]
        for uN in publicKeys:
            print(type(myPublicKey), type(privateKey))
            partialKey = myPublicKey ** privateKey
            partialKey = partialKey % publicKeys[uN]
            self.partialKeys[uN] = partialKey
        print("Partial keys: ", self.partialKeys)

    def addFullKey(self, sUserName, sPartialKey, sPublicKey, privateKey):
        fullKey = sPartialKey ** privateKey
        fullKey = fullKey % sPublicKey
        self.fullKeys[sUserName] = fullKey
        print("Full keys: ", self.fullKeys)


diffieHellman = DiffieHellman()
