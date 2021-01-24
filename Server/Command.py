import enum
# Using enum class create enumerations
class Commands(enum.Enum):
   SIGNUP = 1
   SIGNIN = 1
   SEND = 1
   CREATE = 1
   JOIN = 1
   LIST = 0
   PARTIAL_KEY = 1
   GROUP_SEND = 1
   SENDER_PARTIAL_KEY = 1
   RECEIVER_PARTIAL_KEY = 1
   SEND_FILE_PATH = 1
   FILEBUFFER = 1
   GROUP_SEND_FILE_PATH = 1
   GROUP_FILEBUFFER = 1