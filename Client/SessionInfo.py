class SessionInfo(object):
    def __init__(self):
        self.isLoggedIn = False
        self.publickey = 0
        self.privateKey = 0
        self.publicKeys = {}

    def updateLoggedInStatus(self, loggedIn):
        self.isLoggedIn = loggedIn

    def setKeys(self, publicKey, privateKey):
        self.publickey = publicKey
        self.privateKey = privateKey

    def setPublicKeys(self, keys):
        self.publicKeys = keys
        print(self.publicKeys)

sessionInfo = SessionInfo()