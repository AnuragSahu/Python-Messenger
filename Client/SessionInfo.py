class SessionInfo(object):
    def __init__(self):
        self.isLoggedIn = False

    def updateLoggedInStatus(self, loggedIn):
        self.isLoggedIn = loggedIn


sessionInfo = SessionInfo()