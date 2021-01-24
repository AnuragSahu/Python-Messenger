import binascii

class SessionInfo(object):
    def __init__(self):
        self.socket = None
        self.userName = ""
        self.isLoggedIn = False
        self.publickey = 0
        self.privateKey = 0
        self.publicKeys = {}
        self.groupKeys = {}

    def updateLoggedInStatus(self, loggedIn, userName):
        self.isLoggedIn = loggedIn
        self.userName = userName

    def setKeys(self, publicKey, privateKey):
        self.publickey = publicKey
        self.privateKey = privateKey

    def setPublicKeys(self, keys):
        for key in keys:
            self.publicKeys[key] = int(keys[key])
        #print(self.publicKeys)

    def setSocket(self, socket):
        self.socket = socket

    def joinGroup(self, groupName, groupKey):
        groupKey = binascii.a2b_hex(groupKey)
        self.groupKeys[groupName] = groupKey

sessionInfo = SessionInfo()
