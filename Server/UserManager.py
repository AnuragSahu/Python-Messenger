class UserManager(object):
  def __init__(self):
    self.users = {}

  def addUser(self, userName, password):
    if(userName in self.users.keys()):
      return "UserAlreadyExist"
    else:
      self.users[userName] = password
      print(self.users)
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

userMannager = UserManager()