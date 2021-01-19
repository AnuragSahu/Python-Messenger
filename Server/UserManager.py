class UserManager(object):
  def __init__(self):
    self.users = {}

  def addUser(self, userName, password):
    if(userName in self.users.keys()):
      return "UserAlreadyExist"
    else:
      self.users[userName] = password
      return "UserAdded"
    print(self.users)

  def authUser(self, userName, password):
    if(userName in self.users.keys()):
      if(self.users[userName] == password):
        return "LogIn"
      else:
        return "WrongPassword"
    else:
      return "UserNotFound"

userMannager = UserManager()