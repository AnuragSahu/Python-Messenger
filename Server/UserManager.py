class UserManager(object):
  def __init__(self):
    self.users = {}
    self.userPublicKeys = {}

  def addUser(self, userName, password, publicKey):
    if(userName in self.users.keys()):
      return "UserAlreadyExist"
    else:
      self.users[userName] = password
      self.userPublicKeys[userName] = publicKey
      print(self.users)
      print(self.userPublicKeys)
      return "UserAdded"
    

  def authUser(self, userName, password):
    if(userName in self.users.keys()):
      if(self.users[userName] == password):
        return "LogIn"
      else:
        return "WrongPassword"
    else:
      return "UserNotFound"

  def getUserInfo(self, userName):
    if(userName in self.users.keys()):
      return "UserExists"
    else:
      return "NoSuchUser"

  def getPublicKeys(self):
    return self.userPublicKeys

userMannager = UserManager()