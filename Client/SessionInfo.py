class SessionInfo(object):
    def __init__(self):
        self.userName = ""
        self.isLoggedIn = False
        self.publickey = 0
        self.privateKey = 0
        self.publicKeys = {}

    def updateLoggedInStatus(self, loggedIn, userName):
        self.isLoggedIn = loggedIn
        self.userName = userName

    def setKeys(self, publicKey, privateKey):
        self.publickey = publicKey
        self.privateKey = privateKey

    def setPublicKeys(self, keys):
        for key in keys:
            self.publicKeys[key] = int(keys[key])
        print(self.publicKeys)

sessionInfo = SessionInfo()
