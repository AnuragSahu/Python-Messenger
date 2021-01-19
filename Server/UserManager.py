class UserManager(object):
  def __init__(self):
    self.users = {}

  def addUser(self, userName, password):
    self.users[userName] = password
    print(self.users)

userMannager = UserManager()